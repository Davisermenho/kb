# CHANGELOG — Padrão de Metadados Documentais

Todas as mudanças notáveis deste padrão serão documentadas neste arquivo.

Este changelog segue categorias inspiradas em Keep a Changelog e usa versionamento semântico para indicar impacto de compatibilidade.

---

## [Unreleased]

### Added

- Nenhuma mudança pendente registrada.

### Changed

- Nenhuma mudança pendente registrada.

### Deprecated

- Nenhuma mudança pendente registrada.

### Removed

- Nenhuma mudança pendente registrada.

### Fixed

- Nenhuma mudança pendente registrada.

### Security

- Nenhuma mudança pendente registrada.

### Migration

- Nenhuma migração pendente registrada.

---

## [1.1.0] - 2026-07-07

### Added

- Adicionado campo opcional `risk_level` para documentos do tipo `policy` e `runbook`.
- Adicionados valores controlados para `risk_level`: `low`, `medium`, `high`, `critical`.
- Adicionado registro estrutural `SC-2026-07-07-002` no histórico de mudanças estruturais.

### Changed

- Atualizado o schema `governed-docs.schema.json` para reconhecer `risk_level`.
- Atualizado o documento de governança para incluir regras de avaliação de risco documental.

### Migration

- Documentos existentes não precisam ser migrados, porque `risk_level` foi introduzido como campo opcional.
- Documentos do tipo `policy` podem adotar `risk_level` progressivamente.

### Governance

- Decisão associada: `DR-009 — Introduzir risk_level para documentos operacionais críticos`.

---

## [1.0.0] - 2026-07-07

### Added

- Criado o Perfil de Aplicação de Metadados Documentais.
- Criado o JSON Schema oficial para YAML front matter.
- Criado o contrato de artefato JSON validado.
- Criado o ledger append-only de origem, decisão e destino.
- Criado o registro de decisões de governança.
- Criado o documento de governança do padrão.
- Criado processo de validação automática no CI.
- Criado bloqueio de campos desconhecidos por `additionalProperties: false`.
- Adicionado registro estrutural `SC-2026-07-07-001` no histórico de mudanças estruturais.

### Security

- Definida regra de que saída de IA é candidata, não autoridade.
- Definida separação entre `metadata`, `content`, `derived`, `validation` e `provenance`.
- Definida obrigação de registrar origem rastreável para artefatos.

### Governance

- Decisão associada: `DR-001 — Usar um perfil oficial de metadados`.
- Decisão associada: `DR-002 — Usar JSON Schema como contrato de validação`.
- Decisão associada: `DR-003 — Bloquear campos desconhecidos`.
- Decisão associada: `DR-005 — Usar ledger append-only de origem, decisão e destino`.
