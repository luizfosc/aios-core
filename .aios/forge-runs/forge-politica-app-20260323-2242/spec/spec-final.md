# Spec Final Consolidada — politica-app

> **Motor de Predicao por Inteligencia de Enxame para Simulacao de Opiniao Publica**

| Campo | Valor |
|-------|-------|
| **Produto** | politica-app |
| **Tipo** | AIOS Skill (markdown-driven, sem codigo compilavel) |
| **Localizacao** | `skills/politica-app/` |
| **Versao Spec** | v1.1 — corrigida por QA (3 CRITs + 3 RECs) |
| **Data** | 2026-03-23 |
| **Run ID** | forge-politica-app-20260323-2242 |
| **Complexidade** | STANDARD (14/25) |
| **Esforco Estimado** | 2-3 dias de trabalho efetivo |
| **Fontes** | PRD (Morgan), Arquitetura (Aria), Research (Atlas) |

---

## 1. Sumario Executivo

O **politica-app** e um motor de predicao que usa inteligencia de enxame para simular opiniao publica sobre temas politicos. O sistema cria um painel virtual de agentes AI — cada um representando um perfil demografico e psicografico distinto do eleitorado brasileiro — e os coloca para "deliberar" sobre um tema em multiplas rodadas. O agregado dessas opinioes simuladas gera um relatorio com distribuicao de sentimento, argumentos-chave, vulnerabilidades narrativas e recomendacoes estrategicas. O publico-alvo sao consultores politicos e assessores de campanha que precisam antecipar reacoes publicas rapidamente e a custo baixo, sem depender de pesquisas tradicionais que custam R$50-200k e levam semanas. O diferencial competitivo e a parametrizacao de vieses cognitivos — nenhum concorrente atual expoe isso como configuracao — e o foco exclusivo no contexto politico-eleitoral brasileiro.

---

## 2. Visao do Produto

### 2.1 Problema

Consultores politicos e politicos tomam decisoes de campanha baseados em pesquisas de opiniao tradicionais que sao **caras** (R$50-200k por pesquisa quantitativa), **lentas** (2-4 semanas de campo + analise) e **estaticas** (retratam um momento, nao simulam cenarios). Alem disso, pesquisas tradicionais medem o que as pessoas **dizem** que pensam, nao como **formariam** suas opinioes diante de novos estimulos.

### 2.2 Solucao

O politica-app cria um "painel virtual" de agentes AI com perfis cognitivos diversos (vieses, valores, fontes de informacao, nivel educacional, classe social) e os faz deliberar sobre um tema politico em rodadas. Isso captura a complexidade da formacao de opiniao real, onde pessoas diferentes chegam a conclusoes diferentes a partir das mesmas informacoes.

### 2.3 Proposta de Valor

| Dimensao | Valor |
|----------|-------|
| **Velocidade** | Simulacao completa em minutos, nao semanas |
| **Custo** | Fracao do custo de pesquisa tradicional (apenas API calls) |
| **Cenarios** | Permite testar "e se?" — como a opiniao mudaria se tal fato viesse a tona? |
| **Profundidade** | Nao apenas "a favor/contra", mas argumentos, narrativas e vulnerabilidades |
| **Iteracao** | Roda quantas vezes quiser, ajustando parametros entre simulacoes |

### 2.4 Usuarios-Alvo

**Persona Primaria: Consultor Politico** — Gerencia estrategia de comunicacao de candidatos. Precisa antecipar reacao publica a posicionamentos e crises. Nivel tecnico baixo a medio; usa o sistema via assistente tecnico que opera o CLI. Valor esperado: relatorio com distribuicao de sentimento + argumentos-chave + recomendacoes estrategicas.

**Persona Secundaria: Politico / Assessor Direto** — Precisa decidir posicionamento sobre temas polemicos. Nivel tecnico baixo; consome o relatorio em markdown/PDF. Valor esperado: mapa de riscos e oportunidades por segmento do eleitorado.

[AUTO-DECISION] "O MVP precisa de interface grafica?" -> Nao. O produto roda como AIOS Skill via CLI. Output e relatorio markdown. Razao: alinhado com restricoes tecnicas (AIOS Skill, sem web UI) e filosofia CLI First do AIOS.

---

## 3. Arquitetura

### 3.1 Visao Geral do Sistema

```
[Input]          [Assembly]         [Deliberation]       [Aggregation]      [Report]
                                    +-----------+
User prompt  ->  Gerar N perfis -> | Agent 1   | ->     Calcular         -> Markdown
+ contexto       via template      | Agent 2   |        metricas            report
+ preset                           | Agent 3   |        + vulnerab.
                                   | ...       |        + clusters
                                   | Agent N   |
                                   +-----------+
```

**Padrao arquitetural:** Pipeline Sequencial com Fan-Out Paralelo.

O politica-app e uma AIOS Skill markdown-driven. Nao ha codigo compilavel — o "motor" e um conjunto de templates de prompt e arquivos YAML orquestrados pelo Claude Code via o SKILL.md como entry point. Cada fase e um modulo logico materializado como um template markdown.

### 3.2 Principios Arquiteturais

| Principio | Aplicacao |
|-----------|-----------|
| **File-based state** | Todo estado persiste em YAML. Sem banco, sem memoria volatil. Cada rodada grava checkpoint |
| **Template-driven** | Comportamento definido por templates markdown. Mudanca de comportamento = editar template |
| **Parallel fan-out** | Agentes do painel sao independentes dentro de cada rodada. Spawned em paralelo via Agent tool |
| **Checkpoint recovery** | Cada fase grava output antes de avancar. Se falhar, retoma do ultimo checkpoint |
| **Composicao por preset** | Composicao demografica externalizada em YAML. Novos cenarios = novo preset |
| **Separacao de concerns** | Cada template tem responsabilidade unica |

### 3.3 Modulos e Responsabilidades

| Modulo | Responsabilidade | Inputs | Outputs |
|--------|-----------------|--------|---------|
| **Assembly** | Ler preset, gerar perfis de agentes, salvar painel | preset YAML + config | `panel.yaml` |
| **Deliberation** | Conduzir rodadas de deliberacao (spawn agentes, capturar respostas) | `panel.yaml` + tema + contexto | `rounds/round-N.yaml` |
| **Summarizer** | Condensar argumentos entre rodadas | `round-N.yaml` | sumario para injecao |
| **Aggregation** | Calcular metricas: sentimento, impacto, vulnerabilidades, clusters | todos `round-*.yaml` | `aggregation.yaml` |
| **Report** | Gerar relatorio final legivel por nao-tecnicos | `aggregation.yaml` + `panel.yaml` | `report.md` |

### 3.4 Fluxo de Dados End-to-End

```
ENTRADA
  |
  +-- Tema/pergunta (string)
  +-- Preset demografico (YAML)
  +-- Contexto opcional (markdown/text)
  |
  v
FASE 1: ASSEMBLY
  | Ler preset -> gerar perfis -> salvar panel.yaml
  | Template: templates/agent-persona.md
  | Output: output/{run}/panel.yaml
  |
  v
FASE 2: DELIBERACAO
  | Para cada rodada R de 1 a N:
  |   Se R == 1: spawn agentes com (perfil + tema + contexto)
  |   Se R > 1:  sumarizar rodada anterior -> spawn com (perfil + tema + contexto + sumario)
  |   Capturar outputs -> salvar round-R.yaml
  |   Output: output/{run}/rounds/round-R.yaml
  |
  v
FASE 3: AGREGACAO
  | Ler todos round-R.yaml
  | Calcular: distribuicao, intensidade, ranking, vulnerabilidades, clusters
  | Output: output/{run}/aggregation.yaml
  |
  v
FASE 4: RELATORIO
  | Ler aggregation.yaml + panel.yaml
  | Gerar relatorio via template
  | Output: output/{run}/report.md
  |
  v
SAIDA
  +-- report.md (relatorio final legivel)
  +-- panel.yaml (perfis para reuso)
  +-- rounds/round-*.yaml (dados brutos)
  +-- aggregation.yaml (metricas)
```

### 3.5 Estrutura de Arquivos da Skill

```
skills/politica-app/
+-- SKILL.md                        # Entry point — orquestracao completa
+-- config.yaml                     # Configuracao padrao
|
+-- presets/                         # Presets de composicao demografica
|   +-- brasil-geral.yaml            #   20 agentes, composicao nacional
|   +-- sp-capital.yaml              #   20 agentes, foco SP capital
|   +-- nordeste-evangelico.yaml     #   20 agentes, foco nordeste + evangelico
|   +-- custom-template.yaml         #   Template para preset customizado
|
+-- templates/                       # Templates de prompt
|   +-- agent-persona.md             #   System prompt de cada agente
|   +-- deliberation-round-1.md      #   Prompt da rodada 1 (individual)
|   +-- deliberation-round-n.md      #   Prompt das rodadas 2+ (com exposicao)
|   +-- summarizer.md                #   Prompt de sumarizacao inter-rodada
|   +-- aggregator.md                #   Prompt de agregacao de metricas
|   +-- report-template.md           #   Template do relatorio final
|   +-- recommendations.md           #   Prompt para gerar recomendacoes
|
+-- data/                            # Dados de referencia
|   +-- cognitive-biases.yaml        #   Catalogo de vieses (Munger)
|   +-- influence-principles.yaml    #   Principios de influencia (Cialdini)
|   +-- demographic-archetypes.yaml  #   Arquetipos demograficos base
|
+-- output/                          # Outputs das simulacoes
|   +-- {YYYYMMDD-HHMM}-{slug}/     #   Uma pasta por simulacao
|       +-- report.md                #     Relatorio final
|       +-- panel.yaml               #     Perfis dos agentes (reusavel)
|       +-- config-snapshot.yaml     #     Config usada nesta simulacao
|       +-- rounds/                  #     Dados brutos por rodada
|       |   +-- round-1.yaml
|       |   +-- round-2.yaml
|       |   +-- round-3.yaml
|       +-- aggregation.yaml         #     Metricas agregadas
|
+-- README.md                        # Documentacao tecnica
```

### 3.6 Swarm Engine Design

O enxame e um padrao de orquestracao de sub-agentes do Claude Code. Cada "agente do painel" e um sub-agente spawned via a ferramenta `Agent` com um system prompt unico que encapsula o perfil cognitivo da persona.

**Ciclo de vida de um agente:**

```
1. SPAWN      ->  Agent tool com system prompt do perfil
2. PROMPT     ->  Recebe tema + contexto + (argumentos anteriores, se rodada > 1)
3. RESPOND    ->  Retorna opiniao estruturada (YAML inline)
4. CAPTURE    ->  Output parseado e salvo no round-N.yaml
5. TERMINATE  ->  Agente morre apos responder (stateless entre rodadas)
```

**Estrategia de paralelismo:**
- Rodada 1: spawn agentes 1-N em paralelo (sem dependencia)
- Rodada 2+: sumarizar argumentos (sequencial) -> spawn agentes em paralelo com sumario injetado
- **Batching:** Para paineis >20 agentes, dividir em batches de 10 para evitar sobrecarga

**Tratamento de falhas:**

| Cenario | Comportamento |
|---------|---------------|
| Output malformado | Tentar parse; se falhar, marcar como `status: error` e continuar |
| Timeout de agente | Registrar como `status: timeout`; nao bloquear rodada |
| >30% de falhas na rodada | Abortar e alertar usuario; oferecer retry |
| Falha entre rodadas | Retomar do ultimo round-N.yaml salvo |

### 3.7 Sistema de Personas

Cada agente tem perfil cognitivo completo:

```yaml
id: agent-007
name: "Dona Maria"
demographic:
  age: 58
  gender: feminino
  region: interior-sp
  class: C
  education: fundamental-completo
  religion: evangelica
  occupation: costureira-autonoma

psychographic:
  values: [familia, fe, seguranca-financeira, ordem]
  priorities: [custo-de-vida, saude, seguranca-publica]
  information_sources: [tv-aberta, whatsapp-familia, igreja]
  cognitive_biases:
    - authority_bias
    - status_quo_bias
    - in_group_bias
  influence_susceptibility:
    social_proof: alto
    authority: alto
    scarcity: medio
    reciprocity: alto

deliberative:
  processing_style: emocional
  opinion_flexibility: baixa
  argument_weight: experiencia
  expression_style: anedotico
```

**Vieses cognitivos (Munger):** authority_bias, status_quo_bias, in_group_bias, doubt-avoidance, inconsistency-avoidance, social_proof, contrast_misreaction, reward/punishment.

**Principios de influencia (Cialdini):** reciprocidade, compromisso/consistencia, prova social, autoridade, escassez, afinidade.

### 3.8 Modelo de Formacao de Opiniao

```
Rodada 1: FORMACAO INDIVIDUAL
  Cada agente forma opiniao SEM ver outros
  Input: perfil + tema + contexto
  Output: posicao + intensidade + argumentos

Rodada 2: EXPOSICAO E REVISAO
  Cada agente recebe SUMARIO dos argumentos da rodada anterior
  Input: perfil + tema + contexto + sumario-argumentos
  Output: posicao (pode mudar) + intensidade + argumentos + flag_mudanca

Rodada 3: CONSOLIDACAO
  Cada agente recebe sumario ATUALIZADO + distribuicao de sentimento
  Input: perfil + tema + contexto + sumario + distribuicao
  Output: posicao final + intensidade final + argumento definitivo
```

A mudanca de opiniao e governada pelo perfil do agente (flexibility, social_proof, authority, processing_style).

### 3.9 Motor de Agregacao

Metricas calculadas em `aggregation.yaml`:

- **Distribuicao de sentimento:** % a favor/contra/neutro/indeciso, geral e por segmento
- **Intensidade:** media por posicao (identifica se "contra" e mais veemente que "a favor")
- **Ranking de argumentos:** por frequencia e por impact_score (formula: `impact_score = count(agentes que citaram o argumento como change_trigger)`) <!-- [FIX-QA-CRIT-1] formula explicita -->
- **Vulnerabilidades:** argumentos com `impact_score >= ceil(0.2 × segment_size)` = ponto fraco narrativo <!-- [FIX-QA-CRIT-1] threshold quantitativo: 20% do segmento -->
- **Clusters:** agrupamento semantico de agentes por similaridade de argumentos (via prompt, nao algoritmico)
- **Dinamica de opiniao:** mudancas entre rodadas com gatilho identificado

---

## 4. Estrutura de Epics

### Epic 1: Fundacao e Geracao de Painel

**Objetivo:** Estabelecer a estrutura da skill e implementar a geracao de paineis de agentes virtuais com perfis cognitivos diversos.

| Story | Titulo | Descricao | Complexidade |
|-------|--------|-----------|--------------|
| 1.1 | Scaffold da Skill | Criar estrutura de diretorios conforme secao 3.5, SKILL.md como entry point com orquestracao basica, config.yaml com defaults, README.md | Baixa |
| 1.2 | Gerador de Perfis de Agentes | Implementar template `agent-persona.md` que transforma perfil YAML em system prompt. Incluir vieses de Munger e principios de Cialdini como parametros. Criar `data/cognitive-biases.yaml` e `data/influence-principles.yaml` | Media |
| 1.3 | Presets Demograficos | Criar 3 presets iniciais (`brasil-geral`, `sp-capital`, `nordeste-evangelico`) + template customizado. Composicao inspirada em dados IBGE/TSE (nao precisa ser estatisticamente exata no MVP) | Media |
| 1.4 | Validacao de Painel | Dry-run de geracao de painel com 10 agentes usando preset `brasil-geral`. Validar diversidade e qualidade dos perfis gerados. Criterio: nenhum par de agentes deve ter perfil identico | Baixa |

**Estimativa:** 4 stories, complexidade media

---

### Spike: Validacao de Prompt Engineering

**Objetivo:** Validar que agentes com perfis diversos produzem opinioes genuinamente diferentes. Este spike e **pre-requisito obrigatorio** para o Epic 2.

| Atividade | Descricao | Criterio de Sucesso |
|-----------|-----------|---------------------|
| Teste de diversidade | Rodar 5 agentes com perfis contrastantes (ex: jovem progressista vs. idoso conservador) sobre tema polemico | Opinioes devem divergir claramente; pelo menos 3 posicoes distintas |
| Teste de vies do LLM | Verificar se agentes "conservadores" realmente expressam opinioes conservadoras (nao apenas uma versao "educada" do progressismo) | Agentes com bias conservador devem usar argumentos genuinamente conservadores |
| Teste de linguagem | Verificar se classe C/D usa linguagem diferente de classe A/B | Registros linguisticos visivelmente distintos |
| **Teste de paralelismo** <!-- [FIX-QA-REC-3] --> | Rodar exatamente 10 sub-agentes simultaneos via Agent tool e medir wall-clock total. Comparar com execucao sequencial dos mesmos 10 agentes | Wall-clock do paralelo deve ser < 2× o wall-clock do agente mais lento; documentar tempo absoluto em segundos para dimensionar batches dos Epics 2 e 3 |
| Ajuste de prompts | Com base nos resultados, ajustar template de persona para maximizar diversidade | Documentar ajustes feitos |

**Estimativa:** 1 dia de trabalho

---

### Epic 2: Motor de Deliberacao

**Objetivo:** Implementar o core da simulacao — as rodadas de deliberacao onde agentes formam e revisam opinioes.

| Story | Titulo | Descricao | Complexidade |
|-------|--------|-----------|--------------|
| 2.1 | Rodada 1: Opiniao Individual | Template `deliberation-round-1.md` para formacao de opiniao individual. Spawn de agentes via Agent tool em paralelo (batches de 10). Captura de output estruturado YAML. Salvamento em `round-1.yaml` | Alta |
| 2.2 | Sumarizacao Inter-Rodada | Template `summarizer.md` executado pelo agente principal (nao sub-agente). Agrupa argumentos por posicao, rankeia por frequencia, mantem top 5 por posicao. Inclui distribuicao percentual | Media |
| 2.3 | Rodadas 2+: Deliberacao com Exposicao | Template `deliberation-round-n.md` com sumario + distribuicao injetados. Deteccao de mudanca de opiniao (`opinion_changed`, `change_trigger`, `previous_position`). Mesmo mecanismo de spawn paralelo | Alta |
| 2.4 | Orquestrador de Simulacao | Pipeline completo no SKILL.md: input -> assembly -> rodadas -> output. Progresso visual ("Rodada 2/3 — Agente 15/20"). Tratamento de falhas (threshold de 30%). Checkpoints entre rodadas | Alta |
| 2.5 | Dry-Run End-to-End | Simulacao completa com 10 agentes e 2 rodadas. Validacao do pipeline inteiro: assembly funciona, deliberacao gera dados estruturados, checkpoints salvam corretamente | Media |

**Estimativa:** 5 stories, complexidade alta

---

### Epic 3: Agregacao e Relatorio

**Objetivo:** Transformar os dados brutos da deliberacao em insights acionaveis via relatorio estruturado.

| Story | Titulo | Descricao | Complexidade |
|-------|--------|-----------|--------------|
| 3.1 | Engine de Agregacao | Template `aggregator.md` que le todos `round-*.yaml` e calcula: distribuicao de sentimento (geral + por segmento), intensidade media, ranking de argumentos por frequencia e `impact_score` (`count(change_triggers)` por argumento), vulnerabilidades (threshold: `ceil(0.2 × segment_size)`), clusters semanticos (min 3 agentes) <!-- [FIX-QA-CRIT-1] formula do impact_score e threshold de vulnerabilidade explicitados aqui --> | Alta |
| 3.2 | Template de Relatorio | `report-template.md` com todas as secoes: sumario executivo, dashboard de sentimento, mapa de argumentos, vulnerabilidades, dinamica de opiniao, recomendacoes, metodologia + disclaimer etico. Tom: consultor de campanha, sem jargao de AI | Media |
| 3.3 | Gerador de Recomendacoes | Template `recommendations.md` que transforma dados agregados em 3-5 recomendacoes estrategicas contextualizadas. Cada recomendacao com: acao, justificativa, segmento-alvo, urgencia | Media |
| 3.4 | Ingestao de Contexto | Pipeline de leitura e processamento de documentos de contexto opcionais (pesquisas existentes, noticias, posts, docs de campanha) para enriquecer os prompts dos agentes. **Nota arquitetural:** cada documento de contexto deve ser sumarizado para ≤500 palavras antes de ser injetado nos prompts dos agentes — sem isso, documentos longos consomem context window e limitam o numero de agentes paralelizaveis por batch <!-- [FIX-QA-REC-2] restricao de sumarizacao de contexto adicionada --> | Media |
| 3.5 | Simulacao Completa de Validacao | Simulacao realista: 20 agentes, 3 rodadas, com contexto ingerido. <!-- [FIX-QA-CRIT-3] Cenario canonico de teste: tema fixo "Proposta de reducao da maioridade penal para 16 anos" + contexto minimo: 2 noticias recentes (max 300 palavras cada) — serve como benchmark qualitativo comparavel entre iteracoes da skill. --> ACs mensuráveis: (a) `report.md` gerado com todas as secoes de FR19 (sumario, dashboard, argumentos, vulnerabilidades, recomendacoes, metodologia); (b) `aggregation.yaml` contem pelo menos 10 argumentos unicos (NFR4); (c) pelo menos 2 segmentos demograficos com distribuicao de sentimento distinta (diferenca >= 20pp entre segmentos); (d) nenhum agente tem posicao final identica ao agente imediatamente anterior na ordem de processamento. Review qualitativo adicional: as recomendacoes sao acionaveis? Os argumentos sao plausíveis dentro do perfil demografico? <!-- [FIX-QA-CRIT-2] ACs mensuráveis adicionados --> | Media |

**Estimativa:** 5 stories, complexidade media-alta

---

### Epic 4: Refinamento e Reutilizacao

**Objetivo:** Permitir cenarios comparativos, reutilizacao de paineis e polish para uso em producao.

| Story | Titulo | Descricao | Complexidade |
|-------|--------|-----------|--------------|
| 4.1 | Reutilizacao de Paineis | Carregar `panel.yaml` de simulacao anterior via path. Validar integridade dos perfis. Permitir rodar nova simulacao com mesmo painel mas tema diferente | Baixa |
| 4.2 | Cenarios Comparativos | Rodar multiplas simulacoes com mesmo painel + perguntas diferentes. Gerar relatorio comparativo mostrando deltas entre cenarios | Media |
| 4.3 | Composicao Customizada | Instrucoes no SKILL.md para criar preset demografico customizado sem usar os predefinidos. Template `custom-template.yaml` como guia | Baixa |
| 4.4 | Polish de Relatorio | Refinamento do template com base em feedback. Disclaimer etico mais robusto. Secao de metodologia expandida. Formatacao otimizada para impressao/PDF | Baixa |

**Estimativa:** 4 stories, complexidade baixa-media

---

## 5. Requisitos Funcionais

### Configuracao de Simulacao

- **FR1:** Permitir configurar tema/pergunta via argumento CLI ou prompt interativo
- **FR2:** Aceitar documentos de contexto opcionais (markdown, texto, YAML) como input adicional
- **FR3:** Permitir selecionar presets demograficos (`brasil-geral`, `sp-capital`, `nordeste-evangelico`) ou composicao customizada
- **FR4:** Permitir configurar numero de agentes no painel (padrao: 20, range: 10-50)
- **FR5:** Permitir configurar numero de rodadas de deliberacao (padrao: 3, range: 1-5)

### Geracao de Agentes

- **FR6:** Gerar perfis de agentes com atributos demograficos e psicograficos distintos, seguindo a composicao do preset
- **FR7:** Cada agente deve ter system prompt unico encapsulando perfil cognitivo, vieses e fontes de informacao
- **FR8:** Aplicar modelos mentais de Munger (vieses cognitivos) e principios de Cialdini na construcao dos perfis
- **FR9:** Armazenar perfis gerados em `panel.yaml` para auditoria e reuso

### Deliberacao

- **FR10:** Conduzir rodadas de deliberacao com cada agente spawned como sub-agente via Agent tool
- **FR11:** Na rodada 1, cada agente forma opiniao individual sem exposicao a outros
- **FR12:** Nas rodadas 2+, cada agente recebe sumario dos argumentos das rodadas anteriores
- **FR13:** Capturar para cada agente: posicao (a_favor/contra/neutro/indeciso), intensidade (1-5), argumentos principais, flag de mudanca
- **FR14:** Detectar e registrar mudancas de opiniao entre rodadas (qual argumento causou a mudanca)

### Agregacao

- **FR15:** Calcular distribuicao de sentimento geral e por segmento demografico
- **FR16:** Rankear argumentos por frequencia e por impacto — `impact_score = count(agentes que citaram o argumento como change_trigger)` no campo `change_trigger` dos dados de rodada <!-- [FIX-QA-CRIT-1] formula canonizada -->
- **FR17:** Identificar argumentos-vulnerabilidade: threshold `impact_score >= ceil(0.2 × segment_size)` — ex.: em segmento de 5 agentes, impacto >= 1; em segmento de 10, impacto >= 2 <!-- [FIX-QA-CRIT-1] threshold quantitativo, evita ambiguidade -->
- **FR18:** Identificar clusters de opiniao via analise semantica de argumentos

### Relatorio

- **FR19:** Gerar relatorio final em markdown com todas as secoes (sumario, dashboard, mapa de argumentos, vulnerabilidades, recomendacoes, metodologia)
- **FR20:** Incluir metadados: data, configuracao usada, numero de agentes, rodadas, contexto ingerido
- **FR21:** Salvar relatorio em `skills/politica-app/output/{timestamp}-{slug}/report.md`
- **FR22:** Salvar dados brutos da simulacao em YAML no mesmo diretorio

### Reutilizacao

- **FR23:** Permitir reutilizar paineis de agentes entre simulacoes (carregar perfis de YAML anterior)
- **FR24:** Permitir cenarios comparativos (mesmo painel, perguntas diferentes)

---

## 6. Requisitos Nao-Funcionais

### Performance

- **NFR1:** Simulacao completa (20 agentes, 3 rodadas) em no maximo 15 minutos de wall-clock
- **NFR2:** Paralelizar agentes quando possivel (batches de 10 via Agent tool)
- **NFR3:** Mostrar progresso durante execucao ("Rodada 2/3 — Agente 15/20")

### Qualidade da Simulacao

- **NFR4:** Perfis suficientemente diversos — nenhum segmento demografico relevante ignorado
- **NFR5:** Argumentos plausíveis e ancorados no contexto fornecido, nao alucinacoes genericas
- **NFR6:** Distribuicao de sentimento razoavel (nao 100% para um lado) salvo temas com consenso real

### Confiabilidade

- **NFR7:** Idempotencia relativa — simulacoes com mesma configuracao devem produzir distribuicao de sentimento dentro de ±15pp em pelo menos 80% dos segmentos demograficos <!-- [FIX-QA-REC-1] idempotencia reformulada com metrica quantitativa: antes era qualitativa ("mesma faixa") -->
- **NFR8:** Falhas de agentes individuais nao travam a simulacao inteira
- **NFR9:** Checkpoints entre rodadas para permitir retomada em caso de falha

### Usabilidade

- **NFR10:** SKILL.md auto-documentado — qualquer pessoa que leia entende como rodar
- **NFR11:** Mensagens de erro claras e acionaveis, em portugues
- **NFR12:** Relatorio final legivel por nao-tecnicos (sem jargao de AI/ML)

---

## 7. Restricoes

- **CON-1:** Runtime e AIOS Skill — roda exclusivamente dentro do Claude Code CLI
- **CON-2:** Sem banco de dados — estado persistido via YAML/JSON no filesystem
- **CON-3:** Sem web UI — output e markdown; conversao para PDF e responsabilidade do usuario
- **CON-4:** Sem deploy externo — roda 100% local na maquina do operador
- **CON-5:** Dependencia unica: Claude API via Agent tool — sem dependencias externas adicionais
- **CON-6:** Sem treinamento de modelos — usa prompting e persona engineering
- **CON-7:** Maximo 50 agentes por simulacao (limitado por context window e custo)
- **CON-8:** Output em pt-BR; internals podem ser em ingles
- **CON-9:** Sem package.json proprio — nao e projeto Node.js separado; e conjunto de markdowns e YAMLs
- **CON-10:** Sem testes unitarios tradicionais — validacao por dry-runs com paineis pequenos

---

## 8. Tech Stack

| Tecnologia | Justificativa |
|------------|---------------|
| **Claude Code (AIOS Skill)** | Requisito do projeto; mantem dentro do ecossistema AIOS. Skills sao markdown-driven |
| **YAML** | Persistencia de estado. Mais legivel que JSON para humanos; padrao AIOS; permite edicao manual |
| **Markdown** | Templates de prompt e output. Universal e convertivel |
| **Agent tool (fan-out)** | Unica forma de "paralelismo" no Claude Code. Cada agente do painel e um sub-agente |
| **Analise semantica via prompt** | Clusterizacao e sumarizacao. Sem runtime para algoritmos; LLM faz agrupamento semantico naturalmente |
| **SKILL.md como orquestrador** | Entry point que instrui Claude Code. O "codigo" sao as instrucoes em markdown |
| **Pastas timestamped** | Versionamento de output. Simples, auditavel, sem dependencias |

**Integracoes com ecossistema AIOS:**

| Recurso | Como e Usado | Status |
|---------|-------------|--------|
| Agent tool | Mecanismo principal do enxame (spawn sub-agentes) | Core |
| Read/Write/Edit | Leitura de templates, escrita de outputs | Core |
| Bash | Operacoes simples de parse/sort | Auxiliar |
| WebSearch/WebFetch | Ingestao de contexto adicional (opcional) | Opcional |
| Mind: charlie-munger | Referencia para vieses cognitivos nos perfis | Inspiracao |
| Mind: robert-cialdini | Referencia para principios de influencia | Inspiracao |
| Squad: icp-cloning | Referencia para persona engineering | Inspiracao |
| Skill: deep-research | Pesquisa de contexto pre-simulacao | Futuro |

---

## 9. Insights de Pesquisa

Baseado no research brief de Atlas (@analyst), os achados que impactam diretamente o design:

### CRITICO: Vies Demografico do LLM

LLMs sobre-representam perspectivas liberais, de alta renda e alta escolaridade. Minorias e grupos marginalizados sao sub-representados. Saidas sao "mais educadas, mais longas, mais polidas" que comunicacao humana real. **Impacto no design:** Perfis de agentes devem conter instrucoes fortes e explicitas de vies contrario ao default do LLM. Sem isso, todos os agentes convergem para "opiniao media urbana progressista" — validado na arquitetura como decisao de "diversidade forcada vs. natural".

### CRITICO: Risco de Convergencia de Opiniao

Em revisao de 35 artigos sobre GABMs, 43% validam apenas subjetivamente ("parece convincente"). O risco de construir um sistema que gera resultados homogeneos disfaracados de diversidade e real. **Impacto no design:** Spike obrigatorio de prompt engineering entre Epic 1 e Epic 2. Template de persona com `opinion_flexibility`, `cognitive_biases` e `processing_style` como parametros de primeira classe.

### OPORTUNIDADE: Vieses Cognitivos como Diferenciador

Nenhum dos concorrentes atuais (Aaru, ElectionSim, FlockVote, MiroFish, Signoi) expoe vieses cognitivos como parametros configuraveis. **Impacto no design:** O vetor de vieses por agente e a principal inovacao do produto. Interface principal: cenario + distribuicao demografica + pesos de vieses -> distribuicao de opiniao + delta + explicacao.

### RECOMENDACAO: Modelo Hibrido (LLM para Narrativa + Matematica para Dinamica)

A pesquisa recomenda nao usar LLMs para cada agente em cada tick — isso e ordens de magnitude mais caro que ABMs tradicionais. **Impacto no design:** No contexto de AIOS Skill sem codigo compilavel, a "matematica" e substituida pela logica de sumarizacao e injecao de contexto entre rodadas. O LLM gera perfil (one-shot) e opina (por rodada), mas a dinamica de interacao e controlada pelos templates de deliberacao, nao por simulacao algebrica.

[AUTO-DECISION] "Devemos implementar modelo HK/DW algebrico?" -> Nao. O contexto e AIOS Skill sem codigo compilavel. A dinamica de interacao e aproximada via templates de deliberacao que injetam sumarios e distribuicoes. Isso captura o espirito do HK (bounded confidence) sem requer runtime numerico. Razao: restricao tecnica da plataforma.

### VALIDACAO: Stanford Generative Agents — 85% de Acuracia

O estudo de Stanford (Park et al., 2024) demonstra que agentes LLM replicam respostas humanas com 85% de acuracia quando perfis sao bem construidos com dados qualitativos profundos. Isso valida a abordagem core do politica-app.

### CONTEXTO: Paisagem Competitiva

| Concorrente | Limitacao que o politica-app supera |
|-------------|-------------------------------------|
| Aaru | Caixa-preta, errou eleicao 2024, enterprise-only |
| ElectionSim | Nao disponivel como produto, foco americano |
| FlockVote | Framework de pesquisa, nao produto |
| MiroFish | Sem validacao eleitoral, sem vieses configuraveis |
| Signoi | Foco pesquisa de mercado, nao politico |

**Gaps que o politica-app preenche:** vieses cognitivos configuraveis, acessibilidade para campanhas menores, cenarios "what-if" narrativos, foco em eleicoes brasileiras.

---

## 10. Riscos e Mitigacoes

### Riscos Tecnicos

| Risco | Prob. | Impacto | Mitigacao |
|-------|-------|---------|-----------|
| **Context window overflow** com muitos agentes | Alta | Alto | Limitar a 50 agentes; usar resumos entre rodadas; batches de 10 |
| **Custo de API alto** em simulacoes grandes | Media | Medio | Configuracao de limites; dry-run barato antes de simulacao completa |
| **Agentes convergem para mesma opiniao** | Media | Alto | Perfis com instrucoes fortes de vies; spike de validacao obrigatorio |
| **Latencia alta** no spawn de sub-agentes | Media | Medio | Paralelizacao via batches; progress feedback |
| **Agent tool nao suporta paralelismo real** | Baixa | Alto | Fallback para execucao sequencial com batching |
| **Vies sistemico do LLM** contamina simulacao | Alta | Alto | Perfis com instrucoes contrarias ao vies default; calibracao com dados reais (pos-MVP) |
| **Validacao subjetiva** disfaracada de rigor | Media | Alto | Definir metricas quantitativas; incluir modulo de backtesting como meta pos-MVP |

### Riscos de Produto

| Risco | Prob. | Impacto | Mitigacao |
|-------|-------|---------|-----------|
| **Output nao acionavel** para consultores | Media | Critico | Template revisado por consultor real; recomendacoes explicitas |
| **Resultados nao correlacionam com realidade** | Alta (MVP) | Medio | Posicionar como ferramenta exploratoria, nao pesquisa substituta |
| **Credibilidade excessiva** do usuario | Media | Alto | Disclaimer forte; secao de metodologia transparente; nunca chamar de "pesquisa" |
| **Questoes eticas** sobre simulacao de opiniao | Media | Alto | Transparencia na metodologia; disclaimer obrigatorio; uso apenas consultivo |

### Riscos de Negocio

| Risco | Prob. | Impacto | Mitigacao |
|-------|-------|---------|-----------|
| **Consultores nao confiam em AI** | Alta | Critico | Posicionar como complemento a pesquisa real; mostrar metodologia |
| **Regulacao de AI em campanha** | Media | Alto | Uso como ferramenta interna de analise, nao propaganda |
| **Concorrencia de ferramentas pagas** | Baixa | Medio | Diferencial: customizacao total + roda local + sem lock-in |
| **Dados demograficos brasileiros escassos** | Media | Medio | Presets "aproximadamente certos" no MVP; dados de TSE/IBGE/DataFolha para calibracao futura |

---

## 11. Questoes em Aberto

| ID | Questao | Impacto | Decisao Provisoria |
|----|---------|---------|-------------------|
| OQ-1 | Quantos sub-agentes simultaneos o Claude Code suporta de forma estavel? | Dimensionamento de batches | Assumido 10; validar no spike |
| OQ-2 | O Agent tool retorna output estruturado parseavel de forma confiavel? | Captura de dados | Assumido sim (YAML inline); validar no dry-run |
| OQ-3 | Como calibrar presets contra dados demograficos reais sem acesso a bases pagas? | Qualidade dos presets | Usar dados publicos IBGE/TSE; composicao aproximada |
| OQ-4 | Ha demanda real de consultores politicos brasileiros por este tipo de ferramenta? | Viabilidade comercial | Validar pos-MVP com 2-3 consultores |
| OQ-5 | Qual o custo medio em tokens/dolares de uma simulacao completa (20 agentes, 3 rodadas)? | Precificacao | Estimar apos dry-run do Epic 2 |
| OQ-6 | Limite de conhecimento temporal do LLM impacta cenarios de politica atual? | Qualidade da simulacao | Mitigado por ingestao de contexto (FR2) |

---

## 12. Plano de Implementacao

### Sequencia Recomendada

```
Epic 1: Fundacao         [~1 dia]
  |
  v
Spike: Prompt Engineering [~1 dia]  ** GATE: sem diversidade validada, PARAR **
  |
  v
Epic 2: Motor            [~2-3 dias]
  |
  v
Epic 3: Agregacao        [~2 dias]
  |
  v
Epic 4: Refinamento      [~1 dia]
```

**Total estimado:** 7-9 dias de trabalho efetivo

### Recomendacao Critica: Spike Obrigatorio

O spike de prompt engineering entre Epic 1 e Epic 2 e o ponto de decisao mais importante do projeto. Se os agentes nao produzirem opinioes genuinamente diversas, todo o pipeline construido nos Epics 2-4 nao tera valor. E como construir uma fabrica inteira antes de testar se o prototipo funciona.

**Criterio de sucesso do spike:**
1. 5 agentes com perfis contrastantes produzem pelo menos 3 posicoes distintas
2. Agentes "conservadores" expressam opinioes genuinamente conservadoras
3. Registros linguisticos variam por classe social/escolaridade
4. Se falhar: revisar templates de persona antes de prosseguir

### Ordem de Stories dentro de cada Epic

**Epic 1:** 1.1 (scaffold) -> 1.2 (gerador de perfis) -> 1.3 (presets) -> 1.4 (validacao)

**Spike:** Executar com output do Epic 1; ajustar templates conforme necessario

**Epic 2:** 2.1 (rodada 1) -> 2.2 (sumarizacao) -> 2.3 (rodadas 2+) -> 2.4 (orquestrador) -> 2.5 (dry-run)

**Epic 3:** 3.4 (ingestao de contexto, pode comecar em paralelo) -> 3.1 (agregacao) -> 3.2 (template relatorio) -> 3.3 (recomendacoes) -> 3.5 (validacao completa)

**Epic 4:** 4.1 (reuso) -> 4.2 (comparativo) -> 4.3 (customizacao) -> 4.4 (polish)

### Delegacao de Agentes AIOS

| Story/Atividade | Executor Recomendado |
|----------------|---------------------|
| Scaffold, templates, presets | @dev |
| Spike de prompt engineering | @dev + @pm (review qualitativo) |
| Orquestracao SKILL.md | @dev |
| Review de relatorio (acionabilidade) | @pm |
| Quality gate por epic | @qa (dry-run validation) |

---

## 13. Decisoes Autonomas Consolidadas

| Fonte | Decisao | Razao |
|-------|---------|-------|
| PRD | Sem validacao contra pesquisas reais no MVP | Insight qualitativo ja e acionavel; dados reais sao caros |
| PRD | Sem interface grafica | Restricao tecnica (AIOS Skill) + CLI First |
| PRD | Sem framework de testes | Skills sao markdown-driven, nao code-driven |
| PRD | 3 presets iniciais | Suficiente para demonstrar valor sem over-engineering |
| PRD | Limite de 50 agentes | Balanceamento entre diversidade e custo/context window |
| PRD | Apenas pt-BR no MVP | Mercado-alvo e Brasil |
| PRD | YAML para dados internos | Legivel para humanos; padrao AIOS |
| PRD | 3 rodadas de deliberacao por default | Convergencia tipica em 3-5 rodadas |
| Arch | Agentes stateless | Agent tool nao suporta sessoes persistentes |
| Arch | Sumarizacao pelo agente principal | Tarefa sequencial simples; sub-agente adicionaria latencia |
| Arch | Batch size de 10 | Conservador para estabilidade; agressivo para performance |
| Arch | Clustering semantico via prompt | Sem runtime para algoritmos; LLM agrupa semanticamente |
| Arch | Presets aproximados (nao estatisticamente exatos) | "Aproximadamente certo" ja gera diversidade util |
| Arch | Disclaimer etico obrigatorio | Responsabilidade etica e protecao contra uso indevido |
| Arch | Spike obrigatorio antes do Epic 2 | Sem validar diversidade, pipeline inteiro e risco |
| Arch | Complexidade STANDARD (14/25) | Infra zero + integracao minima compensam dominio novo |
| Spec | Nao implementar modelo HK/DW algebrico | Restricao de AIOS Skill; templates de deliberacao aproximam a dinamica |

---

## 14. Metricas de Sucesso

### MVP

| Metrica | Target | Como Medir |
|---------|--------|------------|
| Simulacao completa sem erro | > 90% das execucoes | Logs de output |
| Tempo de execucao (20 agentes) | < 15 min | Timestamp nos outputs |
| Diversidade de argumentos | > 10 argumentos unicos por simulacao | Contagem no report |
| Relatorio legivel por nao-tecnico | Aprovacao qualitativa | Review manual |

### Pos-MVP

| Metrica | Target | Como Medir |
|---------|--------|------------|
| Correlacao com pesquisas reais | > 60% alinhamento direcional | Comparacao com dados |
| Reuso de paineis | > 50% das simulacoes | Contagem loads vs. creates |
| Cenarios comparativos por sessao | > 2 cenarios | Contagem de outputs |
| Satisfacao do consultor | NPS > 7 | Feedback qualitativo |

---

*Spec consolidada por Morgan (@pm) — Run ID: forge-politica-app-20260323-2242 — 2026-03-23*
*v1.1: correcoes aplicadas por Morgan (@pm) com base no feedback de @qa — 3 CRITs resolvidos, 3 RECs incorporadas — 2026-03-23*
