import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

import YAML from "yaml";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const root = process.cwd();
const domainSchemaPath = "schemas/governed-docs.schema.json";
const artifactSchemaPath = "schemas/canonical-artifact.schema.json";
const casesPath = "tests/test-cases.json";
const reportPath = "tests/reports/conformance-report.json";

const domainSchema = JSON.parse(fs.readFileSync(domainSchemaPath, "utf8"));
const artifactSchema = JSON.parse(fs.readFileSync(artifactSchemaPath, "utf8"));
const testCases = JSON.parse(fs.readFileSync(casesPath, "utf8")).cases;

const ajv = new Ajv2020({
  allErrors: true,
  strict: true,
  strictRequired: false
});

addFormats(ajv);

const validateMetadata = ajv.compile(domainSchema);
const validateArtifact = ajv.compile(artifactSchema);

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

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

function errorCodeFromAjv(error) {
  if (error.keyword === "required") return "SCHEMA_REQUIRED";
  if (error.keyword === "additionalProperties") return "SCHEMA_ADDITIONAL_PROPERTY";
  if (error.keyword === "enum") return "SCHEMA_ENUM";
  if (error.keyword === "format") return "SCHEMA_FORMAT";
  if (error.keyword === "pattern") return "SCHEMA_PATTERN";
  if (error.keyword === "type") return "SCHEMA_TYPE";
  return `SCHEMA_${error.keyword.toUpperCase()}`;
}

function extractFrontMatter(raw) {
  const text = raw.replace(/^\uFEFF/, "");
  const lines = text.split(/\r?\n/);

  if (lines[0]?.trim() !== "---") {
    return {
      ok: false,
      error: {
        code: "NO_FRONTMATTER",
        message: "Documento sem YAML front matter no topo."
      }
    };
  }

  let endIndex = -1;

  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i].trim() === "---") {
      endIndex = i;
      break;
    }
  }

  if (endIndex === -1) {
    return {
      ok: false,
      error: {
        code: "FRONTMATTER_NOT_CLOSED",
        message: "Bloco YAML front matter não foi fechado."
      }
    };
  }

  return {
    ok: true,
    yamlText: lines.slice(1, endIndex).join("\n"),
    bodyMarkdown: lines.slice(endIndex + 1).join("\n")
  };
}

function parseYamlStrict(yamlText) {
  const doc = YAML.parseDocument(yamlText, {
    version: "1.2",
    uniqueKeys: true,
    prettyErrors: true
  });

  if (doc.errors.length > 0) {
    const isDuplicate = doc.errors.some((err) =>
      String(err.message).toLowerCase().includes("map keys must be unique")
      || String(err.message).toLowerCase().includes("unique")
    );

    return {
      ok: false,
      error: {
        code: isDuplicate ? "YAML_DUPLICATE_KEY" : "YAML_INVALID",
        message: doc.errors.map((err) => err.message).join("; ")
      }
    };
  }

  const value = doc.toJS({
    mapAsMap: false,
    maxAliasCount: 20
  });

  if (value === null || Array.isArray(value) || typeof value !== "object") {
    return {
      ok: false,
      error: {
        code: "YAML_NOT_OBJECT",
        message: "Front matter precisa ser objeto chave-valor."
      }
    };
  }

  return {
    ok: true,
    metadata: value
  };
}

function markdownToText(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_`[\]()!-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function compileArtifact(filePath, raw, metadata, bodyMarkdown) {
  return {
    schema_version: "1.0",
    artifact_type: "knowledge_document",
    source: {
      path: filePath,
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
}

function runSingleCase(testCase) {
  const errors = [];
  const filePath = testCase.path;
  const raw = fs.readFileSync(filePath, "utf8");

  const fm = extractFrontMatter(raw);

  if (!fm.ok) {
    errors.push(fm.error);
    return { artifact: null, errors };
  }

  const parsed = parseYamlStrict(fm.yamlText);

  if (!parsed.ok) {
    errors.push(parsed.error);
    return { artifact: null, errors };
  }

  const metadata = parsed.metadata;

  if (JSON.stringify(metadata).includes("{{")) {
    errors.push({
      code: "UNFILLED_PLACEHOLDER",
      message: "Documento contém placeholder não preenchido."
    });
  }

  const schemaOk = validateMetadata(metadata);

  if (!schemaOk) {
    for (const err of validateMetadata.errors ?? []) {
      errors.push({
        code: errorCodeFromAjv(err),
        message: `${err.instancePath || "/"} ${err.message}`
      });
    }
  }

  if (errors.length > 0) {
    return { artifact: null, errors };
  }

  const artifact = compileArtifact(filePath, raw, metadata, fm.bodyMarkdown);
  const artifactOk = validateArtifact(artifact);

  if (!artifactOk) {
    for (const err of validateArtifact.errors ?? []) {
      errors.push({
        code: "ARTIFACT_SCHEMA_INVALID",
        message: `${err.instancePath || "/"} ${err.message}`
      });
    }
    return { artifact: null, errors };
  }

  return { artifact, errors };
}

const results = [];
const metadataById = new Map();
const relationshipChecks = [];

for (const testCase of testCases) {
  const result = runSingleCase(testCase);

  if (result.artifact) {
    const id = result.artifact.metadata.id;

    if (metadataById.has(id)) {
      result.errors.push({
        code: "DUPLICATE_ID",
        message: `ID duplicado: ${id}`
      });
    } else {
      metadataById.set(id, testCase.path);
    }

    for (const rel of result.artifact.metadata.relationships ?? []) {
      relationshipChecks.push({
        sourceCase: testCase.id,
        sourcePath: testCase.path,
        targetId: rel.target_id,
        result
      });
    }
  }

  results.push({
    id: testCase.id,
    path: testCase.path,
    expected_valid: testCase.expected_valid,
    expected_error_codes: testCase.expected_error_codes,
    actual_valid: result.errors.length === 0,
    actual_error_codes: result.errors.map((err) => err.code),
    errors: result.errors,
    artifact_hash: result.artifact ? sha256(canonicalJson(result.artifact)) : null
  });
}

for (const check of relationshipChecks) {
  if (!metadataById.has(check.targetId)) {
    check.result.errors.push({
      code: "DANGLING_RELATIONSHIP",
      message: `Relação aponta para ID inexistente: ${check.targetId}`
    });

    const item = results.find((result) => result.id === check.sourceCase);
    item.actual_valid = false;
    item.actual_error_codes = check.result.errors.map((err) => err.code);
    item.errors = check.result.errors;
    item.artifact_hash = null;
  }
}

/*
  Second pass for duplicate IDs among invalid fixtures:
  Duplicate IDs can only be detected after parsing all metadata.
*/
const idIndex = new Map();

for (const testCase of testCases) {
  try {
    const raw = fs.readFileSync(testCase.path, "utf8");
    const fm = extractFrontMatter(raw);
    if (!fm.ok) continue;
    const parsed = parseYamlStrict(fm.yamlText);
    if (!parsed.ok) continue;

    const id = parsed.metadata.id;
    if (!id) continue;

    if (!idIndex.has(id)) idIndex.set(id, []);
    idIndex.get(id).push(testCase.id);
  } catch {
    // ignore unreadable file in this phase
  }
}

for (const [id, ids] of idIndex.entries()) {
  if (ids.length > 1) {
    for (const caseId of ids) {
      const item = results.find((result) => result.id === caseId);
      if (!item.actual_error_codes.includes("DUPLICATE_ID")) {
        item.actual_valid = false;
        item.actual_error_codes.push("DUPLICATE_ID");
        item.errors.push({
          code: "DUPLICATE_ID",
          message: `ID duplicado: ${id}`
        });
        item.artifact_hash = null;
      }
    }
  }
}

let passed = 0;
let failed = 0;

for (const item of results) {
  const validityMatches = item.expected_valid === item.actual_valid;

  const expectedErrorMatched = item.expected_valid
    ? item.actual_error_codes.length === 0
    : item.expected_error_codes.some((code) => item.actual_error_codes.includes(code));

  item.passed = validityMatches && expectedErrorMatched;

  if (item.passed) {
    passed += 1;
  } else {
    failed += 1;
  }
}

const report = {
  generated_at: new Date().toISOString(),
  total: results.length,
  passed,
  failed,
  results
};

fs.mkdirSync(path.dirname(reportPath), { recursive: true });
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");

for (const item of results) {
  const status = item.passed ? "PASS" : "FAIL";
  console.log(`${status} ${item.id}`);
}

console.log(`\nTotal: ${results.length}`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Report: ${reportPath}`);

if (failed > 0) {
  process.exit(1);
}
