import fs from "node:fs";
import crypto from "node:crypto";
import { execSync } from "node:child_process";

const watchedFiles = [
  "frontmatter/tests/schemas/governed-docs.schema.json",
  "frontmatter/tests/schemas/canonical-artifact.schema.json",
  "frontmatter/ledger/source-ledger-event.schema.json",
  "frontmatter/tests/scripts/run-conformance-tests.mjs",
  "frontmatter/ledger/validate-ledger.mjs"
];

const changelogPath = "frontmatter/change_control/CHANGELOG.md";
const structuralChangesPath = "frontmatter/change_control/structural-changes.jsonl";

function fileExists(path) {
  try {
    fs.accessSync(path);
    return true;
  } catch {
    return false;
  }
}

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function gitDiffNameOnly() {
  try {
    return execSync("git diff --name-only origin/main...HEAD", { encoding: "utf8" })
      .split(/\r?\n/)
      .filter(Boolean);
  } catch {
    return execSync("git diff --name-only", { encoding: "utf8" })
      .split(/\r?\n/)
      .filter(Boolean);
  }
}

const changedFiles = gitDiffNameOnly();
const structuralTouched = changedFiles.filter((file) =>
  watchedFiles.some((watched) => file === watched || file.startsWith(watched))
);

if (structuralTouched.length === 0) {
  console.log("Nenhuma mudança estrutural detectada.");
  process.exit(0);
}

const hasChangelog = changedFiles.includes(changelogPath);
const hasStructuralHistory = changedFiles.includes(structuralChangesPath);

let hasErrors = false;

if (!hasChangelog) {
  console.error("Mudança estrutural detectada, mas CHANGELOG.md não foi atualizado.");
  hasErrors = true;
}

if (!hasStructuralHistory) {
  console.error("Mudança estrutural detectada, mas structural-changes.jsonl não foi atualizado.");
  hasErrors = true;
}

console.log("Arquivos estruturais alterados:");
for (const file of structuralTouched) {
  const content = fileExists(file) ? fs.readFileSync(file, "utf8") : "";
  console.log(`- ${file} ${fileExists(file) ? sha256(content).slice(0, 12) : "(deleted)"}`);
}

if (hasErrors) {
  process.exit(1);
}

console.log("Mudança estrutural possui registros de controle.");
