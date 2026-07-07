---
id: "doc_create_payment_reference"
schema_version: "1.0"
version: "0.1.0"
title: "Criar pagamento"
description: "Referência do endpoint usado para criar um novo pagamento na API."
type: "api_reference"
status: "draft"
owner_team: "billing"
author: "Davi Sermenho"
created_at: "2026-07-07"
updated_at: "2026-07-07"
slug: "criar-pagamento"
tags:
  - "api"
  - "billing"
---

# Criar pagamento

## Visão geral

Este endpoint cria um novo pagamento.

## Endpoint

```http
POST /payments
```

## Autenticação

Requer token Bearer.

## Parâmetros de path

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| — | — | não | Não há parâmetros de path |

## Parâmetros de query

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| idempotency_key | string | não | Chave para evitar duplicação |

## Corpo da requisição

```json
{
  "amount": 1000,
  "currency": "BRL"
}
```

## Resposta

```json
{
  "id": "pay_123",
  "status": "created"
}
```

## Códigos de erro

| Código | Significado | Como resolver |
|---:|---|---|
| 400 | Requisição inválida | Verifique campos obrigatórios |
| 401 | Não autenticado | Envie token válido |

## Exemplo

```bash
curl -X POST "https://api.example.com/payments" \
  -H "Authorization: Bearer $TOKEN"
```
