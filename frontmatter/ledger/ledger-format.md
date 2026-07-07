# Ledger de origem, decisão e destino

O ledger registra cada transição relevante do documento no pipeline.

## Modelo conceitual

- Origem: de onde veio o dado ou documento.
- Decisão: o que o pipeline decidiu e com base em qual regra.
- Destino: para onde o resultado foi enviado.
- Proveniência: qual pipeline, parser, versão e hash participaram do evento.

## Formato recomendado

Use JSON Lines (`.jsonl`), um evento por linha.

Vantagens:

- append-only;
- fácil de validar linha por linha;
- fácil de auditar;
- funciona bem em CI;
- evita reescrever um JSON gigante;
- adequado para logs assináveis ou encadeados por hash.

## Exemplo

```json
{"ledger_version":"1.0","event_id":"evt_...","event_type":"metadata_validated","occurred_at":"2026-07-07T08:28:33Z","actor":{},"source":{},"decision":{},"destination":{},"provenance":{}}
```

## Campos essenciais

- `source.checksum_sha256`: prova qual conteúdo foi processado.
- `decision.status`: accepted, rejected ou warning.
- `decision.rule_set`: qual regra foi aplicada.
- `destination.kind`: artefato, índice, página publicada ou relatório.
- `provenance.previous_event_hash`: encadeia eventos.
- `provenance.event_hash`: hash do evento canônico.

## Arquivo final recomendado

```text
ledgers/source-ledger.jsonl
```
