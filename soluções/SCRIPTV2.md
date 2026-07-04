# Plano de ações — `check_kb_consistency.py` V2

## 1. Objetivo

Criar uma segunda versão do verificador de consistência entre `FONTES_REGISTRADAS.md` e os arquivos `KB-*.md`, eliminando os falsos resultados `OK` identificados após a revisão do script atual.

A V2 deve continuar sendo uma ferramenta somente leitura, baseada apenas na biblioteca padrão do Python, mas deve validar tanto a estrutura mínima dos documentos quanto as sete regras de consistência já documentadas em `LEDGER_KB_VERIFY.md`.

O resultado esperado é simples: o script só pode retornar sucesso quando conseguiu interpretar os arquivos relevantes sem ambiguidades e não encontrou divergências estruturais ou de roteamento.

## 2. Escopo

### Incluído

- Preservar as sete verificações existentes.
- Detectar ledger ou KB malformados antes das verificações de consistência.
- Exigir campos essenciais em cada registro do ledger.
- Detectar mais de um arquivo associado ao mesmo código de KB.
- Tornar a comparação de links conservadora e previsível.
- Melhorar mensagens, resumo e códigos de saída.
- Separar parsing, validação e apresentação do resultado.
- Criar testes automatizados para o comportamento atual e para os novos casos.
- Atualizar a documentação e o hook após a validação da V2.

### Fora do escopo

- Corrigir arquivos automaticamente.
- Alterar `FONTES_REGISTRADAS.md` ou qualquer `KB-*.md`.
- Verificar a fidelidade semântica entre o conteúdo condensado da KB e a fonte original.
- Validar factualidade, qualidade da síntese ou pontuação atribuída à fonte.
- Usar rede, banco de dados, parser Markdown externo ou dependências de terceiros.
- Resolver concorrência entre agentes durante a escrita dos arquivos.

## 3. Contrato da V2

### Entrada

```bash
python3 check_kb_consistency_v2.py [diretorio]
```

- Sem argumento: usar o diretório do próprio script.
- Com um argumento: usar o diretório informado.
- Mais de um argumento, caminho inexistente ou caminho que não seja diretório: erro de execução.
- O script deve abrir os arquivos explicitamente como UTF-8.

### Saída e códigos de retorno

| Código | Significado |
|---|---|
| `0` | Parsing concluído e nenhuma divergência encontrada. |
| `1` | Uma ou mais divergências de estrutura ou consistência foram encontradas. |
| `2` | O verificador não pôde executar: argumento inválido, diretório inacessível, ledger ausente, erro de leitura ou outra falha operacional. |

Um documento malformado que pôde ser lido deve retornar `1`, não `2`. O código `2` fica reservado a situações em que a verificação não pôde ser realizada de forma confiável.

O resumo final deve distinguir:

- fontes válidas interpretadas;
- arquivos de KB encontrados e arquivos efetivamente interpretados;
- erros estruturais;
- divergências de consistência;
- resultado final (`OK`, `DIVERGENTE` ou `ERRO`).

## 4. Princípios de implementação

1. **Falhar de forma fechada:** ausência ou ambiguidade de estrutura nunca pode resultar em `OK`.
2. **Não inferir silenciosamente:** campos obrigatórios ausentes ou repetidos devem gerar diagnóstico.
3. **Não sobrescrever durante o parsing:** códigos de KB repetidos devem ser preservados e reportados.
4. **Diagnósticos localizáveis:** toda ocorrência deve informar arquivo e, quando possível, número da linha e `ID_FONTE`.
5. **Determinismo:** arquivos e issues devem ser processados e impressos em ordem estável.
6. **Compatibilidade consciente:** os formatos atualmente válidos (`CAMPO: valor`, `- CAMPO: valor`, `**CAMPO:** valor` e `- **CAMPO:** valor`) devem continuar aceitos.
7. **Escopo honesto:** `OK` significa consistência estrutural e de roteamento, não fidelidade de conteúdo.

## 5. Modelo interno proposto

Usar `dataclasses` para evitar dicionários sem contrato:

- `Location`: caminho e linha.
- `Issue`: código, categoria, severidade, mensagem e localização.
- `LedgerEntry`: ID do cabeçalho, campos extraídos, destinos e localização.
- `KbEntry`: ID do cabeçalho e localização.
- `KbFile`: código, caminho e entradas.
- `ParseResult`: dados interpretados e issues estruturais.

As categorias devem possuir códigos estáveis, por exemplo:

- `STRUCT-MISSING-SECTION`
- `STRUCT-MISSING-FIELD`
- `STRUCT-DUPLICATE-FIELD`
- `STRUCT-EMPTY-HEADING`
- `STRUCT-DUPLICATE-KB-CODE`
- `LEDGER-DUPLICATE-ID`
- `ID-INVALID-FORMAT`
- `LEDGER-ID-MISMATCH`
- `SOURCE-DUPLICATE-TITLE`
- `SOURCE-DUPLICATE-LINK`
- `KB-DUPLICATE-ID`
- `ROUTING-MISSING`
- `ROUTING-ORPHAN`

As tags humanas atuais (`[LEDGER]`, `[FORMATO]`, `[DUPLICATA]`, `[KB]`, `[MISSING]` e `[ORFAO]`) podem ser preservadas na apresentação para facilitar a transição.

## 6. Ações de implementação

### A01 — Criar uma suíte de caracterização da V1

Antes de alterar a lógica, registrar em testes o comportamento correto já existente:

- ledger e KB consistentes;
- ID duplicado no ledger;
- ID fora do formato;
- campo `ID_FONTE` diferente do cabeçalho;
- título duplicado sob IDs diferentes;
- link duplicado sob IDs diferentes;
- ID duplicado dentro de uma KB;
- destino inexistente;
- bloco ausente em destino existente;
- bloco órfão sem entrada no ledger;
- bloco em KB não declarada como destino;
- múltiplos destinos válidos;
- status diferente de `Roteado` sem exigência de gravação.

Usar `unittest`, `tempfile.TemporaryDirectory` e `pathlib`, sem fixtures externas permanentes.

**Critério de aceite:** cada uma das sete verificações documentadas possui pelo menos um teste positivo e um negativo.

### A02 — Separar CLI, leitura, parsing, validação e renderização

Reorganizar o código em funções sem dependência direta de `sys.argv` ou `print`:

```text
main(argv) -> int
read_documents(directory) -> documentos ou erro operacional
parse_ledger(document) -> ParseResult
parse_kb_file(document) -> ParseResult
validate_structure(...) -> list[Issue]
validate_consistency(...) -> list[Issue]
render_report(...) -> str
```

**Critério de aceite:** os testes conseguem exercitar parsing e validação diretamente, sem subprocesso; testes específicos da CLI validam códigos de saída e stdout/stderr.

### A03 — Validar a seção `## Registros`

Para ledger e KBs:

- exigir exatamente uma linha de seção `## Registros`;
- reportar seção ausente ou repetida;
- permitir seção vazia nas KBs;
- não permitir ledger vazio quando o projeto exigir ao menos uma fonte;
- ignorar exemplos anteriores à seção, mantendo a regra atual.

A exigência de ledger não vazio deve ser configurada como regra da aplicação, não consequência acidental do parser.

**Critério de aceite:** ledger sem seção, com seção repetida ou sem registros retorna `1` e nunca imprime `OK`.

### A04 — Validar cabeçalhos de registro

Cada entrada após `## Registros` deve começar com `### ` e possuir um primeiro token não vazio. No ledger, esse token deve ser validado como `ID_FONTE`; nas KBs, deve ser preservado para as verificações de órfão e duplicidade.

Também devem ser detectados conteúdos soltos relevantes entre a seção e o primeiro registro ou entre blocos que indiquem um registro sem cabeçalho.

**Critério de aceite:** cabeçalho vazio, nível Markdown incorreto e registro sem cabeçalho geram issue estrutural com arquivo e linha.

### A05 — Validar campos obrigatórios do ledger

Para as regras cobertas pelo checker, exigir em cada bloco:

- `ID_FONTE`;
- `TÍTULO`;
- `LINK_REFERÊNCIA`;
- `ARQUIVO_DESTINO_KB`;
- `STATUS_DE_ROTEAMENTO`.

Cada campo deve ocorrer exatamente uma vez. Valor vazio deve ser tratado como ausente. Campos completos do template que não participam do checker permanecem fora desta validação, salvo decisão posterior de ampliar o contrato.

`STATUS_DE_ROTEAMENTO` deve aceitar apenas:

- `Pendente`;
- `Roteado`;
- `Revisar`;
- `Bloqueado`.

**Critério de aceite:** ausência, repetição, valor vazio ou status desconhecido retorna `1` com diagnóstico específico.

### A06 — Tornar o parser de campos explícito

Substituir a regex permissiva por uma expressão que aceite somente os estilos documentados e capture nome e valor de forma inequívoca. Evitar aceitar, por acidente, um ou três asteriscos ou combinações de negrito não previstas.

O parser deve armazenar a linha de cada campo e reportar campos repetidos, em vez de selecionar silenciosamente a primeira ocorrência.

**Critério de aceite:** os quatro estilos compatíveis são aceitos; estilos ambíguos ou campos duplicados são rejeitados nos testes.

### A07 — Validar destinos de KB

- Extrair todos os códigos de destino, preservando ordem e removendo repetições apenas após reportá-las, se repetição for considerada erro.
- Aceitar somente `KB-<n>` e `KB-PROJ-<n>` conforme a convenção vigente.
- Para `Roteado`, exigir pelo menos um destino válido.
- Permitir o valor textual oficial de ausência de destino somente para estados que não exijam gravação, como `Revisar`, conforme a regra atual do projeto.
- Reportar texto que mencione uma KB em formato inválido, em vez de produzir silenciosamente um conjunto vazio.

**Critério de aceite:** uma fonte `Roteado` sem destino válido retorna `1`; múltiplos destinos válidos continuam funcionando.

### A08 — Detectar colisão de códigos de KB

Alterar o índice de:

```python
dict[kb_code, KbFile]
```

para uma estrutura que preserve todas as ocorrências durante a descoberta:

```python
dict[kb_code, list[KbFile]]
```

Se dois arquivos resolverem para o mesmo código, emitir `STRUCT-DUPLICATE-KB-CODE` e verificar ambos sempre que possível, sem sobrescrever nenhum em memória.

Também reportar arquivos que combinam com `KB-*.md`, mas cujo nome não corresponde à convenção `<KB_CODE>_<nome>.md`.

**Critério de aceite:** `KB-01_A.md` e `KB-01_B.md` sempre causam retorno `1`, e issues existentes em ambos aparecem no relatório.

### A09 — Corrigir a normalização de links

Separar normalização de título e de URL:

- título: normalização Unicode (`unicodedata.normalize`), `casefold`, espaços e pontuação, com regra documentada;
- URL: usar `urllib.parse`, normalizando apenas aspectos seguros, como esquema e host em minúsculas e barra final equivalente quando a política assim definir;
- preservar path, query e fragment de modo a não confundir `/a-b` com `/a/b`;
- remover pontuação Markdown externa sem alterar caracteres pertencentes à URL;
- quando o campo contiver várias URLs, definir explicitamente se a chave de duplicidade é a primeira URL canônica ou o conjunto de URLs. Para compatibilidade, a recomendação inicial é usar a primeira URL como referência principal e documentar isso.

**Critério de aceite:** URLs realmente equivalentes são detectadas como duplicadas, enquanto URLs com paths ou queries diferentes não colidem por perda de pontuação.

### A10 — Preservar e endurecer as sete verificações

Executar as verificações de consistência mesmo quando houver erros estruturais recuperáveis, para entregar o máximo de diagnóstico em uma única execução. Não executar uma regra apenas quando seus dados forem impossíveis de determinar; nesse caso, a issue estrutural já deve explicar a impossibilidade.

Regras preservadas:

1. ID duplicado no ledger.
2. ID fora do formato.
3. Campo `ID_FONTE` diferente do cabeçalho.
4. Título ou link duplicado sob IDs diferentes.
5. ID duplicado dentro da mesma KB.
6. Fonte `Roteado` ausente em algum destino.
7. Bloco órfão ou presente em destino não declarado.

**Critério de aceite:** todos os testes de caracterização da A01 passam na V2, com mensagens iguais ou mais específicas.

### A11 — Melhorar o relatório

Formato sugerido:

```text
Resultado: DIVERGENTE
Ledger: 12 registros interpretados
KBs: 11 arquivos encontrados | 11 interpretados | 11 códigos únicos
Issues: 2 estruturais | 1 de consistência

- [STRUCT-MISSING-FIELD] FONTES_REGISTRADAS.md:58 ...
- [ROUTING-MISSING] FONTES_REGISTRADAS.md:104 ...
```

- Ordenar por caminho, linha, categoria e código.
- Enviar relatório normal para `stdout` nos códigos `0` e `1`.
- Enviar falhas operacionais para `stderr` no código `2`.
- Não usar cores quando stdout não for terminal; cores não são necessárias na primeira entrega.

**Critério de aceite:** todas as issues possuem código estável e localização; o resumo não chama códigos únicos de “arquivos verificados”.

### A12 — Completar a matriz de testes de robustez

Adicionar, no mínimo, os seguintes casos:

| Grupo | Caso esperado |
|---|---|
| Estrutura | Ledger sem `## Registros` falha. |
| Estrutura | KB sem `## Registros` falha. |
| Estrutura | Seção repetida falha. |
| Estrutura | Ledger vazio falha. |
| Campos | Cada campo obrigatório ausente falha isoladamente. |
| Campos | Campo vazio falha. |
| Campos | Campo repetido falha. |
| Campos | Os estilos Markdown suportados passam. |
| Status | Cada status permitido passa estruturalmente. |
| Status | Status desconhecido falha. |
| Destino | `Roteado` sem destino falha. |
| Destino | Código de destino inválido falha. |
| Arquivos | Dois arquivos com o mesmo código falham. |
| Arquivos | Nome `KB-*.md` fora da convenção falha. |
| URL | Barra final equivalente segue política definida. |
| URL | `/a-b` e `/a/b` não são duplicados. |
| URL | Queries diferentes não são duplicadas. |
| CLI | Ledger ausente retorna `2`. |
| CLI | Diretório inexistente retorna `2`. |
| CLI | Argumentos excedentes retornam `2`. |
| CLI | Erro UTF-8 ou de leitura retorna `2`. |
| Determinismo | A ordem do relatório é estável. |

**Critério de aceite:** a suíte passa em execução repetida e não depende do conteúdo real da base.

### A13 — Executar validação sobre a base real

Executar V1 e V2 no diretório atual e comparar resultados:

```bash
python3 check_kb_consistency.py /home/davis/dev/kb
python3 check_kb_consistency_v2.py /home/davis/dev/kb
```

Se a V2 encontrar erros que a V1 não encontra, classificar cada ocorrência como:

- defeito real nos documentos;
- incompatibilidade legítima que deve ser suportada;
- convenção ainda não documentada;
- falso positivo da V2.

Não adaptar o parser apenas para fazer a base passar: toda exceção aceita deve virar regra documentada e teste.

**Critério de aceite:** todas as diferenças entre V1 e V2 estão explicadas, corrigidas ou formalmente aceitas.

### A14 — Atualizar documentação

Após estabilizar o comportamento:

- atualizar `LEDGER_KB_VERIFY.md` com contrato, novos erros estruturais e códigos de saída;
- atualizar a docstring e o uso no próprio script;
- revisar `PROTOCOLO.md` e `REGISTRO_FONTES.md` para que “consistente” tenha o mesmo significado;
- documentar exatamente os estilos de campo aceitos;
- registrar explicitamente que a V2 não verifica fidelidade semântica;
- incluir comandos para rodar a suíte de testes.

**Critério de aceite:** não existem diferenças conhecidas entre o comportamento testado e o comportamento descrito.

### A15 — Migrar o hook de forma segura

Somente depois da aprovação da base real e da documentação:

1. Fazer o hook chamar a V2.
2. Confirmar que retorno `0` permite encerramento.
3. Confirmar que retornos `1` e `2` bloqueiam o encerramento e apresentam o relatório.
4. Testar execução com diretório de trabalho diferente.
5. Manter a V1 disponível durante um período curto de comparação.

**Critério de aceite:** testes manuais do hook cobrem sucesso, divergência e falha operacional.

### A16 — Substituir a V1

Depois do período de comparação:

- promover a V2 para `check_kb_consistency.py`, preservando o comando público existente;
- manter histórico pelo controle de versão, sem conservar duas implementações indefinidamente;
- remover referências temporárias a `_v2`;
- executar novamente testes, checker e simulação do hook.

**Critério de aceite:** o comando canônico, a documentação e o hook apontam para uma única implementação aprovada.

## 7. Ordem recomendada de execução

| Fase | Ações | Resultado |
|---|---|---|
| 1 — Baseline | A01 | Comportamento válido da V1 protegido por testes. |
| 2 — Fundação | A02–A06 | Parser estruturado e falhas silenciosas eliminadas. |
| 3 — Consistência | A07–A10 | Destinos, colisões e duplicidades validados corretamente. |
| 4 — Diagnóstico | A11–A12 | Relatório estável e cobertura de robustez. |
| 5 — Homologação | A13–A14 | Base real e documentação alinhadas. |
| 6 — Migração | A15–A16 | Hook e comando público usando a V2. |

Não migrar o hook nem substituir a V1 antes da homologação da fase 5.

## 8. Definição de pronto

A V2 estará concluída quando todos os itens abaixo forem verdadeiros:

- [ ] As sete verificações originais continuam cobertas e funcionando.
- [ ] Ledger sem seção, vazio ou malformado nunca retorna `0`.
- [ ] Campos essenciais ausentes, vazios ou duplicados são detectados.
- [ ] Status inválido e fonte `Roteado` sem destino são detectados.
- [ ] Nenhum arquivo de KB é sobrescrito silenciosamente no índice interno.
- [ ] Códigos de KB repetidos são reportados.
- [ ] URLs distintas não colidem por remoção indiscriminada de pontuação.
- [ ] Toda issue informa código, arquivo e linha quando disponível.
- [ ] O número de arquivos encontrados é diferente do número de códigos únicos quando aplicável.
- [ ] Códigos de saída `0`, `1` e `2` obedecem ao contrato.
- [ ] A suíte automatizada passa integralmente.
- [ ] A base real foi homologada e eventuais diferenças foram explicadas.
- [ ] `LEDGER_KB_VERIFY.md` descreve fielmente a implementação final.
- [ ] O hook foi testado nos três resultados possíveis.
- [ ] O comando público continua sendo `python3 check_kb_consistency.py [diretorio]`.

## 9. Riscos e controles

| Risco | Controle |
|---|---|
| A V2 rejeitar formatação legítima já existente | Rodar caracterização e homologação antes da migração; transformar exceções legítimas em testes. |
| Aumentar demais o escopo para validar todo o template | Limitar campos obrigatórios aos necessários para as regras do checker nesta entrega. |
| Confundir erro estrutural com falha operacional | Aplicar rigorosamente a divisão dos códigos `1` e `2`. |
| Produzir falso positivo de duplicidade por normalização | Manter normalização conservadora, separada para títulos e URLs. |
| Hook bloquear todos os turnos por regressão | Migrar somente após testes e manter rollback simples para a V1 durante a homologação. |
| Documentação voltar a divergir do código | Derivar exemplos dos testes e revisar documentação como critério obrigatório da entrega. |

## 10. Entregáveis

1. `check_kb_consistency_v2.py` durante o desenvolvimento.
2. Suíte automatizada em `tests/test_check_kb_consistency.py` ou nome equivalente.
3. Relatório curto de comparação V1 versus V2 sobre a base real.
4. `LEDGER_KB_VERIFY.md` atualizado.
5. Hook atualizado e validado.
6. V2 promovida ao nome canônico `check_kb_consistency.py` após homologação.

Este plano não autoriza correções automáticas no ledger ou nas KBs. Qualquer divergência encontrada durante a homologação deve ser revisada e corrigida separadamente, preservando o caráter somente leitura do checker.
