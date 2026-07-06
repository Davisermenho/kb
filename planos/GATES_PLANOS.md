# Plano de Implementação dos Gates da Base de Conhecimento

## 1. Controle do plano

| Campo | Valor |
| --- | --- |
| Estado | Planejado |
| Versão | 1.0 |
| Responsável | A definir |
| Revisor técnico | A definir |
| Data de início | A definir |
| Data-alvo | A definir |
| Caso-piloto | Agent Validation Gates |
| Diretório de evidências | `.kb/runs/<RUN_ID>/` |

## 1.1 Estados permitidos

- [ ] Não iniciado.
- `[-]` Em andamento.
- [x] Concluído com evidência.
- `[!]` Bloqueado.
- `[~]` Não aplicável, com justificativa.

Nenhuma tarefa pode ser marcada como concluída sem critérios de aceitação satisfeitos e evidências verificáveis registradas.

## 2. Objetivo e escopo

Implementar uma camada operacional de gates executáveis para que registros, extrações, roteamentos e publicações da Base de Conhecimento somente avancem após validações externas, auditáveis e reexecutáveis.

O plano cobre:

- contrato comum dos gates;
- manifesto e delimitação de escopo;
- gates estruturais, de qualidade, de domínio e de publicação;
- orquestração, logging, evidências, retry, bloqueio e escalação;
- testes unitários, de contrato, integração, regressão e ponta a ponta;
- execução inicial em modo auditoria;
- integração posterior com Git e CI;
- homologação, ativação gradual e rollback.

Não faz parte do escopo substituir revisão humana, factual ou semântica. Scripts determinísticos validam estrutura e invariantes; revisão semântica independente avalia significado, qualidade e causalidade.

## 3. Decisões técnicas preservadas

- O agente executor não aprova sozinho o próprio trabalho.
- Cada etapa crítica passa por um validador externo.
- Gates são módulos independentes e reexecutáveis.
- O orquestrador central é ferramentas/kb_validate.py.
- Gates determinísticos não incorporam julgamento semântico de LLM.
- Revisão semântica ocorre somente após aprovação estrutural.
- O manifesto delimita todo artefato mutável do run.
- Alterações fora do manifesto são bloqueadas.
- Cada execução possui RUN_ID e evidências persistidas.
- O pipeline começa em modo auditoria e só depois passa a bloquear publicação.
- Falhas críticas usam fail-fast; o relatório final registra gates não executados.
- O diff final é revalidado antes da publicação.
- Publicação exige lock, revisão proporcional ao risco e relatório final.
- Nenhum agente pode declarar sucesso sem PASSED externo.

## 4. Contratos normativos

### 4.1 Decisões e códigos de saída

| Exit code | Status | Decisão | Efeito |
| --- | --- | --- | --- |
| 0 | PASSED | ALLOW | Avançar |
| 1 | FAILED | RETRY | Corrigir e reexecutar |
| 2 | FAILED | ESCALATE | Corrigir configuração ou obter decisão externa |
| 3 | FAILED | BLOCK | Interromper imediatamente |

Combinações diferentes das quatro acima são inválidas e devem falhar em teste de contrato.

### 4.2 Retry

- Máximo de três tentativas por gate e RUN_ID.
- Cada tentativa incrementa attempt e preserva os logs anteriores.
- Após a terceira falha corrigível, a decisão muda de RETRY para ESCALATE.
- Falhas BLOCK nunca entram em retry automático.
- Falhas operacionais só podem ser reexecutadas após correção da configuração.

### 4.3 Log obrigatório por gate

```json
{

  "run_id": "RUN_ID",

  "task_id": "F2-G01",

  "test_ids": ["F2-G01-R01", "F2-G01-G01"],

  "gate": "PREFLIGHT",

  "attempt": 1,

  "validator_version": "SEMVER",

  "policy_version": "SEMVER",

  "artifact": "caminho",

  "command": "comando executado",

  "status": "PASSED|FAILED",

  "decision": "ALLOW|RETRY|BLOCK|ESCALATE",

  "exit_code": 0,

  "summary": "resultado objetivo",

  "details": {},

  "stdout_path": "caminho",

  "stderr_path": "caminho",

  "diff_reference": "referência imutável",

  "timestamp": "ISO-8601",

  "duration_ms": 0

}
```

### 4.4 Evidência obrigatória por tarefa

```yaml
task_id:

requirement_ids: []

status:

responsible:

reviewer:

started_at:

finished_at:

dependencies_verified: []

artifacts_created: []

artifacts_changed: []

test_ids: []

red_test:

  command:

  expected_result:

  actual_result:

  exit_code:

  stdout_path:

  stderr_path:

green_test:

  command:

  expected_result:

  actual_result:

  exit_code:

  stdout_path:

  stderr_path:

regression_command:

regression_result:

log_reference:

diff_reference:

commit_reference:

review_decision:

notes:
```

### 4.5 Ciclo obrigatório de implementação

Toda tarefa de código segue esta ordem:

1. Confirmar dependências e baseline.
1. Criar fixture válida e inválida.
1. Escrever teste vermelho e comprovar falha pela razão esperada.
1. Implementar o comportamento mínimo.
1. Executar teste verde e comprovar sucesso.
1. Executar testes negativos e de borda.
1. Executar regressão das tarefas anteriores.
1. Executar integração pelo orquestrador, quando aplicável.
1. Registrar evidências.
1. Obter revisão exigida pelo risco.

## 5. Arquitetura de arquivos esperada

```text
ferramentas/

  kb_validate.py

  check_kb_consistency.py

  gates/

    __init__.py

    base.py

    logger.py

    evidence.py

    manifest.py

    preflight.py

    schema.py

    duplicidade.py

    roteamento.py

    ledger_kb.py

    escopo_diff.py

    pendencias.py

    score_status.py

    claims_traceability.py

    limitacoes.py

    criterios_minimos.py

    referencias_internas.py

    fonte_como_dado.py

    domain_entry_schema.py

    domain_routing.py

    technique_acceptance.py

    best_practices_acceptance.py

    activation_signals.py

    triage_questions.py

    examples_balance.py

    related_domains.py

    decision_record.py

    publication_lock.py

    final_diff.py

    revisao.py

    causalidade.py

    semantic_review_required.py

    final_report.py

tests/

  contract/

  unit/

  integration/

  e2e/

  fixtures/valid/

  fixtures/invalid/

.kb/runs/<RUN_ID>/

  manifest.json

  draft.md

  evidence/

  logs/gates.jsonl

  logs/stdout/

  logs/stderr/

  final-report.json
```

## 6. Plano de ações por fase

### Fase 0 — Baseline, requisitos e contratos

| ID | Tarefa | Dependências | Critérios de aceitação individuais | Teste vermelho | Teste verde | Evidência mínima |
| --- | --- | --- | --- | --- | --- | --- |
| F0-T01 | Inventariar arquivos, schemas e comandos existentes | Nenhuma | Inventário contém caminho, finalidade, proprietário e estado; lacunas estão listadas | Consulta por artefato obrigatório ausente falha | Inventário validado sem item obrigatório desconhecido | Inventário, comando e saída |
| F0-T02 | Definir IDs de requisito, tarefa, gate e teste | F0-T01 | IDs são únicos, estáveis e validados por padrão | Fixture com ID duplicado falha | Catálogo sem duplicidade passa | Catálogo e relatório |
| F0-T03 | Formalizar contrato de resultado | F0-T02 | Apenas quatro combinações status/decisão/exit code são aceitas | Combinação inválida falha | Quatro combinações válidas passam | Schema e testes |
| F0-T04 | Formalizar schemas de manifesto, log e evidência | F0-T03 | Campos, tipos, enums e versões estão definidos | Documento sem campo obrigatório falha | Fixtures válidas passam | Schemas versionados |
| F0-T05 | Criar fixtures-base | F0-T04 | Há fixture válida e inválida para cada tipo de artefato | Fixture inválida é rejeitada | Fixture válida é aceita | Diretórios de fixtures |
| F0-T06 | Configurar executor de testes e cobertura | F0-T05 | Um comando executa toda a suíte e gera relatório | Teste propositalmente falho torna comando não zero | Suíte mínima retorna zero | Comando e relatório |

#### Critério de saída da fase:

- Contratos versionados e aprovados.
- Fixtures e executor funcionam em ambiente limpo.
- Evidências de F0-T01 a F0-T06 estão preenchidas.

### Fase 1 — Infraestrutura comum

| ID | Tarefa | Dependências | Critérios de aceitação individuais | Teste vermelho | Teste verde | Evidência mínima |
| --- | --- | --- | --- | --- | --- | --- |
| F1-T01 | Implementar base.py | Fase 0 | Tipos, enums e validação do contrato correspondem ao schema | Resultado incompatível é rejeitado | Resultado válido é serializado | Testes de contrato |
| F1-T02 | Implementar logger.py | F1-T01 | JSONL válido, append-only e um evento por gate/tentativa | Evento incompleto não é gravado | Evento completo é relido sem perda | JSONL e stdout |
| F1-T03 | Implementar evidence.py | F1-T02 | Evidência liga tarefa, requisito, teste, diff e revisão | Evidência órfã falha | Evidência completa passa | Arquivo de evidência |
| F1-T04 | Implementar carregador do manifesto | F1-T01 | Valida schema, RUN_ID, caminhos e operações permitidas | Manifesto inválido falha | Manifesto válido é carregado | Manifesto e testes |
| F1-T05 | Implementar orquestrador mínimo | F1-T01–F1-T04 | Executa gates declarados, propaga códigos e registra não executados | Gate ausente retorna 2 | Dois gates fictícios passam em ordem | Relatório de integração |
| F1-T06 | Implementar retry limitado | F1-T05 | Máximo três tentativas, histórico preservado e escalação final | Quarta tentativa automática é impedida | Falha transitória passa antes do limite | Logs das tentativas |

#### Critério de saída da fase:

- Contratos, logging, evidências, manifesto, orquestração e retry passam juntos.
- Nenhuma falha é ocultada pelo orquestrador.

### Fase 2 — Gates mínimos de segurança estrutural

| ID | Gate | Critérios de aceitação individuais | Teste vermelho obrigatório | Teste verde obrigatório | Evidência específica |
| --- | --- | --- | --- | --- | --- |
| F2-G01 | PREFLIGHT | Detecta cada arquivo/diretório obrigatório ausente; não altera o repositório | Remover uma fixture obrigatória produz falha e lista o caminho | Estrutura completa retorna ALLOW/0 | Lista verificada e log |
| F2-G02 | MANIFEST | Exige RUN_ID, schema válido, diff e todos os arquivos mutáveis declarados | Alteração fora do manifesto retorna BLOCK/3 | Diff integralmente declarado retorna ALLOW/0 | Manifesto e diff |
| F2-G03 | SCHEMA | Detecta campo ausente, vazio, tipo inválido e enum inválida | Uma fixture para cada classe de erro retorna RETRY/1 | Registro completo retorna ALLOW/0 | Relatório por campo |
| F2-G04 | DUPLICIDADE | Verifica ID, título, link, organização, tema e conteúdo relevante | Duplicata confirmada retorna BLOCK/3 | Registro inédito retorna ALLOW/0 | Candidatos e regra usada |
| F2-G05 | ROTEAMENTO | Destino existe e corresponde à matriz; multidestino é completo ou justificado | Destino inexistente retorna falha | Destinos válidos retornam ALLOW/0 | Matriz e destinos |
| F2-G06 | LEDGER_KB | Ledger e blocos físicos são bidirecionalmente consistentes | Item existente em apenas um lado falha | Ledger e KB sincronizados passam | IDs comparados |
| F2-G07 | ESCOPO_DIFF | Todo diff está autorizado; remoções e arquivos protegidos exigem permissão explícita | Modificação protegida sem autorização retorna BLOCK/3 | Diff autorizado retorna ALLOW/0 | Diff imutável |
| F2-G08 | PENDENCIAS | Conflitos, incertezas, revisões e status Revisar têm pendência motivada | Conflito sem pendência retorna RETRY/1 | Pendências completas retornam ALLOW/0 | IDs de pendência |

Dependência: cada gate depende da Fase 1; dentro da fase, MANIFEST precede gates que leem escopo.

#### Critério de saída da fase:

- Oito gates implementados com testes unitários positivos, negativos e de borda.
- Pipeline estrutural completo passa em integração.
- Alteração fora do manifesto e duplicata confirmada bloqueiam o fluxo.

### Fase 3 — Gates de qualidade do registro

| ID | Gate | Critérios de aceitação individuais | Teste vermelho obrigatório | Teste verde obrigatório | Evidência específica |
| --- | --- | --- | --- | --- | --- |
| F3-G01 | SCORE_STATUS | Soma, confiança, status e decisão obedecem à régua versionada | Pontuação incompatível com status falha | Combinação coerente passa | Cálculo e versão da régua |
| F3-G02 | CLAIMS_TRACEABILITY | Cada claim crítico aponta para fonte e localização reproduzível | Claim crítico órfão falha | Todos os claims resolvidos passam | Mapa claim→origem |
| F3-G03 | LIMITACOES | Limitações obrigatórias estão presentes e não vazias | Registro sem limitações falha | Limitações explícitas passam | Trechos/localizações |
| F3-G04 | CRITERIOS_MINIMOS | Todos os mínimos aplicáveis têm resultado e justificativa | Critério obrigatório ausente falha | Matriz completa passa | Matriz de critérios |
| F3-G05 | REFERENCIAS_INTERNAS | Caminhos, âncoras e IDs internos resolvem para artefatos existentes | Referência quebrada falha | Referências resolvíveis passam | Lista de resolução |
| F3-G06 | FONTE_COMO_DADO | Conteúdo externo é tratado como dado e não como instrução operacional | Fixture com prompt externo acionável é bloqueada | Citação inerte e identificada passa | Trecho sinalizado |

#### Critério de saída da fase:

- Seis gates passam sobre fixtures válidas e rejeitam todas as classes inválidas.
- Regras subjetivas foram encaminhadas à revisão semântica, não codificadas como heurística opaca.

### Fase 4 — Gates específicos de domínio

| ID | Gate | Critérios de aceitação individuais | Teste vermelho obrigatório | Teste verde obrigatório | Evidência específica |
| --- | --- | --- | --- | --- | --- |
| F4-G01 | DOMAIN_ENTRY_SCHEMA | Todas as seções obrigatórias existem, são únicas e não vazias | Remover cada seção em teste parametrizado falha | Entrada completa passa | Seções detectadas |
| F4-G02 | DOMAIN_ROUTING | Domínio, subdomínio e KBs obedecem à taxonomia | Rota incompatível falha | Rota prevista passa | Taxonomia e rota |
| F4-G03 | TECHNIQUE_ACCEPTANCE | Cada técnica possui condição verificável de aceite | Técnica sem critério falha | Todas as técnicas rastreadas passam | Mapa técnica→critério |
| F4-G04 | BEST_PRACTICES_ACCEPTANCE | Cada prática possui critério verificável | Prática sem critério falha | Práticas completas passam | Mapa prática→critério |
| F4-G05 | ACTIVATION_SIGNALS | Há sinais objetivos e não contraditórios | Lista vazia ou contraditória falha | Sinais válidos passam | Lista de sinais |
| F4-G06 | TRIAGE_QUESTIONS | Perguntas cobrem entrada, exclusão e escalação | Ausência de uma categoria falha | Três categorias cobertas passam | Matriz de cobertura |
| F4-G07 | EXAMPLES_BALANCE | Há exemplo correto e incorreto, ambos rotulados | Apenas um tipo de exemplo falha | Par completo passa | IDs dos exemplos |
| F4-G08 | RELATED_DOMAINS | Relações apontam para domínios existentes e têm motivo | Domínio inexistente falha | Relações resolvíveis passam | Grafo de relações |
| F4-G09 | DECISION_RECORD | Escolha do domínio registra alternativas, motivo, autor e data | Decisão sem alternativa ou motivo falha | Registro completo passa | Registro de decisão |

#### Critério de saída da fase:

- Nove gates executados no caso-piloto.
- Entrada completa passa e cada mutilação prevista falha isoladamente.

### Fase 5 — Gates de publicação

| ID | Gate | Critérios de aceitação individuais | Teste vermelho obrigatório | Teste verde obrigatório | Evidência específica |
| --- | --- | --- | --- | --- | --- |
| F5-G01 | PUBLICATION_LOCK | Lock é exclusivo, tem proprietário, timeout e liberação segura | Dois publicadores concorrentes: o segundo falha | Um publicador adquire e libera o lock | Eventos do lock |
| F5-G02 | FINAL_DIFF | Diff final coincide com manifesto e hash revalidado | Alteração após validação retorna BLOCK/3 | Diff estável retorna ALLOW/0 | Hash e diff final |
| F5-G03 | REVISAO | Risco médio exige revisão independente; alto/crítico exige aprovação humana | Aprovação ausente falha | Aprovação compatível passa | Identidade e decisão |
| F5-G04 | CAUSALIDADE | Alegação causal tem CLAIM_ID, CHANGE_ID, decisão, diff e revisão | Elo causal incompleto falha | Cadeia completa passa | Cadeia causal |
| F5-G05 | SEMANTIC_REVIEW_REQUIRED | Escopo semântico, prompt/versão, entrada e decisão ficam registrados | Revisão exigida ausente retorna ESCALATE/2 | Revisão válida permite avanço | Relatório semântico |
| F5-G06 | FINAL_REPORT | Lista todos os gates como aprovados, reprovados ou não executados; resume evidências | Gate obrigatório omitido impede sucesso | Relatório completo e consistente passa | final-report.json |

#### Critério de saída da fase:

- Publicação concorrente, diff alterado e revisão ausente são bloqueados.
- Relatório final nunca converte gate ausente em sucesso.

### Fase 6 — Integração, auditoria e CI

| ID | Tarefa | Dependências | Critérios de aceitação individuais | Teste vermelho | Teste verde | Evidência mínima |
| --- | --- | --- | --- | --- | --- | --- |
| F6-T01 | Integrar os 29 gates ao orquestrador | Fases 2–5 | Ordem, obrigatoriedade e seleção por manifesto são determinísticas | Gate obrigatório removido falha | Pipeline completo passa | Ordem executada |
| F6-T02 | Implementar modo auditoria | F6-T01 | Executa e registra sem publicar ou alterar ledger/KB final | Fixture detecta tentativa de mutação | Run produz apenas evidências | Diff antes/depois |
| F6-T03 | Implementar relatório agregado | F6-T01 | Consolida tentativas, decisões e não executados | Logs inconsistentes impedem relatório aprovado | Logs válidos geram relatório | Relatório JSON |
| F6-T04 | Integrar hook Git versionável | F6-T01 | Hook invoca comando oficial e propaga falha | Pipeline falho impede commit de teste | Pipeline válido permite fluxo | Saída do hook |
| F6-T05 | Integrar CI | F6-T01 | CI usa ambiente limpo, guarda artefatos e bloqueia merge | Teste falho torna job vermelho | Suíte válida torna job verde | URL/ID do job |
| F6-T06 | Testar desempenho e timeout | F6-T01 | Limites por gate e total são definidos; timeout não vira sucesso | Gate suspenso termina com falha operacional | Pipeline normal fica no orçamento | Métricas de duração |

#### Critério de saída da fase:

- Modo auditoria permanece não mutável.
- Hook e CI bloqueiam falhas e preservam evidências.
- Orçamento de execução e timeouts foram homologados.

### Fase 7 — Homologação, ativação e rollback

| ID | Tarefa | Dependências | Critérios de aceitação individuais | Teste vermelho | Teste verde | Evidência mínima |
| --- | --- | --- | --- | --- | --- | --- |
| F7-T01 | Executar caso-piloto válido | Fase 6 | Agent Validation Gates chega a estado publicável sem inconsistência | Baseline incompleto falha | Caso completo passa ponta a ponta | Run completo |
| F7-T02 | Executar caso-piloto inválido | F7-T01 | Cada falha crítica é detectada no gate correto | Mutação inválida não pode passar | Correção posterior passa | Runs antes/depois |
| F7-T03 | Executar regressão em ambiente limpo | F7-T02 | Suíte integral é reproduzível sem estado local | Estado residual é detectado | Ambiente limpo passa | Relatório de regressão |
| F7-T04 | Homologar revisão humana | F7-T03 | Revisor aprova comportamento, riscos residuais e evidências | Aprovação incompleta impede ativação | Aprovação assinada libera próxima etapa | Registro de aprovação |
| F7-T05 | Ativar bloqueio gradualmente | F7-T04 | Ativação por fase é configurável e observável | Gate em auditoria não bloqueia indevidamente | Gate ativado bloqueia cenário previsto | Configuração e logs |
| F7-T06 | Testar rollback | F7-T05 | Reverte configuração de bloqueio sem perder evidências ou corromper estado | Rollback incompleto falha validação | Retorno ao modo auditoria passa | Run de rollback |

## 7. Matriz de testes obrigatórios

| Categoria | Escopo mínimo | Condição de aprovação |
| --- | --- | --- |
| Contrato | Resultados, manifesto, log e evidência | Todos os schemas e enums cobertos |
| Unitário | Cada regra de cada gate | Ao menos um positivo, um negativo e bordas por regra |
| Vermelho | Cada tarefa de implementação | Falha antes da implementação pela razão esperada |
| Verde | Cada tarefa de implementação | Passa após implementação sem relaxar o teste |
| Integração | Gate + logger + manifesto + orquestrador | Código, decisão e evidência consistentes |
| Regressão | Todas as fases concluídas | Nenhuma tarefa anteriormente verde volta a falhar |
| Segurança | Escopo, fonte como dado, arquivos protegidos e lock | Nenhuma violação avança |
| Concorrência | Lock e publicação | Um único publicador por escopo |
| Resiliência | Timeout, erro operacional e retry | Nenhuma falha vira sucesso; tentativas são limitadas |
| Ponta a ponta | Caso válido e casos inválidos | Sucesso e bloqueios ocorrem nos pontos previstos |
| Não mutação | Modo auditoria | Hashes de ledger e KB final permanecem iguais |
| Rollback | Configuração de bloqueio | Retorno seguro ao modo auditoria |

## 8. Caso-piloto: Agent Validation Gates

### 8.1 Roteamento esperado

- KB-03 — Documentação Técnica.
- KB-06 — Gestão do Conhecimento.
- KB-PROJ-05 — Arquitetura da Base de Conhecimento, quando houver aplicação direta ao projeto.

### 8.2 Sequência mínima

1. Criar RUN_ID e manifesto.
1. Registrar hashes do estado inicial.
1. Executar PREFLIGHT, MANIFEST e SCHEMA.
1. Executar os gates estruturais restantes.
1. Executar gates de qualidade.
1. Executar os nove gates de domínio.
1. Executar revisão semântica quando requerida.
1. Executar gates de publicação sobre o diff final.
1. Gerar relatório final.
1. Comparar hashes e registrar evidências.

### 8.3 Cenários obrigatórios

- Entrada completa: todos os gates aplicáveis passam.
- Seção obrigatória ausente: DOMAIN_ENTRY_SCHEMA falha.
- Critério de técnica ausente: TECHNIQUE_ACCEPTANCE falha.
- Rota inválida: DOMAIN_ROUTING falha.
- Referência interna quebrada: REFERENCIAS_INTERNAS falha.
- Alteração fora do manifesto: ESCOPO_DIFF bloqueia.
- Revisão obrigatória ausente: REVISAO ou SEMANTIC_REVIEW_REQUIRED escala.
- Diff modificado após validação: FINAL_DIFF bloqueia.
- Segundo publicador concorrente: PUBLICATION_LOCK bloqueia.

## 9. Critérios globais de aceitação

- Todas as tarefas possuem ID único, responsável, estado e dependências.
- Os 29 gates possuem implementação e especificação rastreáveis.
- Cada tarefa possui teste vermelho, verde, negativo e regressão aplicável.
- Cada regra de falha está coberta por teste automatizado.
- As quatro combinações formais de resultado são respeitadas.
- Retry está limitado a três tentativas e escala corretamente.
- RUN_ID, manifesto e diff são obrigatórios para operações mutáveis.
- Nenhum arquivo fora do manifesto é modificado.
- Modo auditoria não altera ledger nem KB final.
- Logs são válidos, append-only e reproduzíveis.
- Evidências ligam requisito, tarefa, teste, artefato, diff e revisão.
- Lock impede publicação concorrente.
- Diff final é revalidado imediatamente antes da publicação.
- Riscos médio, alto e crítico recebem revisão adequada.
- Relatório final lista gates aprovados, reprovados e não executados.
- Gate obrigatório ausente impede sucesso.
- Hook Git e CI propagam códigos de falha.
- Caso-piloto válido passa ponta a ponta.
- Todos os cenários inválidos são interrompidos no gate esperado.
- Suíte completa passa em ambiente limpo.
- Rollback foi executado e comprovado.
- Revisão humana final foi registrada.
- O agente não consegue declarar conclusão sem PASSED externo.

## 10. Checklist operacional de implementação

### Preparação

- Preencher controle do plano.
- Criar catálogo de requisitos e IDs.
- Criar schemas e fixtures.
- Definir comando oficial de teste.

### Desenvolvimento

- Concluir Fase 0.
- Concluir Fase 1.
- Concluir oito gates da Fase 2.
- Concluir seis gates da Fase 3.
- Concluir nove gates da Fase 4.
- Concluir seis gates da Fase 5.
- Concluir integração da Fase 6.

### Homologação

- Executar caso-piloto válido.
- Executar todos os casos inválidos.
- Executar regressão em ambiente limpo.
- Revisar evidências de todas as tarefas.
- Obter aprovação humana.

### Ativação

- Manter modo auditoria durante período definido pelo responsável.
- Confirmar ausência de falso bloqueio crítico não tratado.
- Ativar bloqueio por fase.
- Monitorar duração, falhas e escalonamentos.
- Testar rollback após ativação.

## 11. Registro de evidências da execução

Copiar este bloco para cada tarefa concluída:

```yaml
task_id: ""

requirement_ids: []

status: "NOT_STARTED|IN_PROGRESS|PASSED|FAILED|BLOCKED|NOT_APPLICABLE"

responsible: ""

reviewer: ""

started_at: ""

finished_at: ""

dependencies_verified: []

artifacts_created: []

artifacts_changed: []

test_ids: []

red_test:

  command: ""

  expected_result: ""

  actual_result: ""

  exit_code: null

  stdout_path: ""

  stderr_path: ""

green_test:

  command: ""

  expected_result: ""

  actual_result: ""

  exit_code: null

  stdout_path: ""

  stderr_path: ""

negative_tests: []

edge_tests: []

regression_command: ""

regression_result: ""

log_reference: ""

diff_reference: ""

commit_reference: ""

review_decision: ""

notes: ""
```

## 12. Riscos e respostas

| Risco | Resposta obrigatória |
| --- | --- |
| Loop infinito de retry | Limite de três tentativas e escalação |
| Gate excessivamente complexo | Separar invariantes determinísticas de revisão semântica |
| Falso sucesso | Contrato fechado, relatório de não executados e CI bloqueante |
| Falso bloqueio | Modo auditoria, fixtures e ativação gradual |
| Corrida de publicação | Lock exclusivo com timeout e proprietário |
| Evidência perdida | Persistência append-only por RUN_ID |
| Mudança após validação | Hash e FINAL_DIFF imediatamente antes da publicação |
| Hook local contornado | Repetir validação obrigatória na CI |
| Regra sem teste | Matriz requisito→tarefa→teste→evidência obrigatória |
| Revisão sem independência | Registrar identidade e impedir autorrevisão quando exigida |

## 13. Regra de encerramento

O plano somente pode ser encerrado quando todos os critérios globais estiverem marcados, todas as tarefas aplicáveis possuírem evidências verificáveis, o caso-piloto válido e os cenários inválidos tiverem sido executados, a regressão em ambiente limpo estiver verde e a revisão humana final tiver sido registrada.

Qualquer item não aplicável deve conter justificativa e aprovação. Item vazio, teste não executado, gate obrigatório ausente ou evidência não resolvível impede a declaração de conclusão.
