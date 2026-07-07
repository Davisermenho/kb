# Document Templates Pack

Este pacote contém templates preenchíveis por tipo documental para reduzir erros humanos em documentos Markdown com YAML front matter.

## Objetivo

Os templates reduzem erros porque:

- mostram apenas campos permitidos;
- separam campos obrigatórios e opcionais;
- usam valores controlados;
- mantêm datas no formato `YYYY-MM-DD`;
- evitam campos ambíguos como `date`, `type`, `name`, `owner`;
- alinham o conteúdo Markdown ao `document_type`;
- facilitam validação automática por JSON Schema.

## Estrutura

```text
templates/
  tutorial.md
  api-reference.md
  release-note.md
  policy.md
  runbook.md

examples/filled/
  tutorial.example.md
  api-reference.example.md
  release-note.example.md
  policy.example.md
  runbook.example.md

template-index.json
TEMPLATE-GUIDE.md
scripts/create-doc-from-template.mjs
```

## Local real neste projeto

```text
frontmatter/templates/templates/tutorial.md
frontmatter/templates/templates/api-reference.md
frontmatter/templates/templates/release-note.md
frontmatter/templates/templates/policy.md
frontmatter/templates/templates/runbook.md
frontmatter/templates/template-index.json
frontmatter/templates/scripts/create-doc-from-template.mjs
```

## Regra de uso

1. Escolha o template pelo tipo documental.
2. Preencha somente os placeholders `{{...}}`.
3. Não crie campos novos.
4. Rode o validador de front matter.
5. Publique apenas se o documento passar no schema.
