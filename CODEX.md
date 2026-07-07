# CODEX.md — Instruções específicas do Codex

Este é um guia complementar. O contrato carregado automaticamente pelo Codex é `AGENTS.md`; em cada sessão, siga esse arquivo, `governanca/PROTOCOLO.md` e o manifesto do run ativo.

## Responsabilidades

- Implementar automações, configurações e testes somente dentro do escopo autorizado.
- Executar os comandos de validação aplicáveis e informar exatamente onde foram executados.
- Revisar o diff antes de encerrar e separar falhas novas de pendências preexistentes.
- Preservar mudanças locais do usuário e evitar edições destrutivas.

## Operação no VS Code

- Trabalhe no repositório local e na branch declarada pelo manifesto.
- Use as tasks `KB: validar consistência`, `KB: validar gates` e `KB: rodar testes` para reproduzir os comandos canônicos.
- Use `KB: publicar run` somente após revisão e aprovação exigidas pelo risco.
- Não configure caminhos absolutos específicos de máquina ou checkout.

## Limites

- Não publique nem faça merge sozinho.
- Não aprove o próprio diff.
- Não alegue execução de CI remoto quando somente testes locais foram executados.
- Não altere scripts, schemas, ledger, KBs ou CI sem autorização explícita no manifesto e na fase corrente.
- Pare e peça decisão humana quando houver exclusão, conflito semântico ou mudança arquitetural não autorizada.
