// Compila um Markdown real (não uma fixture de teste) com Front Matter "governed-docs"
// em um artefato JSON canônico validado, gravado em disco.
//
// Uso: node frontmatter/tests/scripts/compile-governed-doc.mjs <arquivo.md> --output <saida.json>

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

import YAML from "yaml";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const scriptDir = path.dirname(new URL(import.meta.url).pathname);
const schemasDir = path.join(scriptDir, "..", "schemas");

const inputPath = process.argv[2];
const outputFlagIndex = process.argv.indexOf("--output");
const outputPath = outputFlagIndex !== -1 ? process.argv[outputFlagIndex + 1] : null;

if (!inputPath || !outputPath) {
  console.error("Uso: node frontmatter/tests/scripts/compile-governed-doc.mjs <arquivo.md> --output <saida.json>");
  process.exit(2);
}

const domainSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, "governed-docs.schema.json"), "utf8"));
const artifactSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, "canonical-artifact.schema.json"), "utf8"));

const ajv = new Ajv2020({ allErrors: true, strict: true, strictRequired: false });
addFormats(ajv);

const validateMetadata = ajv.compile(domainSchema);
const validateArtifact = ajv.compile(artifactSchema);

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function extractFrontMatter(raw) {
  const lines = raw.replace(/^﻿/, "").split(/\r?\n/);

  if (lines[0]?.trim() !== "---") {
    throw new Error("NO_FRONTMATTER: documento sem YAML front matter no topo.");
  }

  const endIndex = lines.findIndex((line, i) => i > 0 && line.trim() === "---");

  if (endIndex === -1) {
    throw new Error("FRONTMATTER_NOT_CLOSED: bloco YAML front matter não foi fechado.");
  }

  return {
    yamlText: lines.slice(1, endIndex).join("\n"),
    bodyMarkdown: lines.slice(endIndex + 1).join("\n")
  };
}

function markdownToText(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_`[\]()!-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const raw = fs.readFileSync(inputPath, "utf8");
const { yamlText, bodyMarkdown } = extractFrontMatter(raw);

const doc = YAML.parseDocument(yamlText, { version: "1.2", uniqueKeys: true, prettyErrors: true });

if (doc.errors.length > 0) {
  console.error(`YAML_INVALID: ${doc.errors.map((e) => e.message).join("; ")}`);
  process.exit(1);
}

const metadata = doc.toJS({ mapAsMap: false, maxAliasCount: 20 });

if (JSON.stringify(metadata).includes("{{")) {
  console.error("UNFILLED_PLACEHOLDER: documento contém placeholder não preenchido.");
  process.exit(1);
}

if (!validateMetadata(metadata)) {
  for (const err of validateMetadata.errors ?? []) {
    console.error(`${err.instancePath || "/"} ${err.message}`);
  }
  process.exit(1);
}

const artifact = {
  schema_version: "1.0",
  artifact_type: "knowledge_document",
  source: {
    path: inputPath,
    checksum_sha256: sha256(raw)
  },
  metadata,
  content: {
    body_markdown: bodyMarkdown,
    body_text: markdownToText(bodyMarkdown)
  },
  validation: {
    valid: true,
    schema_id: domainSchema.$id,
    errors: []
  },
  provenance: {
    generated_by: "conformance-test-pipeline",
    parser_version: "1.0.0",
    generated_at: new Date().toISOString()
  }
};

if (!validateArtifact(artifact)) {
  for (const err of validateArtifact.errors ?? []) {
    console.error(`${err.instancePath || "/"} ${err.message}`);
  }
  process.exit(1);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(artifact, null, 2), "utf8");

console.log(`Artefato canônico validado gravado em ${outputPath}`);
