import fs from "node:fs";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const ledgerPath = process.argv[2] ?? "frontmatter/ledger/source-ledger.jsonl";
const schemaPath = process.argv[3] ?? "frontmatter/ledger/source-ledger-event.schema.json";

const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));

const ajv = new Ajv2020({
  allErrors: true,
  strict: true
});

addFormats(ajv);

const validate = ajv.compile(schema);
const lines = fs.readFileSync(ledgerPath, "utf8").split(/\r?\n/).filter(Boolean);

let hasErrors = false;
let previousHash = null;

for (const [index, line] of lines.entries()) {
  let event;

  try {
    event = JSON.parse(line);
  } catch (error) {
    hasErrors = true;
    console.error(`Line ${index + 1}: JSON inválido: ${error.message}`);
    continue;
  }

  if (!validate(event)) {
    hasErrors = true;
    console.error(`Line ${index + 1}: schema inválido`);

    for (const err of validate.errors ?? []) {
      console.error(`- ${err.instancePath || "/"}: ${err.message}`);
    }
  }

  const actualPreviousHash = event.provenance?.previous_event_hash ?? null;

  if (actualPreviousHash !== previousHash) {
    hasErrors = true;
    console.error(
      `Line ${index + 1}: previous_event_hash inválido. Esperado ${previousHash}, encontrado ${actualPreviousHash}`
    );
  }

  previousHash = event.provenance?.event_hash ?? null;
}

if (hasErrors) {
  process.exit(1);
}

console.log(`Ledger válido. Eventos: ${lines.length}`);
