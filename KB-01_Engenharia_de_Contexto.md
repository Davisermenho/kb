# KB-01 — Engenharia de Contexto

## Escopo
Conhecimento Permanente. Estruturação de contexto para IA — serve para orientar qualquer agente em qualquer projeto com uso de contexto (não depende deste projeto específico).

## Regras de uso deste arquivo
Este arquivo só deve ser editado seguindo o Passo 6 de `PROTOCOLO.md` (escrita idempotente): um bloco novo por `ID_FONTE`, nunca sobrescrevendo o arquivo inteiro. Ao editar um `ID_FONTE` já existente, atualize o bloco correspondente em vez de duplicá-lo.

Formato de bloco (um por fonte registrada):

```
### <ID_FONTE> — <Título da fonte>
- Nível de confiança: <Fonte forte / média / fraca>
- Conteúdo extraído: <regra, critério, conceito ou instrução acionável>
- Aplicação: <como isso orienta o agente>
- Limitações: <se houver>
- Última atualização: <data>
```

## Registros

### FONTE-2026-MSR-CONTEXT-ENGINEERING — Context Engineering for AI Agents in Open-Source Software
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Estudo empírico (MSR '26) mostra que apenas 5% de 10.000 repositórios OSS populares adotam arquivos de contexto de IA (AGENTS.md, CLAUDE.md, Copilot instructions, GEMINI.md) — prática ainda incipiente, sem estrutura padronizada; estilos variam entre descritivo, prescritivo, proibitivo, explicativo e condicional. Categorias de conteúdo mais comuns (da mais para a menos frequente): convenções de código, diretrizes de contribuição, arquitetura/estrutura, comandos de build, objetivos, testes, metadados, stack técnica, setup, referências, troubleshooting, exemplos, segurança. 50% dos arquivos AGENTS.md nunca foram alterados após criados; quando mudam, é sobretudo para adicionar/modificar instruções.
- Aplicação: Recomendação central, aplicável a qualquer projeto de IA: arquivos de contexto devem ser tratados como artefatos de software mantidos — versionados, revisados, testados — não como documentação estática escrita uma vez. As categorias de conteúdo mais comuns (convenções, contribuição, arquitetura, build, testes etc.) servem de checklist genérico para redigir qualquer arquivo de contexto de agente.
- Limitações: Estudo exploratório/preliminar dos próprios autores; amostra de 10.000 repositórios populares (não necessariamente representativa); análise de evolução baseada em apenas 10 arquivos. Não usar isoladamente para afirmar taxas de adoção da indústria como consenso.
- Última atualização: 2026-07-02

### FONTE-2025-ARXIV-ACE — Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- Nível de confiança: Fonte média (21/21; rebaixada pela regra de conteúdo não confiável)
- Conteúdo extraído: Estruturar o contexto como playbook de itens pequenos com identificadores e sinais de utilidade/dano. Separar Generator (trajetórias), Reflector (lições) e Curator (deltas). Anexar itens novos, atualizar existentes no lugar e deduplicar, evitando reescritas monolíticas que apagam conhecimento. Os experimentos do ACE reportam ganhos de desempenho e redução de custo/latência em agentes e tarefas de domínio.
- Aplicação: Evoluir arquivos de contexto e memórias por deltas rastreáveis; preservar conhecimento anterior; registrar acertos, falhas e sinais de qualidade; revisar e remover seletivamente itens problemáticos.
- Limitações: Depende da qualidade do Reflector e não é necessariamente vantajoso em tarefas simples. O apêndice contém instruções dirigidas a agente; elas foram ignoradas, e a fonte ficou com status Revisar conforme a seção 13 do registro.
- Última atualização: 2026-07-02

### FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY — A Survey of Context Engineering for Large Language Models
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Context Engineering é tratado como disciplina formal que vai além do design isolado de prompts — o contexto é uma carga informacional estruturada, dinâmica e otimizada, montada a partir de instruções, conhecimento externo, ferramentas, memória, estado do usuário/sistema e consulta imediata. A taxonomia unificada organiza o campo em componentes fundacionais (recuperação/geração, processamento, gerenciamento de contexto) e implementações sistêmicas (RAG, memória, ferramentas, multiagentes).
- Aplicação: Usar a taxonomia formal (recuperação/geração, processamento, gerenciamento de contexto) para decompor e desenhar qualquer arquitetura de contexto para agentes — KBs, roteamento, memória — em vez de tratar o sistema de contexto como um bloco de texto único.
- Limitações: Preprint arXiv sem garantia de revisão por pares na versão consultada; é survey (síntese bibliográfica), não estudo empírico primário; conclusões dependem da seleção bibliográfica dos autores.
- Última atualização: 2026-07-02

### FONTE-2024-COMMONMARK-SPEC — CommonMark Spec, seção 1.2 "Why is a spec needed?"
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: A descrição original de Markdown (John Gruber) não especificava a sintaxe de forma inequívoca — deixava sem resposta clara perguntas como indentação de sublistas, necessidade de linha em branco antes de blockquote/heading, listas "tight" vs "loose", precedência entre estruturas inline concorrentes (code span vs link, emphasis vs strong), e qual definição de link-reference prevalece havendo múltiplas. Sem spec inequívoca, implementadores recorriam ao `Markdown.pl`, que era "quite buggy". Resultado: implementações divergiram e o mesmo documento renderizava diferente em sistemas diferentes, sem sinalizar "erro de sintaxe".
- Aplicação: Especificações informais em linguagem natural, destinadas a múltiplos executores (humanos ou agentes de IA), tendem a gerar interpretações divergentes nos pontos que a prosa deixa implícitos. Lição geral: reduzir ambiguidade com convenções explícitas e mecanismos de verificação automatizada, não confiar apenas em prosa bem-intencionada.
- Limitações: Extração restrita à seção de motivação, não cobre a gramática formal da spec; perspectiva de um único autor (John MacFarlane), ainda que amplamente aceita (CommonMark é padrão de fato da indústria).
- Última atualização: 2026-07-02

### FONTE-2004-DARINGFIREBALL-MARKDOWN-SYNTAX — Markdown: Syntax (+ Basics + License)
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Leitura completa do documento original de Gruber confirma, com exemplos concretos, as ambiguidades que a CommonMark Spec só descrevia em abstrato: a regra de "tightness" de listas (linha em branco entre itens decide se viram `<p>`) é declarada, mas casos de borda (lista parcialmente tight/loose) ficam sem resposta; indentação de continuação em listas aninhadas também é subespecificada. Mais revelador: o próprio autor admite, no texto, um bug real de implementação não coberto pela documentação ("known bug in Markdown.pl 1.0.1 which prevents single quotes from being used to delimit link titles") e uma ausência deliberada de funcionalidade (sem sintaxe para dimensão de imagem).
- Aplicação: Estudo de caso real e citável de como uma especificação em prosa natural falha em casos de borda, mesmo quando amplamente adotada. Lição geral: documentar limitações conhecidas explicitamente (como Gruber fez com o bug de aspas simples) em vez de deixá-las implícitas — transparência sobre o que não funciona é mais robusta do que silêncio.
- Limitações: Documento de 2004, superado por variantes modernas (GFM, CommonMark) para uso prático de parsing exato.
- Última atualização: 2026-07-02

### FONTE-2026-STRIPE-API-DOCS — Stripe API Reference completo (overview, versioning, errors, mapa de 91 recursos, llms.txt, 4 Agent Skills + 6 referências)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: O Stripe publica um `llms.txt` real e 4 Agent Skills completas em `.well-known/skills/`. `stripe-best-practices` tem 6 referências internas, todas seguindo o padrão "Traps to avoid" / "BLOCKED combinations (never recommend)" — proibições explícitas além de um simples `CANNOT` (ex. `connect.md`: "NEVER use `type: 'express'`/`'custom'`/`'standard'`"). `stripe-directory` é a mais notável: permite ao agente descobrir E **comprar autonomamente** serviços de terceiros via Machine Payment Protocol (HTTP 402), mas com portão de aprovação obrigatório: "Always show the price and get explicit user approval before any money moves."
- Aplicação: O padrão "Traps to avoid"/"BLOCKED combinations" é técnica complementar a uma seção `CANNOT`: em vez de só listar limites de escopo, lista ativamente erros comuns e combinações proibidas, com base em incidentes reais — aplicável a qualquer sistema de instruções para agentes que já tenha acumulado erros conhecidos. O portão de aprovação humana explícita antes de qualquer ação irreversível (ex. gasto de dinheiro) é prática geral recomendada para ações agênticas de alto risco.
- Limitações: Cobertura agora completa das 4 Skills + 6 referências + mapa de 91 categorias da API Reference. Não lido: o conteúdo detalhado de cada um dos ~91 recursos individuais (escala muito maior, fora do escopo razoável).
- Última atualização: 2026-07-03

### FONTE-2026-TWILIO-API-DOCS — Twilio Docs: General Usage + Building with AI (Twilio Skills, MCP server)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Twilio Skills (Public Beta) são pacotes de conhecimento procedural em 4 categorias (Setup, Planner/consultivas, Product, Guardrail), seguindo o "Agent Skills standard" aberto (`agentskills.io`) com adoção multi-fornecedor confirmada (Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, JetBrains Junie, 30+ plataformas). Arquitetura de "progressive disclosure": metadata leve no início da sessão → skill completo só quando a tarefa bate → referência detalhada sob demanda. Cada skill deve ter seção `CANNOT` explícita documentando o que não faz, "reducing hallucination" — técnica nova, ausente das fontes já registradas. MCP server complementar (`mcp.twilio.com/docs`, sem auth, 1.800+ endpoints, busca-então-recupera) responde "quais parâmetros"; Skills respondem "qual produto/abordagem".
- Aplicação: A seção `CANNOT` obrigatória por skill é uma técnica geral para reduzir alucinação em qualquer sistema de agentes. O modelo Skills-vs-MCP (conhecimento procedural curado vs. especificação viva sempre atual) é um padrão mental replicável para qualquer arquitetura que combine regras curadas com dados vivos. Confirma, junto com Stripe, que `llms.txt` + Agent Skills é prática emergente da indústria, não caso isolado.
- Limitações: Skills e MCP rotulados "Public Beta" pela própria Twilio, sujeitos a mudança. Inconsistência interna encontrada: `/docs/ai/mcp` trata Skills como "futuro" enquanto `/docs/ai/skills` já as documenta funcionando — doc desatualizada, mesmo padrão já visto em `FONTE-2026-GITLAB-RUNBOOKS`. `agentskills.io` não verificado independentemente.
- Última atualização: 2026-07-03
