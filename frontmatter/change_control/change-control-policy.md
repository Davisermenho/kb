# Política de Controle de Mudanças Estruturais

Versão: 1.0  
Status: Ativo  
Responsável: Metadata Governance Board  
Última atualização: 2026-07-07

---

## 1. Objetivo

Esta política impede alterações invisíveis no padrão de metadados documentais.

Uma alteração invisível ocorre quando um schema, script, vocabulário, regra de validação, formato de artefato ou processo de governança muda sem registro explícito, sem decisão associada ou sem impacto de compatibilidade declarado.

---

## 2. Arquivos oficiais de controle

O controle de mudanças estruturais é composto por:

```text
CHANGELOG.md
change-control/structural-changes.jsonl
change-control/structural-change-event.schema.json
change-control/change-control-policy.md
change-control/validate-change-control.mjs
change-control/detect-schema-change.mjs
```

## 3. Diferença entre changelog e histórico estrutural

### CHANGELOG.md

Documento humano, curado, organizado por versão.

Responde:

- o que mudou nesta versão;
- o que foi adicionado;
- o que mudou;
- o que foi removido;
- se há migração;
- se há impacto de segurança.

### structural-changes.jsonl

Registro estruturado, validável por máquina, com um evento por mudança estrutural.

Responde:

- qual componente foi alterado;
- se a mudança é breaking;
- se exige migração;
- qual decisão autorizou;
- quem aprovou;
- quais checks são obrigatórios.

---

## 4. Categorias do changelog

Cada versão deve usar estas categorias quando aplicável:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security
- Migration
- Governance

---

## 5. Tipos de mudança estrutural

Mudanças estruturais incluem:

- campo adicionado;
- campo removido;
- campo renomeado;
- tipo de campo alterado;
- campo obrigatório tornado opcional ou vice-versa;
- valor de enum adicionado ou removido;
- regra de validação alterada;
- formato do artefato final alterado;
- formato do ledger alterado;
- comportamento de script alterado;
- regra de governança alterada.

---

## 6. Regras de versionamento

Use versionamento semântico:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

Use quando a mudança quebra compatibilidade.

Exemplos:

- remover campo aceito;
- mudar significado de campo existente;
- alterar tipo de campo;
- tornar campo opcional em obrigatório;
- remover valor permitido de enum;
- alterar formato do artefato de saída.

### MINOR

Use quando adiciona capacidade sem quebrar documentos válidos.

Exemplos:

- adicionar campo opcional;
- adicionar novo valor de enum;
- adicionar novo tipo de documento;
- adicionar nova regra que só gera warning.

### PATCH

Use para correções sem mudança semântica.

Exemplos:

- corrigir descrição;
- corrigir exemplo;
- corrigir erro de documentação;
- ajustar mensagem de erro sem mudar regra.

---

## 7. Regra de bloqueio

Toda mudança estrutural precisa ter:

1. entrada em `CHANGELOG.md`;
2. evento em `structural-changes.jsonl`;
3. decisão associada em `decision-register.md`;
4. versão antes e depois;
5. classificação de compatibilidade;
6. plano de migração quando breaking;
7. aprovação registrada;
8. validação no CI.

Sem isso, a mudança deve ser bloqueada.

---

## 8. Exemplo de mudança permitida

Adicionar campo opcional:

```json
{
  "change_type": "field_added",
  "version_before": "1.0.0",
  "version_after": "1.1.0",
  "breaking": false,
  "requires_migration": false
}
```

## 9. Exemplo de mudança bloqueada

Alterar `status` sem registro:

```diff
- "enum": ["draft", "review", "approved", "published", "deprecated"]
+ "enum": ["draft", "published"]
```

Essa mudança remove valores permitidos. É breaking. Deve ter decisão, changelog, evento estrutural e plano de migração.

---

## 10. Regra final

Nenhum schema, vocabulário, validador ou formato de artefato deve mudar silenciosamente.

A regra operacional é:

> Mudança estrutural sem changelog, sem decisão e sem evento validado é mudança inválida.
