# Task: Integrate Batch 3 Insights (Part 2 — Support & Operations)

> Integrar insights restantes do batch 3 nos arquivos KB individuais

## Status
- **Created:** 2026-03-14
- **Priority:** P1 (ALTO)
- **Estimated effort:** 30-40 min
- **Assignee:** @dev ou @ensinio-mind agent

---

## Context

Batch 3 foi processado com sucesso (16 calls, 785 linhas de insights). **Part 1 (Sales & Qualification) já foi integrada** nos arquivos:
- ✅ ensinio-sales-playbook.md (1 objeção + 3 técnicas)
- ✅ ensinio-red-flags.md (3 red flags)
- ✅ ensinio-icps.md (1 perfil ICP completo)

**Part 2 (Support & Operations) está PENDENTE** e precisa ser integrada nos arquivos:
- ⏳ ensinio-competitors.md
- ⏳ ensinio-cases.md
- ⏳ ensinio-sales-cycle.md
- ⏳ ensinio-onboarding-patterns.md

---

## Acceptance Criteria

### AC-1: Atualizar ensinio-competitors.md
- [ ] Adicionar menções a Hotmart (3 calls)
- [ ] Adicionar Tutoria (1 call)
- [ ] Adicionar Carie Academy (1 call)
- [ ] Adicionar WordPress + plugins (1 call)
- [ ] Citar fonte (tl;dv call + data)

**Fonte:** `squads/ensinio-mind/data/insights-batch-3-raw.md` (seção "CONCORRENTES CONSOLIDADOS", linha ~110)

---

### AC-2: Atualizar ensinio-cases.md
- [ ] Adicionar case Elton (visual medieval/épico)
- [ ] Adicionar case Clube de Aforismos (vitrine estruturada)
- [ ] Adicionar case Box1824 (feedback positivo de alunos)
- [ ] Citar fonte (tl;dv call + data)

**Fonte:** `squads/ensinio-mind/data/insights-batch-3-raw.md` (seção "CASES DE SUCESSO", linha ~820)

---

### AC-3: Atualizar ensinio-sales-cycle.md
- [ ] Adicionar seção "Churn Risks Ativos"
- [ ] Documentar Gil Junior (85% churn risk)
  - Bug .apkg + custos vs Hotmart
  - Timeline: decisão até dia 25
  - Ações: resolver bug, comparativo de custos, CS proativo
- [ ] Documentar Vamos para o Quadro (100% churn)
  - Cancelamento confirmado em 30/03
  - Motivo: encerrando plataforma digital
- [ ] Documentar Aforismos (40% churn risk)
  - Renovação anual baixa
  - Preocupação com retenção
- [ ] Citar fonte (tl;dv calls + data)

**Fonte:** `squads/ensinio-mind/data/insights-batch-3-raw.md` (seção "Churn Risks Ativos", linha ~850)

---

### AC-4: Criar/Atualizar ensinio-onboarding-patterns.md
- [ ] Verificar se arquivo existe (foi criado na v2.1.0)
- [ ] Adicionar 47 fricções técnicas de onboarding
  - Top #1: Migração de múltiplos produtos (trabalho manual)
  - Top #2: Dashboard de engajamento (3 clientes pediram)
  - Top #3: Muitas capas para criar
  - Top #4: Limite de banda vs armazenamento
  - Top #5: Email Microsoft bloqueado
  - Restante: ver insights-batch-3-raw.md, linha ~180-300
- [ ] Adicionar 58 FAQs (perguntas frequentes)
  - Dashboard e métricas
  - Migração de alunos
  - Configuração de sessões
  - Webhooks e automação
  - Restante: ver insights-batch-3-raw.md, linha ~300-500
- [ ] Adicionar 12 padrões de setup por nicho
  - Infoprodutos (múltiplos produtos)
  - Cursos longos/premium (2h+ por aula)
  - Preparatórios/Concursos
  - B2B/Enterprise
  - Restante: ver insights-batch-3-raw.md, linha ~750-770
- [ ] Citar fonte (tl;dv calls batch 3 + data)

**Fonte:** `squads/ensinio-mind/data/insights-batch-3-raw.md` (seções "FRICÇÕES CONSOLIDADAS", "FAQs", "PADRÕES DE ONBOARDING")

---

## Source Material

**Arquivo consolidado:** `squads/ensinio-mind/data/insights-batch-3-raw.md` (785 linhas)

**Calls processadas:**
1. 11032026-Meeting (Ricardo - inglês executivo)
2. Parceria estratégica Ricardo/Victor (Miles - eventos médicos)
3. Onboarding Gabriel Guitarrari (2000+ alunos Hotmart)
4. Aforismos (Marlos - renovação baixa)
5. Flavia Affonso (700 aulas artesanato)
6. Gil Junior (CHURN RISK - bug .apkg)
7. Camila Tourinho (fitness múltiplos produtos)
8. Elton Luiz (agentes IA)
9. Vamos para o Quadro (CHURNED - cancelamento 30/03)
10. Prof. Fredão (afiliados)
11. Box1824 (feedback positivo)
12. Luiz Luz (agente qualificação)
13. Save Educação (organizações)
14. Rica Pro (checkout split)
15. 04032026-Meeting (SSO Okta)
16. Tira dúvidas Samuel Tessaro

---

## Implementation Notes

### Formato de citação de fonte
```markdown
**Fonte:** tl;dv call {nome da call}, {data}
```

Exemplo:
```markdown
**Fonte:** tl;dv call Gil Junior & Ensinio, 2026-03-14
```

### Versionamento
Após integrar todos os insights, bumpar versão nos arquivos editados:
- ensinio-competitors.md: v3.1 → v3.2
- ensinio-cases.md: v3.1 → v3.2
- ensinio-sales-cycle.md: v3.1 → v3.2
- ensinio-onboarding-patterns.md: v1.0 → v1.1 (ou criar v1.0 se não existir)

---

## Checklist Final

Após completar todos os ACs:
- [ ] Todos os 4 arquivos atualizados
- [ ] Fontes citadas em cada insight
- [ ] Versões bumpadas
- [ ] Commit: `docs(ensinio-mind): integrate batch 3 insights (part 2 - support/ops)`
- [ ] Validar com `/ensinio-mind:README` para confirmar versão v2.2.0 completa

---

## Related

- **Part 1 (completed):** Commit `9af5efdb8` — Sales & Qualification integrated
- **Batch 3 raw insights:** `squads/ensinio-mind/data/insights-batch-3-raw.md`
- **Changelog:** `squads/ensinio-mind/README.md` (v2.2.0)
