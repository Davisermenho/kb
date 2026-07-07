# Guia de Templates Documentais

Versão: 1.0  
Status: Ativo  
Responsável: Docs Platform  
Última atualização: 2026-07-07

---

## 1. Por que templates existem

Templates existem para reduzir erro humano e erro de agentes automatizados.

Sem template, pessoas podem criar variações como:

```yaml
name: "Guia de API"
type: "tutorial"
state: "done"
team: "plataforma"
date: "hoje"
```

Com template, o documento já nasce com os campos corretos:

```yaml
id: "{{doc_snake_case_id}}"
schema_version: "1.0"
version: "0.1.0"
title: "{{title}}"
description: "{{description}}"
type: "tutorial"
status: "draft"
owner_team: "{{owner_team}}"
created_at: "{{YYYY-MM-DD}}"
updated_at: "{{YYYY-MM-DD}}"
```

---

## 2. Princípio central

O template não substitui o schema.

O template ajuda a preencher corretamente.  
O schema decide se o documento é válido.

A relação correta é:

```text
template preenchível
      ↓
documento Markdown
      ↓
validador de front matter
      ↓
schema oficial
      ↓
artefato validado
```

---

## 3. Estrutura de cada template

Cada template contém:

1. YAML front matter com campos permitidos.
2. Comentários editoriais mínimos.
3. Corpo Markdown com seções esperadas.
4. Placeholders claros.
5. Valores controlados quando possível.

Exemplo de placeholder:

```text
{{title}}
{{description}}
{{owner_team}}
{{YYYY-MM-DD}}
```

---

## 4. Tipos documentais

### tutorial

Use quando o documento ensina uma tarefa passo a passo.

### api_reference

Use quando o documento descreve endpoints, parâmetros, respostas, erros e exemplos.

### release_note

Use quando o documento registra mudanças de versão.

### policy

Use quando o documento define regra, obrigação, escopo, exceção e revisão.

### runbook

Use quando o documento orienta operação, incidente, diagnóstico ou recuperação.

---

## 5. Como reduzir erros

### Use campos fechados

Use:

```yaml
status: "draft"
```

Não use:

```yaml
state: "em andamento"
```

### Use datas absolutas

Use:

```yaml
created_at: "2026-07-07"
```

Não use:

```yaml
created_at: "hoje"
```

### Use vocabulários controlados

Use:

```yaml
owner_team: "platform"
```

Não use:

```yaml
owner_team: "time da plataforma"
```

### Não misture campos derivados

Não coloque no front matter:

```yaml
url_path: "/docs/minha-url"
validation: "ok"
checksum: "..."
```

Esses campos pertencem ao pipeline, não ao autor.

---

## 6. Fluxo recomendado

```text
1. Criar documento a partir de template
2. Preencher placeholders
3. Rodar validação local
4. Abrir pull request
5. CI valida schema, Markdown, links e controle de mudanças
6. Pipeline gera artefato validado
7. Ledger registra origem, decisão e destino
```
