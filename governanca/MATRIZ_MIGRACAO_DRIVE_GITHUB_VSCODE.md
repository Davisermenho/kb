# Matriz de Migração Drive ↔ GitHub ↔ VS Code

## 1. Finalidade

Esta matriz define o destino e a fonte de verdade de cada artefato antes de qualquer cópia ou mesclagem. Ela é um plano de controle: a presença de uma linha não significa que o conteúdo já foi migrado.

Durante a migração:

- Google Drive preserva documentação histórica, decisões e materiais de origem.
- GitHub é a fonte operacional de arquivos, scripts, schemas, ledger, testes e CI.
- VS Code é o ambiente de execução; suas configurações não substituem os artefatos versionados.
- Conteúdo do Drive deve ser comparado com o arquivo de destino antes de qualquer alteração.

## 2. Estados usados

- `EXISTENTE`: o destino já existe no repositório.
- `CONFIGURADO`: o artefato local versionado já foi criado ou ajustado.
- `PLANEJADO`: o destino está definido, mas ainda não foi criado.
- `COMPARAÇÃO_PENDENTE`: origem e destino precisam ser comparados antes de mesclar.
- `VALIDAÇÃO_PENDENTE`: o artefato existe, mas a fase de migração correspondente ainda precisa validá-lo.

## 3. Matriz

| Artefato no Drive | Arquivo no GitHub | Tipo | Fonte de verdade | Status | Validador aplicável | Agente autorizado | Observação de migração |
|---|---|---|---|---|---|---|---|
| KB v2 — 005 Decisões Registradas | `governanca/decisoes/DECISOES_KB_V2.md` | Governança documental | GitHub após revisão humana | `PLANEJADO` | Revisão humana e referências internas | Claude Code; humano aprova | Criar somente após comparar decisões e identificar conflitos. |
| KB v2 — 003 Pipeline Operacional | `governanca/PIPELINE_OPERACIONAL.md` | Governança operacional | GitHub | `PLANEJADO` | `python3 ferramentas/kb_validate.py .` e revisão humana | Claude Code ou Codex; humano aprova | Não duplicar regras já canônicas em `governanca/PROTOCOLO.md` e `governanca/LEDGER_KB_VERIFY.md`. |
| KB v2 — 002 Schemas | `governanca/SCHEMAS.md` | Documentação de schemas | GitHub | `PLANEJADO` | Revisão de referências internas | Claude Code; humano aprova | Documento explicativo; não substitui schema executável. |
| KB v2 — 002 Schemas | `schemas/domain_knowledge.schema.json` | Schema operacional | GitHub | `PLANEJADO` | Validação JSON Schema e testes específicos | Codex; humano aprova arquitetura | Comparar versão do Drive e contratos existentes antes de criar. |
| KB v2 — 004 Testes e Evidências | `governanca/TESTES_E_EVIDENCIAS.md` | Governança documental | GitHub | `PLANEJADO` | Revisão humana e conferência dos comandos reais | Claude Code ou Codex; humano aprova | Separar evidência executada de teste apenas planejado. |
| KB v2 — Registro Operacional de Arquivos | `governanca/REGISTRY_OPERACIONAL.md` | Registro documental | GitHub | `PLANEJADO` | Revisão de completude e referências internas | Claude Code; humano aprova | Não concorrer com Git nem com `governanca/Inventario.md` como inventário da árvore. |
| `FONTES_REGISTRADAS.md` | `conteudo/FONTES_REGISTRADAS.md` | Ledger operacional | GitHub | `COMPARAÇÃO_PENDENTE` | `check_kb_consistency.py`, `kb_validate.py` e revisão semântica | Claude Code analisa; Codex valida; humano resolve conflitos | O destino já existe e não pode ser sobrescrito; comparar, mesclar por `ID_FONTE` e validar. |
| `domain_customer.md` | `exemplos/domain_customer.md` | Exemplo de entrada | GitHub | `PLANEJADO` | `kb_compile.py --check-only` quando disponível | Codex | Criar apenas junto do compilador/schema compatível ou após contrato definido. |
| `domain_customer.json` | `exemplos/domain_customer.json` | Exemplo compilado | GitHub | `PLANEJADO` | JSON Schema e teste de não regressão | Codex | Deve corresponder ao Markdown e ao schema versionados. |
| `domain_knowledge.schema.json` | `schemas/domain_knowledge.schema.json` | Schema operacional | GitHub | `PLANEJADO` | JSON Schema e `test_domain_schema.py` quando implementado | Codex; humano aprova arquitetura | Preservar a versão mais atual após comparação reproduzível. |
| `kb_compile.py` | `ferramentas/kb_compile.py` | Ferramenta executável | GitHub | `PLANEJADO` | Testes unitários e execução `--check-only` | Codex; revisão independente | Confirmar imports e caminhos antes de incorporar. |
| `check_kb_consistency.py` | `ferramentas/check_kb_consistency.py` | Ferramenta executável | GitHub | `COMPARAÇÃO_PENDENTE` | Suíte existente e checker canônico | Codex; revisão independente | O destino já existe; não substituir sem diff, testes e justificativa. |
| Configuração Claude Code local | `.claude/settings.json` e `.claude/hooks/kb_consistency_hook.py` | Integração local versionada | GitHub | `CONFIGURADO` | Hook local e `kb_validate.py` | Claude Code ou Codex | Configuração usa caminho relativo; nenhuma regra deve ser duplicada no hook. |
| Configuração VS Code | `.vscode/extensions.json`, `.vscode/settings.json`, `.vscode/tasks.json` | Ambiente local versionado | GitHub | `CONFIGURADO` | Parse JSON e execução das tasks | Codex | VS Code apenas invoca comandos canônicos do repositório. |
| Contrato comum dos agentes | `AGENTS.md` | Governança agentiva | GitHub | `EXISTENTE` | Revisão humana | Humano aprova; agentes obedecem | Porta de entrada comum; não substitui o protocolo. |
| Instruções específicas dos agentes | `CLAUDE.md` e `CODEX.md` | Governança agentiva | GitHub | `CONFIGURADO` | Revisão humana | Humano aprova; agente correspondente obedece | `CODEX.md` é complementar; `AGENTS.md` é o contrato descoberto automaticamente pelo Codex. |

## 4. Regra de decisão

Quando Drive e GitHub divergirem:

1. preservar ambos os conteúdos para comparação;
2. identificar diferenças e impacto operacional;
3. manter o GitHub como estado operacional vigente;
4. solicitar decisão humana para conflito semântico ou arquitetural;
5. mesclar somente em branch, dentro do manifesto e com testes;
6. registrar a evidência no run antes de promover a mudança.

Nenhuma linha desta matriz autoriza exclusão, sobrescrita integral ou publicação automática.
