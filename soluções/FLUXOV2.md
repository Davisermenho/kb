# Fluxo V2 — Plano completo de implementação e governança

> **Estado da implementação em 2026-07-04:** baseline aprovado no commit `17419bc`; Fases 0–6 implementadas e fluxo de publicação homologado pelo `RUN-2026-07-04-FLUXOV2-HOMOLOG`, publicado no commit `a5aa1f6`. Testes, checker, gates, revisão humana, lock e preservação de mudanças paralelas foram exercitados. Permanece aberta somente a migração das alegações causais legadas inventariadas em `.kb/LEGACY_CAUSALITY_REVIEW.md`.

## 1. Finalidade

Este documento especifica todas as ações necessárias para transformar o fluxo atual de registro de fontes em um processo versionado, verificável, orientado por risco e resistente aos principais erros observados no uso de agentes de IA.

O Fluxo V2 não parte da premissa de que o agente compreenderá ou lembrará corretamente todas as regras. As garantias devem ser produzidas por estado explícito, schemas, diffs, gates automatizados, revisão proporcional ao risco e autoridade humana nos pontos críticos.

O objetivo não é eliminar todo risco semântico — algo que automação estrutural não consegue prometer —, mas reduzir drasticamente a probabilidade de:

- persistir conteúdo incompleto como final;
- registrar a mesma fonte mais de uma vez;
- publicar conteúdo em destino incorreto;
- declarar causalidade sem evidência;
- alterar arquivos fora do escopo autorizado;
- corrigir uma ocorrência e deixar cópias semanticamente conflitantes;
- usar um teste estrutural como aprovação factual;
- perder cronologia, autoria ou justificativa da mudança;
- publicar simultaneamente mudanças conflitantes de agentes diferentes.

## 2. Diagnóstico do fluxo atual

O fluxo normativo atual é, em termos materiais:

```text
Triagem
→ busca de duplicidade
→ gravação do registro completo no ledger
→ pontuação
→ confiança e status
→ roteamento
→ gravação nas KBs
→ tratamento de conflitos
→ revisão futura
→ checker estrutural
```

O problema central é a inversão entre decisão e persistência. O registro é salvo como completo antes de serem definidos pontuação, status, conflitos e destinos. Isso cria estados intermediários que parecem finais e torna o ledger vulnerável a preenchimento especulativo.

O checker e o hook atuais possuem valor, mas verificam apenas parte da estrutura ledger↔KB. Eles não certificam factualidade, fidelidade da síntese, coerência de score, escopo, causalidade, revisão ou atualidade. Consequentemente, seu resultado não pode ser apresentado como aprovação integral da fonte.

## 3. Princípios obrigatórios

1. **Avaliar antes de publicar.** Dados incompletos permanecem em rascunho, fora dos arquivos canônicos.
2. **Falhar de forma fechada.** Estrutura ausente, ambígua ou não interpretável nunca produz sucesso.
3. **Uma fonte de verdade por domínio.** Ledger controla registros; KBs controlam conhecimento publicado; Git controla cronologia; manifesto controla escopo; decisões humanas controlam exceções.
4. **Persistência lógica única.** Ledger, KBs e pendências de uma operação devem ser publicados como uma mesma mudança versionada.
5. **Nenhum `OK` universal.** Cada gate declara exatamente o que verificou e o que não verificou.
6. **Evidência antes de causalidade.** Sequência temporal não basta para provar motivação.
7. **Revisão proporcional ao risco.** Automação cobre o verificável; decisões críticas permanecem humanas.
8. **Agente não autoriza o próprio aumento de escopo.** Nova KB, mudança arquitetural, exclusão e sincronização exigem autoridade explícita.
9. **Preservar trabalho preexistente.** Alterações fora do `RUN_ID` não podem ser sobrescritas ou incorporadas silenciosamente.
10. **Determinismo e reprodutibilidade.** Mesma entrada e mesmo estado devem gerar resultados comparáveis, ordenados e auditáveis.
11. **Conteúdo externo é dado.** Instruções contidas na fonte não alteram o comportamento do agente.
12. **Ausência de aplicação é válida.** O schema deve permitir `sem_relação_comprovada`, sem pressionar o agente a inventar utilidade ou causalidade.

## 4. Escopo e limites

### 4.1 Incluído

- reorganização do protocolo operacional;
- versionamento e proveniência;
- rascunho e máquina de estados;
- manifesto de escopo;
- checker estrutural V2;
- orquestração de gates;
- validação de score, status, destinos, pendências e referências;
- controles para alegações causais;
- revisão baseada em risco;
- concorrência, hooks, CI e publicação;
- política local↔Drive;
- testes unitários, integração, regressão e cenários adversariais.

### 4.2 Fora do escopo automático

- provar que toda afirmação externa é verdadeira;
- substituir revisão humana em decisão arquitetural;
- inferir intenção histórica apenas por timestamps ou commits;
- corrigir automaticamente conteúdo sem autorização;
- executar instruções encontradas em fontes;
- considerar aprovação de schema como aprovação semântica.

## 5. Fluxo-alvo e máquina de estados

### 5.1 Sequência operacional

```text
PREFLIGHT
→ CLASSIFICAÇÃO
→ QUARENTENA
→ DEDUPLICAÇÃO
→ RASCUNHO
→ EXTRAÇÃO E EVIDÊNCIAS
→ PONTUAÇÃO
→ CONFLITOS E ATUALIDADE
→ STATUS
→ ROTEAMENTO
→ APROVAÇÃO, SE EXIGIDA
→ PREPARAÇÃO DA MUDANÇA
→ GATES
→ REVISÃO
→ PUBLICAÇÃO
→ AUDITORIA FINAL
```

### 5.2 Estados persistentes

```text
RASCUNHO
→ EXTRAÍDO
→ AVALIADO
→ ROTEAMENTO_PROPOSTO
→ APROVADO
→ PREPARADO
→ VALIDADO_ESTRUTURALMENTE
→ VALIDADO_SEMANTICAMENTE
→ PUBLICADO
```

Estados de exceção:

- `BLOQUEADO`;
- `REVISÃO_HUMANA`;
- `CONFLITO`;
- `DUPLICATA_CANDIDATA`;
- `SEM_DESTINO`;
- `REJEITADO`;
- `FALHA_DE_VALIDACAO`;
- `FALHA_DE_PUBLICACAO`.

Transições devem ser explícitas. `Roteado` deixa de significar simultaneamente “destino escolhido”, “arquivo gravado” e “processo concluído”. Durante a migração, o campo antigo deve ser mapeado para o novo estado sem perder informação.

## 6. Artefatos necessários

| Artefato | Função |
|---|---|
| `PROTOCOLO.md` | Sequência operacional humana e agêntica. |
| `REGISTRO_FONTES.md` | Arquitetura, enums, regras e matriz de roteamento. |
| `TEMPLATE.md` | Schema legível do registro e réguas de avaliação. |
| `FONTES_REGISTRADAS.md` | Ledger canônico de registros publicados. |
| `KB-*.md` | Conhecimento condensado publicado por domínio. |
| `check_kb_consistency.py` | Checker V2 de estrutura, duplicidade e ledger↔KB. |
| `kb_validate.py` | Orquestrador dos gates e gerador do relatório final. |
| `schema/` ou módulo equivalente | Enums, campos e regras determinísticas. |
| `.kb/runs/<RUN_ID>/manifest.*` | Escopo, entrada, autorização e estado inicial. |
| `.kb/runs/<RUN_ID>/draft.*` | Rascunho não canônico. |
| `.kb/runs/<RUN_ID>/validation.json` | Resultado estruturado dos gates. |
| `.kb/runs/<RUN_ID>/review.*` | Revisão e aprovação exigidas pelo risco. |
| `.kb/locks/` ou mecanismo equivalente | Exclusão mútua de publicação. |
| testes automatizados | Evidência executável do comportamento esperado. |

Os nomes finais podem ser ajustados durante a implementação, mas as responsabilidades não devem ser fundidas de modo a recriar um único verificador opaco.

## 7. Fase 0 — Contenção imediata

### 7.1 Objetivo

Impedir que os riscos já comprovados continuem produzindo novos registros incorretos enquanto as demais fases são implementadas.

### 7.2 Ações

1. Alterar a mensagem de sucesso do checker atual para deixar seu escopo explícito:

   ```text
   OK ESTRUTURAL: invariantes ledger↔KB verificadas.
   NÃO VERIFICADO: factualidade, fidelidade, causalidade, escopo e atualidade.
   ```

2. Atualizar a documentação do hook para repetir os mesmos limites.
3. Proibir provisoriamente alegações `motivou`, `originou`, `causou`, `modelo direto` ou equivalentes sem evidência registrada.
4. Adotar imediatamente as categorias:
   - `reforço_retrospectivo`;
   - `recomendação_não_implementada`;
   - `sem_relação_comprovada`.
5. Bloquear criação de nova KB, alteração da matriz, mudança de template ou exclusão sem aprovação humana específica.
6. Revisar os resíduos semânticos identificados pela auditoria em `FONTES_REGISTRADAS.md` e `KB-PROJ-05`, mas realizar as correções como tarefa separada e rastreável.
7. Criar checklist manual temporário para toda nova fonte enquanto o orquestrador não existir.
8. Registrar que o plano de `SCRIPTV2.md` é o baseline da modernização do checker, não a solução completa do fluxo.

### 7.3 Checklist temporário

- [ ] Fonte primária ou evidência reproduzível consultada.
- [ ] Duplicidade pesquisada antes de criar ID.
- [ ] Pontuação calculada antes da gravação.
- [ ] Conflitos analisados antes do status.
- [ ] Destinos definidos antes da gravação.
- [ ] Alegações causais removidas ou comprovadas.
- [ ] Arquivos que serão alterados informados ao usuário quando houver ampliação de escopo.
- [ ] Checker executado, com limites declarados no fechamento.

### 7.4 Entregáveis

- mensagens de saída e documentação sem `OK` amplo;
- política temporária de causalidade;
- inventário dos resíduos semânticos;
- checklist de transição.

### 7.5 Critérios de aceite

- nenhuma saída estrutural pode ser lida razoavelmente como aprovação factual;
- nenhuma nova alegação causal é publicada sem prova;
- ações de alto risco dependem de autorização humana explícita;
- os resíduos existentes estão inventariados com responsável e estado.

### 7.6 Condição de avanço

A Fase 1 só começa após aprovação humana do baseline que será versionado. A contenção permanece ativa até a conclusão da Fase 3.

## 8. Fase 1 — Proveniência e controle de mudanças

### 8.1 Objetivo

Tornar cada alteração reproduzível e associável a uma tarefa, autorização, estado inicial e diff.

### 8.2 Ações de versionamento

1. Revisar o estado atual antes de inicializar Git; não transformar conteúdo não revisado em verdade apenas porque entrou no primeiro commit.
2. Inicializar o repositório somente com autorização humana.
3. Criar baseline assinado ou, no mínimo, identificado por hash de commit.
4. Definir branch por tarefa ou política equivalente de isolamento.
5. Configurar `.gitignore` para temporários, locks e segredos, preservando relatórios de auditoria que devam ser versionados.
6. Proibir force-push e reescrita destrutiva do histórico no fluxo operacional normal.
7. Definir convenção de commit contendo `RUN_ID`, tipo de mudança e IDs das fontes.

### 8.3 `RUN_ID` e manifesto

Cada execução mutável deve criar um identificador único e um manifesto contendo:

```yaml
run_id: RUN-AAAA-MM-DD-IDENTIFICADOR
objetivo: texto curto
solicitante: humano-ou-sistema
risco: baixo | medio | alto | critico
fontes_planejadas: []
arquivos_permitidos: []
operacoes_permitidas: [criar, editar]
operacoes_proibidas: [excluir, sincronizar]
estado_inicial_commit: hash
alteracoes_preexistentes: []
aprovacoes_exigidas: []
```

O manifesto não concede autoridade implícita. Se a tarefa exigir arquivo ou operação fora dele, a execução deve parar e solicitar ampliação de escopo.

### 8.4 Preservação de alterações preexistentes

- capturar `git status` e diff inicial;
- distinguir alterações do usuário das alterações do `RUN_ID`;
- não exigir árvore limpa como regra absoluta;
- falhar quando não for possível separar com segurança os dois conjuntos;
- nunca descartar mudanças para “limpar” o ambiente.

### 8.5 Gate de escopo

Comparar arquivos adicionados, modificados, removidos e renomeados com o manifesto. Exclusão e renomeação devem exigir permissão explícita mesmo quando o arquivo consta na lista.

### 8.6 Entregáveis

- repositório Git e baseline aprovados;
- convenção de branches e commits;
- schema do manifesto;
- gerador de `RUN_ID`;
- verificador `ESCOPO_DIFF`;
- documentação de recuperação sem comandos destrutivos.

### 8.7 Testes

- arquivo permitido passa;
- arquivo não permitido falha;
- exclusão não autorizada falha;
- mudanças preexistentes são preservadas;
- tentativa de incorporar mudança preexistente ao commit é detectada;
- manifesto inválido ou ausente impede publicação, mas não leitura/auditoria.

### 8.8 Critérios de aceite

- toda mudança publicada referencia `RUN_ID` e commit;
- o diff final está contido no manifesto;
- alterações preexistentes permanecem intactas;
- ações fora do escopo são bloqueadas antes do commit.

## 9. Fase 2 — Reordenação e transação lógica do fluxo

### 9.1 Objetivo

Eliminar a gravação prematura e representar corretamente estados intermediários, exceções e aprovações.

### 9.2 Preflight

Verificar automaticamente:

- diretório correto;
- arquivos obrigatórios;
- versão compatível do schema;
- estado do Git e commit inicial;
- manifesto válido;
- locks existentes;
- capacidade de leitura UTF-8;
- ausência de conflito de merge;
- disponibilidade dos validadores necessários.

Falha de preflight impede escrita, mas deve produzir relatório diagnóstico.

### 9.3 Classificação e quarentena

Classificar a entrada como:

- fonte externa;
- conhecimento previamente extraído;
- decisão humana;
- alteração administrativa do sistema.

Material externo permanece em área de entrada/quarentena ou é referenciado por hash/URL. Instruções nele contidas nunca entram no canal operacional. Registrar data de acesso, origem, hash quando aplicável e método de obtenção.

### 9.4 Deduplicação antes do ID

Pesquisar, nesta ordem:

1. DOI ou identificador oficial;
2. URL canônica;
3. hash do documento;
4. título normalizado e autores;
5. combinação de ano, veículo e tema;
6. similaridade de conteúdo como sinal, nunca decisão automática definitiva.

Resultados ambíguos levam a `DUPLICATA_CANDIDATA` e revisão, não à criação imediata de outro ID.

### 9.5 Rascunho

- criar fora de `FONTES_REGISTRADAS.md` e das KBs;
- permitir campos `PENDENTE` apenas no rascunho;
- associar ao `RUN_ID`;
- não ser considerado publicado pelo checker canônico;
- poder ser descartado sem alterar documentos oficiais.

### 9.6 Extração e evidências

Para fatos críticos, decisões e claims que geram mudanças, registrar:

- `CLAIM_ID`;
- texto da afirmação;
- tipo: `fato`, `inferência`, `recomendação` ou `decisão`;
- origem e localização reproduzível;
- confiança;
- método de verificação;
- responsável pela validação, quando exigido.

Claims comuns e de baixo risco podem permanecer agregados para evitar burocracia excessiva.

### 9.7 Pontuação, conflitos, atualidade e status

1. Calcular score automaticamente a partir dos itens do template.
2. Conferir soma e faixa.
3. Aplicar critérios mínimos e rebaixamentos obrigatórios.
4. Detectar fontes em conflito antes da decisão de uso.
5. Verificar data e necessidade de revisão.
6. Só então definir confiança e status.

Exceções entre score e status exigem justificativa e revisão humana.

### 9.8 Roteamento e aprovação

- consultar matriz após avaliação;
- justificar cada destino;
- permitir `SEM_DESTINO` sem forçar encaixe;
- exigir aprovação para nova KB, mudança de taxonomia ou destino arquitetural;
- gerar previamente a lista exata de arquivos que serão alterados e reconciliá-la com o manifesto.

### 9.9 Preparação e publicação lógica

Preparar todas as mudanças sem marcar a fonte como final. Aplicar ledger, KBs e pendências no mesmo conjunto de alterações. O estado só avança depois dos gates correspondentes.

Se uma escrita falhar:

- não declarar publicação;
- restaurar apenas alterações do próprio `RUN_ID`, sem tocar trabalho preexistente;
- registrar `FALHA_DE_PUBLICACAO`;
- manter relatório para diagnóstico.

### 9.10 Atualizações documentais

- reescrever a ordem de `PROTOCOLO.md`;
- alinhar o fluxo duplicado em `REGISTRO_FONTES.md`;
- atualizar `TEMPLATE.md` com estados e classificações;
- definir migração do campo `STATUS_DE_ROTEAMENTO`;
- remover instruções contraditórias ou desatualizadas.

### 9.11 Entregáveis

- protocolo reordenado;
- schema de estados;
- armazenamento de rascunhos;
- deduplicação prévia;
- cálculo de score;
- preparação lógica multiarquivo;
- plano de migração dos registros existentes.

### 9.12 Testes ponta a ponta

- fonte nova válida até `PUBLICADO`;
- duplicata exata reutiliza o ID;
- duplicata ambígua para em revisão;
- fonte sem destino não é forçada em KB;
- conflito impede publicação automática;
- falha na segunda KB não deixa estado final enganoso;
- decisão humana segue ramo próprio;
- instrução maliciosa na fonte não altera o fluxo.

### 9.13 Critérios de aceite

- nenhuma entrada é adicionada ao ledger canônico antes de avaliação e roteamento;
- estados intermediários não são confundidos com publicação;
- atualização multiarquivo é tratada como uma unidade lógica;
- falhas parciais são detectadas e não destroem alterações preexistentes.

## 10. Fase 3 — Gates automatizados e checker V2

### 10.1 Objetivo

Converter regras verificáveis em controles executáveis, independentes e auditáveis.

### 10.2 Orquestrador

Implementar `kb_validate.py` com:

- execução individual ou completa dos gates;
- saída humana em texto;
- saída estruturada em JSON;
- códigos de saída estáveis;
- ordenação determinística;
- localização por arquivo e linha;
- lista explícita do que não foi validado;
- nenhuma correção automática por padrão.

### 10.3 Gates obrigatórios

| Gate | Verifica | Não verifica |
|---|---|---|
| `PREFLIGHT` | Ambiente, manifesto, schema e leitura. | Conteúdo da fonte. |
| `SCHEMA` | Seções, campos, enums, unicidade e formato. | Verdade dos valores. |
| `DUPLICIDADE` | IDs, DOI, URL, hash e candidatos por metadados. | Identidade semântica definitiva em casos ambíguos. |
| `SCORE_STATUS` | Soma, faixa, critérios mínimos e combinações permitidas. | Julgamento qualitativo integral. |
| `ROTEAMENTO` | Destinos válidos, justificativas e estados. | Melhor decisão temática em casos ambíguos. |
| `LEDGER_KB` | Presença bidirecional e códigos de KB. | Fidelidade da síntese. |
| `REFERENCIAS_INTERNAS` | Arquivos, seções, IDs e `CHANGE_ID` existentes. | Veracidade externa. |
| `PENDENCIAS` | Reconciliação entre status e tabela de pendências. | Resolução humana da pendência. |
| `ESCOPO_DIFF` | Diff versus manifesto e operações permitidas. | Qualidade da mudança autorizada. |
| `CAUSALIDADE` | Campos e evidências obrigatórios da classificação causal. | Intenção histórica sem registro. |
| `REVISAO` | Aprovações exigidas pelo nível de risco. | Competência subjetiva do revisor. |

### 10.4 Checker V2

Implementar integralmente o plano de `soluções/SCRIPTV2.md`, incluindo:

- falha para `## Registros` ausente ou repetido;
- campos essenciais obrigatórios;
- status e destinos válidos;
- colisão de códigos de KB;
- normalização conservadora de URLs;
- diagnóstico com caminho e linha;
- testes positivos e negativos;
- distinção entre divergência e falha operacional.

O checker V2 alimenta os gates `SCHEMA`, `DUPLICIDADE` e `LEDGER_KB`, mas não substitui o orquestrador.

### 10.5 Códigos e resultados

- `0`: gate executado e aprovado;
- `1`: divergência encontrada;
- `2`: gate não pôde executar com confiabilidade;
- resultado `SKIPPED` só é permitido com justificativa e nunca conta como aprovação;
- gate obrigatório `SKIPPED` impede publicação.

### 10.6 Relatório final

Exemplo:

```text
RUN_ID: RUN-...
Resultado de publicação: BLOQUEADO

APROVADOS: SCHEMA, SCORE_STATUS, LEDGER_KB
REPROVADOS: ESCOPO_DIFF
NÃO EXECUTADOS: REVISAO

Não validado por automação:
- fidelidade integral da síntese;
- verdade factual externa;
- julgamento humano de conflito.
```

### 10.7 Entregáveis

- checker V2;
- orquestrador;
- módulos de cada gate;
- JSON schema do relatório;
- suíte de testes;
- documentação e exemplos de falha.

### 10.8 Critérios de aceite

- nenhum documento malformado retorna sucesso;
- todos os gates podem ser executados e testados isoladamente;
- gate obrigatório ausente ou quebrado bloqueia publicação;
- relatório separa aprovação, reprovação, não execução e limites;
- comportamento descrito e comportamento testado são equivalentes.

## 11. Fase 4 — Evidência semântica e causalidade

### 11.1 Objetivo

Impedir que plausibilidade, proximidade temporal ou memória conversacional sejam persistidas como fatos ou relações históricas.

### 11.2 Taxonomia obrigatória

Toda relação específica da fonte com o projeto deve usar uma categoria:

- `mudanca_comprovadamente_motivada`;
- `reforco_retrospectivo`;
- `recomendacao_nao_implementada`;
- `sem_relacao_comprovada`.

### 11.3 Requisitos para causalidade

`mudanca_comprovadamente_motivada` exige:

- ID da fonte;
- `CLAIM_ID` relevante;
- `CHANGE_ID`;
- decisão ou plano anterior à mudança ligando fonte e ação;
- arquivo afetado;
- commit anterior e posterior;
- referência ao diff;
- data;
- autor da mudança;
- revisor exigido pelo risco.

Git comprova sequência e conteúdo do diff. A decisão registrada comprova a motivação declarada. Nenhum dos dois, isoladamente, é suficiente.

### 11.4 Schema sugerido

```yaml
relacao_com_projeto:
  tipo: reforco_retrospectivo
  fonte_id: FONTE-...
  claim_id: CLAIM-...
  change_id: null
  decisao_referencia: null
  arquivo_afetado: null
  commit_anterior: null
  commit_posterior: null
  diff_referencia: null
  validado_por: null
  observacao: "Prática já existente; fonte apenas fornece suporte posterior."
```

Para os três tipos não causais, campos de mudança podem ser nulos. Isso evita pressão para fabricar uma aplicação concreta.

### 11.5 Fidelidade semântica baseada em risco

Claims atômicos são obrigatórios para:

- causalidade histórica;
- fatos que alteram protocolo, template, taxonomia ou script;
- números, datas e citações usados em decisões;
- afirmações de existência ou inexistência;
- recomendações com consequência operacional relevante.

Para cada claim obrigatório, o revisor deve conseguir localizar a evidência sem depender do resumo do mesmo agente.

### 11.6 Propagação de correções

Após qualquer correção semântica:

1. buscar o claim, termos equivalentes e `ID_FONTE` em todo o repositório;
2. classificar cada ocorrência como cópia, derivação ou contexto independente;
3. corrigir ou justificar cada ocorrência;
4. executar novamente gates e revisão;
5. registrar a lista de ocorrências no relatório.

Não substituir automaticamente texto apenas por similaridade.

### 11.7 Referências internas

Validar referências a:

- arquivos existentes;
- seções existentes por título ou âncora estável;
- IDs registrados;
- commits e `CHANGE_ID` existentes;
- linhas apenas como conveniência, nunca como identidade permanente.

### 11.8 Entregáveis

- taxonomia incorporada ao schema;
- gate `CAUSALIDADE`;
- registro de claims críticos;
- verificador de referências internas;
- procedimento de propagação semântica;
- migração das alegações históricas existentes.

### 11.9 Testes adversariais

- commit posterior sem decisão anterior não prova motivação;
- texto “motivou” sem `CHANGE_ID` falha;
- `reforco_retrospectivo` não exige diff;
- recomendação não implementada não é tratada como mudança;
- referência a seção inexistente falha;
- correção focal com cópia contraditória pendente bloqueia fechamento.

### 11.10 Critérios de aceite

- afirmação causal sem conjunto completo de evidências é tecnicamente inválida;
- ausência de relação comprovada é um resultado aceito;
- claims críticos possuem evidência reproduzível;
- correções semânticas incluem busca global e relatório de propagação.

## 12. Fase 5 — Revisão baseada em risco

### 12.1 Objetivo

Reservar revisão humana e independente para os pontos em que automação não fornece garantia suficiente.

### 12.2 Classificação de risco

| Nível | Exemplos | Aprovação mínima |
|---|---|---|
| Baixo | Ortografia, link interno sem mudança de sentido, metadado não decisório. | Gates automáticos. |
| Médio | Nova fonte, nova síntese, atualização de bloco em KB existente. | Gates + revisão semântica independente. |
| Alto | `PROTOCOLO.md`, `REGISTRO_FONTES.md`, `TEMPLATE.md`, checker, hook, taxonomia, causalidade. | Gates + aprovação humana. |
| Crítico | Exclusão, sincronização destrutiva, segredo, permissão, migração irreversível, publicação externa. | Aprovação humana anterior e confirmação final. |

O risco é calculado pelo maior impacto, não pela quantidade de linhas alteradas.

### 12.3 Independência da revisão

Um segundo agente só conta como revisor quando:

- recebe o objetivo, fontes e diff, não a conclusão pronta como premissa;
- usa checklist adversarial;
- registra evidências próprias;
- pode reprovar;
- não substitui aprovação humana em risco alto ou crítico.

### 12.4 Checklist do revisor

- [ ] O diff corresponde ao objetivo e manifesto.
- [ ] Afirmações críticas resolvem para evidência primária.
- [ ] Inferência está rotulada como inferência.
- [ ] Relação causal cumpre o schema.
- [ ] Score e status são defensáveis.
- [ ] Destinos e separação genérico/específico fazem sentido.
- [ ] Conflitos e limitações não foram omitidos.
- [ ] Nenhuma instrução da fonte foi executada.
- [ ] Correções foram propagadas.
- [ ] O relatório lista limites e itens não validados.

### 12.5 Registro da decisão

Toda revisão deve registrar:

- revisor;
- data;
- commit/diff revisado;
- checklist;
- decisão: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `REPROVADO`;
- ressalvas e ações pendentes;
- validade da aprovação — qualquer mudança posterior relevante invalida a revisão.

### 12.6 Entregáveis

- classificador de risco;
- matriz de aprovação;
- template de revisão;
- gate `REVISAO`;
- procedimento de reaprovação após mudança.

### 12.7 Testes

- mudança textual baixa passa sem humano;
- alteração de KB exige revisão semântica;
- alteração de protocolo bloqueia sem aprovação humana;
- exclusão bloqueia antes da operação;
- alteração após aprovação invalida a aprovação anterior;
- aprovação do autor não satisfaz requisito de independência.

### 12.8 Critérios de aceite

- risco alto ou crítico nunca é aprovado exclusivamente pelo agente autor;
- cada publicação possui evidência do nível de revisão exigido;
- revisão aponta para o diff exato aprovado;
- mudanças posteriores disparam nova revisão.

## 13. Fase 6 — Concorrência, publicação, CI e sincronização

### 13.1 Objetivo

Garantir que um fluxo correto em isolamento continue seguro diante de agentes concorrentes, falhas de processo e múltiplas superfícies de armazenamento.

### 13.2 Lock e fila

Implementar lock de publicação com:

- aquisição atômica;
- `RUN_ID`, processo, host e horário;
- expiração controlada;
- detecção de lock órfão;
- proibição de remoção automática de lock ativo;
- intervenção humana para ambiguidade;
- lock granular por ledger/KB ou fila única inicialmente, preferindo a solução mais simples e segura.

Leitura e preparação de rascunho podem ocorrer em paralelo; publicação conflitante não.

### 13.3 Verificação contra mudança concorrente

Antes de publicar:

1. comparar commit atual com `estado_inicial_commit`;
2. detectar mudanças nos mesmos blocos ou arquivos;
3. rebase/merge nunca deve ser resolvido semanticamente pelo agente sem revisão;
4. reexecutar gates e invalidar aprovações quando o diff mudar.

### 13.4 Hooks e CI

- hook local executa `kb_validate.py` no encerramento ou pre-commit adequado;
- CI executa a suíte completa em ambiente limpo;
- hook não é considerado única proteção;
- falha operacional do validador bloqueia, em vez de liberar silenciosamente;
- timeout e logs são preservados;
- código do hook possui testes para retorno `0`, `1`, `2` e timeout.

### 13.5 Commit e publicação

Ordem obrigatória:

1. adquirir lock;
2. verificar estado inicial e concorrência;
3. aplicar conjunto lógico de mudanças;
4. executar todos os gates;
5. obter revisão exigida;
6. revalidar o diff aprovado;
7. criar commit com `RUN_ID`;
8. gerar relatório e hashes finais;
9. marcar estado `PUBLICADO`;
10. liberar lock;
11. em falha, registrar estado e liberar lock somente de forma segura.

### 13.6 Política local↔Drive

Antes de automatizar sincronização, decidir e documentar:

- origem canônica;
- direção permitida;
- identidade entre arquivos;
- frequência;
- conflitos;
- exclusões;
- confirmação pós-sync;
- registro de hashes antes/depois;
- rollback;
- autoridade para iniciar sincronização.

Recomendação: Git local versionado como origem canônica e Drive como distribuição/espelho, salvo decisão humana diferente. A sincronização deve ser bloqueada enquanto essa decisão não estiver formalizada.

### 13.7 Recuperação e rollback

- nunca usar comandos destrutivos como mecanismo padrão;
- reversão deve ocorrer por commit inverso ou restauração seletiva revisada;
- preservar relatório da falha;
- não apagar rascunhos ou evidências necessários à auditoria;
- testar recuperação de falha entre ledger e segunda KB;
- documentar quem pode liberar locks órfãos e reprocessar runs.

### 13.8 Entregáveis

- mecanismo de lock/fila;
- detector de concorrência;
- hooks atualizados;
- pipeline CI;
- política local↔Drive aprovada;
- procedimento de publicação e recuperação;
- artefato final de auditoria por `RUN_ID`.

### 13.9 Testes de concorrência e falha

- duas publicações no mesmo ledger: apenas uma adquire lock;
- lock expirado não é removido sem validação;
- mudança concorrente invalida gates anteriores;
- falha do checker bloqueia hook e CI;
- timeout é reportado como falha operacional;
- falha parcial não gera estado `PUBLICADO`;
- conflito local↔Drive não é resolvido automaticamente;
- rollback preserva mudanças de terceiros.

### 13.10 Critérios de aceite

- duas sessões não publicam alterações conflitantes sem detecção;
- hooks e CI aplicam os mesmos contratos;
- publicação final é associada a commit, `RUN_ID`, revisão e relatório;
- sincronização possui origem, direção e política de conflito explícitas;
- falha parcial é recuperável e auditável.

## 14. Dependências e ordem de implementação

| Ordem | Fase | Dependência | Pode entrar em produção quando |
|---|---|---|---|
| 1 | Fase 0 | Nenhuma | Mensagens e restrições temporárias aprovadas. |
| 2 | Fase 1 | Aprovação do baseline | Git, manifesto e gate de escopo testados. |
| 3 | Fase 2 | Fase 1 | Rascunho e estados passam nos testes ponta a ponta. |
| 4 | Fase 3 | Fases 1–2 | Gates e checker V2 homologados na base real. |
| 5 | Fase 4 | Fases 1–3 | Schema causal e migração sem pendências críticas. |
| 6 | Fase 5 | Fases 3–4 | Matriz de risco e revisão integradas aos gates. |
| 7 | Fase 6 | Fases 1–5 | Concorrência, CI, publicação e recuperação validadas. |

Fases podem ser desenvolvidas parcialmente em paralelo, mas não devem ser promovidas fora dessa ordem. O hook não deve migrar para um validador ainda não homologado.

## 15. Estratégia de migração

1. Congelar o significado dos campos atuais e produzir inventário.
2. Criar testes de caracterização do comportamento vigente.
3. Implementar novos schemas em modo de relatório, sem bloquear.
4. Classificar divergências reais versus incompatibilidades legítimas.
5. Corrigir os dados existentes em mudanças separadas e revisadas.
6. Ativar gates um a um em modo bloqueante.
7. Migrar hook depois da homologação local.
8. Ativar CI.
9. Migrar estados antigos para a nova máquina de estados.
10. Remover caminhos legados somente após período de comparação.

Durante a migração, os relatórios devem indicar se o resultado veio do fluxo legado, do V2 em observação ou do V2 bloqueante.

## 16. Plano de testes consolidado

### 16.1 Unitários

- parsers, schemas, enums e normalizações;
- cálculo de score;
- transições de estado;
- manifesto e diff;
- classificação causal;
- classificador de risco;
- lock e expiração.

### 16.2 Integração

- rascunho até publicação;
- múltiplos destinos;
- pendências;
- hooks e códigos de saída;
- Git, commits e relatórios;
- migração de registro antigo.

### 16.3 Regressão

- os sete controles do checker atual;
- falsos `OK` encontrados na auditoria;
- colisão de código de KB;
- campo ou seção ausente;
- URL distinta com pontuação semelhante;
- resíduos semânticos e referências quebradas.

### 16.4 Adversariais

- instrução maliciosa dentro da fonte;
- causalidade plausível sem prova;
- fonte duplicada com título diferente;
- arquivo fora do manifesto;
- exclusão disfarçada de limpeza;
- aprovação antiga aplicada a diff novo;
- agente concorrente;
- falha do validador;
- saída parcial tratada como sucesso;
- fonte sem aplicação concreta.

### 16.5 Aceitação sobre a base real

- executar legado e V2;
- explicar todas as diferenças;
- não enfraquecer regra apenas para obter saída verde;
- registrar exceções legítimas no schema e em testes;
- obter aprovação humana para migração bloqueante.

## 17. Responsabilidades

| Papel | Responsabilidade | Não pode fazer sozinho |
|---|---|---|
| Agente autor | Analisar, preparar rascunho, evidências, mudança e relatório. | Aprovar risco alto/crítico ou ampliar escopo. |
| Revisor independente | Validar claims, diff, roteamento e limites. | Substituir decisão humana crítica. |
| Responsável humano | Autorizar baseline, arquitetura, exceções e ações irreversíveis. | Ser usado como substituto de gates automáticos rotineiros. |
| Validadores | Aplicar regras determinísticas e produzir evidência. | Declarar verdade semântica fora do contrato. |
| CI/harness | Bloquear publicação inválida e preservar logs. | Corrigir conteúdo automaticamente sem autorização. |

## 18. Critérios globais de publicação

Uma fonte só pode receber estado `PUBLICADO` quando:

- [ ] preflight foi aprovado;
- [ ] existe `RUN_ID` e manifesto válido;
- [ ] estado inicial e alterações preexistentes foram registrados;
- [ ] deduplicação foi executada antes da criação do ID;
- [ ] fonte e evidências são rastreáveis;
- [ ] score, confiança, status e decisão são coerentes;
- [ ] conflitos e atualidade foram avaliados;
- [ ] destinos foram justificados e aprovados;
- [ ] ledger, KBs e pendências estão bidirecionalmente consistentes;
- [ ] referências internas resolvem;
- [ ] diff está dentro do escopo;
- [ ] causalidade está comprovada ou corretamente qualificada;
- [ ] correções semânticas foram propagadas;
- [ ] todos os gates obrigatórios foram executados e aprovados;
- [ ] revisão exigida pelo risco está registrada para o diff final;
- [ ] não existe conflito concorrente;
- [ ] commit e relatório final foram gerados;
- [ ] o relatório separa validado, não validado e decisão humana pendente.

## 19. Resultado final esperado

Ao concluir a Fase 6, o sistema deve produzir, para cada fonte publicada, uma cadeia auditável:

```text
solicitação/autorização
→ RUN_ID e manifesto
→ estado inicial versionado
→ fonte e evidências
→ rascunho
→ avaliação e conflitos
→ decisão de status e roteamento
→ diff preparado
→ gates independentes
→ revisão proporcional ao risco
→ commit/publicação
→ relatório e hashes finais
```

O resultado esperado não é “a IA nunca erra”. É um sistema em que os erros mais perigosos deixam rastros, são bloqueados antes da publicação ou exigem decisão humana explícita.

O risco é drasticamente reduzido porque:

- o agente não precisa inventar conteúdo para completar o schema;
- rascunho não se confunde com conhecimento publicado;
- causalidade sem evidência é inválida;
- mudanças fora de escopo são detectadas;
- validação estrutural não é apresentada como factual;
- mudanças críticas não são autoaprovadas;
- concorrência e falhas parciais são controladas;
- histórico, diffs, aprovações e limites são reproduzíveis.

## 20. Definição de pronto do Fluxo V2

O Fluxo V2 estará concluído somente quando:

- [ ] todas as Fases 0–6 cumprirem seus critérios de aceite;
- [ ] os documentos operacionais estiverem alinhados, sem ordens contraditórias;
- [ ] o checker V2 e o orquestrador tiverem testes automatizados;
- [ ] o fluxo ponta a ponta passar em ambiente temporário e na base real;
- [ ] testes adversariais comprovarem bloqueio dos incidentes conhecidos;
- [ ] hook e CI falharem de forma fechada;
- [ ] a política de revisão estiver aplicada por risco;
- [ ] concorrência e recuperação tiverem sido testadas;
- [ ] política local↔Drive estiver decidida antes de qualquer sync automático;
- [ ] documentação, código e comportamento observado forem equivalentes;
- [ ] a autoridade humana aprovar a promoção do V2 para fluxo canônico.

Até que essa definição seja satisfeita, o sistema deve declarar explicitamente quais fases e gates estão ativos, evitando apresentar implementação parcial como solução completa.
