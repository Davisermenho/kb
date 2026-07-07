---
id: "{{doc_snake_case_id}}"
schema_version: "1.0"
version: "0.1.0"
title: "{{runbook_title}}"
description: "{{description_20_to_280_chars}}"
type: "runbook"
status: "draft"
owner_team: "{{docs|platform|security|billing|support}}"
author: "{{author_name}}"
created_at: "{{YYYY-MM-DD}}"
updated_at: "{{YYYY-MM-DD}}"
risk_level: "{{low|medium|high|critical}}"
slug: "{{kebab-case-slug}}"
tags:
  - "operations"
---

# {{runbook_title}}

## Quando usar

Explique em quais situações este runbook deve ser executado.

## Sinais e sintomas

- {{symptom_1}}
- {{symptom_2}}

## Pré-requisitos

- Acesso necessário: {{access}}
- Ferramentas necessárias: {{tools}}

## Procedimento

### 1. Diagnosticar

```bash
{{diagnostic_command}}
```

Resultado esperado:

```text
{{expected_output}}
```

### 2. Mitigar

```bash
{{mitigation_command}}
```

### 3. Validar recuperação

```bash
{{validation_command}}
```

## Critérios de escalonamento

Escalone se:

- {{escalation_condition}}

## Pós-incidente

- Registrar causa raiz.
- Atualizar este runbook se necessário.
- Criar follow-up para prevenção.
