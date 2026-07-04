# Verificação do Fluxo V2

## 1. Escopo

O projeto usa dois níveis de validação:

1. `ferramentas/check_kb_consistency.py`: estrutura, duplicidade, códigos de KB e presença bidirecional ledger↔KB.
2. `ferramentas/kb_validate.py`: orquestra o checker e os gates adicionais do Fluxo V2.

Nenhum deles prova, sozinho, verdade factual externa, fidelidade semântica integral ou julgamento humano de conflitos.

## 2. Checker estrutural V2

```bash
python3 ferramentas/check_kb_consistency.py [diretorio]
python3 ferramentas/check_kb_consistency.py [diretorio] --json
```

Códigos:

- `0`: parsing concluído, sem divergência estrutural;
- `1`: estrutura ou consistência divergente;
- `2`: falha operacional que impediu verificação confiável.

O checker valida:

- presença única de `## Registros`;
- ledger não vazio;
- campos essenciais;
- enums de roteamento;
- formato e coincidência de `ID_FONTE`;
- duplicidade por ID, título e URL canônica;
- códigos e nomes de arquivos de KB;
- colisão de código entre arquivos;
- destino vazio ou inexistente;
- presença bidirecional ledger↔KB;
- duplicidade dentro da mesma KB.

Sua saída de sucesso é deliberadamente limitada:

```text
OK ESTRUTURAL: invariantes ledger↔KB verificadas.
NÃO VERIFICADO: factualidade, fidelidade semântica, causalidade, escopo e atualidade.
```

## 3. Orquestrador

```bash
python3 ferramentas/kb_validate.py [diretorio]
python3 ferramentas/kb_validate.py [diretorio] --json
python3 ferramentas/kb_validate.py [diretorio] --publish --run-id RUN-...
```

Gates:

- `PREFLIGHT`;
- `SCHEMA`;
- `DUPLICIDADE`;
- `SCORE_STATUS`;
- `ROTEAMENTO`;
- `LEDGER_KB`;
- `REFERENCIAS_INTERNAS`;
- `PENDENCIAS`;
- `ESCOPO_DIFF`;
- `CAUSALIDADE`;
- `REVISAO`.

No modo auditoria, gates dependentes de `RUN_ID` aparecem como `SKIPPED` e não são apresentados como aprovados. No modo `--publish`, qualquer `FAIL`, `WARN` ou `SKIPPED` bloqueia a publicação.

## 4. RUN_ID, rascunho e manifesto

```bash
python3 ferramentas/kb_workflow.py --directory . init-run \
  --run-id RUN-2026-EXEMPLO \
  --objective "Registrar uma fonte" \
  --risk medio \
  --file conteudo/FONTES_REGISTRADAS.md \
  --file KB-01_Engenharia_de_Contexto.md \
  --operation editar
```

Isso cria:

- `.kb/runs/<RUN_ID>/manifest.json`;
- `.kb/runs/<RUN_ID>/draft.md`.

O rascunho não é conteúdo publicado. A publicação exige baseline Git, manifesto, diff dentro do escopo e revisão proporcional ao risco.

Antes de validar em modo de publicação, avance o run pelas transições válidas até `PREPARADO` e prepare no índice Git somente os arquivos do manifesto. Os gates validam o diff staged; alterações paralelas não staged permanecem fora da publicação. O hash da revisão cobre esse diff de produto e exclui os artefatos autorreferentes do próprio diretório do run.

Antes de criar um ID, procure candidatos:

```bash
python3 ferramentas/kb_workflow.py --directory . check-source \
  --title "Título da fonte" \
  --url "https://exemplo" \
  --author "Organização"
```

Encontrar candidato retorna código `1` e exige reutilização do ID ou decisão explícita; não cria registro automaticamente.

## 5. Lock

```bash
python3 ferramentas/kb_workflow.py --directory . lock --run-id RUN-...
python3 ferramentas/kb_workflow.py --directory . unlock --run-id RUN-...
```

O lock possui proprietário. Uma execução não pode remover o lock de outra. Lock ambíguo ou órfão exige revisão; não deve ser apagado automaticamente.

## 6. Hook e CI

O hook `.claude/hooks/kb_consistency_hook.py` resolve o diretório de forma portátil e executa `ferramentas/kb_validate.py` em modo auditoria. Retorno diferente de zero é traduzido para `exit 2`, bloqueando o encerramento no Claude Code.

O workflow `.github/workflows/kb-validation.yml` executa testes, checker e gates de auditoria. Hook e CI são defesa adicional; não substituem o modo de publicação com `RUN_ID`.

## 7. Testes

```bash
python3 -m unittest discover -s tests -v
python3 ferramentas/check_kb_consistency.py .
python3 ferramentas/kb_validate.py .
echo '{}' | python3 .claude/hooks/kb_consistency_hook.py
```

## 8. Limitações

- O gate causal verifica presença de evidência e classificação, não lê intenção histórica.
- Similaridade de conteúdo produz candidato a duplicata; decisão ambígua requer revisão.
- Links externos e atualidade exigem processo separado e acesso à rede.
- Revisão pelo mesmo agente autor não satisfaz independência em mudanças que a exijam.
- Sincronização local↔Drive permanece bloqueada até existir política humana explícita.
