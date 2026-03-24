# Research Brief: Motor de Predição por Inteligência de Enxame para Simulação de Opinião Pública

**Run ID:** forge-politica-app-20260323-2242
**Data:** 2026-03-23
**Agente:** Atlas (@analyst)
**Fase:** Forge Phase 1 — Especificação

---

## Sumário Executivo

A simulação de opinião pública por meio de agentes de inteligência artificial é um campo em rápida maturação, impulsionado pela convergência entre Modelagem Baseada em Agentes (ABM) clássica e Grandes Modelos de Linguagem (LLMs). Pesquisas recentes — notadamente o trabalho "Generative Agents of 1,000 People" de Stanford (Park et al., 2024) e o framework ElectionSim (Fudan/Indiana/Rochester) — demonstram viabilidade técnica real, com acurácias de replicação entre 80–85% em survey responses e predição correta em 47/51 estados dos EUA em eleição presidencial. No entanto, o campo enfrenta críticas metodológicas sérias: a maioria dos sistemas valida apenas pelo "parecer convincente" (validação subjetiva), sofre de viés demográfico sistemático (sobre-representação de visões liberais/educadas), e tem custo computacional proibitivo para sensibilidade de grande escala. O sistema proposto se posiciona num nicho ainda não ocupado: motor de enxame multi-agente orientado à simulação de cenários político-estratégicos (e não apenas predição eleitoral), integrando modelos cognitivos de viés explícitos. A maior janela de oportunidade está na camada de vieses cognitivos parametrizáveis — nenhum dos concorrentes atuais expõe isso como API configurável.

---

## Achados por Questão de Pesquisa

### 1. Inteligência de Enxame para Simulação de Opinião

#### Abordagens Acadêmicas e da Indústria

**Modelagem Baseada em Agentes (ABM) — o fundamento clássico**

ABM é a espinha dorsal da simulação de opinião. Cada agente possui estado interno (opinião, biases, rede social), regras de interação local, e o comportamento coletivo emerge das interações. Os principais modelos matemáticos são:

- **Modelo DeGroot**: Agentes atualizam opiniões pela média ponderada das opiniões de seus vizinhos na rede. Base linear, simples de implementar, mas ignora limites de confiança.
- **Modelo Hegselmann-Krause (HK)**: Agentes só interagem com outros dentro de um limiar de confiança (bounded confidence). Produz fenômenos de polarização e clusters naturalmente. Validado empiricamente em múltiplos contextos.
- **Modelo Deffuant-Weisbuch (DW)**: Similar ao HK, mas interações são par a par (assincrônicas). Mais realista para redes sociais online.
- **Modelos de Radical Groups / Líderes Carismáticos**: Agentes com influência constante e assimétrica — modela figuras como líderes de opinião, mídia, ou algoritmos.

**Swarm Intelligence como camada de coordenação**

A inteligência de enxame (SI) acrescenta dinâmicas emergentes sem controle centralizado. O modelo mais relevante industrialmente é o da **Unanimous AI**, que combina SI com loops de feedback em tempo real — em estudos com Oxford University, melhorou acurácia individual de 55% para 72% em previsões (ganho de 131%). O mais recente é o **MiroFish** (GitHub trending em março 2026), que usa 700.000 agentes autônomos em ambiente digital simulado, trocando informações e formando opiniões via emergência — demonstrou viabilidade de escala massiva.

**Abordagens Híbridas (2024–2025)**

A fronteira atual combina ABM + LLMs = **GABM (Generative Agent-Based Modeling)**. O diferencial: agentes não seguem regras hardcoded, mas raciocinam em linguagem natural usando LLMs como motor. Isso captura:
- Difusão de normas sociais
- Formação de câmaras de eco
- Polarização em redes online
- Efeito da "paradoxo da amizade"

[AUTO-DECISION] Qual o nível de detalhe matemático sobre modelos HK/DW? → Incluído com explicação conceitual sem fórmulas densas, pois este brief alimenta a spec, não o paper científico. Razão: equilíbrio entre rigor e acionabilidade para o arquiteto.

---

### 2. Simulações Baseadas em LLMs — O Que Funciona e o Que Não Funciona

#### O Que Funciona

**Stanford Generative Agents of 1,000 People (Park et al., 2024)**
- Arquitetura: LLM (GPT-4) + transcrições de entrevistas qualitativas de 2h por pessoa
- Amostra: 1.052 participantes representativos da população americana (idade, gênero, raça, região, educação, ideologia)
- Resultado: Replicou respostas dos participantes a surveys com **85% de acurácia** — comparável à acurácia de auto-replicação humana em 2 semanas
- Predição de traços de personalidade: comparável ao humano
- Menos enviesado que ferramentas de simulação anteriores

**ElectionSim — Fudan/Indiana/Rochester (2024)**
- Framework de simulação massiva em larga escala (1 milhão de agentes)
- Dados: pool de eleitores baseado em redes sociais reais (demografias reais)
- Resultado: Predições corretas em **47/51 estados** na eleição presidencial de 2020
- Micro-F1 de **0.812** em simulações a nível individual
- Suporta "diálogo" com eleitores simulados para cenários "e se"

**FlockVote (ICAIS 2025)**
- Framework ABM com LLMs para simular eleições presidenciais americanas
- Perfil demográfico de alta fidelidade + informações contextuais dinâmicas
- Foco nos 7 swing states da eleição de 2024 — reproduziu corretamente o resultado macro
- Diferencial: auditabilidade — expõe o raciocínio de cada agente, permite análise de viés e instabilidade sistêmica

#### O Que Não Funciona

**Viés Sistemático dos LLMs**
- GPT e modelos similares sobre-representam perspectivas liberais, de alta renda, e com alta escolaridade
- Minorias e grupos marginalizados são consistentemente sub-representados
- Saídas são "mais educadas, mais longas, mais polidas" que comunicação humana real — viés de estilo

**Problema da Caixa-Preta**
- LLMs são modelos opacos — impossível auditar POR QUE um agente chegou a uma opinião específica
- Isso contradiz o valor prometido pela ABM (revelar mecanismos emergentes simples)

**Validação Inadequada**
- Em revisão sistemática de 35 artigos sobre GABMs, **15/35 (43%) validam apenas subjetivamente** ("parece convincente")
- Validações empíricas existentes medem sintaxe do texto, não o fenômeno que o modelo se propõe a capturar

**Custo Computacional Proibitivo**
- GABMs são "ordens de magnitude mais caros" que ABMs tradicionais
- A maioria dos estudos reporta apenas **uma única rodada** — sensibilidade e repetição são inviáveis

**Limite de Conhecimento Temporal**
- Modelos não têm consciência de eventos recentes após cut-off de treinamento
- A Aaru previu erroneamente a vitória de Harris em 2024, em parte por esse motivo
- Harvard identificou que dados desatualizados introduzem erros sistemáticos

---

### 3. Modelagem de Opinião Política — Ciência Política Computacional

#### Fatores-Chave Identificados na Literatura

**Exposição Midiática**
- Mídia partidária funciona como âncora de opinião — reforça vieses pré-existentes
- Efeito de "enquadramento episódico" (episodic frames): frames que ressoam com vieses cognitivos são transmitidos e lembrados com mais força nas redes sociais
- O fenômeno de "motivação raciocínio afetivo" (affective motivated reasoning): informações negativas sobre um candidato favorito podem, paradoxalmente, *aumentar* o apoio (backfire effect)

**Redes Sociais e Homofilia**
- Homofilia (tendência de se associar com similares) + filtragem algorítmica = câmaras de eco
- Câmaras de eco são o principal driver de polarização digital
- A estrutura de rede (quem conecta com quem) tem impacto causal na distribuição final de opiniões

**Fatores Demográficos**
- Idade, gênero, raça, escolaridade, renda, localização geográfica são preditores robustos de orientação política
- A granularidade demográfica é decisiva para predições locais (municípios, distritos eleitorais)

**Dinâmica de Polarização**
- O fenômeno de polarização segue dois tipos: ideológica (divergência de posições) e afetiva (hostilidade ao outro grupo)
- Modelos computacionais mostram que "mentes ideológicas" específicas polarizam de formas previsíveis quando expostas a certos contextos

**Modelos Clássicos de Dinâmica de Opinião**
| Modelo | Mecanismo | Relevância para o Projeto |
|---|---|---|
| DeGroot | Média ponderada por influência social | Base para cálculo de convergência |
| Hegselmann-Krause | Confiança limitada — só interage com similares | Modela câmaras de eco naturalmente |
| Deffuant-Weisbuch | Interações par a par assíncronas | Mais realista para redes online |
| Radical Groups | Agentes de influência constante | Modela líderes de opinião, mídia, algoritmos |

---

### 4. Integração de Vieses Cognitivos

#### Os Vieses com Maior Impacto em Opinião Política

**Viés de Confirmação** — Criticidade: ALTA
- Pessoas buscam e retêm informações que confirmam crenças pré-existentes
- 80% dos indivíduos apresentados com evidências contraditórias *mantiveram* sua posição original — e 1/5 ficaram *mais confiantes*
- Durante eleições, o efeito se amplifica: estudo do MIT mostra aumento significativo de crença em notícias confirmativas em períodos eleitorais vs. não-eleitorais

**Efeito Bandwagon** — Criticidade: ALTA
- Adoção de comportamentos/opiniões pela observação de que "todos os outros fazem"
- Em política: candidatos com percepção de momentum ganham mais apoio, independente de mérito
- Retroalimenta: mais apoio → mais percepção de liderança → mais apoio

**Viés de Grupo (In-Group Bias / Identidade Social)** — Criticidade: ALTA
- Favorecimento do próprio grupo político + hostilidade ao grupo externo
- Estudo em partidos indianos mostrou uso deliberado de in-group bias, confirmação, bandwagon e negatividade como ferramentas eleitorais
- Driver primário de polarização afetiva (não ideológica)

**Efeito de Ancoragem** — Criticidade: MÉDIA-ALTA
- A primeira informação recebida sobre uma política/candidato funciona como âncora
- Julgamentos subsequentes são ajustados a partir dela, nunca totalmente neutralizando o primeiro impacto
- Quem fala primeiro define o frame de referência

**Negatividade Bias** — Criticidade: MÉDIA-ALTA
- Informações negativas têm peso desproporcional vs. positivas
- Campanhas negativas (negative ads) são mais eficazes que positivas por esse motivo

**Heurística de Disponibilidade** — Criticidade: MÉDIA
- Eventos recentes/vívidos/midiáticos são sobrestimados em probabilidade
- Uma crise recente inflaciona percepção de risco muito além da base-rate estatística

**Efeito de Contraste / Relatividade** — Criticidade: MÉDIA
- Opiniões são avaliadas relativamente ao contexto, não em absoluto
- Um candidato "moderado" parece diferente dependendo de quem está ao lado

#### Framework para Parametrização no Sistema

```
Agente Político Simulado = {
  demografia: {idade, escolaridade, renda, região, ...},
  orientação_base: {espectro: [-1.0, 1.0], intensidade: [0.0, 1.0]},
  vieses: {
    confirmação: peso [0.0, 1.0],      // resistência a info contraditória
    bandwagon: susceptibilidade [0.0, 1.0],  // sensibilidade a percepção de maioria
    in_group: intensidade [0.0, 1.0],  // hostilidade ao outro partido
    ancoragem: força [0.0, 1.0],       // rigidez ao primeiro frame
    negatividade: amplificador [1.0, 3.0]  // peso extra de info negativa
  },
  rede_social: {conexões, câmara_eco: probabilidade}
}
```

---

### 5. Paisagem Competitiva

#### Ferramentas Existentes

| Ferramenta | Tipo | Abordagem | Status 2024–2025 | Limitação Crítica |
|---|---|---|---|---|
| **Aaru** | Startup comercial | LLMs + dados de censo + media diet simulada | Ativa — errou predição presidencial 2024 | Caixa-preta, treino desatualizado |
| **ElectionSim** | Pesquisa acadêmica | LLMs + pool de 1M eleitores de redes sociais | Publicado 2024 (Fudan/Indiana) | Não disponível como produto |
| **FlockVote** | Pesquisa acadêmica | ABM + LLMs + auditabilidade | ICAIS 2025 | Framework de pesquisa, não produto |
| **Unanimous AI** | Comercial | Swarm intelligence real-time (humanos + IA) | Ativo | Requer participação humana real |
| **MiroFish** | Open Source | 700k agentes sintéticos em ambiente digital | GitHub trending Mar 2026 | Novo, sem validação eleitoral |
| **Signoi** | Startup comercial | "AI persona research" — synthetic panels | Ativo | Foco em pesquisa de mercado, não político |
| **Engage** | Polling tool | Chatbot substitui entrevistadores humanos | Ativo 2024 | Não simula população, apenas conduz entrevistas |

#### Gaps de Mercado Identificados

1. **Nenhum produto expõe vieses cognitivos como parâmetros configuráveis por campanha** — todos tratam comportamento como output, não como input configurável
2. **Nenhum produto é acessível para campaigns de pequeno porte** — Aaru e similares são enterprise-only
3. **Nenhum produto permite "what-if" narrativo** — testar como uma narrativa específica muda distribuição de opinião
4. **Nenhum produto tem foco em eleições brasileiras** — dados demográficos, biases culturais e dinâmicas de mídia são diferentes

---

## Implicações para o Design

### Arquitetura Recomendada

**[IMPLICAÇÃO 1] — Modelo Híbrido ABM + LLM com Custo Controlado**

Não usar LLMs para cada agente individual em cada tick. Usar LLMs apenas para:
- Geração do perfil inicial do agente (one-shot por agente)
- Interpretação de eventos narrativos (notícias, declarações) em vetor de impacto
- Explicação de outputs (pós-simulação)

Usar ABM clássico (HK ou DW) para a dinâmica interna entre agentes. Isso reduz custo em 10–100x vs. LLM-por-tick.

**[IMPLICAÇÃO 2] — Vieses como Parâmetros de Primeira Classe**

O principal gap competitivo identificado. Cada agente deve ter um vetor de vieses configurável. A interface principal do motor deve ser:
- Input: cenário (evento, narrativa, política) + distribuição demográfica
- Config: pesos de vieses (por cluster demográfico)
- Output: distribuição de opinião + delta de mudança + explicação

**[IMPLICAÇÃO 3] — Validação por Benchmarks Históricos**

O problema crítico do campo é falta de validação rigorosa. O sistema deve incluir desde o início um módulo de backtesting contra eleições históricas brasileiras (2018, 2022 pelo menos). Isso é o que separa produto de pesquisa de produto comercial.

**[IMPLICAÇÃO 4] — Granularidade Demográfica Brasileira**

Os dados disponíveis (TSE, IBGE, pesquisas DataFolha, Ipec, AtlasIntel) permitem construir um pool demográfico brasileiro robusto. Priorizar: região, escolaridade, renda, raça, religião (variável subestimada na literatura americana, mas crítica no Brasil).

**[IMPLICAÇÃO 5] — Swarm como Agregador, Não como Base**

Usar lógica de swarm intelligence na camada de agregação — como os agentes influenciam uns aos outros no coletivo — não como substituto da lógica individual. O modelo HK/DW opera naturalmente como swarm ao nível local.

**[IMPLICAÇÃO 6] — API-First para AIOS Skill**

Por ser uma AIOS Skill (sem UI, sem DB externo), o design deve priorizar:
- Interface de linha de comando clara
- Output em JSON estruturado + resumo em markdown
- Configuração via YAML (cenário, agentes, vieses)
- Modo dry-run e modo de produção

---

## Riscos Identificados

### Risco 1 — Viés Sistêmico do LLM como Motor [CRÍTICO]

**Problema:** Se LLMs são usados para raciocinar como agentes, eles herdam vieses de treinamento (liberal, anglófono, classe média alta). No contexto brasileiro, isso pode distorcer sistematicamente a representação de eleitores rurais, evangélicos, baixa escolaridade.

**Mitigação:** Calibrar agentes contra dados de pesquisas reais brasileiras. Usar LLMs apenas para tarefas de interpretação de linguagem, não para simular opiniões diretamente. Documentar limitação explicitamente.

### Risco 2 — Validação Subjetiva Disfarçada de Rigor [ALTO]

**Problema:** O campo tem 43% de estudos validados apenas subjetivamente. É fácil construir um sistema que "parece convincente" mas não tem valor preditivo real.

**Mitigação:** Definir desde o início métricas quantitativas de validação (acurácia por estado/região, erro médio percentual). Incluir módulo de backtesting como requisito mínimo, não como feature futura.

### Risco 3 — Custo Computacional Inviável [ALTO]

**Problema:** Simulações com 10.000+ agentes usando LLMs por tick ficam caras rapidamente. MiroFish com 700k agentes foi construído em ambiente de memória local otimizado.

**Mitigação:** Separar geração de perfil (LLM, one-shot) de dinâmica de simulação (ABM matemático, sem LLM). Implementar modo "sampling" — simular subconjunto representativo e escalar estatisticamente.

### Risco 4 — Limite de Conhecimento Temporal [MÉDIO]

**Problema:** LLMs têm cut-off de conhecimento. Eventos políticos recentes (escândalos, crises, novas alianças) não estão no modelo.

**Mitigação:** Sistema de injeção de contexto — permitir que o usuário forneça "briefing de situação atual" como parte do prompt de simulação. Não depender de conhecimento interno do LLM para eventos recentes.

### Risco 5 — Interpretação Política Indevida [MÉDIO]

**Problema:** Outputs de simulação podem ser usados como "pesquisa real" por quem não entende as limitações. Risco de manipulação: Aaru demonstrou que 10–52 respostas sintéticas adicionadas a pesquisas reais já mudam o resultado previsto.

**Mitigação:** Todo output deve incluir aviso explícito de limitações e confiança. Documentar claramente que o sistema é ferramenta de *simulação de cenários*, não *predição*.

### Risco 6 — Ausência de Dados Demográficos Brasileiros Estruturados [MÉDIO]

**Problema:** A maioria dos frameworks existentes usa dados americanos. Construir um pool demográfico brasileiro robusto requer curadoria manual de múltiplas fontes (TSE, IBGE, DataFolha).

**Mitigação:** Identificar e documentar fontes de dados disponíveis como parte da fase de especificação. Considerar usar AtlasIntel ou DataFolha histórico como ground truth para calibração inicial.

---

## Referências

### Fundações Acadêmicas — ABM e Dinâmica de Opinião

- [Bounded confidence opinion dynamics: A survey — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0005109823004661)
- [Opinion Dynamics and Bounded Confidence (Hegselmann & Krause) — JASSS](https://www.jasss.org/5/3/2/2.pdf)
- [Opinion Dynamics: A Comprehensive Overview — arXiv 2025](https://arxiv.org/html/2511.00401v1)
- [Dynamic Opinion Formation in Networks — MDPI 2025](https://www.mdpi.com/2073-431X/13/8/190)

### LLMs para Simulação de Populações

- [Generative Agent Simulations of 1000 People (Park et al., 2024) — arXiv](https://arxiv.org/abs/2411.10109)
- [Performance and Biases of LLMs in Public Opinion Simulation — Nature/Humanities & Social Sciences](https://www.nature.com/articles/s41599-024-03609-x)
- [Do LLMs Solve Problems of Agent-Based Modeling? Critical Review — arXiv 2025](https://arxiv.org/html/2504.03274v1)
- [LLM Social Simulations Are a Promising Research Method — arXiv 2025](https://arxiv.org/html/2504.02234v2)
- [Generative Agents: Interactive Simulacra of Human Behavior (Stanford) — ACM UIST](https://dl.acm.org/doi/abs/10.1145/3586183.3606763)

### Simulação Eleitoral e Frameworks

- [ElectionSim: Massive Population Election Simulation — arXiv 2024](https://arxiv.org/abs/2410.20746)
- [FlockVote: LLM-Empowered ABM for U.S. Presidential Elections — ICAIS 2025](https://arxiv.org/abs/2512.05982)
- [Multi-agent systems powered by LLMs: swarm intelligence — Frontiers in AI 2025](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1593017/full)

### Ferramentas Comerciais e Competidores

- [Aaru — AI startup uses chatbots for political polls (Semafor)](https://www.semafor.com/article/09/20/2024/ai-startup-aaru-uses-chatbots-instead-of-humans-for-political-polls)
- [Aaru admits flaws after wrong 2024 election prediction (CO/AI)](https://getcoai.com/news/ai-polling-firm-admits-flaws-in-us-election-predictions/)
- [Using AI for Political Polling — Harvard Ash Center](https://ash.harvard.edu/articles/using-ai-for-political-polling/)
- [Unanimous AI — Swarm Intelligence methodology](https://unanimous.ai/what-is-si/)
- [MiroFish — Swarm AI with 700k agents (LinkedIn)](https://www.linkedin.com/pulse/swarm-intelligence-comes-forecasting-how-mirofish-simulates-borish-lahve)

### Vieses Cognitivos e Opinião Política

- [11 Cognitive Biases That Influence Political Outcomes — World Economic Forum](https://www.weforum.org/stories/2020/08/11-cognitive-biases-that-influence-political-outcomes/)
- [Cognitive Biases and Communication Strength in Social Networks — Cambridge/British Journal of Political Science](https://www.cambridge.org/core/journals/british-journal-of-political-science/article/abs/cognitive-biases-and-communication-strength-in-social-networks-the-case-of-episodic-frames/CB33C616F33A2ACE07632C5ED5A7793B)
- [Confirmation Bias in Election Cycles — MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/election-cycles-voters-tend-to-believe-news-confirms-their-biases)
- [Cognitive-Motivational Mechanisms of Political Polarization — Nature Reviews Psychology](https://www.nature.com/articles/s44159-022-00093-5)
- [Bandwagon Effect — Wikipedia](https://en.wikipedia.org/wiki/Bandwagon_effect)

### Segurança e Riscos

- [How AI can rig polls — EurekAlert](https://www.eurekalert.org/news-releases/1106172)
- [Fake AI survey answers could sway election predictions — Homeland Security Newswire](https://www.homelandsecuritynewswire.com/dr20251118-fake-survey-answers-from-ai-could-quietly-sway-election-predictions)

---

*Brief gerado por Atlas (@analyst) — Run ID: forge-politica-app-20260323-2242 — 2026-03-23*
