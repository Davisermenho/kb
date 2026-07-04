# KB-06 — Gestão do Conhecimento

## Escopo
Conhecimento Permanente. Curadoria, classificação, RAG, ontologia, reuso, taxonomia ou gestão de conhecimento — organiza conhecimento para agentes e sistemas de IA em qualquer projeto.

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

### FONTE-2025-ARXIV-ACE — Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- Nível de confiança: Fonte média (21/21; rebaixada pela regra de conteúdo não confiável)
- Conteúdo extraído: Gerir conhecimento contextual como itens com ID, conteúdo e contadores de utilidade/dano. Usar atualizações incrementais, deduplicação semântica e refinamento periódico ou acionado por limite de contexto. Essa estrutura permite rastrear, corrigir, podar e preservar unidades de conhecimento.
- Aplicação: Implementar KBs e memórias com escrita idempotente por ID, append de itens novos, edição localizada, sinais de qualidade e revisão seletiva. Usar a separação geração→reflexão→curadoria como fluxo de governança.
- Limitações: Reflexões incorretas podem contaminar a base, exigindo validação e mecanismos de remoção. O apêndice contém instruções dirigidas a agente; elas foram ignoradas, e a fonte ficou com status Revisar.
- Última atualização: 2026-07-02

### FONTE-2026-MSR-CONTEXT-ENGINEERING — Context Engineering for AI Agents in Open-Source Software
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Arquivos de contexto para IA (AGENTS.md, CLAUDE.md, Copilot instructions, GEMINI.md) são artefatos versionados que, segundo o estudo, deveriam ser tratados como software mantido — revisado, testado, com controle de qualidade — e não como documentação estática escrita uma vez. Apenas 5% dos repositórios OSS populares analisados adotam algum desses formatos.
- Aplicação: Reforça, para qualquer sistema de gestão de conhecimento operado por agentes, a prática de tratar artefatos de contexto/documentação como versionados, revisáveis e sujeitos a controle de qualidade contínuo, não como texto estático.
- Limitações: Estudo exploratório/preliminar; amostra de 10.000 repositórios populares via ranking, não necessariamente representativa.
- Última atualização: 2026-07-02

### FONTE-2025-ARXIV-CONTEXT-ENGINEERING-SURVEY — A Survey of Context Engineering for Large Language Models
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Organiza taxonomia, RAG, sistemas de memória, curadoria, recuperação, compressão e avaliação como parte de "gerenciamento de contexto" — disciplina que trata o conhecimento disponível a um agente como um conjunto dinâmico de componentes orquestrados, não um documento estático.
- Aplicação: Usar a taxonomia (recuperação/geração → processamento → gerenciamento) como referência para revisar como qualquer sistema de KBs é estruturado, roteado e avaliado por componente.
- Limitações: Preprint arXiv; survey, não estudo empírico primário; mais de 1400 trabalhos analisados, mas a seleção bibliográfica é dos próprios autores.
- Última atualização: 2026-07-02

### FONTE-2017-GOOGLE-SRE-POSTMORTEM-CULTURE — Site Reliability Engineering, Cap. 13 "Emergency Response" + Cap. 14 "Managing Incidents" + Cap. 15 "Postmortem Culture" + Apêndice D "Example Postmortem"
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Cultura blameless de postmortem — foca em causas sistêmicas, não em indivíduos; revisão formal obrigatória ("an unreviewed postmortem might as well never have existed"); disseminação ativa ("Wheel of Misfortune"). O Cap. 14 define um Sistema de Comando de Incidentes com 4 papéis (Command/Ops/Communication/Planning) e um protocolo de handoff explícito com confirmação obrigatória ("You're now the incident commander, okay?"). O Cap. 13 traz "Keep a History of Outages" e a técnica "Ask the Big, Even Improbable Questions: What If...?" para imaginar desastres proativamente, com um exemplo real de bug ("sometimes zero does mean all" — filtro vazio interpretado como "combina com tudo").
- Aplicação: Cultura blameless de postmortem foca em causas sistêmicas, não indivíduos — aplicável a qualquer equipe ou sistema multiagente que aprenda com falhas. O protocolo de handoff com confirmação obrigatória é aplicável a qualquer transferência de responsabilidade entre agentes/sessões. A técnica "Ask the Big, Even Improbable Questions: What If...?" é um exercício geral para imaginar modos de falha em qualquer sistema antes que aconteçam.
- Limitações: O exemplo do Apêndice D é fictício; os 3 casos do Cap. 13 são reais. Princípios de 2017, ainda padrão da indústria.
- Última atualização: 2026-07-03

### FONTE-2026-GITLAB-HANDBOOK — The GitLab Handbook (homepage + About the Handbook + Values/CREDIT)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Handbook nasceu para garantir que informação da empresa fosse acessível independentemente de quando alguém entrou — leitura assíncrona, "aponte para o diff" em vez de reexplicar mudanças, qualquer um propõe mudança via MR. Reconhece ambiguidade explicitamente: "the handbook is subject to interpretation... check with the content owner of the page" — dono por página como mecanismo de escalonamento. Ressalva importante: "just because something is not yet in the handbook does not mean that it is allowed."
- Aplicação: A prática de "content owner por página" é um mecanismo geral de escalonamento de ambiguidade: qualquer sistema de documentação colaborativa se beneficia de atribuir um responsável explícito por trecho/regra, para resolver dúvidas de interpretação sem depender de convenção implícita.
- Limitações: Conceito de "content owner por página" confirmado pelo texto, mas não verificado diretamente em uma página individual. Extração da página "Values" cobriu só a introdução, não os 6 valores em detalhe.
- Última atualização: 2026-07-03
