import fs from "node:fs";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const changesPath = process.argv[2] ?? "frontmatter/change_control/structural-changes.jsonl";
const schemaPath = process.argv[3] ?? "frontmatter/change_control/structural-change-event.schema.json";
const changelogPath = process.argv[4] ?? "frontmatter/change_control/CHANGELOG.md";

const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const changelog = fs.readFileSync(changelogPath, "utf8");
const lines = fs.readFileSync(changesPath, "utf8").split(/\r?\n/).filter(Boolean);

const ajv = new Ajv2020({ allErrors: true, strict: true, strictRequired: false });
addFormats(ajv);

const validate = ajv.compile(schema);
let hasErrors = false;
const changeIds = new Set();

for (const [index, line] of lines.entries()) {
  let event;

  try {
    event = JSON.parse(line);
  } catch (error) {
    console.error(`Line ${index + 1}: JSON inválido: ${error.message}`);
    hasErrors = true;
    continue;
  }

  if (!validate(event)) {
    console.error(`Line ${index + 1}: evento estrutural inválido`);
    for (const err of validate.errors ?? []) {
      console.error(`- ${err.instancePath || "/"}: ${err.message}`);
    }
    hasErrors = true;
  }

  if (changeIds.has(event.change_id)) {
    console.error(`Line ${index + 1}: change_id duplicado: ${event.change_id}`);
    hasErrors = true;
  }
  changeIds.add(event.change_id);

  if (!changelog.includes(event.version_after)) {
    console.error(`Line ${index + 1}: version_after ${event.version_after} não aparece no CHANGELOG.md`);
    hasErrors = true;
  }

  if (!changelog.includes(event.change_id)) {
    console.error(`Line ${index + 1}: change_id ${event.change_id} não aparece no CHANGELOG.md`);
    hasErrors = true;
  }

  if (event.breaking === true && event.requires_migration !== true) {
    console.error(`Line ${index + 1}: mudança breaking precisa requires_migration=true`);
    hasErrors = true;
  }

  if (event.breaking === true && !event.migration_plan) {
    console.error(`Line ${index + 1}: mudança breaking precisa de migration_plan`);
    hasErrors = true;
  }
}

if (hasErrors) {
  process.exit(1);
}

console.log(`Controle de mudanças válido. Eventos estruturais: ${lines.length}`);
