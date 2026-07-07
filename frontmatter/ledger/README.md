# Provenance Ledger Pack

Este pacote contém um modelo pronto de ledger append-only para registrar origem, decisão e destino no pipeline de documentos.

## Arquivos

- `source-ledger-event.schema.json`: contrato JSON Schema para cada evento do ledger.
- `source-ledger.example.jsonl`: exemplo de ledger em JSON Lines.
- `append-ledger-event.mjs`: script para gerar um evento novo e anexar ao ledger.
- `validate-ledger.mjs`: script para validar o ledger.
- `ledger-format.md`: explicação do formato.

## Local real neste projeto

```text
frontmatter/ledger/source-ledger.jsonl (gerado por append-ledger-event.mjs; não versionar como exemplo estático)
frontmatter/ledger/source-ledger.example.jsonl (exemplo ilustrativo, estático)
frontmatter/ledger/source-ledger-event.schema.json
frontmatter/ledger/append-ledger-event.mjs
frontmatter/ledger/validate-ledger.mjs
```

## Regra operacional

O ledger deve ser append-only. Não edite eventos antigos. Para corrigir um erro, adicione um novo evento de correção ou rejeição.
