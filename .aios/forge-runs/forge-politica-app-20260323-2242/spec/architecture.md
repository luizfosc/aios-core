# Politica App — Documento de Arquitetura

> **Motor de Predicao por Inteligencia de Enxame para Simulacao de Opiniao Publica**

| Campo | Valor |
|-------|-------|
| **Produto** | politica-app |
| **Tipo** | AIOS Skill (markdown-driven, sem codigo compilavel) |
| **Localizacao** | `skills/politica-app/` |
| **Versao** | v1.0 |
| **Data** | 2026-03-23 |
| **Autor** | Aria (Architect Agent) |
| **Run ID** | forge-politica-app-20260323-2242 |
| **PRD Referencia** | `.aios/forge-runs/forge-politica-app-20260323-2242/spec/prd.md` |

---

## 1. Avaliacao de Complexidade

### 1.1 Dimensoes de Complexidade

| Dimensao | Score | Justificativa |
|----------|-------|---------------|
| **Scope** | 4 | 15+ arquivos entre templates, presets, configs, scripts de orquestracao. Cross-cutting: toca gerador de personas, motor de deliberacao, agregador e gerador de relatorio |
| **Integration** | 2 | Unica integracao e o Agent tool do Claude Code (sub-agentes). Sem APIs externas obrigatorias. WebSearch/WebFetch sao opcionais para contexto |
| **Infrastructure** | 1 | Zero infraestrutura. File-based state (YAML). Roda 100% local dentro do Claude Code |
| **Knowledge** | 4 | Dominio novo: swarm intelligence via prompting, engenharia de personas cognitivas, modelagem de formacao de opiniao. Nao ha padrao existente no codebase para replicar |
| **Risk** | 3 | Risco medio-alto de convergencia de opiniao dos agentes (viés do LLM). Risco de outputs nao-acionaveis. Mitigacao depende de prompt engineering sofisticado |

**Score Total: 14 / 25**

### 1.2 Classificacao

| Classificacao | Resultado |
|---------------|-----------|
| **Complexidade** | **STANDARD** (score 14, faixa 9-15) |
| **Fases do Pipeline** | gather, assess, research, spec, critique, plan |
| **Esforco Estimado** | 2-3 dias de trabalho efetivo |

[AUTO-DECISION] "Deveria ser COMPLEX em vez de STANDARD?" -- STANDARD. Apesar do dominio ser novo (knowledge=4), a infraestrutura e zero e a integracao e minima. O produto e puramente markdown-driven, sem codigo compilavel, sem banco de dados, sem deploy. A complexidade real esta na engenharia de prompts, nao na arquitetura de software. Razao: infraestrutura simples compensa dominio complexo.

### 1.3 Flags e Recomendacoes

- **FLAG:** Requer spike de prompt engineering antes do Epic 2 (Motor de Deliberacao). Testar com 5 agentes e 1 rodada para validar diversidade de opinioes
- **FLAG:** Risco de convergencia de opiniao e o maior risco tecnico. Mitigacao requer perfis com instrucoes fortes de vies contrario ao default do LLM
- **FLAG:** Paralelismo via Agent tool precisa de validacao empirica (quantos sub-agentes simultaneos o Claude Code suporta de forma estavel?)

---

## 2. Arquitetura do Sistema

### 2.1 Visao Geral

O politica-app e uma AIOS Skill markdown-driven. Nao ha codigo compilavel — o "motor" e um conjunto de templates de prompt e arquivos YAML orquestrados pelo Claude Code via o SKILL.md como entry point.

A arquitetura segue o padrao **Pipeline Sequencial com Fan-Out Paralelo**:

```
[Input]          [Assembly]         [Deliberation]       [Aggregation]      [Report]
                                    ┌──Agent 1──┐
User prompt  →   Gerar N perfis →  ├──Agent 2──┤  →    Calcular         →  Markdown
+ contexto       via template       ├──Agent 3──┤       metricas            report
+ preset                            ├──  ...  ──┤       + vulnerab.
                                    └──Agent N──┘       + clusters
```

Cada fase e um modulo logico materializado como um template markdown que instrui o Claude Code sobre o que fazer. O "codigo" e o conjunto de instrucoes no SKILL.md que orquestra a leitura/escrita desses templates.

### 2.2 Principios Arquiteturais

| Principio | Aplicacao |
|-----------|-----------|
| **File-based state** | Todo estado persiste em YAML. Sem banco, sem memoria volatil. Cada rodada grava checkpoint |
| **Template-driven** | Comportamento definido por templates markdown, nao por codigo. Mudanca de comportamento = editar template |
| **Parallel fan-out** | Agentes do painel sao independentes dentro de cada rodada. Podem ser spawned em paralelo via Agent tool |
| **Checkpoint recovery** | Cada fase grava output antes de avancar. Se falhar, retoma do ultimo checkpoint |
| **Composicao por preset** | Composicao demografica e externalizada em YAML. Novos cenarios = novo preset, sem mudar "codigo" |
| **Separacao de concerns** | Cada template tem responsabilidade unica: gerar persona != deliberar != agregar != reportar |

---

## 3. Swarm Engine Design

### 3.1 O Que e o "Enxame"

O enxame nao e um framework de software — e um padrao de orquestracao de sub-agentes do Claude Code. Cada "agente do painel" e um sub-agente spawned via a ferramenta `Agent` com um system prompt unico que encapsula o perfil cognitivo daquela persona.

Pensando como analogia: e como um diretor de teatro que diz para cada ator "voce e o joao, classe media, 42 anos, evangelico, pensa X sobre Y" e depois pede para cada um dar sua opiniao sobre um tema.

### 3.2 Ciclo de Vida de um Agente do Painel

```
1. SPAWN      →  Agent tool com system prompt do perfil
2. PROMPT     →  Recebe tema + contexto + (argumentos anteriores, se rodada > 1)
3. RESPOND    →  Retorna opiniao estruturada (YAML inline)
4. CAPTURE    →  Output parseado e salvo no round-N.yaml
5. TERMINATE  →  Agente morre apos responder (stateless entre rodadas)
```

[AUTO-DECISION] "Os agentes devem manter estado entre rodadas?" -- Nao. Cada agente e stateless — e re-spawned a cada rodada com seu perfil + contexto acumulado injetado no prompt. Razao: Agent tool do Claude Code nao suporta sessoes persistentes. O "estado" e simulado via injecao de argumentos anteriores no prompt da proxima rodada.

### 3.3 Estrategia de Paralelismo

O SKILL.md instrui o Claude Code a spawnar multiplos agentes em paralelo quando possivel:

```
Rodada 1 (Individual):
  - Spawn agentes 1-N em paralelo (sem dependencia entre eles)
  - Cada agente recebe: perfil + tema + contexto
  - Output: opiniao individual

Rodada 2+ (Com Exposicao):
  - PRIMEIRO: sumarizar argumentos da rodada anterior (sequencial)
  - DEPOIS: spawn agentes 1-N em paralelo com sumario injetado
  - Output: opiniao revisada + flag de mudanca
```

**Batching:** Para paineis grandes (>20 agentes), dividir em batches de 10 para evitar sobrecarga do Claude Code. Cada batch executa em paralelo, mas batches sao sequenciais.

[AUTO-DECISION] "Qual o tamanho ideal do batch?" -- 10 agentes por batch. Razao: Claude Code suporta multiplos Agent tool calls em paralelo, mas o limite pratico depende do context window. 10 e conservador o suficiente para ser estavel e agressivo o suficiente para manter performance.

### 3.4 Tratamento de Falhas

| Cenario | Comportamento |
|---------|---------------|
| Agente retorna output malformado | Tentar parse; se falhar, marcar como `status: error` no YAML e continuar com os demais |
| Agente nao responde (timeout) | Registrar como `status: timeout`; nao bloquear rodada |
| Mais de 30% dos agentes falham | Abortar rodada e alertar usuario; oferecer retry |
| Falha entre rodadas | Retomar do ultimo round-N.yaml salvo |

---

## 4. Sistema de Personas

### 4.1 Anatomia de uma Persona

Cada agente do painel tem um perfil cognitivo completo definido em YAML. O perfil e transformado em system prompt via template.

```yaml
# Exemplo de perfil de agente
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
    - authority_bias       # Confia em figuras de autoridade
    - status_quo_bias      # Resiste a mudancas
    - in_group_bias        # Favorece quem parece "do mesmo grupo"
  influence_susceptibility:
    social_proof: alto     # "Todo mundo ta dizendo"
    authority: alto        # "O pastor falou que..."
    scarcity: medio        # "Vai acabar / e a ultima chance"
    reciprocity: alto      # "Ele me ajudou, entao..."

deliberative:
  processing_style: emocional    # vs. analitico
  opinion_flexibility: baixa     # quao facil muda de opiniao
  argument_weight: experiencia   # que tipo de argumento pesa mais
  expression_style: anedotico    # como expressa opiniao
```

### 4.2 Mapeamento de Vieses Cognitivos (Munger)

Os vieses cognitivos sao baseados nos 25 modelos mentais de Charlie Munger, filtrados para relevancia politica:

| Vies (Munger) | Aplicacao na Simulacao |
|---------------|----------------------|
| **Reward/Punishment** | Agentes respondem mais forte a promessas de ganho/perda direta |
| **Liking/Loving** | Agentes favorecem candidatos que "parecem" com seu grupo |
| **Disliking/Hating** | Agentes rejeitam argumentos de fontes que desprezam |
| **Doubt-Avoidance** | Agentes com `opinion_flexibility: baixa` resistem a ambiguidade |
| **Inconsistency-Avoidance** | Agentes evitam contradizer posicoes anteriores |
| **Social Proof** | Agentes com `social_proof: alto` mudam opiniao se "maioria" muda |
| **Authority Influence** | Agentes com `authority: alto` mudam se figura de autoridade diz algo |
| **Contrast Misreaction** | Agentes avaliam propostas em relacao ao status quo, nao em absoluto |

### 4.3 Principios de Influencia (Cialdini)

Os principios de Cialdini definem como agentes sao influenciados entre rodadas:

| Principio | Mecanismo na Simulacao |
|-----------|----------------------|
| **Reciprocidade** | Agentes que "receberam" algo (programa social) tendem a apoiar quem deu |
| **Compromisso** | Agentes que declararam posicao na rodada 1 resistem a mudar (consistencia) |
| **Prova Social** | Sumario mostra distribuicao; agentes sensíveis mudam para "maioria" |
| **Autoridade** | Argumentos atribuidos a "especialistas" pesam mais para perfis susceptiveis |
| **Escassez** | Argumentos de "ultima chance" ou "vai perder" ativam urgencia |
| **Afinidade** | Argumentos de "pessoas como voce" ressoam mais que argumentos abstratos |

### 4.4 Template de System Prompt do Agente

O template (`templates/agent-persona.md`) gera o system prompt de cada agente:

```markdown
Voce e {name}, {age} anos, {occupation} de {region}.

## Quem voce e
- Classe {class}, escolaridade {education}
- Seus valores: {values}
- Suas prioridades no dia-a-dia: {priorities}
- Voce se informa por: {information_sources}

## Como voce pensa
- Voce tende a pensar de forma {processing_style}
- {cognitive_biases_description}
- O que mais te convence: {argument_weight}

## Instrucoes
Ao receber um tema politico:
1. Forme sua opiniao com base em quem voce e, nao em analise tecnica
2. Use linguagem natural para sua classe e escolaridade
3. Cite experiencias pessoais plausiveis (nao invente dados)
4. Responda no formato YAML:

```yaml
position: [a_favor | contra | neutro | indeciso]
intensity: [1-5]  # 1=fraco, 5=veemente
main_arguments:
  - "argumento 1"
  - "argumento 2"
  - "argumento 3"
reasoning: "explicacao curta de por que pensa assim"
```
```

### 4.5 Presets Demograficos

Cada preset define a composicao do painel — quantos agentes de cada perfil:

```yaml
# presets/brasil-geral.yaml
name: brasil-geral
description: "Composicao aproximada do eleitorado brasileiro"
total_agents: 20
composition:
  - segment: classe-ab-urbano-sudeste
    count: 3
    template_overrides:
      class: [A, B]
      region: [sp-capital, rj-capital, bh]
      education: [superior-completo, pos-graduacao]

  - segment: classe-c-urbano
    count: 5
    template_overrides:
      class: [C]
      region: [sp-capital, rj-capital, nordeste-urbano, sul-urbano]
      education: [medio-completo, superior-incompleto]

  - segment: classe-de-periferia
    count: 4
    template_overrides:
      class: [D, E]
      region: [periferia-sp, periferia-rj, nordeste-urbano]
      education: [fundamental-completo, medio-incompleto]

  - segment: rural-interior
    count: 3
    template_overrides:
      class: [C, D]
      region: [interior-sp, interior-mg, interior-nordeste]
      education: [fundamental-incompleto, fundamental-completo]

  - segment: jovem-digital
    count: 3
    template_overrides:
      age_range: [18, 29]
      information_sources: [instagram, twitter, youtube, tiktok]

  - segment: evangelico-conservador
    count: 2
    template_overrides:
      religion: evangelica
      values: [fe, familia, moral-crista, ordem]
      cognitive_biases: [authority_bias, in_group_bias]
```

[AUTO-DECISION] "Os presets devem ser baseados em dados do IBGE?" -- Sim, aproximadamente. Os presets usam distribuicao proporcional inspirada em dados demograficos reais (IBGE/PNAD/TSE), mas nao precisam ser estatisticamente exatos no MVP. A precisao vem nas iteracoes futuras. Razao: "aproximadamente certo" ja gera diversidade util; precisao perfeita requer dados pagos.

---

## 5. Modelo de Formacao de Opiniao

### 5.1 Ciclo Deliberativo

O modelo segue um ciclo inspirado em deliberacao real:

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

(Rodadas 4-5: opcionais, mesmo padrao da rodada 3)
```

### 5.2 Mecanismo de Mudanca de Opiniao

A mudanca de opiniao nao e aleatoria — e governada pelo perfil do agente:

| Fator | Efeito |
|-------|--------|
| `opinion_flexibility: alta` | Mais propenso a mudar apos exposicao |
| `opinion_flexibility: baixa` | Tende a reforcar posicao original |
| `social_proof: alto` + distribuicao desigual | Muda para o lado majoritario |
| `authority: alto` + argumento de autoridade | Muda se figura de autoridade e citada |
| `processing_style: analitico` | Muda com dados e evidencias |
| `processing_style: emocional` | Muda com historias e anedotas |

O template de deliberacao (rodada 2+) inclui instrucao explicita:

```markdown
## Argumentos que outros cidadaos apresentaram:
{summary_of_previous_round}

## Distribuicao atual:
- A favor: {pct}% | Contra: {pct}% | Neutro: {pct}% | Indeciso: {pct}%

## Sua tarefa:
Considere esses argumentos. Com base em QUEM VOCE E (nao em logica abstrata):
- Algum argumento te fez repensar? Qual e por que?
- Sua posicao mudou? Se sim, o que te convenceu?
- Responda no mesmo formato YAML, adicionando:

```yaml
opinion_changed: [true | false]
change_trigger: "o argumento que causou a mudanca (se houver)"
previous_position: [sua posicao anterior]
```
```

### 5.3 Sumarizacao Inter-Rodada

Entre cada rodada, o sistema gera um sumario dos argumentos para injecao na proxima. Isso e feito pelo Claude Code principal (nao por sub-agente):

**Regras de sumarizacao:**
1. Agrupar argumentos por posicao (a favor / contra / neutro)
2. Rankear por frequencia (quantos agentes usaram argumento similar)
3. Manter linguagem acessivel (nao academica)
4. Incluir 3-5 argumentos por posicao (nao todos)
5. Incluir distribuicao percentual

[AUTO-DECISION] "A sumarizacao deve ser feita por sub-agente ou pelo agente principal?" -- Pelo agente principal (Claude Code que roda o SKILL.md). Razao: sumarizacao e uma tarefa sequencial simples que nao precisa de paralelismo. Spawnar sub-agente para isso adiciona latencia sem beneficio.

---

## 6. Motor de Agregacao

### 6.1 Metricas Calculadas

Apos a ultima rodada, o sistema agrega dados em `aggregation.yaml`:

```yaml
# aggregation.yaml (exemplo)
simulation_id: "20260323-2242-reforma-tributaria"
total_agents: 20
total_rounds: 3

sentiment_distribution:
  overall:
    a_favor: 45.0
    contra: 30.0
    neutro: 15.0
    indeciso: 10.0
  by_segment:
    classe-ab-urbano:
      a_favor: 66.7
      contra: 33.3
    classe-c-urbano:
      a_favor: 40.0
      contra: 40.0
      indeciso: 20.0
    # ... etc

intensity:
  average: 3.2
  by_position:
    a_favor: 3.5
    contra: 4.1  # contra e mais veemente

argument_ranking:
  a_favor:
    - argument: "Simplifica o sistema que ninguem entende"
      frequency: 8
      impact_score: 3  # causou mudancas de opiniao
    - argument: "Pode reduzir preco de produtos basicos"
      frequency: 6
      impact_score: 2
  contra:
    - argument: "Vai aumentar imposto pra classe media"
      frequency: 7
      impact_score: 4  # ALTO impacto — argumento-vulnerabilidade
    - argument: "Governo nao sabe gastar bem o que ja tem"
      frequency: 5
      impact_score: 1

vulnerabilities:
  - argument: "Vai aumentar imposto pra classe media"
    segment_most_affected: classe-c-urbano
    opinion_change_rate: 40.0  # 40% dos agentes desse segmento mudaram
    severity: critical
    recommendation: "Necessita contranarrativa forte com dados concretos"

opinion_shifts:
  round_1_to_2:
    total_changes: 4
    direction: "2 mudaram para contra, 2 para neutro"
  round_2_to_3:
    total_changes: 2
    direction: "1 mudou para a favor, 1 para indeciso"

clusters:
  - name: "Pragmaticos economicos"
    size: 7
    shared_arguments: ["simplificacao", "reducao burocracia"]
    demographics: "predominantemente classe AB, urbano"
  - name: "Desconfiados do governo"
    size: 5
    shared_arguments: ["governo incompetente", "mais imposto"]
    demographics: "misto, forte em classe C/D"
```

### 6.2 Calculo de Impact Score

O **impact score** de um argumento e calculado por quantas mudancas de opiniao ele causou:

```
impact_score = count(agents where change_trigger contains argument)
```

Argumentos com `impact_score >= 3` em paineis de 20 agentes sao classificados como **vulnerabilidades** — pontos fracos narrativos que o oponente pode explorar ou que o candidato precisa contranarrativar.

### 6.3 Deteccao de Clusters

Clusters sao identificados por similaridade de argumentos:

1. Listar argumentos de todos os agentes na rodada final
2. Agrupar agentes que usaram argumentos tematicamente similares
3. Rotular clusters por tema predominante
4. Mapear demographics predominantes do cluster

[AUTO-DECISION] "Usar algoritmo de clustering (k-means, etc.)?" -- Nao. A "clusterizacao" e feita pelo proprio Claude Code via analise semantica dos argumentos (prompt-based, nao algoritmica). Razao: AIOS Skill nao roda codigo computacional complexo. O LLM ja faz agrupamento semantico naturalmente.

---

## 7. Gerador de Relatorio

### 7.1 Estrutura do Relatorio

O relatorio final (`report.md`) segue este template:

```markdown
# Simulacao de Opiniao Publica: {tema}
> Gerado em {data} | Painel: {preset} ({N} agentes) | Rodadas: {R}

---

## Sumario Executivo
{3-5 paragrafos com conclusoes acionaveis}
{Tom: consultor de campanha escrevendo para o candidato}

---

## Dashboard de Sentimento

### Distribuicao Geral
| Posicao | % | Intensidade Media |
|---------|---|-------------------|
| A favor | X% | Y/5 |
| Contra | X% | Y/5 |
| Neutro | X% | Y/5 |
| Indeciso | X% | Y/5 |

### Por Segmento
{Tabela com breakdown por segmento demografico}

---

## Mapa de Argumentos

### Argumentos A Favor (por impacto)
1. **{argumento}** — Frequencia: X | Impacto: Y
   > Ressoa com: {segmentos}

### Argumentos Contra (por impacto)
1. **{argumento}** — Frequencia: X | Impacto: Y
   > Ressoa com: {segmentos}

---

## Analise de Vulnerabilidades

### Vulnerabilidade #1: {argumento}
- **Segmento mais afetado:** {segmento}
- **Taxa de mudanca:** {X}%
- **Severidade:** {critica/alta/media}
- **Recomendacao:** {contranarrativa sugerida}

---

## Dinamica de Opiniao
{Como as opinioes evoluiram entre rodadas}
{Quais argumentos causaram mais mudancas}

---

## Recomendacoes Estrategicas
1. **{recomendacao acionavel}**
2. **{recomendacao acionavel}**
3. **{recomendacao acionavel}**

---

## Metodologia
- **Motor:** politica-app (AIOS Skill — swarm intelligence via LLM)
- **Painel:** {preset} com {N} agentes
- **Rodadas:** {R} rodadas de deliberacao
- **Contexto ingerido:** {lista de documentos}
- **Disclaimer:** Esta simulacao usa agentes de AI com perfis cognitivos
  diversos, nao substitui pesquisa de opiniao com amostra real.
  Os resultados sao indicativos e exploratórios.
```

### 7.2 Tom do Relatorio

O relatorio e escrito para **nao-tecnicos**. Sem jargao de AI, sem mencao a "LLM", "tokens", "prompts". O tom e de um consultor de campanha experiente apresentando resultados de uma pesquisa qualitativa.

[AUTO-DECISION] "Incluir disclaimer etico?" -- Sim, obrigatorio. A secao Metodologia inclui disclaimer explicito de que a simulacao e feita por AI e nao substitui pesquisa real. Razao: responsabilidade etica e protecao contra uso indevido.

---

## 8. Fluxo de Dados End-to-End

```
ENTRADA
  │
  ├─ Tema/pergunta (string)
  ├─ Preset demografico (YAML)
  ├─ Contexto opcional (markdown/text)
  │
  ▼
FASE 1: ASSEMBLY
  │ Ler preset → gerar perfis → salvar panel.yaml
  │ Template: templates/agent-persona.md
  │ Output: output/{run}/panel.yaml
  │
  ▼
FASE 2: DELIBERACAO
  │ Para cada rodada R de 1 a N:
  │   Se R == 1: spawn agentes com (perfil + tema + contexto)
  │   Se R > 1:  sumarizar rodada anterior → spawn com (perfil + tema + contexto + sumario)
  │   Capturar outputs → salvar round-R.yaml
  │   Output: output/{run}/rounds/round-R.yaml
  │
  ▼
FASE 3: AGREGACAO
  │ Ler todos round-R.yaml
  │ Calcular: distribuicao, intensidade, ranking, vulnerabilidades, clusters
  │ Output: output/{run}/aggregation.yaml
  │
  ▼
FASE 4: RELATORIO
  │ Ler aggregation.yaml + panel.yaml
  │ Gerar relatorio via template
  │ Template: templates/report-template.md
  │ Output: output/{run}/report.md
  │
  ▼
SAIDA
  ├─ report.md (relatorio final legivel)
  ├─ panel.yaml (perfis para reuso)
  ├─ rounds/round-*.yaml (dados brutos)
  └─ aggregation.yaml (metricas)
```

---

## 9. Estrutura de Arquivos

```
skills/politica-app/
├── SKILL.md                        # Entry point — orquestracao completa
├── config.yaml                     # Configuracao padrao
│
├── presets/                         # Presets de composicao demografica
│   ├── brasil-geral.yaml            #   20 agentes, composicao nacional
│   ├── sp-capital.yaml              #   20 agentes, foco SP capital
│   ├── nordeste-evangelico.yaml     #   20 agentes, foco nordeste + evangelico
│   └── custom-template.yaml         #   Template para criar preset customizado
│
├── templates/                       # Templates de prompt
│   ├── agent-persona.md             #   System prompt de cada agente
│   ├── deliberation-round-1.md      #   Prompt da rodada 1 (individual)
│   ├── deliberation-round-n.md      #   Prompt das rodadas 2+ (com exposicao)
│   ├── summarizer.md                #   Prompt de sumarizacao inter-rodada
│   ├── aggregator.md                #   Prompt de agregacao de metricas
│   ├── report-template.md           #   Template do relatorio final
│   └── recommendations.md           #   Prompt para gerar recomendacoes
│
├── data/                            # Dados de referencia
│   ├── cognitive-biases.yaml        #   Catalogo de vieses (Munger)
│   ├── influence-principles.yaml    #   Principios de influencia (Cialdini)
│   └── demographic-archetypes.yaml  #   Arquetipos demograficos base
│
├── output/                          # Outputs das simulacoes
│   └── {YYYYMMDD-HHMM}-{slug}/     #   Uma pasta por simulacao
│       ├── report.md                #     Relatorio final
│       ├── panel.yaml               #     Perfis dos agentes (reusavel)
│       ├── config-snapshot.yaml     #     Config usada nesta simulacao
│       ├── rounds/                  #     Dados brutos por rodada
│       │   ├── round-1.yaml
│       │   ├── round-2.yaml
│       │   └── round-3.yaml
│       └── aggregation.yaml         #     Metricas agregadas
│
└── README.md                        # Documentacao tecnica
```

### 9.1 Descricao dos Arquivos-Chave

| Arquivo | Proposito | Quem Lê | Quem Escreve |
|---------|-----------|---------|-------------|
| `SKILL.md` | Entry point; instrui Claude Code a orquestrar toda a simulacao | Claude Code | Humano (setup) |
| `config.yaml` | Defaults: num_agents, num_rounds, batch_size, output_format | SKILL.md | Humano (config) |
| `presets/*.yaml` | Composicao demografica do painel | Fase Assembly | Humano (config) |
| `templates/agent-persona.md` | Template que gera system prompt de cada agente | Fase Assembly | Humano (design) |
| `templates/deliberation-*.md` | Templates das rodadas de deliberacao | Fase Deliberacao | Humano (design) |
| `output/{run}/panel.yaml` | Perfis gerados dos agentes | Fase Deliberacao, Agregacao | Fase Assembly |
| `output/{run}/rounds/*.yaml` | Respostas brutas de cada rodada | Fase Agregacao | Fase Deliberacao |
| `output/{run}/aggregation.yaml` | Metricas calculadas | Fase Relatorio | Fase Agregacao |
| `output/{run}/report.md` | Relatorio final para consumo humano | Humano | Fase Relatorio |

---

## 10. config.yaml

```yaml
# skills/politica-app/config.yaml
name: politica-app
version: "1.0.0"
description: "Motor de predicao por inteligencia de enxame"

defaults:
  num_agents: 20          # Agentes no painel (range: 10-50)
  num_rounds: 3           # Rodadas de deliberacao (range: 1-5)
  batch_size: 10          # Agentes por batch de paralelismo
  default_preset: brasil-geral

output:
  format: markdown
  location: output/
  naming: "{date}-{slug}"
  save_raw_data: true     # Salvar rounds/*.yaml e aggregation.yaml

deliberation:
  summary_max_arguments: 5     # Argumentos por posicao no sumario
  show_distribution: true       # Mostrar % na rodada 2+
  opinion_change_tracking: true # Rastrear mudancas de opiniao

aggregation:
  vulnerability_threshold: 20   # % de mudanca para classificar como vulnerabilidade
  cluster_min_size: 3           # Minimo de agentes para formar cluster
  argument_ranking_top: 10      # Top N argumentos por posicao

report:
  language: pt-BR
  include_methodology: true
  include_disclaimer: true
  include_raw_data_reference: true
```

---

## 11. Decisoes Tecnologicas

| Decisao | Escolha | Alternativa Descartada | Razao |
|---------|---------|----------------------|-------|
| **Runtime** | AIOS Skill (Claude Code) | Framework Python/Node.js standalone | Requisito do projeto; mantem dentro do ecossistema AIOS |
| **Persistencia** | YAML files | JSON / SQLite | YAML e mais legivel para humanos; padrao AIOS; permite edicao manual |
| **Orquestracao** | SKILL.md instrui Claude Code | Script Node.js com Agent API | AIOS Skills sao markdown-driven; o "codigo" sao as instrucoes |
| **Paralelismo** | Agent tool (fan-out) | Child processes / Workers | Agent tool e a unica forma de "paralelismo" no Claude Code |
| **Clusterizacao** | Analise semantica via prompt | k-means / scikit-learn | Sem runtime Python/Node.js compilavel; LLM faz agrupamento semantico |
| **Formato do relatorio** | Markdown | HTML / PDF | Requisito do PRD; markdown e universal e convertivel |
| **Versionamento de output** | Pasta timestamped | Git branches / Database | Simples, auditavel, sem dependencias |

---

## 12. Analise de Trade-offs

### 12.1 Agentes Stateless vs. Stateful

| | Stateless (escolhido) | Stateful |
|--|----------------------|----------|
| **Pro** | Simples; sem gerenciamento de sessao; cada rodada e independente | Agentes "lembram" rodadas anteriores naturalmente |
| **Contra** | Precisa reinjetar contexto a cada rodada (mais tokens) | Requer persistencia de sessao no Agent tool (nao suportado) |
| **Veredicto** | Escolhido por limitacao tecnica E por simplicidade |

### 12.2 Sumarizacao Centralizada vs. Peer-to-Peer

| | Centralizada (escolhido) | Peer-to-Peer |
|--|-------------------------|--------------|
| **Pro** | Controlavel; evita viés de cascata; sumario consistente | Mais realista (pessoas nao leem "resumos", ouvem umas as outras) |
| **Contra** | Menos realista; sumario pode perder nuances | Explosao combinatoria (NxN interacoes); inviavel com Agent tool |
| **Veredicto** | Centralizada e a unica viavel dentro das restricoes. Peer-to-peer e inviavel com 20+ agentes |

### 12.3 Diversidade Forcada vs. Natural

| | Forcada (escolhido) | Natural |
|--|---------------------|---------|
| **Pro** | Garante diversidade; controla vieses do LLM | Mais "autentico"; menos engenharia |
| **Contra** | Pode parecer artificial; requer engenharia de prompt cuidadosa | LLM tende a convergir; viés sistematico contamina resultados |
| **Veredicto** | Forcada. Sem instrucoes fortes de viés, o LLM converge para "opiniao media urbana progressista". Os perfis com viéses explicitos sao essenciais |

---

## 13. Implicacoes de Seguranca

| Aspecto | Risco | Mitigacao |
|---------|-------|-----------|
| **Uso para manipulacao** | Resultados podem ser usados para manipular eleitorado | Disclaimer obrigatorio; posicionamento como ferramenta exploratoria |
| **Viés sistematico** | LLM tem vieses proprios que contaminam simulacao | Perfis com instrucoes contrarias; rodadas adversariais |
| **Privacidade** | Presets podem conter estereotipos ofensivos | Review etico dos presets; linguagem respeitosa nos perfis |
| **Dados sensíveis** | Contexto ingerido pode conter info confidencial | Todo dado permanece local (file-based); sem envio para APIs externas alem do Claude |
| **Credibilidade excessiva** | Usuario trata simulacao como "pesquisa real" | Disclaimer forte; secao de metodologia transparente; nunca chamar de "pesquisa" |

---

## 14. Compatibilidade com Ecossistema AIOS

| Recurso AIOS | Integracao | Status |
|-------------|-----------|--------|
| **SKILL.md entry point** | Sim — segue padrao de skills existentes | Core |
| **Agent tool (sub-agentes)** | Sim — mecanismo principal do enxame | Core |
| **Read/Write/Edit** | Sim — leitura de templates, escrita de outputs | Core |
| **WebSearch/WebFetch** | Opcional — para ingestao de contexto adicional | Opcional |
| **Bash** | Sim — para operacoes simples de parse/sort | Auxiliar |
| **Mind: charlie-munger** | Referencia — vieses cognitivos nos perfis | Inspiracao |
| **Mind: robert-cialdini** | Referencia — principios de influencia | Inspiracao |
| **Squad: icp-cloning** | Referencia — padroes de persona engineering | Inspiracao |
| **Skill: deep-research** | Integravel — para pesquisa de contexto pre-simulacao | Futuro |

---

## 15. Sequencia de Implementacao Recomendada

| Ordem | Epic | Dependencia | Foco Arquitetural |
|-------|------|-------------|-------------------|
| 1 | **Epic 1: Fundacao** | Nenhuma | Scaffold + config.yaml + presets + template de persona |
| 2 | **Spike: Prompt Engineering** | Epic 1 | Validar diversidade com 5 agentes / 1 rodada |
| 3 | **Epic 2: Motor** | Epic 1 + Spike | Orquestracao + deliberacao + checkpoints |
| 4 | **Epic 3: Agregacao** | Epic 2 | Metricas + relatorio + recomendacoes |
| 5 | **Epic 4: Refinamento** | Epic 3 | Reuso + comparativo + polish |

**Recomendacao critica:** O spike de prompt engineering (entre Epic 1 e 2) e essencial. Sem validar que os agentes produzem opinioes diversas, o resto do pipeline nao tem valor. E como construir uma fabrica inteira antes de testar se o prototipo funciona.

---

## 16. Decisoes Autonomas Documentadas

| ID | Pergunta | Decisao | Razao |
|----|----------|---------|-------|
| [AUTO-DECISION] 1 | Agentes stateless ou stateful? | Stateless | Agent tool nao suporta sessoes persistentes; reinjecao de contexto e simples |
| [AUTO-DECISION] 2 | Sumarizacao por sub-agente ou principal? | Principal | Tarefa sequencial simples; sub-agente adicionaria latencia sem beneficio |
| [AUTO-DECISION] 3 | Batch size ideal? | 10 agentes | Conservador para estabilidade; agressivo o suficiente para performance |
| [AUTO-DECISION] 4 | Clustering algoritmico ou semantico? | Semantico via prompt | Sem runtime para algoritmos; LLM faz agrupamento semantico naturalmente |
| [AUTO-DECISION] 5 | Presets baseados em IBGE? | Sim, aproximadamente | "Aproximadamente certo" gera diversidade util; precisao exata requer dados pagos |
| [AUTO-DECISION] 6 | Disclaimer etico obrigatorio? | Sim | Responsabilidade etica; protecao contra uso indevido |
| [AUTO-DECISION] 7 | Complexidade STANDARD ou COMPLEX? | STANDARD (14/25) | Infra zero + integracao minima compensam dominio novo |
| [AUTO-DECISION] 8 | Spike antes de Epic 2? | Sim, obrigatorio | Sem validar diversidade de opinioes, pipeline inteiro e risco |

---

*Aria, arquitetando o futuro*
