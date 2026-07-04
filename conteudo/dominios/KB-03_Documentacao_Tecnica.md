# KB-03 — Documentação Técnica

## Escopo
Conhecimento Permanente. Manual, norma, documentação técnica, critérios de aceite, rastreabilidade ou template — organiza instruções, registros, guias, governança ou documentação.

## Regras de uso deste arquivo
Este arquivo só deve ser editado seguindo o Passo 6 de `governanca/PROTOCOLO.md` (escrita idempotente): um bloco novo por `ID_FONTE`, nunca sobrescrevendo o arquivo inteiro. Ao editar um `ID_FONTE` já existente, atualize o bloco correspondente em vez de duplicá-lo.

Formato de bloco (um por fonte registrada):

```
### <ID_FONTE> — <Título da fonte>
- Nível de confiança: <Fonte forte / média / fraca>
- Conteúdo extraído: <regra, critério, conceito ou instrução acionável>
- Aplicação: <como isso orienta o agente>
- Limitações: <se houver>
- Última atualização: <data>
```

## Registros

### FONTE-2026-GITLAB-RUNBOOKS — GitLab Runbooks ("Runbooks for the stressed on-call")
- Nível de confiança: Fonte forte (18/21)
- Conteúdo extraído: Repositório MIT mantido pela GitLab.com desde 2016 (~24.583 commits). Estrutura real (confirmada via API, não README): cada serviço tem uma pasta em `docs/<serviço>/` com um arquivo `.md` por procedimento/alerta — ex. `docs/patroni/` tem 60 runbooks individuais. Dois templates formais (`template-alert-playbook.md`, `template-service-overview.md`) padronizam novos runbooks. `on-call/` é separado e contém checklists de plantão, não runbooks técnicos.
- Aplicação: Benchmark de convenção de documentação técnica — o padrão "pasta por serviço, arquivo por procedimento, template formal" é um exemplo real de vínculo rastreável entre alerta/sintoma e procedimento de correção, aplicável a qualquer sistema de runbooks ou documentação operacional.
- Limitações: Estrutura verificada, não o conteúdo de cada arquivo individual. Duas camadas de achado: (1) uma extração via WebFetch do README produziu nomes de pasta que pareciam inventados; (2) ao conferir o README real (baixado pelo usuário) contra a API, confirmei que `troubleshooting/`, `howto/`, `certificates/`, `monitoring/` de fato aparecem no texto — mas como ~10 links de topo quebrados (404), remanescentes de uma reorganização para dentro de `docs/`. Ou seja: até a fonte primária genuína tem links obsoletos. Nunca citar um link ou runbook específico do README sem verificar o path real primeiro.
- Última atualização: 2026-07-02

### FONTE-2024-COMMONMARK-SPEC — CommonMark Spec, seção 1.2 "Why is a spec needed?"
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: Especificação técnica oficial (versão 0.31.2, 2024-01-28, John MacFarlane) que documenta explicitamente por que uma norma formal foi necessária: a descrição original de Markdown era ambígua em pontos concretos (indentação de listas, linhas em branco obrigatórias, precedência de estruturas inline), e diferentes implementações resolviam isso de formas divergentes, causando renderização inconsistente do mesmo documento em sistemas diferentes.
- Aplicação: Exemplo de boa prática de documentação técnica — declarar explicitamente, com casos concretos, por que uma especificação formal existe e quais ambiguidades ela resolve, em vez de apenas impor regras sem justificativa.
- Limitações: Extração restrita à seção de motivação (1.2), não à gramática formal completa da spec.
- Última atualização: 2026-07-02

### FONTE-2004-DARINGFIREBALL-MARKDOWN-SYNTAX — Markdown: Syntax (+ Basics + License)
- Nível de confiança: Fonte forte (20/21)
- Conteúdo extraído: Documento original completo (John Gruber, 17 Dec 2004, v1.0.1): filosofia ("readability is emphasized above all else"), todas as regras de bloco (parágrafos, headers Setext/atx, blockquotes aninháveis, listas ordenadas/não-ordenadas com regra de "tightness" por linha em branco, blocos de código, regra horizontal) e span (links inline/reference, ênfase, code span, imagens — sem suporte a dimensão de imagem por design). A página `basics` é a mesma sintaxe em formato tutorial curto; a página `license` confirma licença BSD de 3 cláusulas, copyright 2004. O documento admite duas limitações conhecidas explicitamente: um bug real no Markdown.pl 1.0.1 (aspas simples em título de link não funcionam) e a ausência deliberada de sintaxe para tamanho de imagem.
- Aplicação: Fonte histórica primária que confirma, com exemplos concretos, as afirmações sobre ambiguidade feitas pela CommonMark Spec. O modelo de documentação em duas camadas (tutorial curto + referência completa, cross-linked) é uma estratégia geral aplicável a qualquer documentação técnica que precise atender tanto iniciantes quanto uso avançado.
- Limitações: Prosa informal, não gramática formal — por isso é ambígua em vários pontos, conforme já documentado por `FONTE-2024-COMMONMARK-SPEC`, e agora confirmado com casos concretos. Datado de 2004; hoje superado por variantes (GFM, CommonMark) para uso prático.
- Última atualização: 2026-07-02

### FONTE-2026-STRIPE-API-DOCS — Stripe API Reference completo (overview, versioning, errors, mapa de 91 recursos, llms.txt, 4 Agent Skills + 6 referências)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: API REST com URL base `https://api.stripe.com`; sandboxes isolam de dados reais; sem atualização em lote. Versionamento data+codinome (`2026-06-24.dahlia`) com regra própria por SDK. Erros: tabela de status HTTP, taxonomia de 4 tipos, objeto de erro rico. A barra lateral da API Reference confirma **91 categorias de recursos de topo** (Charges, Customers, Payment Intents, Products, Invoices, Subscriptions, Accounts, Transfers etc.), confirmando concretamente a escala de "centenas de endpoints". As 6 referências internas de `stripe-best-practices` (billing, connect, payments, security, tax, treasury) seguem todas o mesmo padrão: tabela de roteamento + seção "Traps to avoid" com tabelas de migração API-deprecada→atual.
- Aplicação: Benchmark de documentação técnica de API madura — versionamento data+codinome com regra por SDK, objeto de erro com campos acionáveis que apontam de volta para mais contexto, e um padrão geral de "referência por domínio + tabela de armadilhas comuns + tabela de migração" aplicável a qualquer documentação técnica de sistema complexo.
- Limitações: Cobertura agora inclui o mapa completo de categorias e as 6 referências internas. Não lido: o conteúdo detalhado de cada um dos ~91 recursos individuais.
- Última atualização: 2026-07-03

### FONTE-2026-TWILIO-API-DOCS — Twilio Docs: General Usage + Building with AI (Twilio Skills, MCP server)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: `/docs/usage` é a página guarda-chuva de gestão de conta via REST API — quickstarts por produto, setup de ambiente por linguagem (C#, Java, Node, PHP, Python, Ruby, Go), gestão de API keys/subcontas/access tokens, e guia de segurança/anti-fraude com validação de requisições assinadas por linguagem.
- Aplicação: Benchmark de documentação de onboarding multi-linguagem organizada por tarefa (setup, gestão de conta, segurança) em vez de por endpoint.
- Limitações: Extração cobriu só a página de usage geral, não o restante da documentação de produtos específicos (SMS, Voice, Verify etc.).
- Última atualização: 2026-07-03

### FONTE-2017-GOOGLE-SRE-POSTMORTEM-CULTURE — Site Reliability Engineering, Cap. 13 "Emergency Response" + Cap. 14 "Managing Incidents" + Cap. 15 "Postmortem Culture" + Apêndice D "Example Postmortem"
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: O Apêndice D dá um template de postmortem completo — Date/Authors/Status/Summary/Impact/Root Causes/Trigger/Resolution/Detection, Action Items (Ação/Tipo/Owner/Bug-status), Lessons Learned, Timeline. O Cap. 14 descreve o "Live Incident State Document" — documento vivo, editável concorrentemente, template-based, info mais importante no topo — comparável à nossa `conteudo/FONTES_REGISTRADAS.md`. O Cap. 13 traz 3 casos reais de emergência, cada um com a mesma estrutura Details/Response/Findings.
- Aplicação: Benchmark de template de documentação de incidente/decisão técnica com rastreabilidade completa (causa, ação, dono, status). O "Live Incident State Document" — documento vivo, editável concorrentemente, template-based, informação mais importante no topo — é um modelo geral para qualquer ledger ou registro operacional compartilhado.
- Limitações: O incidente do Apêndice D ("Shakespeare Sonnet++") é fictício/humorístico; os 3 casos do Cap. 13 são apresentados como reais, sem nomes fictícios. Capítulos de 2017; ferramentas internas citadas (Google Docs, IRC) são datadas, mas os princípios permanecem padrão da indústria.
- Última atualização: 2026-07-03

### FONTE-2026-GITLAB-HANDBOOK — The GitLab Handbook (homepage + About the Handbook + Values/CREDIT)
- Nível de confiança: Fonte forte (21/21)
- Conteúdo extraído: "About the Handbook" documenta metodologia de contagem 100% reproduzível (comando shell exato para contar palavras/páginas, comando git para recuperar versão histórica), changelog via merge request, e uma série histórica real mostrando o handbook crescendo de 298.806 palavras (2018) a um pico de 5.129.952 (2025-01-03) e depois **encolhendo** para 3.966.332 (2026-07-03) — poda deliberada, não só crescimento.
- Aplicação: Modelo geral de documentação-como-código com metodologia de auditoria totalmente reproduzível (comandos exatos, não descrição vaga). A contração recente do handbook (queda de ~1,17M palavras em 6 meses) é evidência de que documentação viva madura precisa de poda ativa, não só revisão — não só cresce, também precisa encolher.
- Limitações: Extração cobriu a homepage e "About the Handbook" completos, mas só a introdução da página "Values" (~99KB no total, 6 valores, só 1 lido em detalhe). Não cobre páginas técnicas mais profundas citadas (Style Guide, Escalation, etc.), só títulos.
- Última atualização: 2026-07-03
