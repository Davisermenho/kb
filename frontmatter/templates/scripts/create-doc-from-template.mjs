import fs from "node:fs";
import path from "node:path";

const templateType = process.argv[2];
const outputPath = process.argv[3];

if (!templateType || !outputPath) {
  console.error("Uso: node scripts/create-doc-from-template.mjs <tipo> <saida.md>");
  console.error("Tipos: tutorial, api-reference, release-note, policy, runbook");
  process.exit(1);
}

const templateMap = {
  "tutorial": "frontmatter/templates/templates/tutorial.md",
  "api-reference": "frontmatter/templates/templates/api-reference.md",
  "release-note": "frontmatter/templates/templates/release-note.md",
  "policy": "frontmatter/templates/templates/policy.md",
  "runbook": "frontmatter/templates/templates/runbook.md"
};

const templatePath = templateMap[templateType];

if (!templatePath) {
  console.error(`Tipo de template inválido: ${templateType}`);
  process.exit(1);
}

if (!fs.existsSync(templatePath)) {
  console.error(`Template não encontrado: ${templatePath}`);
  process.exit(1);
}

if (fs.existsSync(outputPath)) {
  console.error(`Arquivo de saída já existe: ${outputPath}`);
  process.exit(1);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });

const template = fs.readFileSync(templatePath, "utf8");
fs.writeFileSync(outputPath, template, "utf8");

console.log(`Documento criado a partir de ${templatePath}: ${outputPath}`);
console.log("Preencha os placeholders {{...}} e rode o validador de front matter.");
