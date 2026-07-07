# Change Control Pack

Este pacote contém os arquivos prontos para controlar changelog e histórico de mudanças estruturais do padrão de metadados documentais.

## Arquivos

- `CHANGELOG.md`: changelog humano por versão.
- `change-control-policy.md`: política que define o que é mudança estrutural e quando bloquear.
- `structural-changes.jsonl`: histórico estruturado e validável de mudanças estruturais.
- `structural-change-event.schema.json`: JSON Schema para validar cada evento estrutural.
- `validate-change-control.mjs`: script que valida o histórico estrutural contra o schema e verifica referência no changelog.
- `detect-schema-change.mjs`: script que detecta alterações em arquivos estruturais e exige atualização do controle.
- `change-control.yml`: workflow GitHub Actions de exemplo.

## Local real neste projeto

```text
frontmatter/change_control/CHANGELOG.md
frontmatter/change_control/change-control-policy.md
frontmatter/change_control/structural-changes.jsonl
frontmatter/change_control/structural-change-event.schema.json
frontmatter/change_control/validate-change-control.mjs
frontmatter/change_control/detect-schema-change.mjs
.github/workflows/frontmatter-conformance-tests.yml
```

Os scripts usam esses caminhos como padrão quando executados a partir da raiz do repositório (`node frontmatter/change_control/validate-change-control.mjs`).

## Regra central

Mudança estrutural sem changelog, sem evento estrutural e sem decisão associada deve falhar no CI.
