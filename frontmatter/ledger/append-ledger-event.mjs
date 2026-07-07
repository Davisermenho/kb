import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";

const ledgerPath = process.argv[2] ?? "frontmatter/ledger/source-ledger.jsonl";

function canonicalJson(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }

  if (Array.isArray(value)) {
    return `[${value.map(canonicalJson).join(",")}]`;
  }

  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`)
    .join(",")}}`;
}

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function nowIso() {
  return new Date().toISOString();
}

function randomEventId() {
  return `evt_${crypto.randomBytes(8).toString("hex")}`;
}

function getPreviousEventHash(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }

  const lines = fs.readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .filter(Boolean);

  if (lines.length === 0) {
    return null;
  }

  const last = JSON.parse(lines.at(-1));
  return last.provenance?.event_hash ?? null;
}

function appendEvent(filePath, partialEvent) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });

  const previousEventHash = getPreviousEventHash(filePath);

  const eventWithoutHash = {
    ledger_version: "1.0",
    event_id: randomEventId(),
    occurred_at: nowIso(),
    ...partialEvent,
    provenance: {
      ...partialEvent.provenance,
      previous_event_hash: previousEventHash,
      event_hash: "0".repeat(64)
    }
  };

  const eventHash = sha256(canonicalJson({
    ...eventWithoutHash,
    provenance: {
      ...eventWithoutHash.provenance,
      event_hash: undefined
    }
  }));

  const finalEvent = {
    ...eventWithoutHash,
    provenance: {
      ...eventWithoutHash.provenance,
      event_hash: eventHash
    }
  };

  fs.appendFileSync(filePath, `${JSON.stringify(finalEvent)}\n`, "utf8");
  return finalEvent;
}

const example = {
  event_type: "metadata_validated",
  actor: {
    type: "ci",
    id: "github-actions",
    run_id: process.env.GITHUB_RUN_ID ?? "local"
  },
  source: {
    path: "docs/auth/oauth2.md",
    format: "markdown_frontmatter",
    checksum_sha256: "a".repeat(64),
    git_commit: process.env.GITHUB_SHA?.slice(0, 40) ?? "1a2b3c4d",
    schema_id: "https://example.org/schemas/governed-docs.schema.json"
  },
  decision: {
    status: "accepted",
    rule_set: "frontmatter-schema-v1.0",
    reason: "Documento validado automaticamente.",
    validation_errors: []
  },
  destination: {
    kind: "artifact",
    path: "artifacts/docs/auth/oauth2.json",
    checksum_sha256: "b".repeat(64)
  },
  provenance: {
    pipeline: "docs-pipeline",
    pipeline_version: "1.0.0",
    parser_version: "1.3.0",
    canonicalization: "RFC8785-JCS"
  }
};

const event = appendEvent(ledgerPath, example);
console.log(`Ledger event appended: ${event.event_id}`);
