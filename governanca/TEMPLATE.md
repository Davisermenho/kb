# Instrução de uso

Preencha primeiro um rascunho em `.kb/runs/<RUN_ID>/draft.md`. Não grave este template no ledger antes da avaliação, do roteamento, dos gates e da revisão exigida pelo risco. O registro só deve ser considerado publicado quando os campos obrigatórios, a pontuação, o status, a decisão de uso e os gates estiverem aprovados.

## 0. Controle do fluxo

- **RUN_ID:**
- **ESTADO_FLUXO:** RASCUNHO / EXTRAÍDO / AVALIADO / ROTEAMENTO_PROPOSTO / APROVADO / PREPARADO / VALIDADO_ESTRUTURALMENTE / VALIDADO_SEMANTICAMENTE / PUBLICADO
- **NÍVEL_RISCO:** Baixo / Médio / Alto / Crítico
- **MANIFESTO_REFERÊNCIA:**
- **REVISÃO_REFERÊNCIA:**
- **RELAÇÃO_COM_PROJETO:** mudanca_comprovadamente_motivada / reforco_retrospectivo / recomendacao_nao_implementada / sem_relacao_comprovada
- **CHANGE_ID:**
- **DECISÃO_CAUSAL_REFERÊNCIA:**
- **DIFF_REFERÊNCIA:**

## 1. Identificação da fonte

- **ID_FONTE:**
- **DATA_REGISTRO:**
- **RESPONSÁVEL:**
- **TÍTULO:**
- **AUTOR_ORGANIZAÇÃO:**
- **DATA_PUBLICAÇÃO:**
- **LINK_REFERÊNCIA:**
- **TIPO_FONTE:**
- **DOMÍNIO:**
- **SUBDOMÍNIO:**
- **TEMA:**
- **CONTEXTO_USO:**
- **TIPO_CONHECIMENTO:** Permanente / Específico / Decisão do Projeto
- **ARQUIVO_DESTINO_KB:**
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Sim / Não / Parcial
- **VINCULA_DECISÃO_PROJETO:** Sim / Não
- **DECISÃO_RELACIONADA:**
- **FONTES_EM_CONFLITO:**
- **STATUS_DE_ROTEAMENTO:** Pendente / Roteado / Revisar / Bloqueado

## 2. Extração de conteúdo

- **CONTEÚDO_EXTRAÍDO:**
- **EVIDÊNCIA_PRINCIPAL:**
- **LIMITAÇÕES:**
- **APLICAÇÃO_IA:**
- **OBSERVAÇÕES:**

## 3. Pontuação da fonte

Use a pontuação máxima indicada em cada critério. Quando a informação não estiver clara, pontue de forma conservadora.

- **IDENTIFICAÇÃO_COMPLETA (0 a 2):**
- **RELEVÂNCIA_TAREFA (0 a 3):**
- **FORÇA_FONTE (0 a 3):**
- **ATUALIDADE (0 a 2):**
- **RASTREABILIDADE (0 a 3):**
- **EXTRAÇÃO_ÚTIL (0 a 3):**
- **LIMITAÇÕES_REGISTRADAS (0 a 2):**
- **APLICAÇÃO_PARA_IA (0 a 3):**
- **PONTUAÇÃO_TOTAL (0 a 21):**

## 4. Status e decisão de uso

- **NÍVEL_CONFIANÇA:**
- **STATUS:**
- **DECISÃO_DE_USO:**
- **PRÓXIMA_REVISÃO:**

**Valores permitidos**

- **NÍVEL_CONFIANÇA:** Fonte forte, Fonte média, Fonte fraca, Fonte rejeitada.
- **STATUS:** Aceita, Pendente, Revisar, Rejeitada.
- **TIPO_CONHECIMENTO:** Permanente, Específico, Decisão do Projeto.
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Sim, Não, Parcial.
- **STATUS_DE_ROTEAMENTO:** Pendente, Roteado, Revisar, Bloqueado.

## 5. Régua de classificação

- **17 a 21 pontos:** Fonte forte. Pode sustentar critérios, decisões e recomendações.
- **11 a 16 pontos:** Fonte média. Pode complementar análise, mas não deve sustentar sozinha uma decisão crítica.
- **6 a 10 pontos:** Fonte fraca. Pode gerar hipótese, mas não sustenta conclusão.
- **0 a 5 pontos:** Fonte rejeitada. Não deve ser usada pelo agente.

## 6. Critérios mínimos de aceite

- [ ] A fonte tem origem identificável?
- [ ] A fonte é relevante para a tarefa?
- [ ] A fonte possui autoridade ou evidência suficiente?
- [ ] A fonte está atualizada para o contexto?
- [ ] A informação extraída é rastreável?
- [ ] A fonte gera conteúdo acionável?
- [ ] As limitações estão registradas?

Se qualquer critério mínimo falhar, a fonte não deve ser usada como base forte.

## 7. Exemplo preenchido

- **ID_FONTE:** FONTE-2026-VENDOR-PROMPT-BEST-PRACTICES (formato: `FONTE-<ANO>-<VEÍCULO_ABREVIADO>-<TEMA_CURTO>`; nunca use contador sequencial genérico como `FONTE-001` — ver `governanca/REGISTRO_FONTES.md` seção 9)
- **DATA_REGISTRO:** 2026-06-30
- **RESPONSÁVEL:** Davi Sermenho
- **TÍTULO:** Documentação oficial sobre boas práticas de prompts e uso de contexto em modelos generativos
- **AUTOR_ORGANIZAÇÃO:** Organização responsável pela ferramenta
- **DATA_PUBLICAÇÃO:** Atualizar conforme a data da fonte consultada
- **LINK_REFERÊNCIA:** Inserir link oficial da fonte
- **TIPO_FONTE:** Documentação oficial
- **DOMÍNIO:** Engenharia de Contexto para IA
- **SUBDOMÍNIO:** Curadoria de fontes e design de tarefas para IA
- **TEMA:** Uso de fontes confiáveis para melhorar respostas de agentes de IA
- **CONTEXTO_USO:** Apoiar criação de prompts, tasks, critérios de aceite e validação de respostas
- **TIPO_CONHECIMENTO:** Permanente
- **ARQUIVO_DESTINO_KB:** KB-01 — Engenharia de Contexto
- **REUTILIZÁVEL_EM_OUTROS_PROJETOS:** Sim
- **VINCULA_DECISÃO_PROJETO:** Não
- **DECISÃO_RELACIONADA:** Não aplicável
- **FONTES_EM_CONFLITO:** Nenhuma registrada
- **STATUS_DE_ROTEAMENTO:** Roteado
- **CONTEÚDO_EXTRAÍDO:** Boas práticas, limitações, recomendações operacionais e exemplos de uso de contexto
- **EVIDÊNCIA_PRINCIPAL:** A qualidade do contexto influencia diretamente a qualidade da resposta gerada pelo agente
- **LIMITAÇÕES:** Pode mudar conforme novas versões da ferramenta ou novas recomendações oficiais
- **APLICAÇÃO_IA:** Ajuda o agente a construir tarefas mais precisas, reduzir erro e justificar melhor suas decisões
- **IDENTIFICAÇÃO_COMPLETA (0 a 2):** 2
- **RELEVÂNCIA_TAREFA (0 a 3):** 3
- **FORÇA_FONTE (0 a 3):** 3
- **ATUALIDADE (0 a 2):** 2
- **RASTREABILIDADE (0 a 3):** 3
- **EXTRAÇÃO_ÚTIL (0 a 3):** 3
- **LIMITAÇÕES_REGISTRADAS (0 a 2):** 2
- **APLICAÇÃO_PARA_IA (0 a 3):** 3
- **PONTUAÇÃO_TOTAL (0 a 21):** 21
- **NÍVEL_CONFIANÇA:** Fonte forte
- **STATUS:** Aceita
- **DECISÃO_DE_USO:** Pode sustentar critérios de aceite, orientar o agente e servir como referência principal para a tarefa
- **PRÓXIMA_REVISÃO:** Revisar quando houver nova versão da documentação ou mudança relevante na ferramenta

## 8. Critério de pronto

Este registro está pronto quando for possível responder:

- De onde veio a informação?
- Por que a fonte é confiável?
- O que foi extraído da fonte?
- Qual é a pontuação da fonte?
- Qual é o status da fonte?
- Como o agente de IA pode usar essa evidência?
- Quando a fonte deve ser revisada?
- Qual é o `RUN_ID` e o diff associado?
- A relação com o projeto é causal, retrospectiva, recomendação ou não comprovada?
- Quais gates foram executados e quais limites permanecem?
