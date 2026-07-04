# Estratégias de Prompt Engineering para Identificação de Domínio por IA

*Otimizando a precisão na descoberta do domínio através de instruções estruturadas*

Este documento explora técnicas fundamentais para guiar modelos de linguagem na identificação precisa do domínio de conhecimento de uma consulta. Aprender a estruturar prompts que contextualizam a tarefa permite reduzir ambiguidades e garantir que a IA aplique a terminologia, o tom e a lógica adequados ao cenário específico, aumentando significativamente a relevância das respostas geradas.

## Prompt Inicial

```txt
Identifique qual o domínio de conhecimento trata [ASSUNTO DO DOMINIO A IDENTIFICAR]

Responda separando:

- Domínio principal
- Subdomínios relacionados
- Tema específico
- Técnicas envolvidas
- Contexto de aplicação
- Diferença entre “gerar um plano textual” e “produzir um plano operacional executável”
- Fontes ou áreas acadêmicas/profissionais que sustentam essa classificação

Não invente uma categoria se houver termos mais reconhecidos. Quando houver mais de uma possibilidade, compare e explique qual é a mais adequada.
```

## Prompt de confirmação

```txt
Essa classificação trata [TEXTO COM O EXEMPLO QUE O DOMINIO NAO TRATA] ou [TEXTO COM O EXEMPLO DO QUE O DOMINIO TARA]?
```
## Prompt de pós classificação

```txt
Com base na classificação validada, consolide a definição final do domínio.

Entregue:

- Nome recomendado do domínio
- Nome recomendado do subdomínio
- Tema central
- Técnicas principais
- Critérios de aceitação das Técnicas principais
- Melhores praticas
- Critérios de aceitação das Melhores praticas
- Contexto
- O que pertence a esse domínio
- O que não pertence a esse domínio
- Exemplos de uso correto
- Exemplos de uso incorreto
- Critérios para reconhecer quando uma tarefa pertence a esse domínio
- Nome curto recomendado para registrar esse domínio em uma base de conhecimento
```

## Prompt Final

``txt
Transforme a definição consolidada deste domínio em uma entrada operacional para uma base de conhecimento.

A entrada deve conter:

- Nome oficial do domínio
- Nome oficial do subdomínio
- Nome curto para referência
- Definição Quando usar
- Quando não usar
- Técnicas principais
- Melhores praticas
- Critérios de aceitação das Melhores praticas
- Critérios de aceitação das Técnicas principais
- Sinais de ativação da tarefa
- Perguntas de triagem que a IA deve fazer antes de responder
- Checklist de validação
- Exemplo de aplicação correta
- Exemplo de aplicação incorreta
- Relação com domínios próximos
- Decisão registrada: por que este domínio foi escolhido
```
