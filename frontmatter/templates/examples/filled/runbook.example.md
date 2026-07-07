---
id: "doc_api_outage_runbook"
schema_version: "1.0"
version: "0.1.0"
title: "Runbook de indisponibilidade da API"
description: "Procedimento operacional para diagnosticar e mitigar indisponibilidade da API."
type: "runbook"
status: "draft"
owner_team: "platform"
author: "Davi Sermenho"
created_at: "2026-07-07"
updated_at: "2026-07-07"
risk_level: "critical"
slug: "runbook-indisponibilidade-api"
tags:
  - "operations"
  - "troubleshooting"
  - "api"
---

# Runbook de indisponibilidade da API

## Quando usar

Use este runbook quando a API apresentar taxa elevada de erros 5xx ou indisponibilidade total.

## Sinais e sintomas

- Aumento de respostas 5xx.
- Alertas de health check falhando.

## Pré-requisitos

- Acesso necessário: observabilidade e deploy.
- Ferramentas necessárias: logs, métricas e terminal.

## Procedimento

### 1. Diagnosticar

```bash
curl -I https://api.example.com/health
```

Resultado esperado:

```text
HTTP/2 200
```

### 2. Mitigar

```bash
kubectl rollout restart deployment/api
```

### 3. Validar recuperação

```bash
curl -I https://api.example.com/health
```

## Critérios de escalonamento

Escalone se:

- A indisponibilidade persistir por mais de 10 minutos.

## Pós-incidente

- Registrar causa raiz.
- Atualizar este runbook se necessário.
- Criar follow-up para prevenção.
