import fs from "node:fs";
import { globSync } from "glob";

const pattern = process.argv[2] ?? "frontmatter/templates/examples/filled/**/*.md";
const files = globSync(pattern);

let hasErrors = false;

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  const matches = text.match(/\{\{[^}]+\}\}/g);

  if (matches) {
    hasErrors = true;
    console.error(`${file}: placeholders não preenchidos: ${[...new Set(matches)].join(", ")}`);
  }
}

if (hasErrors) {
  process.exit(1);
}

console.log("Nenhum placeholder não preenchido encontrado.");
