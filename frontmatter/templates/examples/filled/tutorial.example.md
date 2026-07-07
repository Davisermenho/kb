---
id: "doc_auth_oauth2_tutorial"
schema_version: "1.0"
version: "0.1.0"
title: "Autenticação com OAuth2"
description: "Aprenda a autenticar chamadas à API usando OAuth2 de forma segura."
type: "tutorial"
status: "draft"
owner_team: "platform"
author: "Davi Sermenho"
created_at: "2026-07-07"
updated_at: "2026-07-07"
slug: "autenticacao-com-oauth2"
tags:
  - "api"
  - "authentication"
  - "oauth2"
---

# Autenticação com OAuth2

## Objetivo

Ao final deste tutorial, você conseguirá obter um token OAuth2 e usá-lo em chamadas autenticadas à API.

## Pré-requisitos

- Conta ativa na plataforma.
- Credenciais de cliente OAuth2.

## Passo 1 — Solicitar token

```bash
curl -X POST "https://api.example.com/oauth/token"
```

## Passo 2 — Usar token

Envie o token no cabeçalho `Authorization`.

## Verificação

A chamada deve retornar status `200`.

## Solução de problemas

| Problema | Causa provável | Como resolver |
|---|---|---|
| Token inválido | Credencial incorreta | Gere novas credenciais |

## Próximos passos

- Ler a referência completa da API.
