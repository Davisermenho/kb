---
id: "{{doc_snake_case_id}}"
schema_version: "1.0"
version: "{{MAJOR.MINOR.PATCH}}"
title: "Release {{version}}"
description: "{{description_20_to_280_chars}}"
type: "release_note"
status: "draft"
owner_team: "{{docs|platform|security|billing|support}}"
author: "{{author_name}}"
created_at: "{{YYYY-MM-DD}}"
updated_at: "{{YYYY-MM-DD}}"
published_at: "{{YYYY-MM-DD}}"
release_version: "{{MAJOR.MINOR.PATCH}}"
slug: "release-{{major-minor-patch}}"
tags:
  - "release"
---

# Release {{version}}

## Resumo

Descreva em poucas linhas o objetivo desta release.

## Adicionado

- {{new_feature}}

## Alterado

- {{changed_behavior}}

## Corrigido

- {{bug_fix}}

## Removido

- {{removed_item}}

## Mudanças incompatíveis

- {{breaking_change_or_none}}

## Impacto para usuários

Explique quem é afetado e o que precisa ser feito.

## Migração

```text
{{migration_steps_or_not_applicable}}
```

## Referências

- {{link_or_issue}}
