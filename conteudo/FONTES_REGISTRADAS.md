# FONTES_REGISTRADAS.md — Registro Mestre de Fontes

## Papel deste arquivo
Ledger mestre de todas as fontes já avaliadas pelo `governanca/PROTOCOLO.md`. Cada fonte processada gera exatamente um bloco aqui, preenchido a partir do `governanca/TEMPLATE.md`, preservando pontuação, decisão de uso e rastreabilidade completa — independentemente de o conteúdo extraído condensado também ter sido gravado na(s) KB(s) de destino em `ARQUIVO_DESTINO_KB`.

## Regras de uso
- Um bloco por `ID_FONTE`. Nunca duplicar.
- Se a fonte for revisada, edite o bloco existente e acrescente a nova data em "Última revisão" — não crie um segundo bloco para o mesmo `ID_FONTE`.
- Nunca sobrescrever o arquivo inteiro — apenas append de bloco novo ou edição pontual do bloco existente (mesma regra de `governanca/REGISTRO_FONTES.md` seção 10).

## Registros

### FONTE-2026-MSR-CONTEXT-ENGINEERING — Context Engineering for AI Agents in Open-Source Software
- ID_FONTE: FONTE-2026-MSR-CONTEXT-ENGINEERING
- DATA_REGISTRO: 2026-07-02
- RESPONSÁVEL: Registro original por Davi Sermenho (via Claude) como FONTE-001; consolidado com o registro paralelo de ChatGPT sob este ID em 2026-07-02.
- TÍTULO: Context Engineering for AI Agents in Open-Source Software
- AUTOR_ORGANIZAÇÃO: Seyedmoein Mohsenimofidi (Heidelberg University), Matthias Galster (University of Bamberg), Christoph Treude (Singapore Management University), Sebastian Baltes (Heidelberg University)
- DATA_PUBLICAÇÃO: 2026-04-13 (MSR '26 — 23rd International Conference on Mining Software Repositories, Rio de Janeiro)
- LINK_REFERÊNCIA: https://assets.empirical-software.engineering/pdf/msr26-context-engineering.pdf (DOI: 10.1145/3793302.3793350)
- TIPO_FONTE: Artigo científico revisado por pares (proceedings ACM MSR '26)
- DOMÍNIO: Engenharia de Contexto para IA
- SUBDOMÍNIO: Estruturação e evolução de arquivos de contexto para agentes de IA (AGENTS.md, CLAUDE.md, Copilot instructions, GEMINI.md) em projetos open-source
- TEMA: Adoção, estrutura de conteúdo e evolução temporal de arquivos de contexto de IA em repositórios open-source
- CONTEXTO_USO: KB-01 porque o artigo define e mede empiricamente a estruturação de contexto para agentes; KB-06 porque trata arquivos de contexto como artefatos versionados de gestão de conhecimento, com manutenção, evolução e governança.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-06 — Gestão do Conhecimento, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma; complementa FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY (taxonomia ampla) com dado empírico de adoção real em repositórios OSS.
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: Context engineering é o processo deliberado de projetar, estruturar e fornecer informação relevante para agentes de IA. Apenas 466/10.000 (5%) dos repositórios OSS populares analisados adotam algum arquivo de contexto de IA (AGENTS.md, CLAUDE.md, Copilot instructions, GEMINI.md) — prática ainda incipiente, sem padrão consolidado; estilos variam entre descritivo, prescritivo, proibitivo, explicativo e condicional. Categorias de conteúdo mais comuns em AGENTS.md (da mais para a menos frequente): convenções de código, diretrizes de contribuição, arquitetura/estrutura, comandos de build, objetivos, execução de testes, metadados, estratégia de testes, stack técnica, setup, referências, troubleshooting, padrões/exemplos, segurança. 50% dos arquivos AGENTS.md estudados nunca foram alterados após a criação; quando alterados, é sobretudo para adicionar/modificar instruções existentes.
- EVIDÊNCIA_PRINCIPAL: "AI context files are maintained software artifacts. They are versioned, reviewed, quality-assured, and tested." (Conclusão, seção 5). Em 10.000 repositórios analisados, 466 tinham algum arquivo de contexto para IA; a análise detalhada de AGENTS.md mostrou ausência de estrutura consolidada e evolução por refinamento contínuo de instruções.
- LIMITAÇÕES: Estudo exploratório/preliminar (os próprios autores o descrevem como "primeiro passo"); cobre apenas 4 formatos de arquivo; amostra de 10.000 repositórios populares via ranking, não necessariamente representativa da população geral de projetos OSS; análise de evolução (RQ3) usou apenas 10 arquivos com 10+ commits; autores não classificaram a intenção de cada mudança nem mediram diretamente como estrutura/estilo afetam desempenho dos agentes.
- APLICAÇÃO_IA: Reforça a decisão já tomada neste projeto de tratar `governanca/PROTOCOLO.md` e as KBs como artefatos versionados e revisáveis (alinhado com `governanca/REGISTRO_FONTES.md` seção 12); fornece checklist de categorias de conteúdo com base empírica; sustenta manter regras operacionais, comandos, arquitetura, testes e exemplos como contexto persistente e auditável.
- OBSERVAÇÕES: Esta fonte havia sido registrada de forma independente e duplicada por dois agentes diferentes — como `FONTE-001` (Claude) e `FONTE-2026-MSR-CONTEXT-ENGINEERING` (ChatGPT) — ambas referenciando o mesmo artigo, sem que nenhum dos dois detectasse a duplicidade antes de gravar. Consolidada sob este único ID em 2026-07-02; `FONTE-001` foi descontinuado e todas as referências foram atualizadas para este ID.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar critérios de organização, manutenção, revisão e evolução de arquivos de contexto para agentes de IA neste projeto. Não deve ser usada isoladamente para afirmar taxas de adoção da indústria como um todo, dado o caráter exploratório do estudo.
- PRÓXIMA_REVISÃO: 2027-01-02 (6 meses) ou quando os autores publicarem o estudo estendido mencionado na Conclusão, o que ocorrer primeiro.

### FONTE-2025-ARXIV-ACE
- **ID_FONTE:** FONTE-2025-ARXIV-ACE
- **DATA_REGISTRO:** 2026-07-02
- **RESPONSÁVEL:** ChatGPT, sob solicitação de Davi Sermenho
- **TÍTULO:** Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- **AUTOR_ORGANIZAÇÃO:** Qizheng Zhang; Changran Hu; Shubhangi Upasani; Boyuan Ma; Fenglu Hong; Vamsidhar Kamanuru; Jay Rainton; Chen Wu; Mengmeng Ji; Hanchen Li; Urmish Thakker; James Zou; Kunle Olukotun. Stanford University; SambaNova Systems, Inc.; UC Berkeley.
- **DATA_PUBLICAÇÃO:** 2025-10-06 (arXiv); versão 3 de 2026-03-29; publicado como artigo no ICLR 2026
- **LINK_REFERÊNCIA:** https://arxiv.org/pdf/2510.04618 (arXiv:2510.04618v3)
- **TIPO_FONTE:** Artigo científico revisado por pares / conferência ICLR 2026
- **DOMÍNIO:** Engenharia de Contexto para IA
- **SUBDOMÍNIO:** Adaptação incremental de contexto, memória de agentes e otimização de prompts de sistema
- **TEMA:** ACE (Agentic Context Engineering): contextos como playbooks evolutivos, estruturados e incrementais
- **CONTEXTO_USO:** KB-01 porque define um método geral para estruturar e evoluir contexto de agentes; KB-02 porque aplica geração, reflexão e curadoria à otimização de prompts de sistema; KB-06 porque trata conhecimento e memória como itens identificáveis, atualizados localmente, deduplicados e refinados ao longo do tempo.
- **TIPO_CONHECIMENTO:** Permanente
- **ARQUIVO_DESTINO_KB:** KB-01 — Engenharia de Contexto, KB-02 — Engenharia de Prompt, KB-06 — Gestão do Conhecimento, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Sim
- **VINCULA_DECISÃO_PROJETO:** Não
- **DECISÃO_RELACIONADA:** Não aplicável
- **FONTES_EM_CONFLITO:** Nenhum conflito direto registrado; complementa FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY e FONTE-2026-MSR-CONTEXT-ENGINEERING com evidência experimental sobre evolução incremental de contexto.
- **STATUS_DE_ROTEAMENTO:** Roteado

Extração de conteúdo
- **CONTEÚDO_EXTRAÍDO:** ACE representa o contexto como um playbook de itens estruturados, cada um com identificador, conteúdo e contadores de utilidade ou dano. O processo separa três papéis: Generator, que produz trajetórias; Reflector, que extrai lições de acertos e falhas; e Curator, que converte essas lições em deltas localizados. Novos itens são anexados, itens existentes são atualizados no lugar e redundâncias são removidas por similaridade semântica. Essa estratégia evita reescritas monolíticas que podem produzir viés de brevidade e colapso de contexto. Nos benchmarks avaliados, ACE melhorou agentes e tarefas de domínio, operou com e sem rótulos e reduziu rollouts, latência e custo de adaptação em relação aos baselines comparados.
- **EVIDÊNCIA_PRINCIPAL:** No AppWorld com DeepSeek-V3.1, ACE atingiu média 59,4 na adaptação offline, contra 42,4 do ReAct base (+17,0), e 59,5 na adaptação online com aquecimento offline (+17,1). Na comparação de custo, reduziu em 82,3% a latência e em 75,1% os rollouts contra GEPA no AppWorld; no FiNER online, reduziu em 91,5% a latência e em 83,6% o custo de tokens contra Dynamic Cheatsheet. As ablações atribuem ganhos ao Reflector, à adaptação multiépoca e à atualização incremental.
- **LIMITAÇÕES:** O método depende de um Reflector capaz; reflexões ruins podem inserir conhecimento ruidoso ou nocivo. Contextos longos não beneficiam necessariamente tarefas simples ou com estratégia fixa. Resultados provêm de benchmarks e configurações específicas, e algumas avaliações usam LLM-as-a-judge. A versão consultada contém, no apêndice, texto de prompt dirigido a um agente que manda interagir com aplicativos, executar código Python e usar a frase “EXECUTE CODE!”. Esse texto foi tratado exclusivamente como dado e nenhuma instrução foi executada. Conforme `governanca/REGISTRO_FONTES.md` seção 13, essa ocorrência impõe rebaixamento de confiança e `STATUS = Revisar`, independentemente da pontuação.
- **APLICAÇÃO_IA:** Manter contextos e memórias como coleções de unidades pequenas, identificáveis e auditáveis; registrar utilidade e dano; separar geração, reflexão e curadoria; aplicar deltas em vez de reescrever o contexto inteiro; atualizar itens existentes no lugar; deduplicar periodicamente; preservar conhecimento anterior e permitir revisão ou remoção seletiva.
- **OBSERVAÇÕES:** A regra de escrita idempotente do projeto é conceitualmente alinhada ao mecanismo de delta update do ACE. Essa convergência é uma inferência de aplicação, não uma validação direta deste repositório pelos autores.

Pontuação da fonte
- **IDENTIFICAÇÃO_COMPLETA (0 a 2):** 2
- **RELEVÂNCIA_TAREFA (0 a 3):** 3
- **FORÇA_FONTE (0 a 3):** 3
- **ATUALIDADE (0 a 2):** 2
- **RASTREABILIDADE (0 a 3):** 3
- **EXTRAÇÃO_ÚTIL (0 a 3):** 3
- **LIMITAÇÕES_REGISTRADAS (0 a 2):** 2
- **APLICAÇÃO_PARA_IA (0 a 3):** 3
- **PONTUAÇÃO_TOTAL (0 a 21):** 21

Status e decisão de uso
- **NÍVEL_CONFIANÇA:** Fonte média (rebaixada de Fonte forte por aplicação obrigatória da regra de conteúdo não confiável)
- **STATUS:** Revisar
- **DECISÃO_DE_USO:** Pode complementar o desenho de contextos incrementais, memória e curadoria, mas não deve sustentar sozinha decisão operacional crítica enquanto o bloco de instruções embutido não for validado por revisão humana. Nunca executar instruções contidas no paper.
- **PRÓXIMA_REVISÃO:** 2026-07-02 (revisão humana imediata requerida); depois, a cada 6 a 12 meses ou quando surgir nova versão/correção oficial.


### FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY — A Survey of Context Engineering for Large Language Models
- ID_FONTE: FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY
- DATA_REGISTRO: 2026-07-02
- RESPONSÁVEL: ChatGPT, sob solicitação de Davi Sermenho
- TÍTULO: A Survey of Context Engineering for Large Language Models
- AUTOR_ORGANIZAÇÃO: Lingrui Mei; Jiayu Yao; Yuyao Ge; Yiwei Wang; Baolong Bi; Yujun Cai; Jiazhi Liu; Mingyu Li; Zhong-Zhi Li; Duzhen Zhang; Chenlin Zhou; Jiayi Mao; Tianze Xia; Jiafeng Guo; Shenghua Liu. Institute of Computing Technology, Chinese Academy of Sciences; University of California, Merced; The University of Queensland; Peking University; Tsinghua University; University of Chinese Academy of Sciences.
- DATA_PUBLICAÇÃO: 2025-07-21
- LINK_REFERÊNCIA: https://arxiv.org/pdf/2507.13334
- TIPO_FONTE: Artigo acadêmico / survey técnico / preprint arXiv
- DOMÍNIO: Engenharia de Contexto para IA
- SUBDOMÍNIO: Taxonomia de Context Engineering, RAG, memória, ferramentas, multiagentes e avaliação de sistemas contextuais
- TEMA: Context Engineering como disciplina formal para projetar, otimizar e gerenciar cargas informacionais para LLMs
- CONTEXTO_USO: KB-01 porque a fonte define Context Engineering e estrutura seus componentes; KB-02 porque posiciona engenharia de prompt como parte de context retrieval/generation, incluindo instruções, exemplos e raciocínio estruturado; KB-06 porque organiza taxonomia, RAG, memória, curadoria, recuperação, compressão, avaliação e gestão de conhecimento para agentes e sistemas de IA.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-02 — Engenharia de Prompt, KB-06 — Gestão do Conhecimento, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma registrada; complementa FONTE-2026-MSR-CONTEXT-ENGINEERING ao oferecer uma taxonomia ampla, enquanto aquela fonte trata arquivos de contexto em repositórios open-source.
- STATUS_DE_ROTEAMENTO: Roteado
Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: Context Engineering é apresentado como disciplina formal que ultrapassa o design isolado de prompts e trata o contexto como carga informacional estruturada, dinâmica e otimizada para LLMs. O contexto deixa de ser um texto monolítico e passa a ser montado por componentes como instruções, conhecimento externo, ferramentas, memória, estado do usuário/sistema e consulta imediata. A taxonomia proposta organiza o campo em componentes fundacionais — recuperação/geração de contexto, processamento de contexto e gerenciamento de contexto — e implementações sistêmicas — RAG, sistemas de memória, raciocínio integrado a ferramentas e sistemas multiagentes. A fonte também destaca lacunas: ausência de fundamentos teóricos unificados, dificuldades de alocação/compressão de contexto, desafios de avaliação e assimetria entre compreensão de contexto e geração de saídas longas sofisticadas.
- EVIDÊNCIA_PRINCIPAL: O artigo declara analisar mais de 1400 trabalhos de pesquisa e propõe uma taxonomia unificada para Context Engineering, formalizando o contexto como conjunto dinâmico de componentes orquestrados e apontando aplicações em RAG, memória, ferramentas e multiagentes.
- LIMITAÇÕES: Preprint arXiv; não há garantia de revisão por pares na versão consultada; é survey e não estudo empírico primário; a taxonomia pode mudar conforme o campo amadurece; várias conclusões dependem da seleção bibliográfica dos autores. Não foi identificada instrução disfarçada dirigida ao agente.
- APLICAÇÃO_IA: Usar a fonte para orientar agentes a tratar contexto como arquitetura operacional, não como prompt isolado. Decompor contexto em instruções, conhecimento externo, ferramentas, memória, estado e query; aplicar recuperação, seleção, formatação, compressão e avaliação; desenhar KBs e RAG com rastreabilidade, roteamento, avaliação por componente e avaliação sistêmica.
- OBSERVAÇÕES: Fonte forte para taxonomia e organização conceitual do domínio. Para decisões críticas de implementação, deve ser combinada com documentação oficial, benchmarks e estudos empíricos específicos.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 2
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 20

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar critérios de arquitetura de contexto, taxonomia de componentes, roteamento de conhecimento, desenho de RAG/memória/ferramentas e avaliação de sistemas contextuais. Para decisão operacional crítica, usar em conjunto com documentação oficial, benchmarks ou estudos empíricos específicos.
- PRÓXIMA_REVISÃO: 2027-01-02
.

### FONTE-2022-ARXIV-GRAPH-CREATURES-LADDERS
- **ID_FONTE:** FONTE-2022-ARXIV-GRAPH-CREATURES-LADDERS
- **DATA_REGISTRO:** 2026-07-02
- **RESPONSÁVEL:** ChatGPT, sob solicitação de Davi Sermenho
- **TÍTULO:** Taming Graphs with No Large Creatures and Skinny Ladders
- **AUTOR_ORGANIZAÇÃO:** Jakub Gajarský; Lars Jaffke; Paloma T. Lima; Jana Novotná; Marcin Pilipczuk; Paweł Rzążewski; Uéverton S. Souza. University of Warsaw; University of Bergen; IT University of Copenhagen; Universidade Federal Fluminense; Warsaw University of Technology.
- **DATA_PUBLICAÇÃO:** 2022-05-02 (arXiv v1); publicado online em 2024-12-16 no SIAM Journal on Discrete Mathematics
- **LINK_REFERÊNCIA:** https://arxiv.org/pdf/2205.01191v1 (endereco fornecido `https://arxiv.org/pdf/2205.1191`, canonicalizado pelo arXiv para 2205.01191v1); DOI: 10.1137/23M1550530
- **TIPO_FONTE:** Artigo científico revisado por pares / periódico SIAM Journal on Discrete Mathematics
- **DOMÍNIO:** Matemática discreta e ciência da computação teórica
- **SUBDOMÍNIO:** Teoria estrutural e algorítmica dos grafos; separadores minimais; classes hereditárias de grafos
- **TEMA:** Condições estruturais para limites polinomiais no número de separadores minimais
- **CONTEXTO_USO:** A fonte estabelece resultados formais em teoria dos grafos, mas não se enquadra em nenhuma linha da Matriz de Roteamento atual, que cobre engenharia de contexto/prompt, documentação, audiovisual, psicologia do esporte, gestão do conhecimento e quatro KBs específicas do projeto. O roteamento requer decisão humana ou criação autorizada de uma KB de matemática/algoritmos; não foi escolhido destino por semelhança superficial.
- **TIPO_CONHECIMENTO:** Permanente
- **ARQUIVO_DESTINO_KB:** Nenhum destino compatível na matriz atual
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Parcial
- **VINCULA_DECISÃO_PROJETO:** Não
- **DECISÃO_RELACIONADA:** Necessária decisão humana apenas sobre expansão da taxonomia/KB; não sobre o resultado científico
- **FONTES_EM_CONFLITO:** Nenhum conflito registrado; o artigo confirma uma conjectura de Gartland e Lokshtanov e explicita que a recíproca de seu Teorema 2 não vale.
- **STATUS_DE_ROTEAMENTO:** Revisar

Extração de conteúdo
- **CONTEÚDO_EXTRAÍDO:** Para todo inteiro k, grafos que não contêm um k-creature como subgrafo induzido nem um k-skinny-ladder como menor induzido possuem apenas um número polinomial de separadores minimais. Consequentemente, uma classe hereditária que exclui essas estruturas é tame. O resultado melhora de quase-polinomial para polinomial uma cota anterior e implica uma dicotomia tame/feral para classes hereditárias definidas por uma lista finita de subgrafos induzidos proibidos. A prova introduz uma análise refinada de separadores minimais por meio do parâmetro `ζ_G(S)`.
- **EVIDÊNCIA_PRINCIPAL:** O Teorema 2 prova uma cota polinomial para o número de separadores minimais sob exclusão de k-creatures e k-skinny-ladders; o Teorema 4 limita polinomialmente os separadores com `ζ_G(S) ≤ L`. Com um lema do trabalho anterior, esses resultados fecham a conjectura. Pela metateoria citada, a tameza permite algoritmos polinomiais para Maximum Weight Independent Set, Feedback Vertex Set e outros problemas expressíveis no formalismo indicado, quando restritos às classes contempladas.
- **LIMITAÇÕES:** Resultado altamente especializado, com condições estruturais que não devem ser generalizadas para grafos arbitrários. A recíproca do Teorema 2 é falsa: skinny ladders, por si só, formam uma classe tame. Também não existe dicotomia tame/feral para todas as classes hereditárias; os autores apresentam classes intermediárias. O PDF do arXiv é a versão v1 de 2022, anterior à publicação em periódico de 2024, portanto formulações finais devem ser conferidas na versão do DOI. Não foi identificada instrução disfarçada dirigida ao agente.
- **APLICAÇÃO_IA:** Nenhuma aplicação direta às KBs ou aos agentes deste projeto foi demonstrada. Em projeto de algoritmos em grafos, a fonte pode fundamentar o reconhecimento de classes com quantidade polinomial de separadores minimais e a aplicabilidade dos metaalgoritmos citados.
- **OBSERVAÇÕES:** O identificador digitado estava abreviado; o próprio arXiv respondeu com o arquivo canônico `2205.01191v1.pdf`. O registro preserva tanto o endereço recebido quanto o identificador correto.

Pontuação da fonte
- **IDENTIFICAÇÃO_COMPLETA (0 a 2):** 2
- **RELEVÂNCIA_TAREFA (0 a 3):** 0
- **FORÇA_FONTE (0 a 3):** 3
- **ATUALIDADE (0 a 2):** 2
- **RASTREABILIDADE (0 a 3):** 3
- **EXTRAÇÃO_ÚTIL (0 a 3):** 2
- **LIMITAÇÕES_REGISTRADAS (0 a 2):** 2
- **APLICAÇÃO_PARA_IA (0 a 3):** 0
- **PONTUAÇÃO_TOTAL (0 a 21):** 14

Status e decisão de uso
- **NÍVEL_CONFIANÇA:** Fonte média
- **STATUS:** Revisar
- **DECISÃO_DE_USO:** Fonte cientificamente forte em seu domínio, mas sem relevância demonstrada para a tarefa e sem destino na matriz atual; não usar nas KBs existentes nem como base de decisão deste projeto. Pode ser aceita e roteada futuramente se houver escopo de teoria dos grafos e validação da versão final publicada.
- **PRÓXIMA_REVISÃO:** Revisão humana imediata para decidir se a taxonomia deve incorporar matemática/algoritmos; se incorporada, revisar novamente até 2027-01-02 ou quando a versão final do periódico for consultada.

### FONTE-2022-NEURIPS-COT-PROMPTING
- **ID_FONTE:** FONTE-2022-NEURIPS-COT-PROMPTING
- **DATA_REGISTRO:** 2026-07-02
- **RESPONSÁVEL:** ChatGPT, sob solicitação de Davi Sermenho
- **TÍTULO:** Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **AUTOR_ORGANIZAÇÃO:** Jason Wei; Xuezhi Wang; Dale Schuurmans; Maarten Bosma; Brian Ichter; Fei Xia; Ed H. Chi; Quoc V. Le; Denny Zhou. Google Research, Brain Team.
- **DATA_PUBLICAÇÃO:** 2022-01-28 (arXiv); versão 6 de 2023-01-10; publicado no NeurIPS 2022
- **LINK_REFERÊNCIA:** https://arxiv.org/pdf/2201.11903v6 (arXiv:2201.11903v6)
- **TIPO_FONTE:** Artigo científico revisado por pares / conferência NeurIPS 2022
- **DOMÍNIO:** Engenharia de Prompt
- **SUBDOMÍNIO:** Few-shot prompting, raciocínio intermediário e Chain-of-Thought
- **TEMA:** Uso de exemplos com etapas intermediárias para elicitar raciocínio em modelos de linguagem
- **CONTEXTO_USO:** KB-02 porque o artigo define, testa e delimita uma técnica geral de construção de prompts few-shot para tarefas que exigem raciocínio em múltiplas etapas.
- **TIPO_CONHECIMENTO:** Permanente
- **ARQUIVO_DESTINO_KB:** KB-02 — Engenharia de Prompt
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Sim
- **VINCULA_DECISÃO_PROJETO:** Não
- **DECISÃO_RELACIONADA:** Não aplicável
- **FONTES_EM_CONFLITO:** Nenhum conflito direto registrado. A conclusão de que os ganhos emergem apenas em modelos muito grandes deve ser tratada como resultado das famílias e escalas avaliadas em 2022, não como regra universal para modelos atuais.
- **STATUS_DE_ROTEAMENTO:** Roteado

Extração de conteúdo
- **CONTEÚDO_EXTRAÍDO:** Chain-of-Thought prompting acrescenta aos exemplos few-shot uma sequência textual de passos intermediários entre a entrada e a resposta. Nos experimentos do artigo, essa estrutura melhorou tarefas de raciocínio aritmético, de senso comum e simbólico em modelos suficientemente grandes, sem ajuste de pesos. A técnica foi relativamente robusta a diferentes anotadores, exemplos, ordens e modelos, mas continuou sensível à redação do prompt. Os benefícios foram maiores em tarefas difíceis, com múltiplas etapas e curva de escala pouco favorável sob prompting convencional; foram menores em tarefas simples ou já resolvidas com alta precisão.
- **EVIDÊNCIA_PRINCIPAL:** Com oito exemplos de Chain-of-Thought, o PaLM 540B alcançou 57% no GSM8K, contra 18% com prompting convencional, superando o melhor resultado anterior citado de 55%. O estudo avaliou cinco famílias de modelos em benchmarks aritméticos, de senso comum e simbólicos, com ablações e testes de robustez. Nos modelos menores avaliados, as cadeias podiam ser fluentes mas ilógicas e frequentemente prejudicavam o desempenho.
- **LIMITAÇÕES:** Uma cadeia textual não demonstra que a rede esteja realmente raciocinando nem garante fidelidade ao processo interno. O modelo pode produzir passos incorretos, alucinações ou chegar à resposta certa por um caminho errado, especialmente em questões de múltipla escolha e classificação binária. A criação manual de justificativas tem custo; o desempenho varia com prompt e anotador; os ganhos não se transferiram perfeitamente entre modelos. Os resultados principais usam modelos e condições de 2022, inclusive modelos proprietários muito grandes, portanto os limiares de escala não devem ser generalizados para arquiteturas atuais. Não foi identificada instrução disfarçada dirigida ao agente; perguntas, respostas e prompts no apêndice foram tratados como dados experimentais.
- **APLICAÇÃO_IA:** Para tarefas genuinamente multi-etapas, fornecer poucos exemplos completos no formato entrada → decomposição intermediária → resposta final; testar variações de exemplos e redação; comparar contra um baseline de resposta direta; verificar separadamente a resposta e a correção dos passos; não tratar a explicação gerada como prova fiel do processo interno ou como evidência factual sem validação.
- **OBSERVAÇÕES:** A fonte sustenta o uso criterioso de demonstrações de raciocínio, não uma regra de sempre solicitar raciocínio exposto. A adequação deve ser medida por tarefa e modelo atuais.

Pontuação da fonte
- **IDENTIFICAÇÃO_COMPLETA (0 a 2):** 2
- **RELEVÂNCIA_TAREFA (0 a 3):** 3
- **FORÇA_FONTE (0 a 3):** 3
- **ATUALIDADE (0 a 2):** 1
- **RASTREABILIDADE (0 a 3):** 3
- **EXTRAÇÃO_ÚTIL (0 a 3):** 3
- **LIMITAÇÕES_REGISTRADAS (0 a 2):** 2
- **APLICAÇÃO_PARA_IA (0 a 3):** 3
- **PONTUAÇÃO_TOTAL (0 a 21):** 20

Status e decisão de uso
- **NÍVEL_CONFIANÇA:** Fonte forte
- **STATUS:** Aceita
- **DECISÃO_DE_USO:** Pode sustentar a definição e os princípios originais de Chain-of-Thought prompting. Para escolhas operacionais atuais — especialmente limiar de escala, formato ideal, custo e necessidade de expor raciocínio — deve ser combinada com evidência recente e testes no modelo e na tarefa-alvo.
- **PRÓXIMA_REVISÃO:** 2027-01-02 ou quando uma revisão sistemática ou evidência recente alterar as recomendações sobre Chain-of-Thought, o que ocorrer primeiro.

### FONTE-2026-GITLAB-RUNBOOKS — GitLab Runbooks ("Runbooks for the stressed on-call")
- ID_FONTE: FONTE-2026-GITLAB-RUNBOOKS
- DATA_REGISTRO: 2026-07-02
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: GitLab Runbooks — "Runbooks for the stressed on-call"
- AUTOR_ORGANIZAÇÃO: GitLab.com (GitLab Inc.)
- DATA_PUBLICAÇÃO: Repositório criado em 2016-05, em atualização contínua (~24.583 commits); consultado em 2026-07-02
- LINK_REFERÊNCIA: https://gitlab.com/gitlab-com/runbooks (site publicado: https://runbooks.gitlab.com; espelho: ops.gitlab.net)
- TIPO_FONTE: Documentação oficial da organização responsável (repositório de runbooks operacionais, licença MIT)
- DOMÍNIO: Documentação Técnica / Operações de Infraestrutura (SRE, on-call, resposta a incidentes)
- SUBDOMÍNIO: Runbooks operacionais — guias passo a passo para resolução de incidentes em produção
- TEMA: Estrutura e boas práticas de runbooks para equipes de plantão (on-call)
- CONTEXTO_USO: Servir de referência real de como uma organização madura estrutura, documenta e mantém guias operacionais de resposta a incidentes — aplicável a KB-03 como benchmark de documentação técnica de governança e procedimento, não como fato técnico específico sobre a infraestrutura da GitLab.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-03 — Documentação Técnica, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma registrada
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: Repositório MIT open-source mantido pela GitLab.com desde 2016, com mais de 24 mil commits. Estrutura real confirmada via API do GitLab (não apenas README): os runbooks individuais NÃO ficam numa pasta única — cada serviço/sistema tem sua própria pasta em `docs/<serviço>/`, e dentro dela um arquivo `.md` por procedimento/alerta específico. Há ~250 pastas de serviço em `docs/` (bancos de dados: `patroni`, `pgbouncer`, múltiplas variantes de `redis-cluster-*`, `clickhouse`; infraestrutura: `gitaly`, `kubernetes`-relacionados, `storage`, `consul`, `vault`; CI/CD: `ci-runners`, `ci-orchestration`; IA/Duo: `duo-chat`, `ai-gateway`, `duo-workflow-svc`, `agentic-duo-chat`, `mcp-server`; observabilidade: `monitoring`, `mimir`, `jaeger`, `tracing`, `thanos`; entre outras). Confirmado com `docs/patroni/` como exemplo: 60 arquivos de runbook individuais (ex.: `postgresql-vacuum.md`, `unhealthy_patroni_node_handling.md`, `pg_xid_wraparound_alert.md`), mais subpastas `alerts/`, `img/`, `scripts/`. Existem dois templates formais (`docs/template-alert-playbook.md` e `docs/template-service-overview.md`) que padronizam a criação de novos runbooks. A pasta `on-call/` é separada e contém checklists operacionais de plantão (`on-call/checklists/`), não runbooks técnicos por serviço.
- EVIDÊNCIA_PRINCIPAL: Projeto ativo e maduro (~24.583 commits desde 2016), mantido pela própria equipe de infraestrutura da GitLab para uso real em produção. Estrutura de runbooks confirmada por consulta direta à API do GitLab (`repository/tree`), não por inferência.
- LIMITAÇÕES: Não foi possível confirmar a data da última atualização real nem a completude/atualidade de cada runbook individual (só a estrutura foi verificada, não o conteúdo de cada um dos milhares de arquivos). Sem revisão por pares externa (documentação operacional interna, não norma auditada). **Achado metodológico #1**: uma primeira tentativa de extrair o conteúdo do README via WebFetch (que resume páginas usando um modelo auxiliar) produziu uma resposta que misturava pastas reais (`gitaly`, `monitoring`, `certificates`) com pastas aparentemente inventadas (`troubleshooting/`, `howto/`); descartada e refeita via `curl` direto + API do GitLab. **Achado metodológico #2 (mais preciso)**: o usuário depois baixou o `README.md` real do repositório e, ao cruzar seus links internos contra a API, confirmei que ~10 links de nível superior sem prefixo `docs/` (`howto/postgresql-switchover.md`, `troubleshooting/ci_runner_manager_errors.md`, `certificates/README.md`, `monitoring/grafana.md`, `monitoring/prometheus.md`, entre outros) retornam 404 na árvore atual — não existem mais como pastas de topo. Ou seja, `troubleshooting/` e `howto/` de fato aparecem no texto real do README (não foram inventados pelo WebFetch), mas como **links quebrados/desatualizados**, prováveis remanescentes de uma reorganização que moveu conteúdo para dentro de `docs/<serviço>/` sem atualizar todos os links do README. Links aninhados como `docs/elastic/troubleshooting/README.md` e `docs/logging/troubleshooting/README.md` continuam válidos (200) — só as versões de topo sem `docs/` quebraram. Lição combinada: (a) extração via modelo resumidor precisa de checagem cruzada; (b) mesmo a fonte primária e genuína pode conter links obsoletos — verificar path por path antes de citar como fato, não confiar no texto do documento isoladamente. **Resolução (completa — os 10 links de topo quebrados do README foram todos localizados)** via listagem recursiva da árvore (6.575 arquivos) + leitura do conteúdo real:
- `howto/postgresql-switchover.md` → `docs/patroni/patroni-management.md` (seção "Failover/Switchover")
- `troubleshooting/ci_runner_manager_errors.md` → `docs/ci-runners/troubleshooting-guide.md` (seção "CI runner manager report a high number of errors")
- `howto/silence-alerts.md` → `docs/monitoring/alerts_manual.md`
- `howto/externalvendors/cloudflare.md` → pasta `docs/cloudflare/` (conteúdo dividido em múltiplos arquivos)
- `troubleshooting/elk_mapper_parsing_exception.md` → `docs/elastic/troubleshooting/elk_mapper_parsing_exception.md` (rename direto, confirmado HTTP 200)
- `certificates/README.md` → `docs/certificates/README.md` (rename direto, confirmado HTTP 200)
- `troubleshooting/ci_graphs.md` → `docs/ci-runners/ci_graphs.md` (rename direto, confirmado HTTP 200)
- `monitoring/grafana.md` e `monitoring/prometheus.md` → fundidos em `docs/monitoring/README.md` (visão geral única cobrindo os dois; não há mais arquivo próprio para cada um — inferência por evidência textual, não confirmação de arquivo exato)
- `troubleshooting/ci_introduction.md` → fundido em `docs/ci-runners/README.md` (seção "CI Runner Overview / What are CI Runners?" — mesma base de inferência)

Confirma que nenhum conteúdo foi perdido na reorganização — só as referências do README ficaram desatualizadas. Os 3 casos de fusão têm confiança um pouco menor que os de rename direto, por serem inferência de conteúdo, não confirmação de path exato.
- APLICAÇÃO_IA: Pode servir de referência/benchmark ao desenhar convenções de documentação técnica operacional deste projeto (KB-03) — o padrão `docs/<serviço>/<procedimento>.md` com template formal (`template-alert-playbook.md`) é um exemplo real de como vincular rastreavelmente um alerta a um procedimento de correção, algo que poderia inspirar como `governanca/PROTOCOLO.md` estrutura vínculos entre falha e correção. Não deve ser usada para afirmar fatos técnicos específicos sobre a infraestrutura da GitLab sem verificação direta no repositório.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 2
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 1
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 2
- PONTUAÇÃO_TOTAL (0 a 21): 18

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: A estrutura organizacional (pasta por serviço, arquivo por procedimento, template formal) pode sustentar recomendações de convenção de documentação técnica neste projeto. O conteúdo de qualquer runbook individual específico — e qualquer link citado do README — deve ser verificado diretamente (path por path) antes de ser tratado como fato, já que o próprio README contém links de topo desatualizados.
- PRÓXIMA_REVISÃO: 2027-01-02, ou antes se algum runbook específico for citado como fato e precisar de verificação pontual.

### FONTE-2024-COMMONMARK-SPEC — CommonMark Spec, seção 1.2 "Why is a spec needed?"
- ID_FONTE: FONTE-2024-COMMONMARK-SPEC
- DATA_REGISTRO: 2026-07-02
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: CommonMark Spec — Seção 1.2 "Why is a spec needed?"
- AUTOR_ORGANIZAÇÃO: John MacFarlane / projeto CommonMark
- DATA_PUBLICAÇÃO: 2024-01-28 (versão 0.31.2, confirmada no cabeçalho da própria página)
- LINK_REFERÊNCIA: https://spec.commonmark.org/0.31.2/#why-is-a-spec-needed-
- TIPO_FONTE: Documentação oficial / especificação técnica formal (padrão de fato da indústria, adotado por GitHub, GitLab, Reddit etc.)
- DOMÍNIO: Documentação Técnica / Especificação de Linguagem de Marcação
- SUBDOMÍNIO: Motivação para especificação formal quando a descrição original de uma sintaxe é ambígua
- TEMA: Por que Markdown precisou de uma especificação formal (CommonMark) já que a descrição original de John Gruber e o script Markdown.pl não resolviam ambiguidades de forma consistente
- CONTEXTO_USO: KB-03 porque é uma especificação técnica oficial e um exemplo de como documentar justificativa de norma; KB-01 porque a lição central — ambiguidade em instruções em linguagem natural causa divergência de interpretação entre diferentes implementações/agentes — é diretamente análoga ao problema de escrever `governanca/PROTOCOLO.md` para múltiplos agentes de IA, já observado na prática neste projeto (duplicidade `FONTE-001`/`FONTE-2026-MSR-CONTEXT-ENGINEERING` por Claude vs. ChatGPT).
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-03 — Documentação Técnica, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma registrada
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: A descrição original de Gruber sobre a sintaxe do Markdown não especifica a sintaxe de forma inequívoca, deixando várias perguntas sem resposta clara: quanto de indentação é necessária para uma sublista; se uma linha em branco é necessária antes de blockquote/heading/bloco de código indentado; a regra exata para quando itens de lista viram parágrafos (listas "tight" vs "loose"); se marcadores de lista podem ser indentados ou alinhados à direita; regras de precedência entre estruturas inline concorrentes (ex.: code span vs link, emphasis vs strong emphasis); precedência entre estrutura de bloco e inline; se itens de lista podem conter headings ou ficar vazios; se definições de link-reference podem estar dentro de blockquotes/list items; e qual definição prevalece quando há múltiplas para a mesma referência. Sem spec inequívoca, implementadores recorriam ao `Markdown.pl` para resolver ambiguidades, mas esse script era "quite buggy" e não servia como substituto satisfatório de uma especificação.
- EVIDÊNCIA_PRINCIPAL: "Because there is no unambiguous spec, implementations have diverged considerably. As a result, users are often surprised to find that a document that renders one way on one system... renders differently on another" — e, por Markdown não ter "erro de sintaxe", essa divergência frequentemente não era percebida de imediato.
- LIMITAÇÕES: Extração restrita à seção 1.2 (motivação), não cobre a gramática formal da especificação em si. É a perspectiva de um único autor (John MacFarlane) sobre a história do problema — embora amplamente aceita, já que o CommonMark se tornou padrão de fato adotado pela indústria.
- APLICAÇÃO_IA: Analogia direta com este projeto: `governanca/PROTOCOLO.md` é, em essência, uma especificação informal em linguagem natural para agentes de IA processarem fontes — e já observamos na prática exatamente o problema descrito aqui (Claude e ChatGPT interpretando o mesmo protocolo de forma ligeiramente diferente, causando duplicidade de `ID_FONTE` e dessincronia ledger↔KB). Reforça a decisão já tomada de reduzir ambiguidade com convenções explícitas (formato de `ID_FONTE`, formato de bloco rígido) e verificação automatizada (`ferramentas/check_kb_consistency.py`) em vez de confiar só em prosa bem-intencionada.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar a justificativa teórica para reduzir ambiguidade nas regras operacionais deste projeto (convenções explícitas de formato, verificação automatizada em vez de só prosa) — o projeto já implementou essas escolhas antes de registrar esta fonte; ela fundamenta retroativamente por que essas escolhas são corretas.
- PRÓXIMA_REVISÃO: Sem prazo crítico (conteúdo conceitual estável); revisar apenas se uma nova versão principal do CommonMark spec alterar a seção de motivação.

### FONTE-2004-DARINGFIREBALL-MARKDOWN-SYNTAX — Markdown: Syntax (+ Basics + License)
- ID_FONTE: FONTE-2004-DARINGFIREBALL-MARKDOWN-SYNTAX
- DATA_REGISTRO: 2026-07-02 (aprofundado no mesmo dia — 2ª leitura, navegando as abas Main/Basics/Syntax/License do projeto)
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: Markdown: Syntax — documentação completa (Overview, Block Elements, Span Elements, Miscellaneous), mais as páginas irmãs Basics (tutorial before/after) e License (BSD)
- AUTOR_ORGANIZAÇÃO: John Gruber / Daring Fireball
- DATA_PUBLICAÇÃO: 2004-12-17 (versão 1.0.1, confirmada na página principal do projeto: "Download Markdown 1.0.1 (18 KB) — 17 Dec 2004")
- LINK_REFERÊNCIA: https://daringfireball.net/projects/markdown/syntax (+ /basics, /license, mesmo site)
- TIPO_FONTE: Documentação oficial do criador da linguagem/ferramenta (fonte primária histórica)
- DOMÍNIO: Documentação Técnica / Especificação de Linguagem de Marcação
- SUBDOMÍNIO: Descrição original (informal) da sintaxe Markdown — filosofia de design, regras de formatação completas, licenciamento
- TEMA: Sintaxe, filosofia e regras de formatação do Markdown na sua forma original (pré-CommonMark)
- CONTEXTO_USO: KB-03 porque é a documentação técnica primária e histórica de uma linguagem de marcação amplamente adotada, e porque o par Basics/Syntax é um exemplo real de estratégia de documentação em duas camadas (tutorial rápido + referência exaustiva). KB-01 porque a leitura completa revela, com exemplos concretos e citações diretas, várias das ambiguidades específicas que `FONTE-2024-COMMONMARK-SPEC` só descrevia em abstrato — inclusive um bug reconhecido pelo próprio autor — servindo de estudo de caso real sobre como instruções em linguagem natural para "processar" algo (aqui, um parser; no nosso caso, um agente) falham sem regras explícitas para casos de borda.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-03 — Documentação Técnica, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Não há conflito factual, mas há relação direta documentada com `FONTE-2024-COMMONMARK-SPEC` — esta é a fonte "ambígua" que aquela fonte critica nominalmente; a leitura completa agora confirma exemplos concretos dessa ambiguidade na própria fonte primária.
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: **Filosofia** (já registrada antes): legibilidade acima de tudo, sintaxe inspirada em e-mail em texto puro, HTML complementar não substituído. **Block Elements**: parágrafos separados por linha em branco, com suporte a "hard-wrap" (quebra de linha manual não vira `<br>` automaticamente — precisa de 2+ espaços no fim da linha); headers Setext (`=`/`-`) e atx (`#` a `######`, fechamento cosmético opcional com hashes à direita, que não precisam bater em quantidade com os de abertura); blockquotes com `>` estilo e-mail, aninháveis, aceitam modo "preguiçoso" (só a primeira linha da linha dura precisa do `>`), podem conter outros elementos de bloco; listas não-ordenadas usam `*`/`+`/`-` de forma intercambiável, listas ordenadas usam número+ponto mas **o número real não afeta a saída HTML** (todas viram sequência 1,2,3...) — o autor recomenda começar em 1 "por enquanto" mas já cogita suporte futuro a números arbitrários; marcadores podem ser indentados até 3 espaços; **linha em branco entre itens de lista determina se cada item é envolvido em `<p>` ("loose") ou não ("tight")** — exatamente a ambiguidade de "list tightness" que `FONTE-2024-COMMONMARK-SPEC` menciona como não resolvida para casos parcialmente loose/tight; parágrafos subsequentes num item de lista precisam de 4 espaços/1 tab; blockquote dentro de item de lista precisa indentar o `>`, bloco de código dentro de item de lista precisa indentar 8 espaços/2 tabs (indentação duplicada); alerta explícito sobre listas ordenadas acidentais (`"1986. What a great season."` vira lista sem querer) — resolvido só com escape manual (`1986\.`); blocos de código via indentação de 4 espaços/1 tab, sintaxe Markdown não processada dentro; regra horizontal via 3+ hífens/asteriscos/underscores numa linha. **Span Elements**: links inline e reference; nomes de referência não fazem diferença maiúsc./minúsc.; três estilos de aspas para título de link (duplas, simples, parênteses) são ditos equivalentes, mas **o próprio documento reconhece**: "There is a known bug in Markdown.pl 1.0.1 which prevents single quotes from being used to delimit link titles" — um bug de implementação admitido pelo autor, não apenas ambiguidade de spec; justificativa quantitativa para links reference-style (mesmo parágrafo: 81 caracteres em reference-style vs. 176 em inline vs. 234 em HTML puro); emphasis via `*`/`_` simples (`<em>`) ou duplo (`<strong>`), delimitador de abertura e fechamento deve ser o mesmo caractere, funciona no meio de palavra, mas cercado de espaços vira literal; code span via backtick(s), múltiplos backticks permitem incluir backtick literal; imagens espelham a sintaxe de links (`![alt](url "title")`), e o documento admite explicitamente que **não existe sintaxe Markdown para especificar dimensões de imagem** — recomenda HTML puro para isso. **Miscellaneous**: links automáticos via `<url>` ou `<email>`, com ofuscação de e-mail por entidades decimais/hex aleatorizadas contra spambots (o autor admite que isso "won't fool all of them"); lista explícita de 12 caracteres com escape via backslash (`\`, backtick, `*`, `_`, `{}`, `[]`, `()`, `#`, `+`, `-`, `.`, `!`). **Basics** (página irmã): mesma sintaxe, formato tutorial "antes/depois", claramente pensada como porta de entrada mais curta antes do documento de referência completo. **License** (página irmã): licença BSD de 3 cláusulas, copyright 2004 John Gruber, sem garantias — confirma que o Markdown original é livre para redistribuição/modificação com atribuição.
- EVIDÊNCIA_PRINCIPAL: Duas citações-chave novas desta leitura completa: (1) sobre um bug real, não apenas ambiguidade — "There is a known bug in Markdown.pl 1.0.1 which prevents single quotes from being used to delimit link titles"; (2) sobre ausência deliberada de funcionalidade — "As of this writing, Markdown has no syntax for specifying the dimensions of an image; if this is important to you, you can simply use regular HTML `<img>` tags." Ambas mostram o autor documentando limitações conhecidas de forma transparente, em vez de omiti-las.
- LIMITAÇÕES: É uma descrição informal/prosa, não uma gramática formal — o motivo pelo qual `FONTE-2024-COMMONMARK-SPEC` considera este documento ambíguo em vários pontos, agora confirmados concretamente nesta leitura (tightness de listas, indentação em casos de borda). Não deve ser usado como referência de comportamento exato de parsing — para isso, a fonte mais forte e atual é a CommonMark Spec. Documento de 2004; o ecossistema atual de "Markdown" é dominado por variantes (GFM, CommonMark) que divergem deste original em detalhes. A página "Basics" é redundante em conteúdo com "Syntax" (mesmo material, forma tutorial) — não adiciona regras novas, só facilita onboarding.
- APLICAÇÃO_IA: Serve de contraponto histórico/factual à `FONTE-2024-COMMONMARK-SPEC`, agora com exemplos concretos e citações diretas (não só a afirmação abstrata de ambiguidade). Estudo de caso real e citável de como uma "especificação" em prosa natural falha em casos de borda (list tightness, indentação aninhada, bug de implementação não coberto pela doc) — diretamente análogo ao risco de `governanca/PROTOCOLO.md` ser interpretado de formas diferentes por agentes diferentes, como já ocorreu neste projeto. O padrão de documentação em duas camadas (Basics tutorial + Syntax referência completa, cross-linked) é um modelo replicável para este projeto.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 1
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 20

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar afirmações históricas/factuais detalhadas sobre a sintaxe, filosofia e limitações conhecidas do Markdown original, e agora serve de material de verificação cruzada concreto (não só abstrato) para as afirmações de `FONTE-2024-COMMONMARK-SPEC` sobre ambiguidade. Pode sustentar recomendação de documentar limitações conhecidas explicitamente (como o autor fez com o bug de aspas simples e a ausência de sintaxe para dimensão de imagem) em vez de omiti-las. Não deve ser usada como referência de comportamento de parsing exato — para isso, usar a CommonMark Spec.
- PRÓXIMA_REVISÃO: Sem prazo crítico — documento histórico estável, não deve mudar.

### FONTE-2026-STRIPE-API-DOCS — Stripe API Reference completo (overview, versioning, errors, mapa de 91 recursos, llms.txt, 4 Agent Skills + 6 arquivos de referência)
- ID_FONTE: FONTE-2026-STRIPE-API-DOCS
- DATA_REGISTRO: 2026-07-03 (aprofundado no mesmo dia — 2ª leitura, cobrindo os 2 skills e 6 referências que antes estavam listados como lacuna, mais o mapa completo da barra lateral da API Reference)
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: Stripe API Reference — visão geral, versionamento, erros, mapa completo de recursos, `llms.txt` e as 4 Agent Skills completas (`stripe-best-practices` + suas 6 referências, `stripe-directory`, `stripe-projects`, `upgrade-stripe`)
- AUTOR_ORGANIZAÇÃO: Stripe, Inc.
- DATA_PUBLICAÇÃO: Documentação viva/contínua; versão da API vigente no momento da consulta confirmada como `2026-06-24.dahlia` (na página, no `llms.txt` e nos SKILL.md)
- LINK_REFERÊNCIA: https://docs.stripe.com/api (+ /api/versioning, /api/errors, /llms.txt, /.well-known/skills/index.json, /.well-known/skills/stripe-best-practices/SKILL.md, /.well-known/skills/stripe-best-practices/references/{billing,connect,payments,security,tax,treasury}.md, /.well-known/skills/stripe-directory/SKILL.md, /.well-known/skills/stripe-projects/SKILL.md, /.well-known/skills/upgrade-stripe/SKILL.md)
- TIPO_FONTE: Documentação oficial de API de uma empresa (fonte primária, mantida pelo próprio provedor do serviço)
- DOMÍNIO: Documentação Técnica de API / Engenharia de Contexto para Agentes de IA
- SUBDOMÍNIO: Referência de API REST, política de versionamento, taxonomia de erros, e infraestrutura formal de descoberta de contexto para agentes de IA (`llms.txt` + Agent Skills)
- TEMA: Como uma empresa de infraestrutura crítica (processamento de pagamentos) documenta sua API para desenvolvedores E estrutura contexto especificamente para agentes de IA consumirem
- CONTEXTO_USO: KB-01 porque o Stripe publica, em produção, exatamente o tipo de infraestrutura de contexto para agentes que este projeto tenta construir — um `llms.txt` real com instrução anti-alucinação explícita, e Skills formais em `.well-known/skills/` no mesmo formato SKILL.md (frontmatter YAML `name`/`description`) usado neste ambiente Claude Code. KB-03 porque é documentação técnica de API de referência (REST, versionamento, códigos de erro) de altíssima maturidade, útil como benchmark.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-03 — Documentação Técnica, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma; complementa `FONTE-2026-MSR-CONTEXT-ENGINEERING` (estudo acadêmico sobre adoção de AGENTS.md) com um caso real e maduro de adoção de `llms.txt` + Agent Skills por uma empresa de grande porte.
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: **API Reference (overview)**: API REST, corpo form-encoded, resposta JSON; URL base `https://api.stripe.com`; sandboxes isolam de dados reais; sem atualização em lote. **Mapa completo**: a barra lateral da API Reference confirma **91 categorias de recursos de topo** (Balance, Charges, Customers, Payment Intents, Setup Intents, Payment Methods, Products, Prices, Checkout Sessions, Invoices, Subscriptions, Meters, Accounts, Transfers, Persons etc.) — confirma concretamente a escala de "centenas de endpoints" citada antes. **Versionamento**: esquema data+codinome (`2026-06-24.dahlia`); releases mensais compatíveis vs. major com breaking changes; regra própria por SDK. **Erros**: tabela de status HTTP, taxonomia de 4 tipos, objeto de erro rico. **`llms.txt`**: índice curado com instrução anti-alucinação. **As 4 Agent Skills completas**: `stripe-best-practices` com suas **6 referências internas**, cada uma seguindo o mesmo padrão — tabela de roteamento de decisão, seção "Traps to avoid" com proibições explícitas (`security.md`: nunca embutir chaves em código-cliente, preferir RAK sobre secret key, runbook de resposta a incidente de vazamento; `connect.md`: seção "Critical rules (never violate)" e "BLOCKED combinations (never recommend)" — ex. nunca usar `type: 'express'`/`'custom'`/`'standard'` na Accounts v2 API; `payments.md`: nunca usar Charges API ou Card Element, tabela de migração API-deprecada→atual; `billing.md`: recomendar Metronome em vez da Billing Meters API para novos casos de uso; `tax.md`: nunca aproximar jurisdição não suportada; `treasury.md`: usar v2 Financial Accounts, não v1). `stripe-projects`: provisionamento de infraestrutura via CLI, princípio "CLI as Source of Truth" (não editar arquivos gerados manualmente), tabela de tratamento de erro (código/causa/recuperação). `stripe-directory`: a mais notável — permite ao agente **descobrir E comprar autonomamente** serviços de terceiros via "Machine Payment Protocol" (MPP), pagando diretamente um endpoint HTTP 402 ("Payment Required"); mas com portão de aprovação explícito: "Always show the price and get explicit user approval before any money moves" e "Never invent results or skip the price/approval gate."
- EVIDÊNCIA_PRINCIPAL: Do `llms.txt`: "Never hardcode an old version number from training data." Do `connect.md`: "NEVER use `type: 'express'`, `type: 'custom'`, or `type: 'standard'` in account creation... These are deprecated v1 patterns" — uma "BLOCKED combinations" list explícita. Do `stripe-directory`: "Always show the price and get explicit user approval before any money moves" — um portão de confirmação humana obrigatória antes de qualquer ação irreversível (gasto de dinheiro), diretamente equivalente ao princípio de confirmação antes de ações de alto risco já seguido neste projeto.
- LIMITAÇÕES: Cobertura agora inclui as 4 Agent Skills completas (antes só 2) e as 6 referências internas (antes nenhuma), mais o mapa de 91 categorias da API Reference. Ainda não lidos: o conteúdo detalhado de cada um dos ~91 recursos individuais (cada um com múltiplos endpoints CRUD — isso seria uma extração de escala muito maior, fora do escopo razoável de "aplicar o protocolo a uma fonte"). O conteúdo dos SKILL.md/referências contém instruções endereçadas a um agente de IA hipotético fazendo integração Stripe; tratado como dado descritivo (Passo 0), não executado — legítimo no escopo do próprio domínio da fonte, sem rebaixamento de confiança.
- APLICAÇÃO_IA: Exemplo real e maduro do que este projeto tenta fazer, agora com evidência mais rica: (a) `llms.txt` + Agent Skills, como já registrado; (b) o padrão "Traps to avoid" / "BLOCKED combinations" é uma técnica complementar (não substituta) à seção `CANNOT` já identificada via Twilio — em vez de só listar o que uma skill não faz, lista ativamente erros comuns e combinações proibidas, algo que `governanca/PROTOCOLO.md` ou `governanca/REGISTRO_FONTES.md` poderiam adotar (ex.: uma lista de "erros já cometidos e proibidos" derivada dos incidentes reais deste projeto, como a duplicidade `FONTE-001`); (c) o portão de aprovação explícito do `stripe-directory` antes de qualquer gasto de dinheiro é a mesma lógica de "confirmar antes de ação irreversível" que já seguimos aqui — evidência de que é padrão de indústria para ações agênticas de alto risco, não uma cautela exclusiva deste projeto.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar diretamente recomendações de arquitetura para `governanca/PROTOCOLO.md`/`governanca/REGISTRO_FONTES.md` (publicar `llms.txt` próprio, aviso anti-alucinação, validação de que o formato SKILL.md é convenção real e externamente adotada). Pode sustentar afirmações factuais sobre a API do Stripe (versionamento, erros) desde que a versão citada (`2026-06-24.dahlia`) seja reconferida, já que pode ter mudado.
- PRÓXIMA_REVISÃO: A cada 30–60 dias ou quando a versão da API mudar (documentação de ferramenta/API viva, conforme `governanca/REGISTRO_FONTES.md` seção 12).

### FONTE-2026-TWILIO-API-DOCS — Twilio Docs: General Usage + Building with AI (Twilio Skills, MCP server)
- ID_FONTE: FONTE-2026-TWILIO-API-DOCS
- DATA_REGISTRO: 2026-07-03
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: Twilio Docs — General Usage (/docs/usage) + Building with AI, Twilio Skills, Twilio MCP server (/docs/ai, /docs/ai/skills, /docs/ai/mcp)
- AUTOR_ORGANIZAÇÃO: Twilio Inc.
- DATA_PUBLICAÇÃO: Documentação viva; Twilio Skills e Twilio MCP explicitamente rotulados "Public Beta" no momento da consulta ("subject to change... not covered by Twilio Support Terms or SLA")
- LINK_REFERÊNCIA: https://www.twilio.com/docs/usage (+ /docs/ai, /docs/ai/skills, /docs/ai/mcp, /llms.txt, /docs/llms.txt)
- TIPO_FONTE: Documentação oficial de API de uma empresa (fonte primária)
- DOMÍNIO: Documentação Técnica de API / Engenharia de Contexto para Agentes de IA
- SUBDOMÍNIO: Uso geral de conta/API REST + infraestrutura formal de contexto para agentes de IA (Agent Skills, MCP)
- TEMA: Como a Twilio documenta uso geral da API E estrutura acesso formal para agentes de IA via Skills e MCP
- CONTEXTO_USO: KB-01 porque `/docs/ai/skills` é a explicação mais detalhada já registrada do padrão Agent Skills — cita um padrão aberto (`agentskills.io`) com adoção multi-fornecedor (Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, JetBrains Junie, "30+ outras plataformas"), descreve arquitetura de "progressive disclosure" e introduz a técnica de seção `CANNOT` obrigatória por skill para reduzir alucinação — não vista em nenhuma fonte registrada até agora. KB-03 porque `/docs/usage` é documentação técnica de API padrão (contas, REST, segurança, ambiente de desenvolvimento).
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-01 — Engenharia de Contexto, KB-03 — Documentação Técnica, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Não é conflito, mas forte relação com `FONTE-2026-STRIPE-API-DOCS` — segundo caso real e independente (empresa de comunicações, não pagamentos) de adoção de `llms.txt` + Agent Skills; juntas, formam evidência de prática emergente da indústria, não caso isolado. Achado à parte: pequena inconsistência interna na própria documentação Twilio — `/docs/ai/mcp` lista "Twilio Skills" em "What's next" (como algo futuro), enquanto `/docs/ai/skills` já documenta comandos de instalação reais e funcionais — sinal de que a doc do MCP não foi atualizada após o lançamento de Skills (mesmo padrão de conteúdo desatualizado já visto em `FONTE-2026-GITLAB-RUNBOOKS`).
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: **General Usage**: página guarda-chuva para gerenciar conta via REST API — quickstarts por produto (SMS, Voice, Verify), setup de ambiente por linguagem (C#/ASP.NET, Java/Servlets, Node/Express, PHP, Python/Flask, Ruby/Sinatra, Go/Gin), gestão de API keys/subcontas/access tokens, e guia de segurança/anti-fraude com validação de requisições assinadas por linguagem. **Building with AI**: hub com dois caminhos — MCP (acesso à documentação/API) e Skills (conhecimento procedural curado) — mais produtos de IA conversacional (Agent Connect, Conversation Relay, Conversation Intelligence). **Twilio MCP server**: servidor hospedado (`mcp.twilio.com/docs`, sem autenticação, sem instalação) que indexa 1.800+ endpoints via workflow busca-então-recupera (`twilio__search` + `twilio__retrieve`), cobrindo specs OpenAPI públicas, docs Twilio/SendGrid/Segment; explicitamente somente leitura (não executa chamadas); versão retornada por padrão é a mais recente, com filtro `filter.version` para escolher outra. **Twilio Skills**: pacotes estruturados de conhecimento de produto, organizados em 4 categorias — Setup (`twilio-account-setup`, `twilio-iam-auth-setup`, `twilio-numbers-senders`, `twilio-webhook-architecture`), Planner/consultivas (`twilio-identity-verification-advisor`, `twilio-marketing-promotions-advisor`, `twilio-notifications-alerts-advisor`, `twilio-voice-ai-agent-advisor`), Product (`twilio-sms-send-message`, `twilio-whatsapp-send-message`, `twilio-verify-send-otp`, `twilio-sendgrid-email-send`) e Guardrail (`twilio-security-hardening`, `twilio-compliance-traffic`, `twilio-compliance-onboarding`). Segue o "Agent Skills standard" aberto (`agentskills.io`): arquitetura de "progressive disclosure" (metadata leve escaneada no início da sessão → skill completo carregado só quando a tarefa bate com a descrição → referência detalhada sob demanda) e cada skill deve ter uma seção `CANNOT` documentando explicitamente o que não faz, "reducing hallucination". Instalável via plugin (Claude Code, Cursor, Codex) ou manualmente copiando para `~/.agents/skills/` (compatível com GitHub Copilot, Gemini CLI, JetBrains Junie e 30+ plataformas).
- EVIDÊNCIA_PRINCIPAL: "Skills use a progressive disclosure architecture: your agent sees lightweight metadata for all skills at startup, loads the full skill only when your task matches, and can drill into detailed reference material on demand." E: "Explicit boundaries — Every skill includes a `CANNOT` section documenting what it cannot do, reducing hallucination." E, sobre o padrão: "The format is compatible with Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, JetBrains Junie, and any tool supporting the Agent Skills standard."
- LIMITAÇÕES: Twilio Skills e Twilio MCP são explicitamente rotulados "Public Beta" pela própria Twilio no momento da consulta — sujeitos a mudança, não cobertos por SLA ou termos de suporte padrão. O padrão `agentskills.io` citado não foi verificado de forma independente nesta extração (só reportado como fonte pela Twilio, não visitado diretamente). Inconsistência interna encontrada entre `/docs/ai/mcp` (trata Skills como "futuro") e `/docs/ai/skills` (já documenta Skills funcionando) — sinal de doc desatualizada em uma das duas páginas. Extração não cobriu o repositório `github.com/twilio/ai` nem cada uma das 15 Skills individualmente.
- APLICAÇÃO_IA: A seção `CANNOT` obrigatória é uma ideia nova e diretamente acionável, ainda ausente de `governanca/PROTOCOLO.md`/`governanca/TEMPLATE.md`/todas as KBs deste projeto — poderia ser adotada (ex.: o próprio `governanca/PROTOCOLO.md` ganhar uma seção "o que este protocolo não resolve/decide sozinho"). A tabela Skills-vs-MCP (conhecimento procedural curado, atualizado com releases, vs. especificação viva, sempre atual) é um modelo mental direto para a distinção já existente neste projeto entre `governanca/PROTOCOLO.md` (procedural, curado) e `ferramentas/check_kb_consistency.py` (verificação sobre estado vivo dos arquivos). A taxonomia de Skills por categoria (Setup/Planner/Product/Guardrail) é um padrão de organização replicável caso este projeto crie múltiplas Skills no futuro.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar diretamente a recomendação de seção `CANNOT` e o modelo mental Skills-vs-MCP para a arquitetura deste projeto. Não deve ser citada como garantia de estabilidade de longo prazo do produto Twilio Skills/MCP em si, já que ambos são declarados Public Beta pela própria fonte.
- PRÓXIMA_REVISÃO: A cada 30–60 dias (produto em Beta, sujeito a mudança rápida, conforme `governanca/REGISTRO_FONTES.md` seção 12).

### FONTE-2017-GOOGLE-SRE-POSTMORTEM-CULTURE — Site Reliability Engineering, Cap. 13 "Emergency Response" + Cap. 14 "Managing Incidents" + Cap. 15 "Postmortem Culture" + Apêndice D "Example Postmortem"
- ID_FONTE: FONTE-2017-GOOGLE-SRE-POSTMORTEM-CULTURE
- DATA_REGISTRO: 2026-07-03 (aprofundado no mesmo dia — 2ª leitura, navegando os capítulos cruzados citados no capítulo original)
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: Site Reliability Engineering (Google SRE Book) — Capítulo 13 "Emergency Response", Capítulo 14 "Managing Incidents", Capítulo 15 "Postmortem Culture: Learning from Failure" e Apêndice D "Example Postmortem"
- AUTOR_ORGANIZAÇÃO: Google, Inc. (Cap. 13 por Corey Adam Baye, ed. Diane Bates; Cap. 14 por Andrew Stribblehill, ed. Kavita Guliani; Cap. 15 por John Lunney e Sue Lueder, ed. Gary O'Connor); publicado por O'Reilly Media
- DATA_PUBLICAÇÃO: 2017 (copyright confirmado no rodapé de todas as páginas); licença CC BY-NC-ND 4.0
- LINK_REFERÊNCIA: https://sre.google/sre-book/postmortem-culture/ (+ /sre-book/example-postmortem/, /sre-book/managing-incidents/, /sre-book/emergency-response/)
- TIPO_FONTE: Livro técnico de referência de uma organização (fonte primária, best practices de engenharia consolidadas e amplamente citadas na indústria)
- DOMÍNIO: Documentação Técnica / Gestão do Conhecimento Organizacional
- SUBDOMÍNIO: Cultura de postmortem sem culpa (blameless), template de postmortem, práticas de disseminação de aprendizado organizacional a partir de falhas
- TEMA: Como transformar incidentes/falhas em conhecimento organizacional duradouro e acionável, sem cultura de culpa
- CONTEXTO_USO: KB-03 porque o Apêndice D fornece um template de documento estruturado (Summary, Impact, Root Causes, Trigger, Resolution, Detection, Action Items com Owner/Bug/Status, Lessons Learned, Timeline) diretamente comparável ao `governanca/TEMPLATE.md` deste projeto, e o Cap. 14 descreve o "Live Incident State Document" — documento vivo, editável concorrentemente, comparável à nossa `conteudo/FONTES_REGISTRADAS.md`. KB-06 porque o conjunto dos três capítulos é sobre gestão de conhecimento organizacional a partir de falhas — cultura blameless, revisão obrigatória ("No Postmortem Left Unreviewed"), disseminação ampla (newsletter mensal, "Wheel of Misfortune"), papéis claros de comando de incidente, e a técnica "Ask the Big, Even Improbable Questions" — diretamente aplicável ao modo como já documentamos, de forma blameless, o incidente real da duplicidade `FONTE-001`.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-03 — Documentação Técnica, KB-06 — Gestão do Conhecimento, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma; conecta-se ao histórico deste próprio projeto — a forma como já documentamos a duplicidade `FONTE-001`/`FONTE-2026-MSR-CONTEXT-ENGINEERING` (seção OBSERVAÇÕES daquele registro) já seguiu o espírito blameless descrito aqui, sem que tivéssemos citado essa prática formalmente até agora.
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: **Filosofia de postmortem**: escrito não é punição, é oportunidade de aprendizado para toda a empresa; gatilhos objetivos definidos ANTES de qualquer incidente (indisponibilidade visível ao usuário, perda de dados, intervenção manual do on-call, tempo de resolução acima de limiar, falha de monitoramento) — qualquer stakeholder também pode pedir um postmortem. **Cultura blameless**: assume que todos agiram com boa intenção e informação disponível na hora; foca em causas sistêmicas, não em indivíduos — "you can't fix people, but you can fix systems and processes"; dois exemplos lado a lado (linguagem de culpa vs. linguagem blameless) ilustrando a diferença concreta de tom. **Colaboração**: documento colaborativo em tempo real, com comentários abertos e notificação por e-mail; revisão formal obrigatória por engenheiros seniores antes de compartilhar amplamente, com critérios explícitos (dados coletados? causa raiz suficientemente profunda? plano de ação com prioridade adequada?) — "an unreviewed postmortem might as well never have existed". **Disseminação cultural**: "postmortem of the month" (newsletter), grupo de discussão interno, clubes de leitura de postmortem (às vezes revisando incidentes de anos atrás), e "Wheel of Misfortune" — reencenação de um incidente antigo com engenheiros novos assumindo os papéis originais, com o incident commander original presente para dar realismo. Reconhecimento público de bons postmortems, inclusive por lideranças (TGIF com os fundadores da Google). **Apêndice D — template de postmortem completo e preenchido** (incidente fictício "Shakespeare Sonnet++"): campos Date/Authors/Status/Summary/Impact/Root Causes/Trigger/Resolution/Detection; tabela de Action Items com colunas Ação/Tipo(mitigate,prevent,process,other)/Owner/Bug-e-status; seção "Lessons Learned" dividida em "What went well" / "What went wrong" / "Where we got lucky" (near misses); Timeline minuto a minuto do incidente; seção de informação de suporte (dashboards, logs).
- EVIDÊNCIA_PRINCIPAL: "Writing a postmortem is not punishment—it is a learning opportunity for the entire company." "An unreviewed postmortem might as well never have existed." Do Cap. 13, sobre um bug real de um filtro vazio interpretado como "combina com tudo", que mandou toda uma frota global para fila de destruição de disco: "Yes, sometimes zero does mean all." Do Cap. 14, sobre o protocolo de handoff do incident commander: deve dizer explicitamente "You're now the incident commander, okay?" e não pode desligar sem confirmação recebida.
- LIMITAÇÕES: O incidente do Apêndice D ("Shakespeare Sonnet++") é explicitamente fictício/humorístico — detalhes como "Delorean's glove compartment", "flux capacitor" e "goat teleporter" deixam isso claro por design; os três casos do Cap. 13 (Test/Change/Process-Induced Emergency), ao contrário, são apresentados como incidentes reais da Google, sem nomes fictícios. Os capítulos são de 2017; práticas de ferramentas internas (Google Docs, IRC) são datadas, embora os princípios (blameless, revisão obrigatória, comando de incidente, disseminação) permaneçam padrão da indústria até hoje. Não há detalhamento de técnicas de análise de causa raiz (o próprio texto remete a outra referência, [Roo04], fora do escopo desta extração).
- APLICAÇÃO_IA: Sustenta formalizar, em `governanca/REGISTRO_FONTES.md`, uma prática de "postmortem leve" sempre que `ferramentas/check_kb_consistency.py` (Passo 10) encontrar uma divergência real, no espírito blameless já praticado informalmente com o incidente `FONTE-001`. A estrutura de Action Items com tipo/status é um padrão replicável para os itens listados em "O que este protocolo NÃO resolve". O "Live Incident State Document" (Cap. 14) — vivo, template-based, info mais importante no topo — é um modelo direto para `conteudo/FONTES_REGISTRADAS.md`. O protocolo de handoff explícito com confirmação obrigatória é aplicável a qualquer transferência de responsabilidade entre agentes/sessões neste projeto. A técnica "Ask the Big, Even Improbable Questions: What If...?" (Cap. 13) é um exercício direto para revisar `governanca/PROTOCOLO.md`: "e se dois agentes gravarem na mesma KB ao mesmo tempo?", "e se o checker de consistência falhar silenciosamente?".

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar a adoção formal de um "postmortem leve" para divergências reais encontradas pelo checker, e de uma tabela de Action Items com tipo/owner/status para itens pendentes de arquitetura (como os já listados em "O que este protocolo NÃO resolve"). Não deve ser usada para afirmar fatos sobre incidentes reais do Google — o exemplo do Apêndice D é fictício.
- PRÓXIMA_REVISÃO: Sem prazo crítico — livro de referência estável desde 2017; revisar apenas se surgir edição atualizada.

### FONTE-2026-GITLAB-HANDBOOK — The GitLab Handbook (homepage + About the Handbook + Values/CREDIT)
- ID_FONTE: FONTE-2026-GITLAB-HANDBOOK
- DATA_REGISTRO: 2026-07-03
- RESPONSÁVEL: Davi Sermenho (via Claude)
- TÍTULO: The GitLab Handbook — homepage + "About the Handbook" (histórico, filosofia, metodologia) + visão geral de "GitLab Values" (CREDIT)
- AUTOR_ORGANIZAÇÃO: GitLab Inc.
- DATA_PUBLICAÇÃO: Documentação viva, editada continuamente via merge request; contagem de palavras "ao vivo" confirmada na própria página no momento da consulta (2026-07-03): 3.966.332 palavras, 3.277 páginas, "Hugo generated Live Count"
- LINK_REFERÊNCIA: https://handbook.gitlab.com/ (+ /handbook/about/, /handbook/values/)
- TIPO_FONTE: Documentação oficial de uma organização (fonte primária; o próprio site do handbook é código aberto: gitlab.com/gitlab-com/content-sites/handbook)
- DOMÍNIO: Documentação Técnica / Gestão do Conhecimento Organizacional
- SUBDOMÍNIO: Cultura "handbook-first", single source of truth, colaboração assíncrona, valores organizacionais
- TEMA: Como uma empresa 100% remota trata seu handbook como o sistema primário de gestão de conhecimento e comunicação da organização
- CONTEXTO_USO: KB-03 porque documenta práticas concretas de documentação-como-código: histórico de contagem de palavras/páginas com metodologia reproduzível via shell (`find ... -name "*.md" | xargs wc -w`), instrução exata de `git checkout` para recuperar uma versão histórica do handbook, changelog via merge request. KB-06 porque é, no fundo, sobre gestão de conhecimento organizacional — "handbook-first" como estratégia deliberada para comunicação assíncrona — e principalmente porque resolve exatamente uma lacuna que identificamos em `governanca/PROTOCOLO.md` ("O que este protocolo NÃO resolve", item 7): "The handbook is subject to interpretation... check with the content owner of the page" define um dono explícito por página como mecanismo de escalonamento de ambiguidade — algo que `governanca/PROTOCOLO.md`/`governanca/REGISTRO_FONTES.md` não têm hoje.
- TIPO_CONHECIMENTO: Permanente
- ARQUIVO_DESTINO_KB: KB-03 — Documentação Técnica, KB-06 — Gestão do Conhecimento, KB-PROJ-05 — Arquitetura da Base de Conhecimento
- REUTILIZÁVEL_EM_OUTROS_PROJETOS: Sim
- VINCULA_DECISÃO_PROJETO: Não
- DECISÃO_RELACIONADA: Não aplicável
- FONTES_EM_CONFLITO: Nenhuma; relacionada (mesma organização, não duplicata) a `FONTE-2026-GITLAB-RUNBOOKS` já registrada — aquela cobre documentação operacional técnica (runbooks de SRE), esta cobre a cultura e o processo de documentação da empresa como um todo. Juntas mostram duas camadas do mesmo compromisso organizacional com documentação como produto.
- STATUS_DE_ROTEAMENTO: Roteado

Extração de conteúdo
- CONTEÚDO_EXTRAÍDO: O handbook nasceu quando a GitLab tinha 10 pessoas, para garantir que informação da empresa fosse acessível independentemente de quando alguém entrou. Vantagens listadas explicitamente: leitura é mais rápida e mais assíncrona que ouvir; contratação e retenção melhoram com transparência prévia; onboarding fica mais fácil; discussão de mudanças fica mais fácil ("aponte para o diff" em vez de reexplicar); qualquer pessoa pode propor mudança via merge request. Reconhecimento explícito de ambiguidade: "the handbook is subject to interpretation" — mecanismo de dono por página para resolver dúvida de interpretação; "everything is in draft at GitLab and subject to change, this includes our handbook"; e uma ressalva importante: "just because something is not yet in the handbook does not mean that it is allowed" (o handbook documenta o processo atual, não é uma lista exaustiva do permitido). Metodologia de contagem 100% reproduzível: comando shell exato para contar palavras, e comando git exato para recuperar uma versão histórica do handbook. Série histórica real de contagem: de 298.806 palavras/228 páginas (2018-01-01) até pico de 5.129.952 palavras/3.823 páginas (2025-01-03), com uma migração completa de plataforma registrada em 2023-12-22 (reset a zero), e uma **contração real e recente**: de 5.137.908 palavras (2026-01-01) para 3.966.332 palavras (2026-07-03) — queda de ~1,17 milhão de palavras em 6 meses, sinal de poda/consolidação deliberada, não só crescimento orgânico. Página "Values" (CREDIT): Collaboration, Results for Customers, Efficiency, Diversity/Inclusion/Belonging, Iteration, Transparency — valores tratados como "living document", revisáveis via MR endereçada ao Chief People Officer; "Collaboration" detalhada com práticas específicas (kindness, compartilhar problemas abertamente, feedback negativo em ambiente pequeno/1-a-1, feedback positivo público, escalonamento de discordância "sem represália").
- EVIDÊNCIA_PRINCIPAL: "The handbook is subject to interpretation... If you have any questions or need further clarification please check with the content owner of the page." E: "Just because something is not yet in the handbook does not mean that it is allowed." E a série histórica real de contagem de palavras, confirmando contração recente de ~1,17M palavras entre 2026-01-01 e 2026-07-03.
- LIMITAÇÕES: Extração cobriu a homepage e "About the Handbook" por completo, mas só a introdução + elaboração de "Collaboration" da página "Values" (~99KB de conteúdo total, cobrindo os 6 valores em detalhe — os outros 5 não foram lidos integralmente). Não cobre páginas técnicas mais profundas citadas ali (Handbook Direction, Handbook Style Guide, Handbook Escalation, Contributing to the Handbook) — só apareceram como títulos/resumos de uma linha. O conceito de "content owner por página" foi confirmado pelo texto, mas não verifiquei diretamente como esse dono é atribuído/exibido em uma página individual qualquer.
- APLICAÇÃO_IA: A prática de "content owner por página" resolve diretamente o item 7 de "O que este protocolo NÃO resolve" em `governanca/PROTOCOLO.md` (falta de mecanismo de acompanhamento para validação humana pendente) — sugere adotar um campo de responsável/dono explícito por KB ou por regra em `governanca/REGISTRO_FONTES.md` para resolver ambiguidade de interpretação entre agentes, exatamente o problema já vivido (Claude vs. ChatGPT). A metodologia de contagem reproduzível via shell é um modelo direto para o espírito de `ferramentas/check_kb_consistency.py`. A contração real e recente do handbook é evidência de que mesmo uma cultura "handbook-first" madura precisa de poda ativa — relevante para a seção 12 de `governanca/REGISTRO_FONTES.md` (obsolescência): documentação viva também precisa ser podada, não só revisada.

Pontuação da fonte
- IDENTIFICAÇÃO_COMPLETA (0 a 2): 2
- RELEVÂNCIA_TAREFA (0 a 3): 3
- FORÇA_FONTE (0 a 3): 3
- ATUALIDADE (0 a 2): 2
- RASTREABILIDADE (0 a 3): 3
- EXTRAÇÃO_ÚTIL (0 a 3): 3
- LIMITAÇÕES_REGISTRADAS (0 a 2): 2
- APLICAÇÃO_PARA_IA (0 a 3): 3
- PONTUAÇÃO_TOTAL (0 a 21): 21

Status e decisão de uso
- NÍVEL_CONFIANÇA: Fonte forte
- STATUS: Aceita
- DECISÃO_DE_USO: Pode sustentar a recomendação concreta de adicionar um campo de responsável/dono por KB ou por regra em `governanca/REGISTRO_FONTES.md`, endereçando diretamente o item 7 (e parcialmente o item 1) de "O que este protocolo NÃO resolve" em `governanca/PROTOCOLO.md`.
- PRÓXIMA_REVISÃO: 30–60 dias — é documentação viva de uma empresa, e a própria fonte mostra que ela muda substancialmente em poucos meses.
