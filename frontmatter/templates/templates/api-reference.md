---
id: "{{doc_snake_case_id}}"
schema_version: "1.0"
version: "0.1.0"
title: "{{endpoint_or_api_title}}"
description: "{{description_20_to_280_chars}}"
type: "api_reference"
status: "draft"
owner_team: "{{docs|platform|security|billing|support}}"
author: "{{author_name}}"
created_at: "{{YYYY-MM-DD}}"
updated_at: "{{YYYY-MM-DD}}"
slug: "{{kebab-case-slug}}"
tags:
  - "api"
---

# {{endpoint_or_api_title}}

## Visão geral

Descreva o objetivo deste endpoint ou recurso da API.

## Endpoint

```http
{{METHOD}} {{/path/to/resource}}
```

## Autenticação

Descreva o mecanismo de autenticação exigido.

## Parâmetros de path

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| {{param_name}} | {{string|number|boolean}} | {{sim|não}} | {{description}} |

## Parâmetros de query

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| {{param_name}} | {{string|number|boolean}} | {{sim|não}} | {{description}} |

## Corpo da requisição

```json
{
  "{{field}}": "{{value}}"
}
```

## Resposta

```json
{
  "{{field}}": "{{value}}"
}
```

## Códigos de erro

| Código | Significado | Como resolver |
|---:|---|---|
| 400 | {{meaning}} | {{resolution}} |
| 401 | {{meaning}} | {{resolution}} |

## Exemplo

```bash
curl -X {{METHOD}} "https://api.example.com{{/path/to/resource}}" \
  -H "Authorization: Bearer $TOKEN"
```
