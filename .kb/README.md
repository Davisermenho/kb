# Artefatos do Fluxo V2

- `runs/<RUN_ID>/manifest.json`: escopo e estado inicial.
- `runs/<RUN_ID>/draft.md`: rascunho não canônico.
- `runs/<RUN_ID>/validation.json`: relatório dos gates.
- `runs/<RUN_ID>/review.json`: revisão vinculada ao diff.
- `locks/`: locks transitórios, não versionados.

Rascunhos nunca são conhecimento publicado. A existência de um `RUN_ID` não autoriza operações fora do manifesto.
