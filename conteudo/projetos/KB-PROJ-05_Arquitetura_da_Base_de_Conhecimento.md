# KB-PROJ-05 — Arquitetura da Base de Conhecimento

## Escopo
Conhecimento Específico. Lições, decisões e ajustes concretos feitos na arquitetura deste sistema de fontes (`governanca/PROTOCOLO.md`, `governanca/REGISTRO_FONTES.md`, `governanca/TEMPLATE.md`, `conteudo/FONTES_REGISTRADAS.md`, os scripts de verificação) motivados por fontes externas processadas. Não é sobre Gemini Web, Projeto IDEC ou o vídeo motivacional — é sobre a construção e manutenção deste próprio sistema de curadoria de conhecimento.

## Por que este arquivo existe
KB-01, KB-03 e KB-06 se declaram genéricas — reutilizáveis "em qualquer projeto", não amarradas a este. Na prática, boa parte do campo `Aplicação` das fontes já registradas tinha se tornado comentário sobre este projeto específico (ex. referências a `governanca/PROTOCOLO.md`, ao incidente `FONTE-001`), contradizendo o escopo declarado dessas KBs. Este arquivo separa essa camada: a lição genérica fica em KB-01/03/06; a aplicação concreta e específica — o que de fato mudamos ou decidimos aqui por causa da fonte — fica aqui.

## Regras de uso deste arquivo
Este arquivo só deve ser editado seguindo o Passo 6 de `governanca/PROTOCOLO.md` (escrita idempotente): um bloco novo por `ID_FONTE`, nunca sobrescrevendo o arquivo inteiro. Ao editar um `ID_FONTE` já existente, atualize o bloco correspondente em vez de duplicá-lo. Uma fonte pode ter um bloco aqui e, ao mesmo tempo, blocos em KB-01/03/06 — mesmo `ID_FONTE`, ângulos diferentes (genérico vs. específico), nunca o mesmo texto duplicado.

Formato de bloco (um por fonte registrada):

```
### <ID_FONTE> — <Título da fonte>
- Nível de confiança: <Fonte forte / média / fraca>
- Lição específica: <o que mudamos, decidimos ou reforçamos neste sistema por causa desta fonte>
- Onde isso aparece: <arquivo/seção concreta afetada — PROTOCOLO.md, REGISTRO_FONTES.md, script, etc.>
- Última atualização: <data>
```

## Registros

### FONTE-2026-MSR-CONTEXT-ENGINEERING — Context Engineering for AI Agents in Open-Source Software
- Nível de confiança: Fonte forte (21/21)
- Lição específica: **Correção (2026-07-03): claim anterior estava errado.** Nenhuma mudança concreta em `governanca/PROTOCOLO.md`/`governanca/REGISTRO_FONTES.md` é atribuível a esta fonte — não existe checklist de categorias refletida em nenhum dos dois arquivos. A recomendação de tratar arquivos de contexto como artefatos versionados e revisáveis já era a prática seguida neste projeto antes desta leitura (`governanca/REGISTRO_FONTES.md` seção 12 já existia); o estudo reforça essa prática com dado empírico externo, mas não a originou.
- Onde isso aparece: Nenhuma. Serve apenas como validação retrospectiva da seção 12 de `governanca/REGISTRO_FONTES.md`, já existente.
- Última atualização: 2026-07-03

### FONTE-2025-ARXIV-ACE — Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- Nível de confiança: Fonte média (21/21; rebaixada pela regra de conteúdo não confiável)
- Lição específica: **Correção (2026-07-03): causalidade estava invertida.** A regra de escrita idempotente por `ID_FONTE` (`governanca/REGISTRO_FONTES.md` seção 10) já existia antes de processarmos esta fonte — ela não a inspirou. A separação Generator→Reflector→Curator e a lógica de deltas rastreáveis por item reforçam, com evidência experimental externa, uma prática já adotada aqui, mas não a originaram.
- Onde isso aparece: Nenhuma edição direta. Validação retrospectiva da seção 10 de `governanca/REGISTRO_FONTES.md`, escrita anteriormente.
- Última atualização: 2026-07-03

### FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY — A Survey of Context Engineering for Large Language Models
- Nível de confiança: Fonte forte (20/21)
- Lição específica: **Correção (2026-07-03): causalidade estava invertida.** A Matriz de Roteamento (`governanca/REGISTRO_FONTES.md` seção 6) já existia, com a mesma estrutura, antes de processarmos esta fonte. A taxonomia formal do survey (recuperação/geração → processamento → gerenciamento) confirma retrospectivamente que a lógica da matriz é compatível com um modelo acadêmico reconhecido — mas não motivou nenhuma mudança nela.
- Onde isso aparece: Nenhuma edição direta. Validação conceitual retrospectiva da seção 6 de `governanca/REGISTRO_FONTES.md`.
- Última atualização: 2026-07-03

### FONTE-2024-COMMONMARK-SPEC — CommonMark Spec, seção 1.2 "Why is a spec needed?"
- Nível de confiança: Fonte forte (21/21)
- Lição específica: **Correção (2026-07-03): causalidade estava invertida.** Já tínhamos observado o problema que esta fonte descreve — Claude e ChatGPT interpretaram `governanca/PROTOCOLO.md` de forma diferente, causando a duplicidade `FONTE-001`/`FONTE-2026-MSR-CONTEXT-ENGINEERING` — e já tínhamos corrigido isso com a convenção `FONTE-<ANO>-<VEÍCULO>-<TEMA>` (`governanca/REGISTRO_FONTES.md` seção 9) **antes** de processar esta fonte. O item 1 de "Erros já cometidos e proibidos" em `governanca/PROTOCOLO.md` também foi escrito depois, motivado pela fonte Stripe, não por esta. O que esta fonte de fato oferece é um paralelo histórico que reforça por que a convenção era necessária, não a origem dela.
- Onde isso aparece: Nenhuma edição direta atribuível a esta fonte. Validação histórica retrospectiva da seção 9 de `governanca/REGISTRO_FONTES.md`.
- Última atualização: 2026-07-03

### FONTE-2004-DARINGFIREBALL-MARKDOWN-SYNTAX — Markdown: Syntax (+ Basics + License)
- Nível de confiança: Fonte forte (20/21)
- Lição específica: **Correção (2026-07-03): causalidade estava invertida.** A seção "Erros já cometidos e proibidos" de `governanca/PROTOCOLO.md` foi criada depois, motivada pela fonte Stripe — não por esta. O que esta fonte de fato oferece é um paralelo retrospectivo: a prática de Gruber de admitir um bug conhecido explicitamente (em vez de omiti-lo) confirma, com um segundo caso histórico, que nomear incidentes reais é mais robusto do que generalidades — algo que já estava sendo feito na seção quando esta fonte foi lida.
- Onde isso aparece: Nenhuma edição direta atribuível a esta fonte.
- Última atualização: 2026-07-03

### FONTE-2026-STRIPE-API-DOCS — Stripe API Reference completo (overview, versioning, errors, mapa de 91 recursos, llms.txt, 4 Agent Skills + 6 referências)
- Nível de confiança: Fonte forte (21/21)
- Lição específica: O padrão "Traps to avoid"/"BLOCKED combinations" das referências da Stripe é a base direta da seção "Erros já cometidos e proibidos" adicionada a `governanca/PROTOCOLO.md` (incluindo o caso do `ID_FONTE` sequencial `FONTE-001`). O portão de aprovação humana do `stripe-directory` antes de gastar dinheiro confirma, como padrão de indústria, a prática já seguida neste projeto de confirmar antes de qualquer ação irreversível (ex. apagar arquivo do usuário).
- Onde isso aparece: `governanca/PROTOCOLO.md`, seção "Erros já cometidos e proibidos" (itens 1–7).
- Última atualização: 2026-07-03

### FONTE-2026-TWILIO-API-DOCS — Twilio Docs: General Usage + Building with AI (Twilio Skills, MCP server)
- Nível de confiança: Fonte forte (21/21)
- Lição específica: A seção `CANNOT` obrigatória por skill da Twilio motivou a seção "O que este protocolo NÃO resolve" em `governanca/PROTOCOLO.md`. O modelo Skills-vs-MCP (procedural curado vs. especificação viva) espelha a distinção já existente aqui entre `governanca/PROTOCOLO.md` (procedural, curado) e `ferramentas/check_kb_consistency.py` (verificação sobre estado vivo dos arquivos).
- Onde isso aparece: `governanca/PROTOCOLO.md`, seção "O que este protocolo NÃO resolve".
- Última atualização: 2026-07-03

### FONTE-2026-GITLAB-RUNBOOKS — GitLab Runbooks ("Runbooks for the stressed on-call")
- Nível de confiança: Fonte forte (18/21)
- Lição específica: O padrão "pasta por serviço, arquivo por procedimento, template formal", com vínculo rastreável entre alerta e correção, é uma referência para pensar em como `governanca/PROTOCOLO.md` poderia, no futuro, vincular tipos de erro/divergência a procedimentos de correção padronizados.
- Onde isso aparece: Nenhuma mudança concreta ainda — ideia registrada para revisão futura de `governanca/PROTOCOLO.md`.
- Última atualização: 2026-07-03

### FONTE-2017-GOOGLE-SRE-POSTMORTEM-CULTURE — Site Reliability Engineering, Cap. 13 "Emergency Response" + Cap. 14 "Managing Incidents" + Cap. 15 "Postmortem Culture" + Apêndice D "Example Postmortem"
- Nível de confiança: Fonte forte (21/21)
- Lição específica: **Correção (2026-07-03): causalidade parcialmente invertida.** `conteudo/FONTES_REGISTRADAS.md` já existia, com o mesmo papel de ledger vivo, antes de processarmos esta fonte — o "Live Incident State Document" não é o modelo que originou o ledger, é uma semelhança estrutural notada em retrospecto. Da mesma forma, a cultura blameless já tinha sido praticada informalmente (registro do incidente `FONTE-001`, focando na convenção ausente, não em qual agente errou) antes desta leitura. A técnica "Ask the Big, Even Improbable Questions: What If...?" foi de fato aplicada diretamente a `governanca/PROTOCOLO.md` nesta conversa (e se dois agentes gravarem na mesma KB ao mesmo tempo? E se o checker falhar silenciosamente?) — isso é uma aplicação real, não retrospectiva. A ideia de formalizar um "postmortem leve" continua em aberto, não implementada.
- Onde isso aparece: Nenhuma edição de arquivo diretamente atribuível a esta fonte. Validação retrospectiva do formato de `conteudo/FONTES_REGISTRADAS.md` e da prática blameless já em uso; "postmortem leve" permanece como ideia não implementada.
- Última atualização: 2026-07-03

### FONTE-2026-GITLAB-HANDBOOK — The GitLab Handbook (homepage + About the Handbook + Values/CREDIT)
- Nível de confiança: Fonte forte (21/21)
- Lição específica: A prática de "content owner por página" motivou diretamente a seção 19 de `governanca/REGISTRO_FONTES.md` (Decisões Pendentes e Responsabilidade), que cita esta fonte nominalmente — confirmado, esta parte é verificável. A metodologia de contagem reproduzível do handbook é do mesmo espírito de `ferramentas/check_kb_consistency.py` (observação, não mudança de código). **Correção (2026-07-03): a alegação anterior sobre uma "nota de poda futura" na seção 12 de `governanca/REGISTRO_FONTES.md` era falsa** — reli a seção 12 inteira e ela não contém nenhuma menção a poda/pruning de KBs. A lição sobre poda ativa (o handbook encolheu ~1,17M palavras em 6 meses) segue como consideração relevante para o futuro, mas ainda não foi incorporada a nenhum arquivo.
- Onde isso aparece: `governanca/REGISTRO_FONTES.md` seção 19 (Decisões Pendentes e Responsabilidade — cita esta fonte por nome). A lição sobre poda ainda não foi incorporada a nenhum arquivo — permanece como consideração em aberto, não implementada.
- Última atualização: 2026-07-03
