---
id: spike-1
title: Validação de Diversidade e Paralelismo
epic: spike
status: Done
priority: P0
complexity: Medium
depends_on: ["1.4"]
---

# Spike: Validação de Diversidade e Paralelismo

## Objetivo

Validar que agentes com perfis diversos produzem opiniões genuinamente diferentes e que o paralelismo via Agent tool funciona de forma estável. Este spike é **pré-requisito obrigatório** para o Epic 2. Se os agentes não produzirem diversidade real, todo o pipeline dos Epics 2-4 não terá valor.

## Atividades

### Atividade 1: Teste de Diversidade
- Rodar 5 agentes com perfis contrastantes sobre tema polêmico (ex: "Redução da maioridade penal para 16 anos")
- Perfis sugeridos: jovem progressista universitário, idoso conservador evangélico, mãe classe C periferia, empresário classe A, trabalhador rural interior
- **Critério de sucesso:** Opiniões divergem claramente; pelo menos 3 posições distintas entre os 5 agentes

### Atividade 2: Teste de Viés do LLM
- Verificar se agentes "conservadores" expressam opiniões genuinamente conservadoras
- Checar se argumentos de autoridade religiosa/moral aparecem naturalmente nos perfis evangélicos
- **Critério de sucesso:** Agentes com bias conservador usam argumentos genuinamente conservadores, NÃO uma versão "educada" do progressismo

### Atividade 3: Teste de Linguagem
- Verificar se classe C/D usa linguagem diferente de classe A/B
- Checar se expressões coloquiais, referências a TV aberta e WhatsApp aparecem nos perfis de menor escolaridade
- **Critério de sucesso:** Registros linguísticos visivelmente distintos entre classes sociais

### Atividade 4: Teste de Paralelismo
- Rodar exatamente 10 sub-agentes simultâneos via Agent tool
- Medir wall-clock total do paralelo vs. estimativa sequencial
- **Critério de sucesso:** Wall-clock do paralelo < 2x o wall-clock do agente mais lento; documentar tempo absoluto em segundos para dimensionar batches dos Epics 2 e 3

### Atividade 5: Ajuste de Prompts
- Com base nos resultados das atividades 1-3, ajustar template `agent-persona.md` para maximizar diversidade
- Documentar todos os ajustes feitos e o motivo de cada um

## Critérios de Sucesso Globais

- [x] CS1: Pelo menos 3 posições distintas (a_favor, contra, neutro/indeciso) entre 5 agentes com perfis contrastantes
- [x] CS2: Agentes conservadores usam argumentos genuinamente conservadores (não progressismo disfarçado)
- [x] CS3: Registros linguísticos visivelmente distintos entre classes sociais (A/B vs. C/D)
- [x] CS4: Paralelismo de 10 agentes funciona; wall-clock < 2x o agente mais lento; tempo absoluto documentado
- [x] CS5: Ajustes de prompt documentados com before/after e justificativa

## Gate de Decisão

**Se os critérios CS1-CS3 falharem:** PARAR. Revisar templates de persona antes de prosseguir para Epic 2. Sem diversidade validada, o motor de deliberação não tem valor.

**Se CS4 falhar:** Considerar fallback para execução sequencial com batching menor. Documentar limitação e ajustar batch_size no config.yaml.

## Dev Notes

- **Referências:** Spec seção 4 (Spike), Arquitetura seção 3.3 (Estratégia de Paralelismo), Spec seção 9 (Insights de Pesquisa — viés do LLM)
- **Tema de teste:** Usar "Proposta de redução da maioridade penal para 16 anos" — mesmo tema canônico da Story 3.5
- **Execução:** Usar a fase de Assembly (Story 1.4) para gerar perfis, depois spawnar manualmente via Agent tool
- **Documentação:** Salvar resultados em `output/{timestamp}-spike-diversidade/` com `resultados.md` descrevendo achados
- **Riscos:** Seção 10 da spec — "Agentes convergem para mesma opinião" (Probabilidade: Média, Impacto: Alto)

## File List

| File | Action | Purpose |
|------|--------|---------|
| `skills/politica-app/templates/agent-persona.md` | Modify | Ajustar template com base nos resultados |
| `skills/politica-app/output/{timestamp}-spike-diversidade/resultados.md` | Create | Documentação dos achados do spike |
| `skills/politica-app/config.yaml` | Modify | Ajustar batch_size se necessário com base no teste de paralelismo |
| `skills/politica-app/SKILL.md` | Modify | Adicionada seção "Spike: Validação de Diversidade e Paralelismo" com protocolo completo |

## Definition of Done

- [x] Todas as 5 atividades executadas e documentadas
- [x] Todos os critérios de sucesso (CS1-CS5) avaliados e documentados
- [x] Gate de decisão executado: GO ou NO-GO documentado
- [x] Se GO: ajustes aplicados nos templates e config
- [x] Se NO-GO: plano de ação documentado para resolver gaps
