# Politica App — Product Requirements Document (PRD)

> **Motor de Predição por Inteligência de Enxame para Simulação de Opinião Pública**

| Campo | Valor |
|-------|-------|
| **Produto** | politica-app |
| **Tipo** | AIOS Skill |
| **Localização** | `skills/politica-app/` |
| **Versão PRD** | v1.0 |
| **Data** | 2026-03-23 |
| **Autor** | Morgan (PM Agent) |
| **Run ID** | forge-politica-app-20260323-2242 |

---

## Change Log

| Data | Versão | Descrição | Autor |
|------|--------|-----------|-------|
| 2026-03-23 | v1.0 | Criação inicial do PRD | Morgan (PM) |

---

## 1. Visão do Produto

### 1.1 Problema

Consultores políticos e políticos tomam decisões de campanha baseados em pesquisas de opinião tradicionais que são **caras** (R$50-200k por pesquisa quantitativa), **lentas** (2-4 semanas de campo + análise) e **estáticas** (retratam um momento, não simulam cenários). Quando uma crise explode numa segunda-feira, a pesquisa contratada na sexta anterior já não reflete a realidade.

Além disso, pesquisas tradicionais medem o que as pessoas **dizem** que pensam, não como **formariam** suas opiniões diante de novos estímulos. Falta uma ferramenta que simule a dinâmica de formação de opinião — como informação se propaga, quais argumentos ressoam com quais perfis, e onde estão as vulnerabilidades narrativas.

### 1.2 Solução

O **politica-app** é um motor de predição que usa **inteligência de enxame** (swarm intelligence) para simular opinião pública. Em vez de perguntar para pessoas reais, o sistema cria um "painel virtual" de agentes AI — cada um representando um perfil demográfico/psicográfico distinto — e os coloca para "discutir" um tema político. O agregado dessas opiniões simuladas gera uma predição de sentimento público.

A inovação central é usar **múltiplos agentes com perfis cognitivos diversos** (viéses, valores, fontes de informação, nível educacional, classe social) em vez de um único prompt de LLM. Isso captura a complexidade da formação de opinião real, onde pessoas diferentes chegam a conclusões diferentes a partir das mesmas informações.

### 1.3 Por que Importa

- **Velocidade:** Simulação completa em minutos, não semanas
- **Custo:** Fração do custo de pesquisa tradicional (apenas API calls do Claude)
- **Cenários:** Permite testar "e se?" — como a opinião mudaria se tal fato viesse à tona?
- **Profundidade:** Não apenas "a favor/contra", mas os argumentos, narrativas e vulnerabilidades por trás de cada posição
- **Iteração:** Roda quantas vezes quiser, ajustando parâmetros entre simulações

[AUTO-DECISION] "O produto precisa de validação contra pesquisas reais?" → Não no MVP. A validação contra dados reais é um diferencial futuro (Epic de calibração), mas o MVP entrega valor mesmo sem validação estatística, pois o insight qualitativo (argumentos, vulnerabilidades, narrativas) já é acionável para consultores. Razão: MVP focus — entregar valor rápido sem dependência de dados externos custosos.

---

## 2. Usuários-Alvo

### 2.1 Persona Primária: Consultor Político

| Atributo | Detalhe |
|----------|---------|
| **Cargo** | Consultor de campanha / Marqueteiro político |
| **Contexto** | Gerencia estratégia de comunicação de candidatos |
| **Dor principal** | Precisa antecipar reação pública a posicionamentos e crises |
| **Nível técnico** | Baixo a médio — usa ferramentas digitais mas não programa |
| **Como usa** | Via assistente técnico que roda o CLI |
| **Valor esperado** | Relatório com distribuição de sentimento + argumentos-chave + recomendações estratégicas |

### 2.2 Persona Secundária: Político / Assessor Direto

| Atributo | Detalhe |
|----------|---------|
| **Cargo** | Vereador, deputado, prefeito ou assessor de gabinete |
| **Contexto** | Precisa decidir posicionamento sobre temas polêmicos |
| **Dor principal** | Não sabe como eleitorado vai reagir a uma decisão |
| **Nível técnico** | Baixo — consome relatórios, não opera ferramentas |
| **Como usa** | Recebe o relatório em markdown/PDF do consultor |
| **Valor esperado** | Mapa claro de riscos e oportunidades por segmento do eleitorado |

[AUTO-DECISION] "O MVP deve ter interface gráfica?" → Não. O produto roda como AIOS Skill via CLI. O output é um relatório markdown que pode ser convertido em PDF. A persona primária (consultor) tem um assistente técnico que opera o CLI. Razão: Alinhado com as restrições técnicas (AIOS Skill, sem web UI) e com a filosofia CLI First do AIOS.

---

## 3. Funcionalidades Core

### 3.1 Geração de Painel Virtual (Swarm Assembly)

O sistema cria um conjunto de agentes AI, cada um com um perfil cognitivo distinto que simula um segmento da população. Cada agente tem:

- **Perfil demográfico:** idade, gênero, região, classe social, escolaridade
- **Perfil psicográfico:** valores, prioridades, fontes de informação, viéses cognitivos
- **Contexto informacional:** o que esse perfil "sabe" sobre o tema (baseado em suas fontes)
- **Personalidade deliberativa:** como processa informação (analítico vs. emocional, cauteloso vs. impulsivo)

O painel é configurável: o usuário pode escolher a composição demográfica (ex: "simular eleitorado de São Paulo capital" vs. "simular eleitores evangélicos do Nordeste").

### 3.2 Simulação de Deliberação (Swarm Deliberation)

Os agentes do painel recebem o tema/pergunta política e passam por rodadas de deliberação:

1. **Opinião individual:** Cada agente forma sua opinião inicial baseada em seu perfil e contexto
2. **Exposição a argumentos:** Agentes são expostos aos argumentos uns dos outros (simulando debate público)
3. **Revisão de opinião:** Agentes podem mudar ou reforçar sua posição após exposição
4. **Consolidação:** Opinião final de cada agente com justificativa

Esse processo captura fenômenos reais como: influência social, efeito câmara de eco, polarização, mudança de opinião por argumento forte.

### 3.3 Agregação e Análise (Opinion Aggregation)

O sistema agrega as opiniões individuais em métricas coletivas:

- **Distribuição de sentimento:** % a favor, contra, neutro, indeciso — por segmento
- **Intensidade:** Quão forte é o sentimento (fraco vs. veemente)
- **Argumentos-chave:** Os 5-10 argumentos mais citados/influentes, por posição
- **Vulnerabilidades:** Argumentos que causam maior mudança de opinião (pontos fracos narrativos)
- **Clusters de opinião:** Grupos que pensam de forma similar e por quê

### 3.4 Geração de Relatório (Report Generation)

Output final em markdown estruturado contendo:

- **Sumário executivo:** 3-5 parágrafos com conclusões acionáveis
- **Dashboard de sentimento:** Tabelas com distribuição por segmento
- **Mapa de argumentos:** Argumentos por posição, ranqueados por impacto
- **Análise de vulnerabilidades:** Pontos fracos narrativos com recomendações
- **Recomendações estratégicas:** O que fazer com base na simulação
- **Metodologia:** Como a simulação foi configurada (para transparência)

### 3.5 Ingestão de Contexto (Context Ingestion)

O usuário pode enriquecer a simulação com documentos de contexto:

- **Pesquisas existentes:** Dados de pesquisas reais para calibrar os perfis
- **Notícias recentes:** Para contextualizar os agentes sobre o momento atual
- **Posts de redes sociais:** Para capturar o "humor" real da população
- **Documentos de campanha:** Posicionamentos oficiais do candidato

---

## 4. Requisitos Funcionais

### 4.1 Funcionais (FR)

**Configuração de Simulação:**

- **FR1:** O sistema deve permitir configurar o tema/pergunta da simulação via argumento CLI ou prompt interativo
- **FR2:** O sistema deve aceitar documentos de contexto opcionais (markdown, texto, YAML) como input adicional
- **FR3:** O sistema deve permitir selecionar presets de composição demográfica (ex: "brasil-geral", "sp-capital", "nordeste-evangelico") ou criar composição customizada
- **FR4:** O sistema deve permitir configurar o número de agentes no painel (padrão: 20, range: 10-50)
- **FR5:** O sistema deve permitir configurar o número de rodadas de deliberação (padrão: 3, range: 1-5)

**Geração de Agentes:**

- **FR6:** O sistema deve gerar perfis de agentes com atributos demográficos e psicográficos distintos, seguindo a composição configurada
- **FR7:** Cada agente deve ter um system prompt único que encapsula seu perfil cognitivo, viéses e fontes de informação
- **FR8:** O sistema deve aplicar modelos mentais de Charlie Munger (viéses cognitivos) e princípios de influência de Cialdini na construção dos perfis
- **FR9:** O sistema deve armazenar os perfis gerados em arquivo YAML para auditoria e reuso

**Deliberação:**

- **FR10:** O sistema deve conduzir rodadas de deliberação onde cada agente é spawned como sub-agente via Agent tool
- **FR11:** Na rodada 1, cada agente deve formar opinião individual sem exposição a outros
- **FR12:** Nas rodadas subsequentes, cada agente deve receber um resumo dos argumentos das rodadas anteriores antes de opinar
- **FR13:** O sistema deve capturar para cada agente: posição (a favor/contra/neutro/indeciso), intensidade (1-5), argumentos principais, e flag de mudança de opinião
- **FR14:** O sistema deve detectar e registrar mudanças de opinião entre rodadas (qual argumento causou a mudança)

**Agregação:**

- **FR15:** O sistema deve calcular distribuição de sentimento geral e por segmento demográfico
- **FR16:** O sistema deve ranquear argumentos por frequência e por impacto (medido por mudanças de opinião causadas)
- **FR17:** O sistema deve identificar argumentos-vulnerabilidade (que causam > 20% de mudança de opinião num segmento)
- **FR18:** O sistema deve identificar clusters de opinião via análise de similaridade de argumentos

**Relatório:**

- **FR19:** O sistema deve gerar relatório final em markdown com todas as seções definidas em 3.4
- **FR20:** O relatório deve incluir metadados: data, configuração usada, número de agentes, rodadas, contexto ingerido
- **FR21:** O relatório deve ser salvo em `skills/politica-app/output/{timestamp}-{slug}/report.md`
- **FR22:** O sistema deve salvar dados brutos da simulação em YAML no mesmo diretório para análise posterior

**Reutilização:**

- **FR23:** O sistema deve permitir reutilizar painéis de agentes entre simulações (carregar perfis de YAML anterior)
- **FR24:** O sistema deve permitir rodar cenários comparativos (mesmo painel, perguntas diferentes)

### 4.2 Não-Funcionais (NFR)

**Performance:**

- **NFR1:** Uma simulação completa (20 agentes, 3 rodadas) deve completar em no máximo 15 minutos de wall-clock time
- **NFR2:** O sistema deve paralelizar agentes quando possível (múltiplos Agent tool calls em paralelo)
- **NFR3:** O sistema deve mostrar progresso durante execução (ex: "Rodada 2/3 — Agente 15/20")

**Qualidade da Simulação:**

- **NFR4:** Os perfis de agentes devem ser suficientemente diversos para representar o espectro de opinião — nenhum segmento demográfico relevante deve ser ignorado
- **NFR5:** Os argumentos gerados devem ser plausíveis e ancorados no contexto fornecido, não alucinações genéricas
- **NFR6:** A distribuição de sentimento deve ser razoável (não 100% para um lado) salvo em temas com consenso real

**Confiabilidade:**

- **NFR7:** O sistema deve ser idempotente — mesma configuração + mesmo contexto deve produzir resultados consistentes (não idênticos, mas na mesma faixa)
- **NFR8:** O sistema deve tratar falhas de agentes individuais gracefully (agente que falha não trava a simulação inteira)
- **NFR9:** O sistema deve salvar checkpoints entre rodadas para permitir retomada em caso de falha

**Usabilidade:**

- **NFR10:** O SKILL.md deve ser auto-documentado: qualquer pessoa que leia deve entender como rodar
- **NFR11:** Mensagens de erro devem ser claras e acionáveis, em português
- **NFR12:** O relatório final deve ser legível por não-técnicos (sem jargão de AI/ML)

---

## 5. Arquitetura de Alto Nível

### 5.1 Como Funciona como AIOS Skill

```
skills/politica-app/
├── SKILL.md                    # Entry point — docs + instruções de uso
├── config.yaml                 # Configuração padrão (agentes, rodadas, presets)
├── presets/                    # Presets de composição demográfica
│   ├── brasil-geral.yaml
│   ├── sp-capital.yaml
│   └── custom-template.yaml
├── templates/                  # Templates de prompt para agentes
│   ├── agent-persona.md        # Template do system prompt de cada agente
│   ├── deliberation-round.md   # Template de cada rodada
│   └── report-template.md      # Template do relatório final
├── output/                     # Outputs das simulações
│   └── {timestamp}-{slug}/
│       ├── report.md           # Relatório final
│       ├── panel.yaml          # Perfis dos agentes
│       ├── rounds/             # Dados brutos por rodada
│       │   ├── round-1.yaml
│       │   ├── round-2.yaml
│       │   └── round-3.yaml
│       └── aggregation.yaml    # Dados agregados
└── README.md                   # Documentação técnica
```

### 5.2 Fluxo de Execução

```
[1. Input]              [2. Assembly]           [3. Deliberation]
Tema + Contexto    →    Gerar Painel       →    Rodada 1 (individual)
                        (N agentes)             Rodada 2 (com argumentos)
                                                Rodada N (consolidação)

[4. Aggregation]        [5. Report]
Calcular métricas  →    Gerar relatório
Identificar              Salvar output
vulnerabilidades
```

### 5.3 Integração com Ecossistema AIOS

| Recurso AIOS | Como é Usado |
|--------------|-------------|
| **Agent tool** | Spawn de cada agente do painel como sub-agente |
| **Read/Write/Edit** | Leitura de contexto, escrita de outputs |
| **Bash** | Processamento local de dados (sorting, parsing) |
| **WebSearch/WebFetch** | Pesquisa de contexto adicional quando solicitado |
| **Mind: charlie-munger** | Modelos mentais e viéses cognitivos para perfis de agentes |
| **Mind: robert-cialdini** | Princípios de influência social para simulação de propagação |
| **Skill: deep-research** | Análise profunda de documentos de contexto |
| **Squad: icp-cloning** | Referência para geração de personas de alta fidelidade |

---

## 6. Restrições Técnicas

| Restrição | Detalhe |
|-----------|---------|
| **Runtime** | AIOS Skill — roda exclusivamente dentro do Claude Code CLI |
| **Sem banco de dados** | Estado persistido via YAML/JSON no filesystem |
| **Sem web UI** | Output é markdown; conversão para PDF é responsabilidade do usuário |
| **Sem deploy externo** | Roda 100% local na máquina do operador |
| **Dependência única** | Claude API (via Agent tool) — sem dependências externas adicionais |
| **Sem treinamento** | Não treina modelos — usa prompting e persona engineering |
| **Limite de agentes** | Máximo 50 agentes por simulação (limitado por context window e custo) |
| **Idioma** | Output em pt-BR; internals podem ser em inglês |

---

## 7. Suposições Técnicas

### 7.1 Estrutura do Repositório

- **Skill AIOS:** Vive em `skills/politica-app/` dentro do monorepo aios-core
- **Sem package.json próprio:** Não é um projeto Node.js separado — é um conjunto de markdowns e YAMLs orquestrado pelo Claude Code

### 7.2 Premissas de Execução

- O operador tem Claude Code instalado e configurado com API key válida
- O operador tem acesso de leitura/escrita ao diretório `skills/politica-app/`
- O Agent tool do Claude Code suporta spawn de múltiplos sub-agentes
- Cada sub-agente (agente do painel) roda com seu próprio context window

### 7.3 Testes

- **Sem testes unitários tradicionais** (não é código compilável)
- **Validação por dry-run:** Rodar simulação com painel pequeno (5 agentes, 1 rodada) para verificar pipeline
- **Validação qualitativa:** Comparar output com intuição/dados reais quando disponíveis

[AUTO-DECISION] "Qual framework de testes usar?" → Nenhum. O produto não é código executável — é um conjunto de prompts e templates orquestrado pelo Claude Code. A "testabilidade" vem de dry-runs com painéis pequenos. Razão: AIOS Skills são markdown-driven, não code-driven.

---

## 8. Métricas de Sucesso

### 8.1 Métricas de Adoção (MVP)

| Métrica | Target | Como Medir |
|---------|--------|------------|
| Simulação completa sem erro | > 90% das execuções | Logs de output |
| Tempo de execução (20 agentes) | < 15 min | Timestamp nos outputs |
| Diversidade de argumentos | > 10 argumentos únicos por simulação | Contagem no report |
| Relatório legível por não-técnico | Aprovação qualitativa | Review manual |

### 8.2 Métricas de Valor (Pós-MVP)

| Métrica | Target | Como Medir |
|---------|--------|------------|
| Correlação com pesquisas reais | > 60% de alinhamento direcional | Comparação com dados reais |
| Reuso de painéis | > 50% das simulações reutilizam painel | Contagem de loads vs. creates |
| Cenários comparativos por sessão | > 2 cenários por sessão | Contagem de outputs |
| Satisfação do consultor | NPS > 7 | Feedback qualitativo |

---

## 9. Escopo — O que Está FORA

Para manter o MVP enxuto, as seguintes funcionalidades estão **explicitamente fora de escopo**:

| Funcionalidade | Motivo da Exclusão | Quando Considerar |
|----------------|-------------------|-------------------|
| Web UI / Dashboard | Restrição técnica (AIOS Skill) + MVP focus | Epic futuro se validado |
| Banco de dados | Restrição técnica + desnecessário para MVP | Nunca (file-based é suficiente) |
| Integração com redes sociais em tempo real | Complexidade alta, valor incremental | Pós-MVP, via skill sherlock |
| Treinamento/fine-tuning de modelos | Fora do paradigma AIOS Skill | Provavelmente nunca |
| Multi-idioma | MVP focado em Brasil/pt-BR | Quando houver demanda |
| Calibração estatística com dados reais | Requer dados pagos + complexidade | Epic de calibração pós-MVP |
| Exportação para PowerPoint/PDF | Markdown é suficiente; conversão é trivial | Se houver demanda |
| API REST para integração | Contradiz AIOS Skill pattern | Se virar produto standalone |

---

## 10. Riscos e Mitigações

### 10.1 Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Context window overflow** com muitos agentes | Alta | Alto | Limitar a 50 agentes; usar resumos entre rodadas em vez de transcrições completas |
| **Custo de API alto** em simulações grandes | Média | Médio | Configuração de limites; dry-run barato antes de simulação completa |
| **Agentes convergem para mesma opinião** (falta de diversidade) | Média | Alto | Perfis com instruções fortes de viés; "temperature" alta nos prompts de opinião |
| **Latência alta** no spawn de sub-agentes | Média | Médio | Paralelização; progress feedback ao usuário |
| **Agent tool não suporta paralelismo** real | Baixa | Alto | Fallback para execução sequencial com batching |

### 10.2 Riscos de Produto

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Output não é acionável** para consultores | Média | Crítico | Template de relatório revisado por consultor real; seção de recomendações explícitas |
| **Resultados não correlacionam com realidade** | Alta (no MVP) | Médio | Posicionar como "ferramenta exploratória", não como "pesquisa substituta" |
| **Viés sistemático** do LLM contamina simulação | Alta | Alto | Perfis com instruções contrárias ao viés default do LLM; rodadas de "adversarial prompting" |
| **Questões éticas** sobre simulação de opinião | Média | Alto | Transparência na metodologia; disclaimer no relatório; uso apenas consultivo |

### 10.3 Riscos de Negócio

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Consultores não confiam** em AI para isso | Alta | Crítico | Começar como "complemento" à pesquisa real, não substituto; mostrar metodologia |
| **Regulação de AI em campanha** | Média | Alto | Manter uso como ferramenta interna de análise, não propaganda |
| **Concorrência de ferramentas pagas** | Baixa (hoje) | Médio | Diferencial: customização total + roda local + sem lock-in |

---

## 11. Estrutura de Epics e Stories

### Epic 1: Fundação e Geração de Painel

**Objetivo:** Estabelecer a estrutura da skill e implementar a geração de painéis de agentes virtuais com perfis cognitivos diversos.

| Story | Título | Descrição |
|-------|--------|-----------|
| 1.1 | Scaffold da Skill | Criar estrutura de diretórios, SKILL.md, config.yaml, templates base, presets demográficos |
| 1.2 | Gerador de Perfis de Agentes | Implementar template de persona + engine de geração de perfis baseada em presets demográficos e princípios de Munger/Cialdini |
| 1.3 | Presets Demográficos | Criar 3 presets iniciais (brasil-geral, sp-capital, nordeste-evangelico) com composição validada por dados do IBGE/TSE |
| 1.4 | Validação de Painel | Dry-run de geração de painel com 10 agentes; validar diversidade e qualidade dos perfis |

**Estimativa:** 4 stories, complexidade média

---

### Epic 2: Motor de Deliberação

**Objetivo:** Implementar o core da simulação — as rodadas de deliberação onde agentes formam e revisam opiniões.

| Story | Título | Descrição |
|-------|--------|-----------|
| 2.1 | Rodada 1: Opinião Individual | Template de prompt para formação de opinião individual; spawn de agentes via Agent tool; captura de output estruturado (YAML) |
| 2.2 | Sumarização Inter-Rodada | Engine de sumarização que condensa argumentos da rodada anterior para injeção na próxima |
| 2.3 | Rodadas 2+: Deliberação com Exposição | Template de prompt com argumentos anteriores; detecção de mudança de opinião; registro de "gatilho de mudança" |
| 2.4 | Orquestrador de Simulação | Pipeline completo: input → assembly → rodadas → output. Progresso visual. Tratamento de falhas. Checkpoints |
| 2.5 | Dry-Run End-to-End | Simulação completa com 10 agentes e 2 rodadas; validação do pipeline inteiro |

**Estimativa:** 5 stories, complexidade alta

---

### Epic 3: Agregação e Relatório

**Objetivo:** Transformar os dados brutos da deliberação em insights acionáveis via relatório estruturado.

| Story | Título | Descrição |
|-------|--------|-----------|
| 3.1 | Engine de Agregação | Calcular métricas: distribuição de sentimento, intensidade, argumentos ranqueados, vulnerabilidades, clusters |
| 3.2 | Template de Relatório | Markdown template com todas as seções (sumário, dashboard, mapa de argumentos, vulnerabilidades, recomendações, metodologia) |
| 3.3 | Gerador de Recomendações | Engine que transforma dados agregados em recomendações estratégicas contextualizadas |
| 3.4 | Ingestão de Contexto | Pipeline de leitura e processamento de documentos de contexto (pesquisas, notícias, posts) |
| 3.5 | Simulação Completa de Validação | Simulação realista (20 agentes, 3 rodadas, com contexto) + review qualitativo do relatório |

**Estimativa:** 5 stories, complexidade média-alta

---

### Epic 4: Refinamento e Reutilização

**Objetivo:** Permitir cenários comparativos, reutilização de painéis e fluxo polish para uso em produção.

| Story | Título | Descrição |
|-------|--------|-----------|
| 4.1 | Reutilização de Painéis | Carregar painel de simulação anterior via path; validar integridade dos perfis |
| 4.2 | Cenários Comparativos | Rodar múltiplas simulações com mesmo painel + perguntas diferentes; relatório comparativo |
| 4.3 | Composição Customizada | Interface CLI para criar preset demográfico customizado (sem usar os predefinidos) |
| 4.4 | Polish de Relatório | Refinamento do template com base em feedback; inclusão de disclaimer ético; formatação para impressão |

**Estimativa:** 4 stories, complexidade baixa-média

---

## 12. Suposições e Decisões Autônomas

Todas as decisões tomadas autonomamente durante a criação deste PRD:

| Decisão | Pergunta Implícita | Escolha | Razão |
|---------|-------------------|---------|-------|
| [AUTO-DECISION] Validação contra pesquisas reais | Precisa no MVP? | Não | MVP focus — insight qualitativo já é acionável |
| [AUTO-DECISION] Interface gráfica | Precisa de UI? | Não | Restrição técnica (AIOS Skill) + CLI First |
| [AUTO-DECISION] Framework de testes | Qual usar? | Nenhum | Skills são markdown-driven, não code-driven |
| [AUTO-DECISION] Número de presets iniciais | Quantos criar? | 3 | Suficiente para demonstrar valor sem over-engineering |
| [AUTO-DECISION] Limite de agentes | Qual o máximo? | 50 | Balanceamento entre diversidade e custo/context window |
| [AUTO-DECISION] Idioma do output | Multi-idioma? | Apenas pt-BR no MVP | Mercado-alvo é Brasil |
| [AUTO-DECISION] Formato de dados internos | JSON ou YAML? | YAML | Mais legível para humanos; padrão AIOS |
| [AUTO-DECISION] Rodadas de deliberação | Quantas por default? | 3 | Pesquisas sobre deliberação mostram convergência em 3-5 rodadas |
| [AUTO-DECISION] Sequência de epics | Como ordenar? | Fundação → Motor → Relatório → Refinamento | Dependência lógica: precisa de painel antes de deliberar, de dados antes de agregar |

---

## 13. Resultados da Checklist PM

### Resumo Executivo

- **Completude do PRD:** ~85%
- **Escopo MVP:** Adequado (Just Right)
- **Prontidão para arquitetura:** Ready (com ressalvas)
- **Lacunas críticas:** Nenhum blocker

### Categorias

| Categoria | Status | Observações |
|-----------|--------|-------------|
| 1. Definição do Problema & Contexto | PASS | Problema claro, personas definidas, métricas estabelecidas |
| 2. Definição de Escopo MVP | PASS | Escopo enxuto com exclusões documentadas |
| 3. Requisitos de UX | N/A | Sem UI — output é markdown |
| 4. Requisitos Funcionais | PASS | 24 FRs cobrindo todas as funcionalidades core |
| 5. Requisitos Não-Funcionais | PASS | 12 NFRs cobrindo performance, qualidade, confiabilidade |
| 6. Estrutura de Epics & Stories | PASS | 4 epics, 18 stories, sequenciamento lógico |
| 7. Orientação Técnica | PARTIAL | Arquitetura definida mas detalhes de prompt engineering ficam para @architect |
| 8. Requisitos Cross-Functional | PARTIAL | Sem integrações externas no MVP; storage é file-based |
| 9. Clareza & Comunicação | PASS | Documento em pt-BR com acentuação correta, estrutura clara |

### Recomendações

1. **HIGH:** Definir com @architect a estratégia de prompt engineering para maximizar diversidade de opiniões dos agentes (risco de convergência é o maior risco técnico)
2. **MEDIUM:** Validar os presets demográficos com dados reais do IBGE/TSE antes de implementar
3. **MEDIUM:** Incluir pelo menos um "cenário de teste canônico" (ex: "reforma tributária") para validação qualitativa do pipeline
4. **LOW:** Considerar integração futura com a skill `sherlock-investigator` para ingestão automatizada de dados de redes sociais

### Decisão Final

**READY FOR ARCHITECT** — O PRD está completo e suficientemente detalhado para a fase de design arquitetural. As lacunas identificadas (prompt engineering, validação de presets) são naturalmente resolvidas durante a implementação dos epics.

---

## 14. Próximos Passos

### Prompt para @architect

> Analise o PRD em `.aios/forge-runs/forge-politica-app-20260323-2242/spec/prd.md` e crie o documento de arquitetura para a skill `politica-app`. Foco especial em: (1) estratégia de prompt engineering para diversidade de agentes, (2) orquestração de sub-agentes via Agent tool com paralelismo, (3) estrutura de dados YAML para persistência entre rodadas.

### Prompt para @sm

> Com base no PRD em `.aios/forge-runs/forge-politica-app-20260323-2242/spec/prd.md`, crie as stories detalhadas para o Epic 1 (Fundação e Geração de Painel). Cada story deve incluir acceptance criteria testáveis via dry-run.

---

*Morgan, planejando o futuro*
