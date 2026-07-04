# Base de Conhecimento

Este repositório mantém fontes rastreáveis, conhecimento condensado por domínio e
as ferramentas que validam o fluxo de publicação.

## Por onde começar

1. Leia o [protocolo operacional](governanca/PROTOCOLO.md).
2. Consulte a [arquitetura e matriz de roteamento](governanca/REGISTRO_FONTES.md).
3. Preencha o [template de fonte](governanca/TEMPLATE.md) em um run de trabalho.

## Estrutura

- `conteudo/FONTES_REGISTRADAS.md`: ledger canônico das fontes publicadas.
- `conteudo/dominios/`: conhecimento geral reutilizável (`KB-01` a `KB-06`).
- `conteudo/projetos/`: conhecimento específico dos projetos (`KB-PROJ-*`).
- `governanca/`: protocolo, arquitetura, template e contrato de validação.
- `ferramentas/`: checker, gates de auditoria e workflow de publicação.
- `planos/`: planos de evolução e registros de implementação.
- `.kb/`: estado operacional, runs, revisões e locks.
- `tests/`: testes automatizados.

## Comandos

```bash
python3 ferramentas/check_kb_consistency.py .
python3 ferramentas/kb_validate.py .
python3 ferramentas/kb_workflow.py --directory . <comando>
python3 -m unittest discover -s tests -v
```

Os validadores verificam estrutura e consistência interna. Eles não substituem a
revisão factual, semântica e humana definida no protocolo.
