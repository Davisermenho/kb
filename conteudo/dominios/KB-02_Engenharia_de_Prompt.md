# KB-02 — Engenharia de Prompt

## Escopo
Conhecimento Permanente. Engenharia de prompts — serve para criar, avaliar, refinar ou validar prompts em qualquer projeto ou ferramenta.

## Regras de uso deste arquivo
Este arquivo só deve ser editado seguindo o Passo 6 de `governanca/PROTOCOLO.md` (escrita idempotente): um bloco novo por `ID_FONTE`, nunca sobrescrevendo o arquivo inteiro. Ao editar um `ID_FONTE` já existente, atualize o bloco correspondente em vez de duplicá-lo.

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

### FONTE-2025-ARXIV-ACE — Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- Nível de confiança: Fonte média (21/21; rebaixada pela regra de conteúdo não confiável)
- Conteúdo extraído: Prompts de sistema podem ser otimizados como playbooks evolutivos. Em vez de substituir todo o prompt a cada ciclo, ACE extrai lições de trajetórias e produz deltas localizados, com refinamento multiépoca e controle de redundância.
- Aplicação: Avaliar prompts com traces e feedback de execução; converter falhas e acertos em alterações pequenas e auditáveis; preservar instruções úteis em vez de aceitar resumos cada vez mais curtos.
- Limitações: Os ganhos dependem do modelo, do benchmark e da qualidade da reflexão. O apêndice contém instruções dirigidas a agente; elas foram ignoradas, e a fonte ficou com status Revisar.
- Última atualização: 2026-07-02

### FONTE-2022-NEURIPS-COT-PROMPTING — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Chain-of-Thought prompting insere nos exemplos few-shot passos intermediários entre a entrada e a resposta. No estudo, isso melhorou raciocínio aritmético, de senso comum e simbólico em modelos suficientemente grandes, com maior utilidade em tarefas difíceis e multi-etapas. A eficácia variou conforme escala, modelo, prompt e anotador; modelos menores frequentemente produziram cadeias fluentes mas ilógicas.
- Aplicação: Em tarefas multi-etapas, testar exemplos no formato entrada → decomposição → resposta contra um baseline direto. Validar tanto a resposta quanto os passos e testar variações do prompt. Não interpretar a cadeia gerada como prova fiel do raciocínio interno nem como evidência factual sem verificação.
- Limitações: Resultados baseados em modelos de 2022, sobretudo modelos proprietários muito grandes; limiares de escala podem não valer para modelos atuais. Cadeias podem conter erros ou justificar por acaso uma resposta correta. Há sensibilidade ao prompt e custo de anotação.
- Última atualização: 2026-07-02

### FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY — A Survey of Context Engineering for Large Language Models
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Posiciona engenharia de prompt como uma parte específica de "context retrieval/generation" dentro do campo mais amplo de context engineering — instruções, exemplos e raciocínio estruturado são componentes de geração de contexto, não uma disciplina isolada.
- Aplicação: Ao avaliar ou refinar prompts, considerar também que conhecimento, ferramentas e memória estão disponíveis ao agente — um prompt bem escrito não compensa contexto mal estruturado.
- Limitações: Preprint arXiv, síntese bibliográfica sem validação empírica própria; taxonomia pode mudar conforme o campo amadurece.
- Última atualização: 2026-07-02
