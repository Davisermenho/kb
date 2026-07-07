# Plano de Testes de Conformidade

Versão: 1.0  
Status: Ativo  
Última atualização: 2026-07-07

---

## 1. Objetivo

Provar que o padrão de Front Matter governável funciona na prática.

O padrão só é considerado funcional se:

1. documentos válidos são aceitos;
2. documentos inválidos são rejeitados;
3. campos inventados são bloqueados;
4. status `approved` e `published` exigem evidência;
5. IDs duplicados são detectados;
6. relações quebradas são detectadas;
7. placeholders não preenchidos são bloqueados;
8. artefatos canônicos são gerados apenas para documentos válidos;
9. o resultado dos testes é reproduzível em CI.

---

## 2. Camadas testadas

| Camada | O que testa |
|---|---|
| Parser | Front matter ausente, YAML inválido, chave duplicada |
| Schema | Required, enum, format, pattern, additionalProperties |
| Governança | Aprovação sem evidência, type sem contrato, campos desconhecidos |
| Integridade | ID único, relação sem destino, placeholder não preenchido |
| Artefato | JSON canônico validado, provenance mínima |
| Pipeline | Resultado agregado com pass/fail |

---

## 3. Casos válidos

| Caso | Prova |
|---|---|
| `tutorial-approved.md` | Tutorial aprovado com evidência formal |
| `policy-approved.md` | Policy com campos específicos obrigatórios |
| `runbook-draft.md` | Runbook em draft com risk_level |
| `plan-review.md` | Plano em review sem exigir evidência de aprovação |

---

## 4. Casos inválidos

| Caso | Erro esperado |
|---|---|
| `no-frontmatter.md` | `NO_FRONTMATTER` |
| `invalid-yaml.md` | `YAML_INVALID` |
| `duplicate-yaml-key.md` | `YAML_DUPLICATE_KEY` |
| `missing-required-title.md` | `SCHEMA_REQUIRED` |
| `invented-field.md` | `SCHEMA_ADDITIONAL_PROPERTY` |
| `invalid-status.md` | `SCHEMA_ENUM` |
| `approved-without-evidence.md` | `SCHEMA_REQUIRED` |
| `published-without-evidence.md` | `SCHEMA_REQUIRED` |
| `unknown-type.md` | `SCHEMA_ENUM` |
| `policy-missing-risk-level.md` | `SCHEMA_REQUIRED` |
| `bad-date-format.md` | `SCHEMA_FORMAT` |
| `duplicate-id-a.md` e `duplicate-id-b.md` | `DUPLICATE_ID` |
| `dangling-relationship.md` | `DANGLING_RELATIONSHIP` |
| `unfilled-placeholder.md` | `UNFILLED_PLACEHOLDER` |

---

## 5. Critério de aceite

O pacote de testes passa se:

```text
total de casos executados = total de casos declarados
todos os casos válidos passam
todos os casos inválidos falham
cada caso inválido contém pelo menos um erro esperado
nenhum artefato é gerado para caso inválido
todos os artefatos válidos passam no schema de artefato
```

---

## 6. Comando

```bash
npm test
```

ou:

```bash
node scripts/run-conformance-tests.mjs
```
