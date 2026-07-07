# Front Matter System Design

Status: Aceito
Versão: 2.0.0
Data de criação: 2026-07-06
Data de atualização: 2026-07-07
Responsável: agente_ia (revisão humana pendente para publicação)

Protocolos técnicos para governança e consumo de dados em Markdown desta Knowledge Base.

Para o Front Matter virar sistema real, não pode ser só um bloco YAML no topo do Markdown. Ele precisa ter contrato, validação, governança, arquivos de suporte e regras de uso — e cada uma dessas camadas precisa apontar para um arquivo que existe de fato neste repositório, não para um exemplo genérico.

Este documento substitui a versão anterior (7.161 linhas, ~97% dump de pesquisa colado de um chat externo, com três schemas ilustrativos e inconsistentes entre si e nenhum passo a passo verificável). O material antigo não tinha decisão, não tinha caminho real e não rodava. Este documento só descreve o que existe e funciona hoje, mais o que falta.

## 1. Estrutura mínima

```text
Markdown com Front Matter
  → parser/conversor        (ferramentas/kb_compile.py | frontmatter/tests/scripts/run-conformance-tests.mjs)
  → JSON canônico           (saída de kb_compile.py     | frontmatter/tests/scripts/compile-governed-doc.mjs)
  → JSON Schema             (schemas/domain_knowledge.schema.json | frontmatter/tests/schemas/governed-docs.schema.json)
  → validação               (ferramentas/check_kb_consistency.py, kb_validate.py | frontmatter/tests/scripts/run-conformance-tests.mjs)
  → registro de evidência   (conteudo/FONTES_REGISTRADAS.md | frontmatter/ledger/source-ledger.jsonl)
  → consumo pela IA/pipeline
```

## 2. Dois contratos, não um

Este repositório tem dois tipos de artefato Markdown governado, com formatos estruturalmente diferentes. Forçar os dois em um único schema exigiria redesenhar um dos dois — por isso são dois contratos separados, não concorrentes:

| Contrato | Quando usar | Schema | Exemplo real |
|---|---|---|---|
| `domain_knowledge` | Entradas de conhecimento de domínio (conceitos, entidades, regras de negócio) | `schemas/domain_knowledge.schema.json` (produção, rastreado, roda no CI `kb-validation.yml`) | `exemplos/domain_customer.md` |
| `governed-docs` (tutorial / api_reference / policy / runbook / release_note / decision_record / agent_contract / flow / plan) | Documentação operacional, templates, playbooks, planos e contratos de agente | `frontmatter/tests/schemas/governed-docs.schema.json` | `frontmatter/templates/examples/filled/*.example.md` |

Um arquivo com nome quase idêntico ao contrato real (`frontmatter/tests/schemas/domain-knowledge.schema.json`, sem underscore) existia com um formato totalmente incompatível (validava `tutorial/policy/runbook`, não `domain_knowledge`). Ele foi descontinuado no lugar — o manifesto do run ativo proíbe renomear/excluir arquivos, então ele foi esvaziado para um aviso de descontinuação; o conteúdo real está em `governed-docs.schema.json`.

### 2.1 Campos obrigatórios mínimos — `domain_knowledge`

```yaml
---
id: domain.customer
title: Cliente
type: domain_knowledge
version: 1.0.0
status: approved
domain: Comercial
boundedContext: CRM
aliases: [Customer, Cliente comercial]
tags: [cliente, crm, cadastro]
relationships:
  dependsOn: [domain.person, domain.address]
  relatedTo: [process.customer_registration]
retrieval:
  searchable: true
  priority: high
  canonical: true
content:
  summary: Representa uma pessoa física ou jurídica que mantém relacionamento comercial com a organização.
---
```
(exemplo real, `exemplos/domain_customer.md`; `content.markdown` é injetado por `kb_compile.py` a partir do corpo do documento — não precisa ser escrito à mão.)

Campos exigidos por `schemas/domain_knowledge.schema.json`: `id`, `title`, `type` (`const: domain_knowledge`), `version`, `status` (`draft|review|approved|deprecated`), `domain`, `boundedContext`, `aliases`, `tags`, `relationships.{dependsOn,relatedTo}`, `retrieval.{searchable,priority,canonical}`, `content.markdown`.

Campos adicionais recomendados por `governanca/CAMPOS FRONTMATTER.md` (catálogo mais amplo, ainda não todos exigidos pelo schema hoje): `schema_version`, `owner`, `created_at`, `updated_at`, `governance.{decision,priority,review_required}`, `validation.{schema,acceptanceCriteria,rejectionCriteria}`, `source.{ids,links}`.

### 2.2 Campos obrigatórios mínimos — `governed-docs`

```yaml
---
id: doc_log_retention_policy
schema_version: "1.0"
version: "0.1.0"
title: "Política de retenção de logs"
description: "Define prazos, responsabilidades e critérios para retenção de logs operacionais."
type: "policy"
status: "draft"
owner_team: "security"
created_at: "2026-07-07"
updated_at: "2026-07-07"
effective_date: "2026-08-01"
next_review_at: "2027-08-01"
risk_level: "high"
---
```
(exemplo real, `frontmatter/templates/examples/filled/policy.example.md`)

Campos exigidos por `frontmatter/tests/schemas/governed-docs.schema.json`: `id`, `schema_version`, `type`, `title`, `description`, `status`, `owner_team`, `created_at`, `updated_at`, `version` — mais condicionais: `approved`/`published` exigem `approved_by`/`approved_at`/`approval_ref`; `policy` exige `effective_date`/`next_review_at`/`risk_level`; `runbook` exige `risk_level`; `release_note` exige `published_at`/`release_version`.

### 2.3 Contrato de contrato de agente (papel)

```yaml
---
role:
  id: revisor_formal
  authority: []
  responsibilities: []
  permissions: []
  forbidden_actions: []
  escalation: {}
---
```
Campos descritos em `governanca/CAMPOS FRONTMATTER.md` §12 (`role.id`, `role.authority`, `role.permissions`, `role.forbidden_actions`, `role.escalation`) — ainda sem schema JSON dedicado; registrado como trabalho futuro (§8).

## 3. O Que Não Pode Faltar

| Camada | O que precisa existir | Onde está hoje neste repositório |
|---|---|---|
| Padrão de campos | Lista oficial de campos permitidos | `governanca/CAMPOS FRONTMATTER.md` (catálogo `domain_knowledge`); este documento §2.2 (`governed-docs`) |
| Schema | JSON Schema executável | `schemas/domain_knowledge.schema.json`; `frontmatter/tests/schemas/governed-docs.schema.json` |
| Parser/conversor | Script que lê Markdown + YAML | `ferramentas/kb_compile.py`; `frontmatter/tests/scripts/run-conformance-tests.mjs` e `compile-governed-doc.mjs` |
| JSON canônico | Saída estruturada validada | Saída de `kb_compile.py`; `frontmatter/tests/schemas/canonical-artifact.schema.json` |
| Validador | Script/check de conformidade | `ferramentas/check_kb_consistency.py`, `ferramentas/kb_validate.py`; `frontmatter/tests/scripts/run-conformance-tests.mjs` (`npm --prefix frontmatter/tests test`) |
| Registro de fontes | Ledger de origem, decisão e destino | `conteudo/FONTES_REGISTRADAS.md`; `frontmatter/ledger/source-ledger-event.schema.json` + `append-ledger-event.mjs`/`validate-ledger.mjs` |
| Registro de decisões | Documento de governança | `frontmatter/governance/decision-register.md` (DR-001 a DR-009) |
| Changelog | Histórico de mudanças estruturais | `frontmatter/change_control/CHANGELOG.md` + `structural-changes.jsonl` |
| Templates | Modelos preenchíveis por tipo | `frontmatter/templates/templates/*.md` (tutorial, api_reference, release_note, policy, runbook) |
| Testes | Casos válidos e inválidos | `frontmatter/tests/tests/test-cases.json` (19 casos: 4 válidos, 15 inválidos), fixtures em `frontmatter/tests/tests/fixtures/` |

## 4. Regras vitais

1. **Todo campo precisa estar documentado** — nenhum campo novo entra sem definição, tipo, regra, exemplo e impacto no pipeline. Enforced por `additionalProperties: false` nos dois schemas; processo de proposta em `frontmatter/governance/metadata-governance.md` §6 e `governanca/CAMPOS FRONTMATTER.md` §13.
2. **Todo documento precisa ter `id` único** — checado por `check_kb_consistency.py` (produção) e por `run-conformance-tests.mjs` (`DUPLICATE_ID`, testado em `duplicate-id-a/b.md`).
3. **Todo `type` precisa ter schema** — `domain_knowledge` → `schemas/domain_knowledge.schema.json`; os nove tipos de `governed-docs` → `frontmatter/tests/schemas/governed-docs.schema.json`.
4. **Todo `status` precisa ser controlado** — `draft/review/approved/deprecated` (`domain_knowledge`) e `draft/review/approved/published/deprecated` (`governed-docs`), ambos como `enum` no schema.
5. **Todo artefato `approved` precisa ter evidência** — regra condicional `allOf`/`if`/`then` em `governed-docs.schema.json` (exige `approved_by`/`approved_at`/`approval_ref`); testado em `approved-without-evidence.md` e `published-without-evidence.md`.
6. **Toda relação deve apontar para outro artefato identificável** — checado em `run-conformance-tests.mjs` (`DANGLING_RELATIONSHIP`, testado em `dangling-relationship.md`).
7. **O corpo explica, o Front Matter governa** — o Markdown detalha; o Front Matter permite controle, busca, validação e execução automatizada.

## 5. Arquivos que devem existir

| Arquivo | Função | Status |
|---|---|---|
| `planos/Frontmatter.md` | Este documento — plano e catálogo de decisões | Existe |
| `schemas/domain_knowledge.schema.json` | Contrato de validação de conhecimento de domínio (produção) | Existe, tracked, em CI |
| `frontmatter/tests/schemas/governed-docs.schema.json` | Contrato de validação de documentação operacional | Existe |
| `ferramentas/kb_compile.py` | Converte Markdown + YAML `domain_knowledge` para JSON | Existe, tracked |
| `frontmatter/tests/scripts/compile-governed-doc.mjs` | Converte Markdown + YAML `governed-docs` para JSON canônico | Existe |
| `exemplos/domain_customer.md` / `.json` | Exemplo humano de entrada / saída canônica (`domain_knowledge`) | Existe, tracked |
| `frontmatter/templates/examples/filled/*.example.md` | Exemplos preenchidos por tipo (`governed-docs`) | Existe |
| `conteudo/FONTES_REGISTRADAS.md` | Ledger de fontes (produção) | Existe, tracked |
| `frontmatter/ledger/source-ledger-event.schema.json` | Contrato do ledger de origem/decisão/destino (`governed-docs`) | Existe |
| `ferramentas/check_kb_consistency.py` | Verifica consistência entre fontes e KB (produção) | Existe, tracked |
| `frontmatter/change_control/CHANGELOG.md` | Registra mudanças estruturais do contrato `governed-docs` | Existe |
| `frontmatter/governance/decision-register.md` | Justifica decisões de governança (DR-001 a DR-009) | Existe |
| `frontmatter/templates/` | Modelos por tipo de artefato (`governed-docs`) | Existe |
| `frontmatter/tests/` | Casos válidos e inválidos, harness de conformidade | Existe, roda 19/19 |

## 6. Configurações essenciais

Para planos, fluxos, pipelines e contratos (`domain_knowledge`, ver `governanca/CAMPOS FRONTMATTER.md` §10):

```yaml
governance:
  decision: DEC-KB-FORMATO-AUTORIA-001
  priority: high
  review_required: true
validation:
  schema: domain_knowledge.schema.json
  acceptanceCriteria: []
  rejectionCriteria: []
source:
  ids: []
  links: []
```

Para contratos de agente (ver §2.3 acima e `governanca/CAMPOS FRONTMATTER.md` §12).

## 7. Critérios de reprovação

Um documento deve ser reprovado se:

1. não tem Front Matter (`NO_FRONTMATTER`);
2. tem campo obrigatório ausente (`SCHEMA_REQUIRED`);
3. usa campo não documentado (`SCHEMA_ADDITIONAL_PROPERTY`);
4. tem `id` duplicado (`DUPLICATE_ID`);
5. tem `status` inválido (`SCHEMA_ENUM`);
6. diz `approved`/`published` sem evidência (`SCHEMA_REQUIRED` nos campos `approved_by`/`approved_at`/`approval_ref`);
7. aponta relação para artefato inexistente (`DANGLING_RELATIONSHIP`);
8. usa `type` sem schema (`SCHEMA_ENUM`, tipo fora do enum conhecido);
9. foi alterado sem changelog quando a mudança é estrutural (enforced por `frontmatter/change_control/detect-schema-change.mjs` + `validate-change-control.mjs`);
10. não pode ser convertido para JSON canônico;
11. usa YAML com chave duplicada (`YAML_DUPLICATE_KEY`);
12. contém placeholder `{{...}}` não preenchido (`UNFILLED_PLACEHOLDER`).

Todos os doze critérios têm um caso de teste correspondente em `frontmatter/tests/tests/fixtures/invalid/` e passam hoje (`npm --prefix frontmatter/tests test` → 19/19).

Regra principal: **Front Matter só vira sistema real quando existe schema, validação, evidência, rastreabilidade e bloqueio para erro. Sem isso, ele é apenas metadado decorativo.**

## 8. Limite atual (honestidade sobre o que ainda falta)

- `ferramentas/kb_validate.py` audita as fontes/ledger de `conteudo/` + `governanca/` (gates PREFLIGHT/SCHEMA/LEDGER_KB/etc.) — **não** varre todo `.md` do repositório exigindo Front Matter.
- O workflow `.github/workflows/frontmatter-conformance-tests.yml` só roda sobre `frontmatter/**` (as fixtures de teste). Ainda não existe, neste repositório, um diretório real de documentação operacional (`governed-docs`) fora de `frontmatter/templates/examples/`; quando existir, seu caminho deve ser adicionado aos gatilhos do workflow.
- Não existe ainda schema JSON dedicado para `role` (contrato de agente, §2.3/§6) — só descrito em prosa. Registrado como trabalho futuro.
- Extensão do contrato `governed-docs` para os demais tipos catalogados em `governanca/CAMPOS FRONTMATTER.md` §5 (`ledger_fonte`, `pipeline`, `teste`, `evidencia`) fica para uma decisão futura (`DR-0XX`), não implementada aqui.

## 9. Passo a passo executado (com critério de aceitação)

| # | Ação | Critério de aceitação | Status |
|---|---|---|---|
| 1 | Confirmar `frontmatter/**` autorizado no manifesto do run ativo | Presente em `arquivos_permitidos` | ✅ |
| 2 | Corrigir `document_type` → `type` em templates, exemplos e `template-index.json`; adicionar `id`/`schema_version`/`version` ausentes | Nenhuma ocorrência de `document_type:` resta em `frontmatter/templates/` | ✅ |
| 3 | Criar `governed-docs.schema.json` com `author`/`slug`/`release_version`/`published_at` declarados; descontinuar o arquivo homônimo antigo (sem renomear/excluir, por restrição do manifesto) | `grep` não mostra mais colisão de nome com `domain_knowledge` | ✅ |
| 4 | Corrigir a fixture `tutorial-approved.md` (relação apontava para `id` inexistente) | Harness aprova o caso com `actual_error_codes: []` | ✅ |
| 5 | Rodar o harness e regenerar `EXPECTED-REPORT.json` a partir de execução real | `npm --prefix frontmatter/tests test` → 19/19 | ✅ |
| 6 | Registrar `DR-009` como decisão real (estava só como exemplo de template) | `decision-register.md` tem seção própria para DR-009 | ✅ |
| 7 | Corrigir nomes de arquivo inexistentes citados em prosa/scripts (`docs-frontmatter.schema.json` etc.) | `grep -r` não retorna mais esses nomes em `frontmatter/` | ✅ |
| 8 | Corrigir caminhos-padrão dos scripts `change_control/`/`ledger/` para o layout real; criar `package.json` próprios | Scripts rodam com sucesso via `node <script>.mjs` a partir da raiz do repo | ✅ |
| 9 | Corrigir o workflow `.github/workflows/frontmatter-conformance-tests.yml` (gatilhos e `working-directory`) | Só referencia caminhos existentes; roda `npm ci`/`npm test` em `frontmatter/tests` | ✅ |
| 10 | Criar `compile-governed-doc.mjs` para gerar JSON canônico de documentos reais (não só fixtures) | Gera artefato válido a partir de `policy.example.md` | ✅ |
| 11 | Reescrever este documento | Sem a string `chatgpt response`; todo caminho citado existe | ✅ |
| 12 | Atualizar `AGENTS.md` com o novo comando obrigatório de validação | Comando presente e executa com sucesso | Ver `AGENTS.md` |

## 10. Verificação end-to-end

```bash
python3 ferramentas/kb_compile.py exemplos/domain_customer.md --schema schemas/domain_knowledge.schema.json --check-only
python3 ferramentas/check_kb_consistency.py .
python3 ferramentas/kb_validate.py .
npm --prefix frontmatter/tests ci && npm --prefix frontmatter/tests test
node frontmatter/change_control/validate-change-control.mjs
node frontmatter/ledger/validate-ledger.mjs frontmatter/ledger/source-ledger.example.jsonl
python3 -m unittest discover -s tests -v
```

A regra final é: **Front Matter YAML é a camada que permite que planos, fluxos, pipelines, contratos, papéis e decisões deixem de ser apenas documentos e passem a ser artefatos controláveis dentro de uma Base de Conhecimento viva — e isso só é verdade enquanto os comandos acima continuarem passando.**
