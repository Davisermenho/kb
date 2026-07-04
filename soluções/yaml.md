## Resultado da auditoria

O arquivo [front..md](/home/davis/dev/kb/soluções/front..md) não está estruturalmente formatado como Markdown. Ele contém texto UTF-8 legível, porém quase toda a hierarquia documental foi achatada em texto corrido.

Nenhum arquivo foi alterado.

### Diagnóstico geral

| Elemento | Situação atual | Impacto para o agente |
|---|---|---|
| Título principal | Sem `#` | O assunto central não é identificado estruturalmente |
| Capítulos | Texto comum, como `Chapter 1.` | Prejudica segmentação e navegação |
| Seções e subseções | Numeração misturada ao parágrafo | Dificulta reconhecer relações pai–filho |
| Exemplos técnicos | Sem blocos cercados | YAML, texto e explicação ficam misturados |
| Listas | Itens transformados em frases contínuas | Perda da relação entre os elementos |
| Tabelas | Conteúdo tabular achatado | Colunas deixam de ser semanticamente reconhecíveis |
| Links e referências | Números anexados às palavras | Referências podem ser interpretadas como conteúdo |
| Figuras | Apenas legendas, sem sintaxe própria | O agente não consegue distinguir legenda de texto |
| Metadados | Misturados ao início do documento | Autoria, versão e conteúdo não ficam separados |
| Linhas | Até 961 caracteres | Chunking e recuperação ficam menos precisos |
| Espaçamento | 705 linhas vazias e distribuição irregular | Gera fragmentação artificial |
| Markdown efetivo | Praticamente inexistente | O arquivo funciona como texto simples |

Foram encontrados:

- 1.576 linhas;
- 871 linhas não vazias;
- 372 linhas com mais de 120 caracteres;
- 243 linhas com mais de 200 caracteres;
- 10 capítulos identificáveis pelo texto;
- aproximadamente 106 marcadores numerados de seção;
- nenhuma hierarquia Markdown com `#`, `##`, `###` ou `####`;
- nenhum bloco cercado com crases;
- nenhuma lista Markdown consistente;
- nenhuma nota de rodapé Markdown;
- quatro linhas contendo tabulação;
- onze linhas com espaços finais.

## Problemas estruturais identificados

### 1. Título e metadados sem delimitação

O documento começa diretamente com informações editoriais em [front..md:1](/home/davis/dev/kb/soluções/front..md:1). O título, a versão, a revisão, o copyright e o corpo aparecem no mesmo nível.

Sintaxe recomendada:

```markdown
# Título do documento

**Versão:** ...
**Revisão:** ...
**Copyright:** ...
```

Alternativamente, metadados estritamente documentais poderiam usar front matter:

```markdown
---
title: ...
version: ...
revision: ...
---
```

O front matter é opcional. Para máxima compatibilidade entre agentes e renderizadores, título e campos em Markdown comum são mais previsíveis.

### 2. Capítulos não são títulos Markdown

Em [front..md:35](/home/davis/dev/kb/soluções/front..md:35), capítulo, título e primeiro parágrafo estão na mesma linha:

```text
Chapter 1. Introduction to YAML YAML (...) is a data serialization...
```

O mesmo ocorre nos capítulos seguintes, por exemplo em [front..md:63](/home/davis/dev/kb/soluções/front..md:63), [front..md:380](/home/davis/dev/kb/soluções/front..md:380) e [front..md:1442](/home/davis/dev/kb/soluções/front..md:1442).

Hierarquia recomendada:

```markdown
# Título do documento

## Chapter 1. Introduction to YAML

### 1.1. Goals

#### 1.1.1. Subsection
```

Como já existe um título principal, os capítulos devem começar em `##`, não em outro `#`.

### 3. Seções estão fundidas aos parágrafos

Exemplo em [front..md:43](/home/davis/dev/kb/soluções/front..md:43):

```text
1.1. Goals The design goals for YAML are...
```

Sintaxe necessária:

```markdown
### 1.1. Goals

The design goals for YAML are...
```

Cada título precisa:

- ocupar uma linha própria;
- possuir um espaço depois dos `#`;
- ser seguido por uma linha vazia;
- manter nível compatível com sua numeração.

### 4. Listas foram achatadas

Na seção de objetivos, vários itens aparecem sequencialmente como prosa. Isso elimina a fronteira entre os itens.

Sintaxe recomendada:

```markdown
- Primeiro item.
- Segundo item.
- Terceiro item.
```

Para sequências que dependam de ordem:

```markdown
1. Primeiro passo.
2. Segundo passo.
3. Terceiro passo.
```

Não se deve usar números apenas para efeito visual quando a ordem não possui significado.

### 5. Exemplos YAML não estão em blocos de código

Os exemplos começam com legendas como em [front..md:67](/home/davis/dev/kb/soluções/front..md:67), mas os dados são apresentados como texto comum. Isso é especialmente problemático porque espaços e quebras de linha fazem parte da sintaxe do YAML.

Estrutura recomendada:

````markdown
#### Example 2.1 — Sequence of Scalars

```yaml
conteúdo original do exemplo
```
````

Linguagens apropriadas:

- `yaml` para exemplos YAML;
- `json` para resultados JSON;
- `text` para diagramas ASCII e conteúdo sem linguagem;
- `bnf` ou `abnf` somente se o renderizador utilizado oferecer suporte;
- bloco sem identificador quando não houver linguagem segura.

Essa é a correção estrutural de maior impacto: impede que o agente confunda exemplos com instruções ou prosa normativa.

### 6. Tabelas foram convertidas em texto linear

No final do documento, expressões regulares e tags aparecem como colunas separadas apenas por tabulações, por exemplo próximo de [front..md:1556](/home/davis/dev/kb/soluções/front..md:1556).

Sintaxe recomendada:

```markdown
| Regular expression | Resolved to tag |
|---|---|
| valor original | valor original |
```

Se uma célula contiver muitos caracteres especiais ou código extenso, um bloco de código pode ser mais seguro que uma tabela.

### 7. Figuras não possuem separação semântica

As legendas, como `Figure 3.1` em [front..md:240](/home/davis/dev/kb/soluções/front..md:240), estão representadas como parágrafos comuns.

Quando houver imagem:

```markdown
![Descrição da figura](caminho-da-imagem)

*Figure 3.1. Processing Overview*
```

Quando a imagem estiver ausente, a legenda pode permanecer como subtítulo:

```markdown
#### Figure 3.1. Processing Overview
```

Não se deve inventar caminho de imagem ou descrição ausente.

### 8. Referências e notas estão concatenadas

Ocorrências como `Team1`, `hosted2`, `specification3` e `characters4` indicam provável perda da marcação de notas durante a extração.

Sintaxe apropriada:

```markdown
Texto referenciado.[^1]

[^1]: Referência original.
```

Ou, quando existir URL explícita:

```markdown
[Texto da referência](https://exemplo.com)
```

A reconstrução só deve ser realizada quando for possível associar inequivocamente cada marcador à referência original. Caso contrário, haveria risco de alteração de conteúdo.

### 9. Parágrafos e quebras de linha são inconsistentes

O arquivo alterna grandes linhas corridas com várias linhas vazias. A normalização recomendada é:

```markdown
Primeiro parágrafo completo.

Segundo parágrafo completo.
```

Regras:

- exatamente uma linha vazia entre parágrafos;
- uma linha vazia antes e depois de títulos, listas e blocos;
- remover espaços no fim das linhas;
- substituir tabulações estruturais por espaços;
- não inserir quebras no meio de frases apenas para limitar largura, salvo convenção explícita do projeto.

## Padrão estrutural recomendado

```markdown
# Título do documento

Metadados documentais.

## Status of this Document

Parágrafos originais.

### See also

- Referência original.
- Referência original.

## Chapter 1. Introduction to YAML

Parágrafos originais.

### 1.1. Goals

- Item original.
- Item original.

## Chapter 2. Language Overview

### 2.1. Collections

Parágrafos originais.

#### Example 2.1 — Título original

```yaml
conteúdo original
```

#### Figure 2.1 — Título original

![Descrição original](caminho-original)
```

## Prioridade recomendada

1. Separar capítulos, seções e subseções com `##`, `###` e `####`.
2. Isolar todos os exemplos em blocos de código.
3. Restaurar listas e tabelas.
4. Separar títulos, legendas e respectivos conteúdos.
5. Normalizar linhas vazias, tabulações e espaços finais.
6. Reconstruir links e notas somente com fonte verificável.

Essa padronização melhora diretamente o chunking, a recuperação por seção, o reconhecimento de exemplos, a distinção entre texto normativo e código e a preservação da hierarquia durante o processamento por agentes de IA.