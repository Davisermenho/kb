# Registro de Decisões do Padrão de Metadados Documentais

Versão: 1.0  
Status: Ativo  
Responsável: Docs Platform / Metadata Governance  
Última atualização: 2026-07-07

---

## 1. Finalidade

Este documento registra as decisões arquiteturais, editoriais e técnicas que justificam o padrão de metadados usado nos documentos digitais do projeto.

O objetivo é evitar que campos de metadados sejam criados de forma arbitrária por pessoas, agentes de IA, scripts ou sistemas diferentes.

Este registro responde:

- por que o padrão existe;
- quais decisões foram tomadas;
- quais alternativas foram consideradas;
- quais consequências foram aceitas;
- quem é responsável por manter o padrão;
- como mudanças devem ser propostas e aprovadas.

---

## 2. Decisão DR-001 — Usar um perfil oficial de metadados

### Status

Aceita.

### Contexto

Documentos Markdown com YAML front matter podem ser criados por múltiplas pessoas, agentes de IA e automações. Sem um perfil oficial, diferentes autores tendem a criar campos equivalentes com nomes diferentes.

Exemplos de variações indesejadas:

```yaml
title: "Guia de API"
name: "Guia de API"
doc_title: "Guia de API"
titulo: "Guia de API"
```

Essas variações dificultam busca, publicação, validação, governança, migração e consumo por IA.

### Decisão

Será adotado um Perfil de Aplicação de Metadados oficial, contendo:

- lista de campos permitidos;
- definição de cada campo;
- tipo de dado;
- obrigatoriedade;
- valores permitidos;
- exemplos;
- dono do campo;
- versão do schema;
- regras de validação.

### Alternativas consideradas

1. Permitir campos livres.
2. Usar apenas convenção informal em README.
3. Validar somente durante publicação.
4. Usar um perfil oficial com schema executável.

### Opção escolhida

Usar um perfil oficial com schema executável.

### Motivos

A opção escolhida permite padronização, automação e bloqueio preventivo de documentos inválidos.

### Consequências

- Campo novo precisa ser proposto e aprovado.
- Agentes de IA não podem inventar novos campos.
- Pull requests com metadados inválidos devem falhar no CI.
- O padrão precisa ser versionado.

---

## 3. Decisão DR-002 — Usar JSON Schema como contrato de validação

### Status

Aceita.

### Contexto

O front matter é escrito em YAML, mas precisa ser validado automaticamente. YAML pode ser convertido para um objeto equivalente a JSON, permitindo validação com JSON Schema.

### Decisão

O contrato oficial de validação será escrito em JSON Schema.

### Alternativas consideradas

1. Validação manual.
2. Regras ad hoc em scripts.
3. JSON Schema.
4. Zod/Joi/TypeScript como contrato principal.
5. SHACL ou RDF.
6. XSD/Relax NG.

### Opção escolhida

JSON Schema.

### Motivos

JSON Schema é adequado para objetos chave-valor, permite validação de tipos, campos obrigatórios, enums, formatos, padrões e proibição de campos desconhecidos.

### Consequências

- Todo front matter deve ser convertido para objeto antes de validar.
- O schema passa a ser a fonte de verdade.
- Scripts e CI devem usar o mesmo schema.
- Regras fora do alcance do schema podem ser implementadas como checks adicionais.

---

## 4. Decisão DR-003 — Bloquear campos desconhecidos

### Status

Aceita.

### Contexto

Sem bloqueio explícito, agentes e pessoas podem criar campos com nomes diferentes para conceitos semelhantes.

Exemplo:

```yaml
status: "published"
state: "done"
situacao: "pronto"
publication_status: "live"
```

### Decisão

Campos não listados no schema oficial serão rejeitados automaticamente.

### Implementação

No JSON Schema:

```json
{
  "additionalProperties": false
}
```

### Motivos

Essa regra elimina divergência semântica e impede crescimento descontrolado do vocabulário.

### Consequências

- Documentos com campos não aprovados falham.
- Necessidades novas devem virar propostas formais de campo.
- A governança precisa manter um processo simples de aprovação.

---

## 5. Decisão DR-004 — Separar metadados originais, conteúdo, derivados e proveniência

### Status

Aceita.

### Contexto

Misturar campos fornecidos pelo autor com campos calculados pelo pipeline cria riscos de segurança, inconsistência e perda de rastreabilidade.

Exemplo perigoso:

```yaml
url_path: "/admin/delete"
published: true
```

### Decisão

O artefato final deve separar:

- `metadata`: campos validados vindos do front matter;
- `content`: corpo convertido ou extraído;
- `derived`: campos calculados pelo pipeline;
- `validation`: resultado da validação;
- `provenance`: dados de rastreabilidade.

### Motivos

A separação impede que autores ou agentes controlem campos que devem ser responsabilidade do sistema.

### Consequências

- Campos como URL final, hash, validação e destino não devem vir do front matter.
- O pipeline deve calcular e registrar esses campos.
- Consumidores devem confiar apenas no artefato validado, não no documento bruto.

---

## 6. Decisão DR-005 — Usar ledger append-only de origem, decisão e destino

### Status

Aceita.

### Contexto

É necessário rastrear como um documento foi transformado em artefato, índice, página publicada ou relatório de rejeição.

Sem um ledger, torna-se difícil responder:

- qual arquivo originou este artefato?
- qual schema estava em vigor?
- qual commit foi processado?
- quem ou qual sistema executou?
- por que o documento foi aceito ou rejeitado?
- para onde o resultado foi enviado?

### Decisão

Cada etapa relevante do pipeline deve registrar um evento em um ledger append-only no formato JSON Lines.

### Eventos mínimos

- `document_ingested`
- `metadata_validated`
- `document_rejected`
- `artifact_generated`
- `artifact_published`
- `ai_output_validated`

### Motivos

O ledger cria rastreabilidade operacional e auditoria do processo documental.

### Consequências

- Eventos antigos não devem ser editados.
- Correções devem ser registradas como novos eventos.
- Cada evento deve conter origem, decisão, destino, ator e proveniência.
- O ledger deve ser validado por schema.

---

## 7. Decisão DR-006 — Tratar saída de IA como candidata, não como autoridade

### Status

Aceita.

### Contexto

Agentes de IA podem gerar metadados, resumos, classificações e propostas de campos. Porém, a saída da IA pode conter erro, alucinação, campos inventados ou instruções embutidas.

### Decisão

Saídas de IA devem ser tratadas como candidatas e só podem ser consumidas após validação.

### Regras

- IA não pode alterar diretamente status de publicação.
- IA não pode aprovar campo novo.
- IA não pode escrever proveniência final.
- IA não pode publicar documento sem validação.
- IA não pode sobrescrever decisões do schema.

### Motivos

Essa regra reduz risco de prompt injection, inconsistência e decisões não auditáveis.

### Consequências

- Saída da IA deve usar formato estruturado.
- Saída da IA deve passar por schema.
- Ações sensíveis exigem regra de negócio ou revisão humana.

---

## 8. Decisão DR-007 — Versionar o padrão

### Status

Aceita.

### Contexto

Campos e regras mudam ao longo do tempo. Sem versionamento, documentos antigos podem se tornar inválidos sem explicação.

### Decisão

Todo schema, perfil e documento de governança deve ter versão explícita.

### Campos obrigatórios

```yaml
schema_version: "1.0"
```

ou, no artefato final:

```json
{
  "schema_version": "1.0"
}
```

### Motivos

Versionamento permite migração, compatibilidade e auditoria.

### Consequências

- Mudanças incompatíveis devem gerar nova versão maior.
- Mudanças retrocompatíveis podem gerar versão menor.
- Scripts devem registrar qual versão foi usada.

---

## 9. Decisão DR-008 — Validar antes de publicar

### Status

Aceita.

### Contexto

Publicar documentos inválidos pode quebrar busca, navegação, páginas, automações e consumo por IA.

### Decisão

Nenhum documento pode ser publicado sem passar por validação automática.

### Ordem mínima

1. Parsing de front matter.
2. Validação YAML.
3. Validação JSON Schema.
4. Regras de negócio.
5. Conversão para artefato.
6. Validação do artefato.
7. Registro no ledger.
8. Publicação.

### Motivos

Validação antecipada reduz falhas posteriores.

### Consequências

- Pull requests inválidos falham.
- Artefatos inválidos não entram em índice.
- Rejeições devem gerar relatório e evento no ledger.

---

## 10. Decisão DR-009 — Introduzir risk_level para documentos operacionais críticos

### Status

Aceita.

### Contexto

Documentos do tipo `policy` e `runbook` podem descrever procedimentos ou regras cujo descumprimento tem impacto operacional alto (ex.: retenção de logs de segurança, runbook de indisponibilidade de API). Sem um campo controlado de risco, não há como priorizar revisão nem alertar automaticamente sobre documentos críticos desatualizados.

### Decisão

Adicionar o campo opcional `risk_level` (`low`, `medium`, `high`, `critical`) ao schema `governed-docs.schema.json`, obrigatório para `type: policy` e `type: runbook` via regra condicional (`allOf`/`if`/`then`).

### Alternativas consideradas

1. Não ter campo de risco (deixar a criticidade implícita na prosa).
2. Usar um campo de texto livre (`risk: "muito perigoso"`).
3. Usar um enum controlado `risk_level`, obrigatório por tipo.

### Motivos

Um enum controlado permite priorização automática, alertas e relatórios de qualidade sem ambiguidade textual.

### Consequências

- `policy` e `runbook` sem `risk_level` passam a ser reprovados pelo schema (`SCHEMA_REQUIRED`).
- Documentos existentes desses tipos precisam adotar o campo antes de serem `approved`/`published`.
- Registrado em `CHANGELOG.md` [1.1.0] e em `structural-changes.jsonl` (`SC-2026-07-07-002`).

### Critério de aceite

`frontmatter/tests/schemas/governed-docs.schema.json` exige `risk_level` para `policy` e `runbook`; as fixtures `policy-missing-risk-level.md` (deve reprovar) e `policy-approved.md`/`runbook-draft.md` (devem aprovar) confirmam o comportamento no harness de testes.

---

## 11. Como propor nova decisão

Toda nova decisão deve conter:

```yaml
id: "DR-XXX"
title: "Título da decisão"
status: "proposed | accepted | rejected | superseded"
context: "Problema ou necessidade"
decision: "Decisão tomada"
alternatives: []
rationale: "Motivos"
consequences: []
owner: "Equipe responsável"
date: "YYYY-MM-DD"
```

---

## 12. Regra final

O padrão existe para garantir que documentos digitais sejam:

- consistentes;
- validáveis;
- processáveis;
- rastreáveis;
- seguros para IA;
- interoperáveis;
- auditáveis;
- mantidos por governança explícita.

A regra operacional é:

> Pessoas e agentes podem criar conteúdo, mas somente o padrão validado decide quais metadados existem, quais valores são aceitos e quais documentos podem seguir no pipeline.
