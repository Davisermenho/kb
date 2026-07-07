---
id: "{{doc_snake_case_id}}"
schema_version: "1.0"
version: "0.1.0"
title: "{{policy_title}}"
description: "{{description_20_to_280_chars}}"
type: "policy"
status: "draft"
owner_team: "{{docs|platform|security|billing|support}}"
author: "{{author_name}}"
created_at: "{{YYYY-MM-DD}}"
updated_at: "{{YYYY-MM-DD}}"
effective_date: "{{YYYY-MM-DD}}"
next_review_at: "{{YYYY-MM-DD}}"
risk_level: "{{low|medium|high|critical}}"
slug: "{{kebab-case-slug}}"
tags:
  - "policy"
---

# {{policy_title}}

## Propósito

Explique por que esta política existe.

## Escopo

Defina onde esta política se aplica.

## Política

Descreva a regra obrigatória.

## Responsabilidades

| Papel | Responsabilidade |
|---|---|
| {{role}} | {{responsibility}} |

## Exceções

Explique se exceções são permitidas e como devem ser aprovadas.

## Conformidade

Explique como a conformidade será verificada.

## Revisão

Esta política deve ser revisada até `{{next_review_at}}`.

## Histórico

| Data | Mudança | Responsável |
|---|---|---|
| {{YYYY-MM-DD}} | Criação da política | {{owner}} |
