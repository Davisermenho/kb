# Front Matter Conformance Tests Pack

Este pacote contém cenários de teste para provar que o padrão de Front Matter governável funciona.

## Arquivos principais

```text
TEST-PLAN.md
schemas/governed-docs.schema.json
schemas/canonical-artifact.schema.json
tests/test-cases.json
tests/fixtures/valid/*.md
tests/fixtures/invalid/*.md
scripts/run-conformance-tests.mjs
tests/reports/EXPECTED-REPORT.json
.github/workflows/frontmatter-conformance-tests.yml
package.json
```

## O que os testes provam

- Documentos válidos geram artefato canônico validado.
- Documentos sem front matter são rejeitados.
- YAML inválido é rejeitado.
- Chaves YAML duplicadas são rejeitadas.
- Campos obrigatórios ausentes são rejeitados.
- Campos inventados são rejeitados por `additionalProperties: false`.
- Valores fora do vocabulário controlado são rejeitados.
- `approved` e `published` exigem evidência.
- `type` desconhecido é rejeitado.
- Campos condicionais por tipo são exigidos.
- Datas inválidas são rejeitadas.
- IDs duplicados são detectados.
- Relações quebradas são detectadas.
- Placeholders não preenchidos são bloqueados.

## Como executar

```bash
npm install
npm test
```

O relatório de execução será gerado em:

```text
tests/reports/conformance-report.json
```

## Critério de sucesso

O teste passa quando todos os casos válidos são aceitos e todos os casos inválidos são rejeitados com os erros esperados.
