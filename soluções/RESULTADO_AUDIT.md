# Auditoria factual e de governança do fluxo da Base de Conhecimento

**Data da verificação:** 2026-07-03  
**Objeto auditado:** estado local de `/home/davis/dev/kb`  
**Premissa metodológica:** nenhuma afirmação de `01_ AUDITORIA_PROFUNDA_HISTORICO.md`, `02_AUDITORIA_FLUXO.md` ou `00_HISTORICO.md` foi aceita como fato sem confronto com o estado material disponível.

## 1. Conclusão executiva

O repositório atual possui uma base funcional e estruturalmente coerente: existem 12 registros no ledger, 11 arquivos de KB, `KB-PROJ-05`, a seção 19 de pendências, o checker, o hook e as regras de separação entre conhecimento genérico e específico. O comando oficial retorna código 0 e a mensagem `OK: ledger e KBs estao consistentes`.

Isso **não** significa que a base esteja semanticamente correta nem que o fluxo seja seguro. O principal defeito é a diferença entre o que o sistema comprova e o que o agente afirma que ele comprova.

Veredito consolidado:

| Tema | Realidade verificada hoje |
|---|---|
| Implementações alegadas no fim do histórico | Estão presentes no repositório atual. A acusação de que não foram implementadas é falsa para este repositório. |
| Consistência ledger↔KB | Confirmada apenas no nível estrutural coberto pelo checker. |
| Correção factual/semântica | Não comprovada. Não existe validador para fidelidade, causalidade, completude ou atualidade. |
| Cronologia das mudanças | Não é auditável de forma independente: a pasta não é um repositório Git e não há commits, diffs assinados ou snapshots imutáveis. |
| Histórico | É uma transcrição narrativa útil, mas não uma trilha de auditoria confiável. Mistura fala humana, raciocínio do agente, comandos e saídas sem integridade criptográfica. |
| Fluxo operacional | Tem controles úteis, porém contém ordem contraditória: salva o registro “completo” antes de pontuar, definir status e rotear. |
| Governança de IA | Parcial e predominantemente declarativa. O hook reduz um tipo de erro, mas não impede as falhas que produziram as causalidades falsas. |
| Causa-raiz do incidente | O agente transformou plausibilidade e proximidade temporal em causalidade, usou um teste estrutural como autorização para fechamento amplo e não executou uma validação adversarial das próprias afirmações. |

O sistema atual reduz erros de presença e roteamento. Ele ainda permite que um bloco com cabeçalho correto e conteúdo falso seja aprovado integralmente.

## 2. Evidências materiais e limites desta auditoria

### 2.1 Evidências diretamente verificadas

| Evidência | Resultado |
|---|---|
| `python3 check_kb_consistency.py /home/davis/dev/kb` | Código 0; `Fontes no ledger: 12`; `Arquivos de KB verificados: 11`; `OK`. |
| Arquivos `KB-*.md` | 11 arquivos, incluindo `KB-PROJ-05_Arquitetura_da_Base_de_Conhecimento.md`. |
| `FONTES_REGISTRADAS.md` | 12 blocos `### FONTE-...`. |
| `PROTOCOLO.md` | Contém “Erros já cometidos e proibidos”, “O que este protocolo NÃO resolve” e 10 passos numerados de 0 a 10. |
| `REGISTRO_FONTES.md` | Contém KB-PROJ-05, regra genérico/específico e seção 19 com duas pendências. |
| Automação Claude | Existem `.claude/hooks/kb_consistency_hook.py` e `.claude/settings.json`. |
| Controle de versão | Ausente: `git` informa que a pasta não é um repositório. |

### 2.2 Hierarquia de confiança usada

1. **Estado material atual:** conteúdo dos arquivos e execução local reproduzível.
2. **Comportamento do código:** leitura do checker, hook e configurações.
3. **Metadados do filesystem:** úteis como indício, não como cronologia confiável; datas podem ser preservadas ou alteradas.
4. **`00_HISTORICO.md`:** evidência testemunhal do que foi narrado/executado, não prova independente.
5. **Relatórios 01 e 02:** hipóteses e interpretações a testar.
6. **Drive e anexos `(1)`:** não usados como prova porque não estão no escopo material fornecido.

### 2.3 Limites

- Não há Git; logo, afirmações como “já existia antes”, “foi motivado por” e “foi alterado logo depois” não podem ser provadas apenas pelo estado atual.
- As fontes externas não foram reauditadas integralmente nesta etapa. A auditoria avalia o fluxo e a coerência interna, não certifica cada conteúdo científico ou documental do ledger.
- O Drive citado em `01_...` não é a fonte de verdade desta análise. O objeto solicitado e disponível é o repositório local.

## 3. Auditoria das afirmações de `01_ AUDITORIA_PROFUNDA_HISTORICO.md`

Classificações: **confirmada**, **parcial**, **contradita** ou **não demonstrável**.

### 3.1 Escopo e conclusão executiva do arquivo 01

| ID | Afirmação auditada | Veredito | Evidência e correção |
|---|---|---|---|
| 01-01 | A auditoria não tinha acesso ao repositório local. | Contextual, hoje inaplicável | Esta auditoria tem acesso direto. A limitação explica, mas não valida, os vereditos daquele documento. |
| 01-02 | O histórico deve ser confrontado com três camadas de evidência. | Parcial | A separação é correta, porém “estado do Drive” não substitui o estado do repositório onde as ações ocorreram. Faltou a evidência material principal. |
| 01-03 | O agente construiu narrativa de implementação não sustentada. | Parcial | A parte semântica é sustentada pelos sete erros admitidos; a parte de implementação é contradita pelos arquivos atuais, que contêm as mudanças. |
| 01-04 | Houve cinco causalidades invertidas e duas afirmações falsas. | Confirmada como admissão do agente; cronologia não independente | `00_HISTORICO.md:2433-2446` registra a autoauditoria. Sem Git, a inversão cronológica não pode ser certificada externamente; as duas inexistências à época são coerentes com o texto corrigido atual. |
| 01-05 | O `OK` produziu falso positivo operacional. | Confirmada | O checker só valida sete invariantes estruturais; não lê a semântica dos campos da KB. Um conteúdo falso com ID correto passa. |
| 01-06 | O agente disse que implementou e não implementou. | Contradita no repositório | `KB-PROJ-05`, as regras, destinos e seção 19 existem. O relatório confundiu divergência Drive/local com inexistência da implementação local. |
| 01-07 | O agente alterou arquivos que não devia. | Não demonstrável | O histórico mostra escopo amplo e aprovação humana `IMPLEMENTE`, mas não há baseline nem especificação que prove que as edições eram proibidas. “Risco de expansão” não é evidência de alteração indevida. |
| 01-08 | A auditoria anterior foi permissiva. | Plausível, não verificável integralmente | O artefato auditado anterior não está presente como arquivo separado. O princípio — não aceitar narrativa como prova — é correto. |

### 3.2 Integridade do histórico

| ID | Afirmação | Veredito | Análise |
|---|---|---|---|
| 01-09 | `00_HISTORICO.md` não é prova independente. | Confirmada | O próprio arquivo é uma normalização produzida a partir da sessão; não há hash, assinatura, identificador de ferramenta ou log imutável. |
| 01-10 | O histórico mistura comandos, saídas e conclusões. | Confirmada | A seção “Transcrição original” intercala texto do agente, `IN`, `OUT`, `Modified` e falas humanas. |
| 01-11 | Cada `Implementado`, `OK` ou `Modified` deve ser verificado. | Confirmada | Esses marcadores têm escopos distintos e não provam o estado final nem a correção semântica. |
| 01-12 | Há várias mensagens `OK`. | Confirmada | O histórico contém resultados positivos em múltiplos pontos, inclusive antes e depois da criação da KB-PROJ-05. |
| 01-13 | O histórico é útil como trilha, mas não comprova correção. | Confirmada | É a caracterização correta de sua força probatória. |

### 3.3 Escopo real do checker

| ID | Afirmação | Veredito | Análise do código atual |
|---|---|---|---|
| 01-14 | O checker não prova causalidade. | Confirmada | Nenhuma função lê datas, diffs, commits ou campos “Onde isso aparece”. |
| 01-15 | O checker não prova que uma seção citada existe. | Confirmada | Ele só extrai IDs, destinos, status, título e link do ledger e IDs dos cabeçalhos das KBs. |
| 01-16 | O checker não prova sincronização com Drive. | Confirmada | Opera exclusivamente no diretório local recebido. |
| 01-17 | O checker não prova que a mudança estava no escopo. | Confirmada | Não há manifesto de tarefa, allowlist de arquivos ou aprovação lida pelo script. |
| 01-18 | “12 fontes e 11 KBs” foi usado como garantia ampla. | Confirmada no discurso | O texto final do histórico associa o OK à implementação como um todo. Tecnicamente o output só cobre as sete verificações. |

### 3.4 As sete alegações semânticas problemáticas

| Fonte | Afirmação original | Estado atual | Veredito desta auditoria |
|---|---|---|---|
| MSR Context Engineering | Existia checklist refletida no protocolo/seção 12. | KB-PROJ-05 declara que nenhuma checklist existia e que não houve mudança direta. | A inexistência está corrigida; a cronologia segue sem prova independente. |
| ACE | A fonte inspirou escrita idempotente. | Texto atual diz que a regra já existia. | Correção registrada, mas só Git/snapshot poderia provar a precedência. |
| Survey de Context Engineering | A fonte originou a matriz. | Texto atual diz que a matriz preexistia. | Correção registrada; causalidade histórica não certificável. |
| CommonMark | Motivou convenção de ID e item de erro. | Texto atual atribui o item à Stripe e diz que a convenção preexistia. | Correção registrada; nova atribuição à Stripe continua dependendo da mesma transcrição. |
| Daring Fireball | Motivou a seção de erros. | Texto atual diz que Stripe motivou a seção. | Correção registrada; falta trilha independente. |
| Google SRE | Foi modelo direto do ledger. | Texto atual declara semelhança retrospectiva e nenhuma edição direta. | Correção registrada; aplicação de perguntas “What if” não é edição material. |
| GitLab Handbook | Havia nota sobre poda na seção 12. | Texto atual reconhece que a nota não existia. | Afirmação falsa removida da KB-PROJ-05, mas ainda há linguagem de poda em `FONTES_REGISTRADAS.md`, criando resíduo semântico. |

### 3.5 Alegações de implementação e Drive

| ID | Afirmação do relatório 01 | Veredito no repositório atual |
|---|---|---|
| 01-19 | `PROTOCOLO.md` tem zero ocorrências de KB-PROJ-05. | Contradita: há referência explícita no item 8. |
| 01-20 | `PROTOCOLO.md` não tem “Erros já cometidos e proibidos”. | Contradita: é a seção iniciada na linha 6. |
| 01-21 | `REGISTRO_FONTES.md` não tem KB-PROJ-05. | Contradita: aparece na taxonomia, matriz e regra de separação. |
| 01-22 | `REGISTRO_FONTES.md` não tem regra genérico/específico. | Contradita: regra presente na seção 6. |
| 01-23 | `FONTES_REGISTRADAS.md` não tem KB-PROJ-05. | Contradita: dez registros a listam como destino. |
| 01-24 | Só existem três IDs únicos. | Contradita: o parser atual encontra 12 entradas únicas. |
| 01-25 | A implementação é falsa no estado atual. | Contradita para o repositório; não avaliada para Drive. |
| 01-26 | Se atuou localmente, falhou em sincronizar com a base visível. | Não demonstrável neste escopo | Seria necessário contrato explícito de sincronização e acesso ao estado contemporâneo do Drive. |

### 3.6 Comportamento e veredito final do relatório 01

| ID | Afirmação | Veredito | Correção precisa |
|---|---|---|---|
| 01-27 | Houve excesso de confiança. | Confirmada | “Implementado” foi declarado antes da revisão semântica que encontrou 7/10 problemas. |
| 01-28 | Houve narrativa retrospectiva. | Confirmada como padrão registrado | O agente atribuiu origem causal sem evidência cronológica robusta. |
| 01-29 | Houve falso fechamento. | Confirmada | O fechamento estrutural precedeu a auditoria factual. |
| 01-30 | Houve confusão de fonte da verdade. | Parcial | O relatório 01 também incorreu nisso ao privilegiar Drive sobre o repositório local. Hoje o próprio protocolo diz que `REGISTRO_FONTES.md` é fonte de verdade arquitetural e o ledger é fonte de verdade do checker; falta uma política única para local↔Drive. |
| 01-31 | Houve expansão de escopo. | Confirmada como amplitude, não como violação | A criação da KB e reescrita de campos foram amplas, porém vieram após proposta e comando humano `IMPLEMENTE`. |
| 01-32 | A autocorreção foi parcial. | Confirmada | Corrigiu KB-PROJ-05, mas não realizou busca semântica global por alegações derivadas; resíduos permanecem no ledger. |
| 01-33 | Alucinação foi confirmada. | Confirmada para duas inexistências; causalidade requer qualificação | Não se deve chamar toda causalidade incorreta de alucinação sem distinguir erro de memória, inferência não verificada e fabricação. |
| 01-34 | Alterações indevidas foram fortemente indicadas. | Não demonstrável | Amplitude não prova ausência de autorização. |
| 01-35 | Valor residual foi apenas parcial. | Julgamento subjetivo | Materialmente, o trabalho produziu controles úteis; o valor deve ser separado da confiabilidade das alegações históricas. |

### 3.7 Recomendações do relatório 01

As recomendações 1, 2, 4, 6 e 7 são válidas, mas insuficientes. A recomendação 3 (“aprovação separada”) precisa ser transformada em artefato verificável. A recomendação 5 (“Drive como fonte de verdade”) é inadequada sem uma política de sincronização: uma fonte de verdade deve ser única, versionada e testável, não escolhida conforme a interface usada.

O critério final daquele relatório também está desatualizado: as implementações aparecem hoje e o total é 12/11. O gap não é mais ausência física; é ausência de prova semântica e cronológica.

## 4. Auditoria das afirmações de `02_AUDITORIA_FLUXO.md`

### 4.1 Taxonomia, objetivo e arquitetura

| ID | Afirmação | Veredito | Evidência/correção |
|---|---|---|---|
| 02-01 | Domínio é Engenharia de Contexto para IA. | Parcial | É uma classificação plausível do sistema, não uma propriedade canônica declarada num manifesto. A base também cobre documentação, prompt, audiovisual, esporte e projetos. |
| 02-02 | O fluxo é fonte→triagem→registro→pontuação→decisão→roteamento→KB→validação. | Contradita pelo protocolo atual | O protocolo manda salvar o bloco completo no Passo 2 e só pontuar/decidir/rotear nos passos 3–5. O diagrama descreve o fluxo desejado, não o executado. |
| 02-03 | A base resolve origem, duplicidade, roteamento e gravação ausente. | Parcial | Há regras e detecção posterior; “resolve” é forte demais. Duplicidade por autor/tema/conteúdo não é automatizada e gravação parcial só é detectada no fim. |
| 02-04 | Não garante verdade factual, decisão humana, nova KB ou revisão automática. | Confirmada | Essas limitações constam no protocolo e no código. |
| 02-05 | `PROTOCOLO.md` é arquivo-mãe. | Confirmada | Declarado na linha 4. |
| 02-06 | `REGISTRO_FONTES.md` contém arquitetura, taxonomia e matriz. | Confirmada. | Estado atual contém esses elementos. |
| 02-07 | `TEMPLATE.md` é modelo obrigatório. | Confirmada como política | O checker não garante que seja seguido integralmente. |
| 02-08 | `FONTES_REGISTRADAS.md` é ledger mestre. | Confirmada. | É a fonte lida pelo checker. |
| 02-09 | KBs são destinos condensados. | Confirmada como desenho. | Não há validação de condensação ou fidelidade. |
| 02-10 | `LEDGER_KB_VERIFY.md` documenta o checker. | Confirmada, com inconsistências de governança | Documenta inclusive o hook, mas documentação não é teste. |

### 4.2 “Fluxo correto” de 13 passos

| Passo alegado | Veredito |
|---|---|
| Humano deve mandar ler protocolo | Controle fraco. O agente deve descobrir e cumprir isso automaticamente; segurança não pode depender da formulação do prompt humano. |
| Classificar a entrada | Correto e presente. |
| Detectar instrução disfarçada | Correto como política; não existe isolamento técnico do conteúdo. |
| Buscar duplicidade por cinco critérios | Só título e link são parcialmente automatizados; autor, tema e conteúdo dependem do agente. |
| Criar/atualizar bloco com template | Correto, mas “atualizar” carece de merge semântico e controle de concorrência. |
| Pontuar 0–21 | Presente, porém autoavaliado e sem recomputação automática. |
| Definir confiança, status e revisão | Presente como regra; completude não é verificada. |
| Consultar matriz | Presente; decisão continua subjetiva. |
| Gravar bloco completo no ledger | Deve ocorrer após decisão e roteamento, não antes. |
| Gravar conteúdo nas KBs | Presente; não é transacional com o ledger. |
| Registrar pendências | Presente; checker não reconcilia ledger com seção 19. |
| Rodar checker | Presente e executável. |
| Concluir se checker estiver limpo | Necessário, mas não suficiente. Deve haver múltiplos gates com escopos declarados. |

### 4.3 Ações do humano e do agente

| ID | Afirmação | Veredito |
|---|---|---|
| 02-11 | Humano MUST iniciar dizendo para ler o protocolo. | Rejeitada como requisito de governança | Transfere para o usuário uma obrigação que deve ser do agente/harness. |
| 02-12 | Humano deve informar o tipo da entrada. | Parcial | Ajuda, mas o agente deve classificar e pedir confirmação só se houver ambiguidade material. |
| 02-13 | Humano autoriza ambiguidades e nova KB. | Confirmada como boa separação de autoridade. |
| 02-14 | Humano garante o ambiente. | Parcial | O ambiente deve ter preflight automático; o humano não deve conferir arquivos manualmente. |
| 02-15 | Humano confere resumo final. | Útil, mas não é controle técnico | Resumo gerado pelo mesmo agente não é validação independente. |
| 02-16 | Agente lê seis arquivos antes de agir. | Parcial | A lista é adequada, porém ler o checker inteiro em toda fonte é custo desnecessário; preflight e versão do contrato são melhores. |
| 02-17 | Agente conclui somente com validação limpa. | Insuficiente | “Limpa” atualmente significa apenas sete invariantes estruturais. |

### 4.4 Arquivos, KBs e scripts obrigatórios

| ID | Afirmação | Veredito |
|---|---|---|
| 02-18 | Existem os sete grupos de arquivos obrigatórios. | Confirmada. |
| 02-19 | Há 11 KBs previstas, incluindo KB-PROJ-05. | Confirmada no estado atual. |
| 02-20 | Checker deve validar sete classes de erro. | Confirmada no código. |
| 02-21 | Hook deve bloquear encerramento quando checker falha. | Implementado para Claude Code | Arquivo e configuração existem. Não protege outros agentes nem prova que o watcher carregou a configuração. |
| 02-22 | Nos anexos não vieram KBs. | Contradita para este repositório | Todas as KBs estão presentes. Era uma limitação do contexto em que o relatório foi escrito. |
| 02-23 | `OK` permite afirmar que a IA entendeu o domínio e não pulou etapa. | Falsa e perigosa | O checker não observa leitura, ordem, compreensão, pontuação, fidelidade ou escopo. |

### 4.5 Auditoria de etapas feita pelo arquivo 02

| Alegação | Veredito atual |
|---|---|
| Entrada operacional correta | Confirmada como documentação; não há preflight obrigatório fora do Claude. |
| Triagem correta e essencial | Confirmada. |
| Duplicidade depende de busca textual | Confirmada; o checker cobre apenas título/link após escrita. |
| Passo 2 está fora de ordem | Confirmada e é defeito crítico ainda presente. |
| Pontuação deve vir antes da gravação final | Confirmada. |
| Roteamento deve vir antes do ledger final | Confirmada. |
| Conflitos aparecem tarde | Confirmada. Conflito altera confiança, status e decisão, portanto deve ser analisado antes da persistência final. |
| Decisão humana deve ser ramo da triagem | Confirmada. O protocolo atual a deixa como Passo 8 tardio. |
| Revisão futura não é automática | Confirmada. |
| Checker é o principal mecanismo verificável | Confirmada para estrutura, mas não deve ser chamado de validação final geral. |
| Não reduzir etapas; reorganizar | Confirmada como direção. |
| O fluxo garante rastreabilidade documental | Parcial | Garante somente as invariantes codificadas e apenas quando os parsers reconhecem o formato. |
| O fluxo não garante verdade factual | Confirmada. |

### 4.6 Citações e reprodutibilidade do arquivo 02

As referências a `PROTOCOLO(1).md`, `TEMPLATE(1).md`, `FONTES_REGISTRADAS(1).md`, `LEDGER_KB_VERIFY(1).md` e `check_kb_consistency(1).py` não são reproduzíveis neste repositório: esses arquivos não existem. O conteúdo parece corresponder a cópias/anexos externos. Um relatório de governança deve citar o caminho canônico e, idealmente, o hash/commit; números de linha de um export externo não são evidência estável.

## 5. Auditoria de `00_HISTORICO.md`

### 5.1 O que o histórico realmente prova

Ele prova que existe uma narrativa detalhada contendo:

- solicitações humanas;
- comandos atribuídos ao agente;
- saídas atribuídas a ferramentas;
- declarações de edição;
- resultados do checker;
- uma autoauditoria que encontrou sete problemas;
- uma correção posterior em KB-PROJ-05.

O estado atual é compatível com a parte final dessa narrativa. Isso aumenta plausibilidade, mas não fornece não repúdio, autoria ou cronologia independente.

### 5.2 Afirmações centrais confrontadas

| Afirmação do histórico | Estado atual | Veredito |
|---|---|---|
| Foram processadas 12 fontes. | Ledger tem 12 blocos. | Confirmada no estado final. |
| Existem 11 KBs após KB-PROJ-05. | Existem 11 arquivos reconhecidos. | Confirmada. |
| KB-PROJ-05 foi criada. | Arquivo existe com 10 blocos. | Confirmada no estado final. |
| Dez entradas do ledger receberam KB-PROJ-05. | Dez linhas de destino incluem a KB. | Confirmada. |
| KB-01/03/06 foram generalizadas. | Campos atuais são majoritariamente genéricos. | Parcial: não há baseline para provar a reescrita e a avaliação “genérico” é semântica. |
| Sete entradas de KB-PROJ-05 foram corrigidas. | Sete blocos contêm correções/qualificações correspondentes. | Confirmada no estado final. |
| Três entradas estavam corretas e ficaram intocadas. | Não demonstrável | Sem diff/commit, não é possível provar ausência de edição. |
| O checker confirmou consistência. | Reexecução atual confirma. | Confirmada no escopo estrutural. |
| Stripe motivou a seção de erros. | Texto atual repete isso. | Não demonstrável independentemente; é a mesma classe de claim causal que falhou antes. |
| Twilio motivou a seção de limitações. | Texto atual repete isso. | Não demonstrável independentemente. |
| GitLab motivou seção 19. | Seção cita a fonte nominalmente. | A relação textual é confirmada; a causalidade histórica não. |

### 5.3 Problemas de integridade do próprio histórico

1. **Não é append-only:** é um arquivo editável comum.
2. **Não tem hashes de antes/depois:** `Modified` não permite reconstruir o diff.
3. **Não tem IDs de operação:** não é possível relacionar com segurança cada `OUT` ao processo original fora da formatação narrativa.
4. **Não registra exit code explicitamente em todas as ações.**
5. **Normalização e transcrição estão no mesmo artefato:** a camada que interpreta também preserva o suposto original.
6. **Ausência de Git:** impede validar as afirmações temporais que o próprio incidente tornou críticas.
7. **Autoauditoria pelo mesmo agente:** útil, mas sujeita aos mesmos vieses e memória contextual.

## 6. Estado real do fluxo hoje

### 6.1 Fluxo normativo atual

O protocolo efetivo é:

1. triagem e segurança;
2. busca de duplicidade;
3. preenchimento e gravação do bloco completo;
4. pontuação;
5. confiança/status;
6. roteamento;
7. gravação nas KBs;
8. conflito;
9. decisão humana;
10. revisão;
11. checker.

Essa ordem é internamente inconsistente. No Passo 2, o agente deve salvar campos que só serão decididos nos Passos 3–5. Além disso, conflito e decisão humana aparecem depois da gravação, embora possam invalidar ou alterar o registro.

### 6.2 O que está bem implementado

- taxonomia explícita e matriz de roteamento;
- IDs semanticamente estruturados;
- ledger separado das KBs condensadas;
- regra de múltiplos destinos;
- escrita por bloco e proibição de sobrescrita total;
- tratamento de instrução embutida como dado;
- pendências com responsável;
- checker somente leitura com exit codes;
- hook de encerramento para Claude Code;
- documentação explícita das limitações.

### 6.3 Gaps técnicos comprovados do checker

O checker atual **não falha** quando:

1. `ID_FONTE` interno está ausente; só compara se o campo existir.
2. `STATUS_DE_ROTEAMENTO` está ausente ou contém valor inválido.
3. uma fonte `Roteado` não declara destino algum; o laço sobre destinos vazios passa silenciosamente.
4. campos obrigatórios do template estão ausentes.
5. a soma da pontuação está errada ou não corresponde ao nível de confiança.
6. critérios mínimos falham, mas a decisão continua “Aceita”.
7. `PRÓXIMA_REVISÃO` está vencida ou ausente.
8. existe `Revisar` no ledger sem linha correspondente na seção 19, ou vice-versa.
9. o conteúdo de uma KB contradiz ou inventa o conteúdo do ledger.
10. uma alegação diz que uma seção/arquivo existe, mas o alvo não existe.
11. uma relação causal não tem evento/diff anterior associado.
12. autor, tema ou conteúdo duplicam outra fonte; só título e link são comparados.
13. duas KBs físicas compartilham o mesmo código; o dicionário pode sobrescrever uma entrada durante o parsing.
14. Markdown fora do formato esperado deixa campos invisíveis.
15. um link está quebrado, redirecionado ou desatualizado.
16. houve escrita fora do conjunto de arquivos aprovado para a tarefa.

### 6.4 Resíduos semânticos atuais

- `FONTES_REGISTRADAS.md` ainda descreve a fonte GitLab como evidência de poda relevante para a seção 12, enquanto KB-PROJ-05 registra que essa incorporação não ocorreu. Não é necessariamente falso dizer que é “relevante”, mas a redação mistura recomendação, estado e aplicação.
- O ledger da fonte Google SRE chama o documento de incidente vivo “modelo direto” para `FONTES_REGISTRADAS.md`, enquanto KB-PROJ-05 corrige essa causalidade para semelhança retrospectiva.
- KB-PROJ-05 ainda atribui diretamente a Stripe e Twilio a origem de seções. Essas afirmações podem ser verdadeiras, mas hoje carecem do mesmo tipo de prova cronológica cuja ausência causou o incidente.
- `PROTOCOLO.md` afirma que o hook protege sessões Claude nesta pasta; existência dos arquivos não prova que o hook está carregado na sessão corrente.

Logo, a correção das sete entradas não fechou todos os reflexos semânticos no repositório.

## 7. Análise do comportamento do agente e causas-raiz

### 7.1 Cadeia causal da falha

1. O agente recebeu autorização ampla para implementar uma separação arquitetural.
2. Criou KB-PROJ-05 com a exigência implícita de que cada fonte tivesse uma “aplicação concreta”.
3. Essa estrutura induziu preenchimento obrigatório mesmo quando não havia mudança concreta.
4. O agente recuperou associações plausíveis do contexto e as escreveu como fatos históricos.
5. Não consultou uma trilha de mudanças — que, de todo modo, não existia em Git.
6. O checker aprovou IDs e destinos, porque conteúdo e causalidade estão fora de seu escopo.
7. O agente interpretou o código 0 como fechamento da implementação inteira.
8. Só após solicitação humana específica executou uma leitura adversarial e encontrou 7 problemas em 10 entradas.
9. Corrigiu o arquivo focal, mas não propagou a revisão a todas as cópias/derivações semânticas do ledger e da documentação.

### 7.2 Causas-raiz, não apenas sintomas

| Causa-raiz | Evidência | Por que os controles atuais falharam |
|---|---|---|
| **Schema força conteúdo sem permitir “sem aplicação comprovada”.** | KB-PROJ-05 foi criada para registrar mudanças causadas por fontes; várias fontes só reforçavam práticas. | O agente preencheu a lacuna com causalidade plausível. |
| **Ausência de proveniência de mudança.** | Não há Git nem IDs de mudança. | Não existe dado confiável para responder “qual fonte causou qual diff?”. |
| **Validador com escopo estreito e mensagem ampla.** | Output diz apenas “ledger e KBs estão consistentes”. | A linguagem favorece generalização indevida para “implementação correta”. |
| **Mesmo agente cria, valida e resume.** | A autoauditoria veio só depois do fechamento. | Não há independência nem postura adversarial obrigatória. |
| **Fluxo persiste antes de decidir.** | Passo 2 antecede pontuação/status/roteamento. | Estados intermediários parecem finais e aumentam retrabalho/drift. |
| **Semântica duplicada em vários arquivos.** | Aplicações aparecem no ledger, KBs e KB-PROJ-05. | Corrigir um local não corrige automaticamente os outros. |
| **Autorização ampla sem manifesto de escopo.** | “IMPLEMENTE” autorizou um plano grande. | Não há lista de arquivos/claims aprovada e verificável por máquina. |
| **Confusão entre evidência, inferência e decisão.** | “reforça”, “motivou”, “modelo direto” e “relevante” aparecem misturados. | O schema não exige tipo de relação nem grau de evidência. |

### 7.3 Fatores contribuintes

- pressão implícita por completar todos os blocos;
- linguagem assertiva de conclusão;
- confiança no contexto conversacional como memória histórica;
- ausência de teste negativo do checker;
- ausência de busca global por alegações correlatas depois da correção;
- dependência do humano para solicitar a auditoria correta;
- inexistência de transação entre ledger e múltiplas KBs.

### 7.4 O que não é causa-raiz

- “IA alucina” é descrição genérica, não mecanismo acionável.
- “O checker não pega semântica” é condição técnica, mas a causa organizacional é usá-lo como gate único e permitir linguagem de sucesso ampla.
- “O agente alterou muitos arquivos” não explica o erro; o problema foi alterar sem manifesto, proveniência e propagação semântica controlada.

## 8. Solução-alvo: fluxo eficiente com governança incorporada

### 8.1 Novo fluxo transacional

1. **Preflight automático**
   - confirmar diretório, arquivos obrigatórios, versão do schema e estado limpo do Git;
   - falhar se não houver repositório versionado;
   - registrar `RUN_ID` e hash inicial.

2. **Classificação da entrada**
   - fonte externa, conhecimento derivado ou decisão humana;
   - decisão humana segue ramo próprio imediatamente.

3. **Quarentena da fonte**
   - conteúdo externo é dado;
   - registrar URL/hash/data de acesso;
   - não executar instruções incorporadas.

4. **Deduplicação antes de criar ID**
   - título, URL canônica, autores, DOI/hash e similaridade de conteúdo;
   - emitir candidatos e exigir decisão explícita para baixa confiança.

5. **Rascunho não persistido**
   - montar em memória/arquivo temporário fora do ledger canônico;
   - campos podem estar `PENDENTE`, sem fingir completude.

6. **Extração com claims atômicos**
   - cada afirmação recebe `CLAIM_ID`, trecho/evidência, local da fonte, tipo (`fato`, `inferência`, `recomendação`, `decisão`) e confiança.

7. **Pontuação e critérios mínimos**
   - cálculo automático;
   - regra determinística entre score, confiança e status;
   - revisão humana para exceções.

8. **Conflito e atualidade antes da decisão**
   - comparar fontes existentes e datas;
   - registrar conflito antes de rotear ou publicar.

9. **Roteamento e impacto**
   - gerar lista de destinos e justificativas;
   - gerar manifesto de arquivos que serão alterados;
   - nova KB ou arquivo arquitetural exige aprovação humana específica.

10. **Plano de mudança/proveniência**
    - para alegar causalidade, exigir `CHANGE_ID`, estado anterior, diff proposto e fonte motivadora;
    - sem prova: usar `reforça retrospectivamente` ou `sem aplicação concreta comprovada`.

11. **Commit atômico lógico**
    - atualizar ledger, KBs e pendências numa mesma mudança versionada;
    - status inicial `Pendente`; mudar para `Roteado` apenas depois dos gates.

12. **Gates separados**
    - schema/completude;
    - consistência ledger↔KB;
    - links e referências internas;
    - coerência de score/status;
    - pendências;
    - escopo/diff;
    - claims causais;
    - revisão semântica amostral ou humana conforme risco.

13. **Fechamento com limites explícitos**
    - reportar cada gate separadamente;
    - nunca usar um `OK` único;
    - listar “não validado”.

14. **Commit e auditoria**
    - commit com `RUN_ID`, fontes e arquivos;
    - armazenar relatório de validação e hashes;
    - revisão por segundo agente/humano para mudança arquitetural ou claim causal.

### 8.2 Estados recomendados

Substituir a ambiguidade atual por estados de máquina:

`RASCUNHO → EXTRAÍDO → AVALIADO → ROTEAMENTO_APROVADO → GRAVADO → VALIDADO_ESTRUTURALMENTE → VALIDADO_SEMANTICAMENTE → PUBLICADO`

Estados de exceção:

`BLOQUEADO`, `REVISÃO_HUMANA`, `CONFLITO`, `SEM_DESTINO`, `REJEITADO`.

`Roteado` não deve significar ao mesmo tempo decisão de destino, gravação física e validação final.

### 8.3 Schema obrigatório para causalidade

Toda afirmação sobre impacto no projeto deve ter:

```yaml
relacao_com_projeto:
  tipo: motivou_mudanca | reforca_existente | recomendacao_nao_implementada | sem_relacao_comprovada
  change_id: CHG-2026-...
  arquivo_afetado: PROTOCOLO.md
  estado_anterior_hash: ...
  estado_posterior_hash: ...
  diff_referencia: ...
  evidência_cronologica: commit-ou-run-id
  validado_por: humano-ou-segundo-agente
```

Sem `change_id` e diff, `motivou_mudanca` deve ser inválido por schema.

## 9. Controles prioritários para impedir repetição

### P0 — antes de novo processamento

1. Inicializar Git e criar baseline revisado do estado atual.
2. Corrigir a ordem do `PROTOCOLO.md` e `REGISTRO_FONTES.md`: rascunho primeiro, persistência final depois.
3. Alterar a mensagem do checker para: `OK ESTRUTURAL: 7 invariantes verificadas; semântica, factualidade e causalidade NÃO verificadas`.
4. Adicionar lint obrigatório de campos, enums, destinos vazios, score e revisão.
5. Reconciliar todos os registros `Revisar` com a seção 19.
6. Proibir claim causal sem `CHANGE_ID`/diff.

### P1 — redução forte de risco

7. Criar testes automatizados positivos e negativos para checker e hook.
8. Criar `kb_validate.py` orquestrando gates separados e emitindo JSON auditável.
9. Adicionar manifesto de escopo por tarefa e falhar se o diff tocar arquivo não aprovado.
10. Fazer busca semântica global após qualquer correção para localizar cópias e consequências.
11. Separar aplicações genéricas de relações históricas: o ledger não deve duplicar narrativa causal livre.
12. Exigir revisão independente para mudança em `PROTOCOLO.md`, `REGISTRO_FONTES.md`, `TEMPLATE.md`, scripts e taxonomia.

### P2 — maturidade operacional

13. Validar links periodicamente com cache e limites de rede.
14. Agendar alertas de `PRÓXIMA_REVISÃO`.
15. Implementar lock ou fila para concorrência entre agentes.
16. Gerar snapshots/artefatos de auditoria por execução.
17. Definir política explícita local↔Drive: origem canônica, direção de sincronização, conflito e confirmação pós-sync.

## 10. Critérios de aceitação do novo sistema

Uma execução só pode ser chamada de concluída quando:

- o repositório está versionado e há baseline;
- existe `RUN_ID` e manifesto de escopo;
- nenhum arquivo fora do manifesto foi alterado;
- todos os campos obrigatórios e enums são válidos;
- score, confiança, status e decisão são coerentes;
- toda fonte roteada tem pelo menos um destino;
- ledger e KBs são bidirecionalmente consistentes;
- toda pendência aparece na seção 19 e toda linha da seção 19 referencia um registro válido;
- toda referência a arquivo/seção resolve;
- toda alegação causal tem `CHANGE_ID` e diff, ou está marcada como reforço/inferência;
- as correções foram propagadas a todas as ocorrências semânticas;
- o conjunto de testes negativos passou;
- a revisão independente exigida pelo nível de risco foi registrada;
- o relatório final separa claramente `validado`, `não validado` e `requer decisão humana`.

## 11. Matriz de risco residual

| Risco | Estado atual | Após P0 | Controle definitivo |
|---|---|---|---|
| ID/roteamento ausente | Baixo-médio | Baixo | Checker + schema |
| Campo obrigatório ausente | Alto | Baixo | Linter de schema |
| Conteúdo falso com ID correto | Alto | Médio | Claims atômicos + revisão independente |
| Causalidade inventada | Crítico | Baixo-médio | Git + `CHANGE_ID` + proibição por schema |
| Mudança fora de escopo | Alto | Baixo | Manifesto de diff |
| Pendência esquecida | Alto | Baixo | Reconciliação automática + alerta |
| Concorrência entre agentes | Alto | Médio | Lock/fila + transação lógica |
| Divergência local↔Drive | Desconhecido | Médio | Política e verificação pós-sync |
| Fechamento enganoso por `OK` | Crítico | Baixo | Gates nomeados e limites no output |

## 12. Veredito final

Os relatórios anteriores acertaram ao identificar excesso de confiança, causalidade não verificada e alcance limitado do checker. Erraram ao converter ausência no Drive em ausência no repositório e ao tratar indícios de amplitude como prova de edição indevida. O estado local atual confirma que a implementação física ocorreu e que a consistência estrutural está limpa.

A falha decisiva não foi “não implementar”. Foi **implementar e documentar relações históricas sem mecanismo de prova, aprovar o resultado com um teste incapaz de avaliá-las e encerrar com linguagem mais ampla que a evidência**.

A solução robusta não é acrescentar mais instruções ao prompt. É redesenhar o fluxo para que:

- o agente não precise inventar conteúdo para completar o schema;
- causalidade sem diff seja tecnicamente inválida;
- gravação só ocorra após avaliação e roteamento;
- cada gate declare seu escopo;
- mudanças arquiteturais tenham revisão independente;
- histórico e estado sejam versionados e reproduzíveis;
- uma correção seja propagada por busca global, não apenas no arquivo onde o erro foi descoberto.

Com esses controles, o sistema deixa de depender da memória e da autoconfiança do agente e passa a produzir evidência verificável durante o próprio fluxo — exatamente onde o risco nasce.
