# Inventário completo do repositório

## 1. Finalidade e escopo da auditoria

Este documento cataloga a árvore de arquivos que compõe a Base de Conhecimento na data da auditoria. O inventário cobre arquivos rastreados pelo Git e arquivos novos não ignorados, incluindo este próprio catálogo. Diretórios e arquivos excluídos pelas regras de ignore não participam da contagem: ambientes virtuais, bytecode e caches Python, caches de teste e locks transitórios. Metadados internos de `.git/` também não são conteúdo do repositório e ficam fora.

**Data da auditoria:** 2026-07-06

**Branch auditada:** `codex/reorganiza-estrutura-kb`

**Total catalogado:** 49 arquivos, contando `governanca/Inventario.md`

**Método de completude:** enumeração por `git ls-files --cached --others --exclude-standard`, leitura da estrutura e do conteúdo de cada arquivo e comparação final entre a lista de caminhos e as entradas deste documento.

## 2. Visão arquitetural

O repositório está organizado em seis camadas principais:

1. **Conteúdo canônico:** ledger mestre e bases de conhecimento em `conteudo/`.
2. **Governança:** protocolo, arquitetura, template e contratos em `governanca/`.
3. **Execução e validação:** scripts em `ferramentas/`, hook local e workflow de CI.
4. **Estado operacional:** manifests, estados, revisões e resultados em `.kb/`.
5. **Planejamento:** planos de evolução em `planos/`.
6. **Verificação:** testes e fixtures em `tests/`.

O fluxo central é: uma fonte é triada conforme o protocolo, registrada no ledger, roteada para uma ou mais KBs, validada pelos checkers e publicada dentro de um `RUN_ID` com escopo, estado, revisão e evidências auditáveis.

## 3. Catálogo de arquivos

### 3.1 Raiz e configuração geral

#### `README.md`

- **Nome:** README.md
- **Descrição:** porta de entrada do repositório, com finalidade, ordem de leitura, estrutura de diretórios e comandos principais.
- **Função e objetivo:** orientar pessoas e agentes para o protocolo, a arquitetura, o template e os validadores corretos.
- **Papel:** documentação de navegação. Conecta as camadas do sistema e explicita que os validadores cobrem consistência interna, não verdade factual ou julgamento semântico integral.

#### `.gitignore`

- **Nome:** .gitignore
- **Descrição:** regras de exclusão para `__pycache__/`, bytecode Python, `.venv/` e `.kb/locks/`.
- **Função e objetivo:** impedir versionamento de dependências locais, artefatos derivados e locks transitórios.
- **Papel:** higiene do versionamento e proteção do pipeline contra estado local acidental.

### 3.2 Integrações de automação

#### `.claude/settings.json`

- **Nome:** settings.json
- **Descrição:** configuração local do Claude Code que registra um hook no evento `Stop`.
- **Função e objetivo:** executar o checker de encerramento com timeout de 30 segundos ao fim de uma sessão.
- **Papel:** integração local do pipeline; aciona `.claude/hooks/kb_consistency_hook.py`. O comando contém caminho absoluto e, portanto, é específico deste checkout.

#### `.claude/hooks/kb_consistency_hook.py`

- **Nome:** kb_consistency_hook.py
- **Descrição:** adaptador Python para a execução automática dos gates auditáveis.
- **Função e objetivo:** localizar a raiz e `ferramentas/kb_validate.py`, executar o validador, capturar saída e transformar falha em código 2 para o host do hook.
- **Papel:** ponte entre Claude Code e o pipeline de validação. Não implementa regras próprias; delega ao orquestrador canônico.

#### `.github/workflows/kb-validation.yml`

- **Nome:** kb-validation.yml
- **Descrição:** workflow do GitHub Actions disparado em pushes e pull requests.
- **Função e objetivo:** preparar Python 3.12, executar testes unitários/de integração, o checker estrutural e os gates de auditoria.
- **Papel:** controle remoto de qualidade e regressão. Reexecuta validações fora do ambiente local e fornece sinal de CI para integração de mudanças.

### 3.3 Estado operacional do Fluxo V2

#### `.kb/README.md`

- **Nome:** README.md
- **Descrição:** guia breve dos artefatos operacionais sob `.kb/`.
- **Função e objetivo:** explicar manifests, drafts, validações, revisões e locks, além de separar rascunho de conhecimento publicado.
- **Papel:** documentação da camada transacional do pipeline e aviso de que um `RUN_ID` não amplia o escopo autorizado.

#### `.kb/LEGACY_CAUSALITY_REVIEW.md`

- **Nome:** LEGACY_CAUSALITY_REVIEW.md
- **Descrição:** inventário de quatro alegações causais anteriores ao Fluxo V2 que ainda exigem revisão contextual.
- **Função e objetivo:** impedir que relações históricas não comprovadas sejam tratadas como causalidade estabelecida; registra arquivo, localização, alegação, estado, responsável e ação necessária.
- **Papel:** backlog de governança semântica e entrada do gate `CAUSALIDADE`. Não confirma nem refuta as alegações.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-HOMOLOG/draft.md`

- **Nome:** draft.md
- **Descrição:** rascunho do run de homologação do Fluxo V2, marcado como `PUBLICADO`.
- **Função e objetivo:** registrar, em linguagem humana, o objetivo e o estado resumido da execução.
- **Papel:** artefato não canônico de trabalho vinculado ao run; complementa os registros JSON.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-HOMOLOG/manifest.json`

- **Nome:** manifest.json
- **Descrição:** manifesto de risco alto da homologação, com objetivo, solicitante, arquivos e operações autorizados, commit inicial e aprovações exigidas.
- **Função e objetivo:** congelar o escopo mutável e o baseline do run para detectar mudanças não autorizadas.
- **Papel:** entrada dos gates de preflight e escopo. A lista contém caminhos da estrutura anterior à reorganização e funciona também como evidência histórica daquele run.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-HOMOLOG/review.json`

- **Nome:** review.json
- **Descrição:** aprovação humana do diff de homologação, com identidade do revisor, decisão, data, hashes e ressalvas.
- **Função e objetivo:** vincular a autorização humana a uma versão específica da mudança.
- **Papel:** evidência para o gate `REVISAO`; documenta também a equivalência entre hashes obtidos com representações diferentes de caminhos Unicode.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-HOMOLOG/state.json`

- **Nome:** state.json
- **Descrição:** estado final `PUBLICADO` e histórico completo das transições do run de homologação.
- **Função e objetivo:** registrar cronologicamente a passagem por rascunho, extração, avaliação, roteamento, aprovação, preparação e validações.
- **Papel:** trilha de auditoria da máquina de estados operada por `kb_workflow.py`.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-HOMOLOG/validation.json`

- **Nome:** validation.json
- **Descrição:** relatório de validação em modo `publish`, com resultado aprovado e onze gates aprovados.
- **Função e objetivo:** preservar a evidência estruturada da execução dos gates e declarar limites não cobertos pela automação.
- **Papel:** evidência de publicação e auditabilidade do pipeline.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-STATUS/draft.md`

- **Nome:** draft.md
- **Descrição:** rascunho do run que atualizou o estado factual do plano após a homologação, marcado como `PUBLICADO`.
- **Função e objetivo:** resumir o propósito e o estado humano-legível dessa atualização de baixo risco.
- **Papel:** artefato de trabalho não canônico ligado ao run de status.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-STATUS/manifest.json`

- **Nome:** manifest.json
- **Descrição:** manifesto de baixo risco que restringiu a atualização ao documento do Fluxo V2 e aos artefatos do próprio run.
- **Função e objetivo:** delimitar arquivos, operações permitidas e commit inicial.
- **Papel:** controle de escopo e proveniência; preserva caminhos históricos anteriores à reorganização.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-STATUS/state.json`

- **Nome:** state.json
- **Descrição:** histórico das transições do run de status até `PUBLICADO`.
- **Função e objetivo:** provar a sequência de estados e as razões de cada avanço.
- **Papel:** trilha de auditoria transacional.

#### `.kb/runs/RUN-2026-07-04-FLUXOV2-STATUS/validation.json`

- **Nome:** validation.json
- **Descrição:** relatório aprovado em modo de publicação para o run de atualização de status.
- **Função e objetivo:** registrar o resultado de todos os gates aplicáveis e as limitações da automação.
- **Papel:** evidência estruturada de que a atualização passou pelo pipeline.

#### `.kb/runs/RUN-2026-07-04-MIGRACAO-CAUSALIDADE-LEGADA/draft.md`

- **Nome:** draft.md
- **Descrição:** rascunho do run destinado a migrar as quatro alegações de causalidade legada; estado atual `RASCUNHO`.
- **Função e objetivo:** declarar o trabalho planejado antes de qualquer publicação.
- **Papel:** ponto de partida humano-legível de uma operação de risco alto ainda não concluída.

#### `.kb/runs/RUN-2026-07-04-MIGRACAO-CAUSALIDADE-LEGADA/manifest.json`

- **Nome:** manifest.json
- **Descrição:** manifesto de risco alto para revisar causalidade em três artefatos canônicos, com aprovação humana obrigatória.
- **Função e objetivo:** restringir a operação a criação/edição dos caminhos listados e preservar alterações preexistentes em `planos/FLUXOV2.md` por snapshot.
- **Papel:** contrato de escopo do próximo trabalho de causalidade; ainda não possui revisão nem validação final.

#### `.kb/runs/RUN-2026-07-04-MIGRACAO-CAUSALIDADE-LEGADA/state.json`

- **Nome:** state.json
- **Descrição:** estado inicial e único evento histórico do run de migração, ambos `RASCUNHO`.
- **Função e objetivo:** persistir o início da máquina de estados.
- **Papel:** evidência de que o run foi criado, mas não avançou no pipeline.

### 3.4 Conteúdo canônico e ledger

#### `conteudo/FONTES_REGISTRADAS.md`

- **Nome:** FONTES_REGISTRADAS.md
- **Descrição:** ledger mestre das fontes processadas, com IDs, metadados, pontuação, confiança, status, destinos, síntese, limitações e decisões.
- **Função e objetivo:** ser a fonte canônica de verdade sobre quais referências externas foram avaliadas e como foram tratadas.
- **Papel:** núcleo do pipeline de conteúdo. É lido pelo checker, comparado bidirecionalmente com as KBs e usado pelos gates de schema, duplicidade, roteamento, score/status, pendências e causalidade. Contém atualmente doze registros.

#### `conteudo/dominios/KB-01_Engenharia_de_Contexto.md`

- **Nome:** KB-01_Engenharia_de_Contexto.md
- **Descrição:** KB permanente sobre estruturação e manutenção de contexto para agentes e sistemas de IA.
- **Função e objetivo:** condensar conhecimento reutilizável por fonte em conteúdo, aplicação e limitações.
- **Papel:** destino de roteamento `KB-01`; participa da consistência ledger↔KB e exige escrita idempotente por `ID_FONTE`.

#### `conteudo/dominios/KB-02_Engenharia_de_Prompt.md`

- **Nome:** KB-02_Engenharia_de_Prompt.md
- **Descrição:** KB permanente sobre criação, avaliação e refinamento de prompts.
- **Função e objetivo:** reunir técnicas e cautelas reutilizáveis, incluindo evolução incremental de prompts e Chain-of-Thought.
- **Papel:** destino `KB-02`, validado contra o ledger e mantido por blocos idempotentes.

#### `conteudo/dominios/KB-03_Documentacao_Tecnica.md`

- **Nome:** KB-03_Documentacao_Tecnica.md
- **Descrição:** KB permanente para documentação técnica, normas, runbooks, templates, rastreabilidade e critérios de aceite.
- **Função e objetivo:** transformar fontes de documentação em práticas acionáveis e registrar suas limitações.
- **Papel:** destino `KB-03`; alimenta governança documental e participa das verificações de referências e consistência.

#### `conteudo/dominios/KB-04_Comunicacao_Audiovisual.md`

- **Nome:** KB-04_Comunicacao_Audiovisual.md
- **Descrição:** estrutura de KB permanente para roteiro, narrativa, edição, áudio e composição visual.
- **Função e objetivo:** reservar um destino canônico para conhecimento audiovisual reutilizável.
- **Papel:** destino `KB-04`; atualmente é um placeholder válido, sem registros publicados.

#### `conteudo/dominios/KB-05_Psicologia_do_Esporte.md`

- **Nome:** KB-05_Psicologia_do_Esporte.md
- **Descrição:** estrutura de KB permanente para motivação, liderança, atletas e comportamento esportivo.
- **Função e objetivo:** sustentar conhecimento reutilizável para mensagens e projetos esportivos.
- **Papel:** destino `KB-05`; atualmente é um placeholder válido, sem registros.

#### `conteudo/dominios/KB-06_Gestao_do_Conhecimento.md`

- **Nome:** KB-06_Gestao_do_Conhecimento.md
- **Descrição:** KB permanente sobre curadoria, taxonomia, RAG, ontologia, memória e reuso de conhecimento.
- **Função e objetivo:** consolidar práticas para organizar conhecimento destinado a agentes e sistemas de IA.
- **Papel:** destino `KB-06`, diretamente relacionado à arquitetura desta base e validado contra o ledger.

#### `conteudo/projetos/KB-PROJ-01_Gemini_Web.md`

- **Nome:** KB-PROJ-01_Gemini_Web.md
- **Descrição:** KB específica para regras, limitações e procedimentos do Gemini Web aplicados à geração/edição de vídeo.
- **Função e objetivo:** evitar que conhecimento particular da ferramenta seja promovido indevidamente a regra geral.
- **Papel:** destino de projeto `KB-PROJ-01`; placeholder válido ainda sem registros.

#### `conteudo/projetos/KB-PROJ-02_Projeto_IDEC.md`

- **Nome:** KB-PROJ-02_Projeto_IDEC.md
- **Descrição:** KB específica para contexto institucional, atletas, público e identidade esportiva do IDEC.
- **Função e objetivo:** isolar conhecimento que só vale para o projeto IDEC.
- **Papel:** destino `KB-PROJ-02`; placeholder sem registros.

#### `conteudo/projetos/KB-PROJ-03_Video_Motivacional_2026.md`

- **Nome:** KB-PROJ-03_Video_Motivacional_2026.md
- **Descrição:** KB específica do vídeo motivacional de 2026.
- **Função e objetivo:** concentrar conteúdo aplicado exclusivamente a esse entregável.
- **Papel:** destino `KB-PROJ-03`; placeholder sem registros.

#### `conteudo/projetos/KB-PROJ-04_Decisoes_do_Projeto.md`

- **Nome:** KB-PROJ-04_Decisoes_do_Projeto.md
- **Descrição:** registro destinado a escolhas humanas, restrições e preferências do projeto.
- **Função e objetivo:** separar decisão interna de evidência científica ou fonte oficial.
- **Papel:** destino `KB-PROJ-04`; usa formato próprio de “Decisão do Projeto” e ainda não possui registros.

#### `conteudo/projetos/KB-PROJ-05_Arquitetura_da_Base_de_Conhecimento.md`

- **Nome:** KB-PROJ-05_Arquitetura_da_Base_de_Conhecimento.md
- **Descrição:** KB específica sobre decisões e lições aplicadas à construção desta própria base.
- **Função e objetivo:** separar conhecimento genérico de contexto/documentação/curadoria das mudanças concretas no protocolo, arquitetura, template, ledger e scripts.
- **Papel:** destino `KB-PROJ-05`, importante para rastreabilidade causal. Algumas alegações históricas nele contidas estão inventariadas para revisão em `.kb/LEGACY_CAUSALITY_REVIEW.md`.

### 3.5 Ferramentas executáveis

#### `ferramentas/kb_paths.py`

- **Nome:** kb_paths.py
- **Descrição:** módulo de constantes para caminhos canônicos e descoberta das KBs publicadas.
- **Função e objetivo:** centralizar nomes de diretórios, ledger e arquivos obrigatórios de governança, evitando caminhos divergentes entre ferramentas.
- **Papel:** dependência compartilhada do pipeline; fornece `kb_paths(root)` para enumerar KBs de domínio e projeto.

#### `ferramentas/check_kb_consistency.py`

- **Nome:** check_kb_consistency.py
- **Descrição:** checker estrutural do ledger e das KBs, com modelos de issue, entrada, arquivo e relatório.
- **Função e objetivo:** ler UTF-8, analisar seções e campos, validar IDs/status/destinos, detectar duplicatas e colisões e conferir consistência bidirecional ledger↔KB.
- **Papel:** motor determinístico de integridade. É chamado diretamente, pelos gates, pela CI e coberto por `tests/test_check_kb_consistency.py`.

#### `ferramentas/kb_validate.py`

- **Nome:** kb_validate.py
- **Descrição:** orquestrador dos gates de auditoria e publicação.
- **Função e objetivo:** agregar preflight, verificações estruturais, coerência entre score e status, referências, pendências, escopo Git/manifesto, causalidade e revisão; renderizar relatório e opcionalmente persistir `validation.json`.
- **Papel:** ponto central de decisão automatizada do Fluxo V2. É executado pelo hook local, CI, CLI e workflow operacional.

#### `ferramentas/kb_workflow.py`

- **Nome:** kb_workflow.py
- **Descrição:** CLI de gestão do ciclo de vida dos runs.
- **Função e objetivo:** criar manifests e drafts, registrar snapshots preexistentes, operar máquina de estados, adquirir/liberar lock, executar validação e consultar candidatos a duplicidade.
- **Papel:** camada transacional do pipeline. Implementa proveniência, contenção de escopo, concorrência local e comandos operacionais.

### 3.6 Governança

#### `governanca/Inventario.md`

- **Nome:** Inventario.md
- **Descrição:** catálogo completo e auditável da árvore atual do repositório.
- **Função e objetivo:** oferecer um mapa único dos arquivos, de seus propósitos e das relações entre conteúdo, governança, pipeline, evidências e testes.
- **Papel:** documentação operacional e de arquitetura. Não é entrada canônica de fonte nem gate executável; serve para descoberta, auditoria de completude, manutenção e onboarding.

#### `governanca/PROTOCOLO.md`

- **Nome:** PROTOCOLO.md
- **Descrição:** procedimento operacional normativo para processar fontes do preflight à publicação e auditoria.
- **Função e objetivo:** prevenir erros conhecidos, definir estados, triagem, quarentena, duplicidade, extração, pontuação, conflitos, roteamento, aprovação por risco, escrita e gates.
- **Papel:** regra de execução humana e agentiva. É o primeiro documento recomendado pelo README e coordena ledger, template, matriz de roteamento e pipeline.

#### `governanca/REGISTRO_FONTES.md`

- **Nome:** REGISTRO_FONTES.md
- **Descrição:** especificação da arquitetura de fontes e KBs e matriz de roteamento.
- **Função e objetivo:** definir KBs permanentes/específicas, prioridade de fontes, decisões humanas, idempotência, conflitos, obsolescência, conteúdo não confiável e critérios de pronto.
- **Papel:** arquitetura normativa do sistema e fonte das regras de destino usadas no processo de publicação.

#### `governanca/TEMPLATE.md`

- **Nome:** TEMPLATE.md
- **Descrição:** formulário padronizado para registrar e avaliar uma fonte.
- **Função e objetivo:** capturar controle do fluxo, identificação, extração, pontuação, status, decisão, régua de classificação, critérios mínimos e exemplo preenchido.
- **Papel:** contrato editorial de entrada; reduz omissões e fornece estrutura compatível com validações e ledger.

#### `governanca/LEDGER_KB_VERIFY.md`

- **Nome:** LEDGER_KB_VERIFY.md
- **Descrição:** contrato e manual de verificação do Fluxo V2.
- **Função e objetivo:** documentar checker estrutural, orquestrador, RUN_ID/manifesto, locks, hook, CI, testes e limitações.
- **Papel:** ponte entre a governança declarada e sua implementação executável; orienta reprodução e interpretação dos resultados.

#### `governanca/PROMPTS_REVISAO.md`

- **Nome:** PROMPTS_REVISAO.md
- **Descrição:** esqueleto que apenas anuncia prompts-padrão para revisor técnico, juiz semântico, auditor remoto e aprovador humano.
- **Função e objetivo:** pretende centralizar instruções de revisão por papel.
- **Papel:** artefato de governança ainda incompleto. No estado atual não contém prompts utilizáveis, critérios, entradas ou formatos de saída; portanto não deve ser tratado como mecanismo de revisão implementado.

### 3.7 Planos de evolução

#### `planos/FLUXOV2.md`

- **Nome:** FLUXOV2.md
- **Descrição:** plano abrangente de implementação e governança do Fluxo V2, incluindo estado verificável, diagnóstico, máquina de estados, fases, gates, causalidade, revisão, concorrência, CI e recuperação.
- **Função e objetivo:** descrever a arquitetura-alvo, entregáveis, testes e critérios de aceite por fase, além de registrar evidências já concluídas e a próxima ação recomendada.
- **Papel:** roadmap principal e memória de implementação. Não substitui o estado executável dos scripts ou os relatórios de run.

#### `planos/GATES_PLANOS.md`

- **Nome:** GATES_PLANOS.md
- **Descrição:** plano detalhado para uma suíte de 29 gates, com contratos de resultado, retry, logs, evidências, fases, testes, riscos e encerramento.
- **Função e objetivo:** decompor a evolução dos gates em tarefas rastreáveis, critérios vermelhos/verdes e casos de homologação.
- **Papel:** backlog técnico e especificação futura; descreve capacidades além das atualmente implementadas em `kb_validate.py`.

#### `planos/SCRIPTV2.md`

- **Nome:** SCRIPTV2.md
- **Descrição:** plano de ações para a versão 2 do checker estrutural.
- **Função e objetivo:** especificar contrato, arquitetura interna, quinze ações, matriz de testes, migração do hook e definição de pronto.
- **Papel:** registro de desenho e implementação de `check_kb_consistency.py`; ajuda a explicar decisões e expectativas de regressão.

### 3.8 Testes e fixtures

#### `tests/test_check_kb_consistency.py`

- **Nome:** test_check_kb_consistency.py
- **Descrição:** suíte `unittest` do checker estrutural.
- **Função e objetivo:** construir bases temporárias e testar caso consistente, seções/campos ausentes, status inválido, roteamento, códigos duplicados, normalização de URL, duplicidade e divergência ledger↔KB.
- **Papel:** proteção de regressão do núcleo determinístico; é executada localmente e na CI.

#### `tests/test_kb_workflow.py`

- **Nome:** test_kb_workflow.py
- **Descrição:** suíte `unittest` do workflow e de integrações selecionadas.
- **Função e objetivo:** testar criação e duplicidade de run, lock atômico, máquina de estados, busca prévia de duplicatas, preflight e exclusão de artefatos do run no diff de revisão.
- **Papel:** validação da camada transacional e de escopo do pipeline.

#### `tests/fixtures/valid/agent_roles_valid.yaml`

- **Nome:** agent_roles_valid.yaml
- **Descrição:** fixture declarativa de papéis permitidos e ações proibidas para Codex, Claude Code, ChatGPT com conector GitHub e Gemini Pro Web.
- **Função e objetivo:** representar uma separação válida entre execução técnica, revisão, auditoria remota e julgamento semântico.
- **Papel:** dado de teste planejado para governança de agentes. Atualmente nenhuma suíte existente carrega este YAML, logo ele ainda não participa efetivamente da validação automatizada.

#### `tests/fixtures/invalid/agent_roles_invalid_external_claims_local_tests.yaml`

- **Nome:** agent_roles_invalid_external_claims_local_tests.yaml
- **Descrição:** arquivo vazio reservado para um cenário inválido no qual um agente externo alegaria ter executado testes locais.
- **Função e objetivo:** deveria fornecer entrada negativa para validar limites de acesso e veracidade operacional.
- **Papel:** fixture planejada, porém não implementada nem consumida pelos testes atuais; no estado vazio não testa comportamento algum.

#### `tests/fixtures/invalid/agent_roles_invalid_self_review.yaml`

- **Nome:** agent_roles_invalid_self_review.yaml
- **Descrição:** arquivo vazio reservado para um cenário inválido de autorrevisão.
- **Função e objetivo:** deveria verificar a proibição de um executor aprovar o próprio diff quando independência é exigida.
- **Papel:** fixture planejada, ainda sem conteúdo e sem integração com a suíte; não oferece cobertura real no estado atual.

## 4. Relações críticas e fluxos operacionais

- `governanca/PROTOCOLO.md`, `governanca/REGISTRO_FONTES.md` e `governanca/TEMPLATE.md` definem como uma fonte deve entrar.
- `conteudo/FONTES_REGISTRADAS.md` registra a decisão canônica; `conteudo/dominios/` e `conteudo/projetos/` materializam os destinos de conhecimento.
- `ferramentas/kb_paths.py` define os caminhos; `check_kb_consistency.py` confere ledger e KBs; `kb_validate.py` agrega gates; `kb_workflow.py` controla o run.
- `.kb/runs/` preserva escopo, estado, revisão e validação de cada operação.
- `.claude/` aciona auditoria local e `.github/workflows/kb-validation.yml` repete verificações no remoto.
- `tests/` protege o comportamento implementado; `planos/` descreve evolução e capacidades ainda pretendidas.

### 4.1 Fluxo de registro de fonte

1. Ler `governanca/PROTOCOLO.md` para obter estados, controles e sequência normativa.
2. Abrir um run e preparar o rascunho com `governanca/TEMPLATE.md`.
3. Consultar a arquitetura e a matriz de roteamento em `governanca/REGISTRO_FONTES.md`.
4. Registrar a avaliação canônica em `conteudo/FONTES_REGISTRADAS.md`.
5. Publicar o conhecimento nas KBs aplicáveis em `conteudo/dominios/` ou `conteudo/projetos/`.
6. Verificar consistência com `ferramentas/check_kb_consistency.py` e executar os gates de `ferramentas/kb_validate.py`.
7. Preservar escopo, estado, revisão e resultado sob `.kb/runs/<RUN_ID>/`.

### 4.2 Fluxo de validação automatizada

1. `tests/` verifica o comportamento implementado nos scripts.
2. `ferramentas/check_kb_consistency.py` valida estrutura e invariantes ledger↔KB.
3. `ferramentas/kb_validate.py` orquestra os demais gates auditáveis.
4. `.claude/hooks/kb_consistency_hook.py` aciona a auditoria no encerramento de uma sessão local configurada.
5. `.github/workflows/kb-validation.yml` repete testes e validações em pushes e pull requests.

### 4.3 Fluxo de governança operacional

1. `.kb/README.md` define o significado dos artefatos transitórios.
2. `ferramentas/kb_workflow.py` cria e controla `RUN_ID`, manifesto, rascunho, estados e lock.
3. `governanca/LEDGER_KB_VERIFY.md` declara o que a automação comprova e seus limites.
4. Revisão humana ou semântica complementa os gates quando o risco e o manifesto exigem.

## 5. Achados da auditoria

1. **Cobertura do inventário:** todos os 49 caminhos catalogáveis, incluindo este inventário, possuem uma entrada individual neste documento.
2. **Fixtures incompletas:** os dois YAMLs em `tests/fixtures/invalid/` estão vazios e não são usados pelos testes atuais.
3. **Fixture válida desconectada:** `agent_roles_valid.yaml` tem conteúdo, mas também não é carregado pela suíte atual.
4. **Prompts não implementados:** `governanca/PROMPTS_REVISAO.md` é somente um esqueleto.
5. **Run pendente:** a migração de causalidade legada permanece em `RASCUNHO`, sem `review.json` ou `validation.json`.
6. **Evidência histórica:** manifests antigos contêm alguns caminhos anteriores à reorganização atual; isso é coerente como registro histórico, mas esses caminhos não descrevem a árvore presente.
7. **Portabilidade local:** `.claude/settings.json` usa um caminho absoluto para o hook e requer ajuste em outro checkout.
8. **Separação entre plano e implementação:** `GATES_PLANOS.md` especifica uma arquitetura mais ampla que a suíte de gates hoje existente; o plano não deve ser confundido com funcionalidade entregue.

### 5.1 Consultas negativas preservadas da auditoria comparativa

A auditoria remota comparativa consultou os paths abaixo na branch auditada e recebeu 404. Eles não são arquivos existentes e, por isso, não contam como itens do catálogo. A lista é preservada como evidência histórica da comparação, não como requisito de criação:

- `.github/workflows/kb-validate.yml`
- `.github/workflows/ci.yml`
- `.kb/state.json`
- `.kb/locks/.gitkeep`
- `.kb/runs/.gitkeep`
- `AGENTS.md`
- `PLANOS.md`
- `pyproject.toml`
- `requirements.txt`
- `ferramentas/__init__.py`
- `ferramentas/kb_compile.py`
- `schemas/domain_knowledge.schema.json`
- `tests/__init__.py`
- `tests/test_kb_paths.py`
- `tests/test_kb_validate.py`
- `tests/test_kb_validation.py`
- `tests/test_validate.py`
- `planos/README.md`
- `planos/.gitkeep`
- `planos/PLANO.md`
- `planos/TASK-PLAN-001.md`
- `planos/fluxo-v2.md`
- `planos/plano-fluxo-v2.md`
- `planos/plano-arquitetura-fontes-kbs.md`
- `planos/implementacao-arquitetura-fontes-kbs.md`
- `planos/plano-implementacao-arquitetura-fontes-kbs.md`
- `planos/plano-implementacao-sistema-multiagentes-kb.md`
- `planos/plano-sistema-multiagentes-kb-drive.md`

## 6. Regra de manutenção

Toda criação, remoção ou renomeação de arquivo catalogável deve atualizar este inventário no mesmo conjunto lógico de mudanças. A verificação de completude deve comparar os caminhos enumerados por:

```bash
git ls-files --cached --others --exclude-standard | sort
```

com os caminhos documentados neste arquivo. Arquivos ignorados devem continuar ausentes do catálogo enquanto forem apenas estado local, derivado ou transitório.
