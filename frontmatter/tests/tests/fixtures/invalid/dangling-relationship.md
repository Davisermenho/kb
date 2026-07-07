---
id: "doc_dangling_rel"
schema_version: "1.0"
type: "tutorial"
title: "Documento com relação quebrada"
description: "Este documento referencia um ID que não existe no conjunto de testes."
status: "draft"
owner_team: "platform"
created_at: "2026-07-07"
updated_at: "2026-07-07"
version: "0.1.0"
relationships:
  - type: "depends_on"
    target_id: "doc_does_not_exist"
---

# Documento com relação quebrada

Corpo.
