# Story: Hardening do skill /audit-project-config

**Status:** In Progress
**Priority:** P0 (Critical)
**Effort:** 6.5h (3 sprints)
**Source:** Analise Tripartida 2026-03-18 (Kaizen 7.5 | Knowledge 8.0 | Process 4.2 VETO)
**Report:** `docs/reports/audit-project-config-analysis.md`

---

## Context

O skill `/audit-project-config` tem arquitetura solida mas foi vetado pelo @pedro-valerio (4.2/10) por ter 8 wrong paths criticos e zero enforcement em checkpoints. @oalanicolas identificou 3 gaps P0 de documentacao (template path, project types, placeholders). Kaizen identificou validacao superficial do settings.json e ausencia de dry-run.

Sem hardening, o skill pode: computar paths errados silenciosamente, fazer bulk corruption via auto-fix sem preview, e falhar silenciosamente no subprocess.

---

## Acceptance Criteria

### Sprint 1: Blockers (~3h)

- [x] **AC-1: Input Validation (Vetos 1-3)** — Skill DEVE validar ACTIVE.md antes de processar
  - VETO_1: Se `docs/projects/ACTIVE.md` nao existe -> HALT com mensagem clara
  - VETO_2: Se table nao tem colunas "Projeto" e "INDEX" -> HALT com schema esperado
  - VETO_3: Se 0 projetos parseados -> HALT com mensagem
  - Arquivos: `tools/audit-project-configs.js`

- [x] **AC-2: Path Safety (Vetos 4-6)** — Paths DEVEM ser validados antes de qualquer operacao
  - VETO_4: Link INDEX sem `.aios/` nem `docs/projects/` -> SKIP projeto + WARN
  - VETO_5: Path computado fora de project root esperado -> HALT
  - VETO_6: Path relativo nao resolve para absoluto -> HALT
  - Regra: Converter TUDO para path absoluto antes de operar
  - Arquivos: `tools/audit-project-configs.js`

- [x] **AC-3: Dry-Run Obrigatorio (Veto 7)** — Auto-fix DEVE mostrar preview antes de executar
  - Mostrar lista: projeto -> destination path -> tipo
  - Opcao "corrigir 1 primeiro (validacao)" antes de batch (--first-only)
  - Se primeiro fix falha -> HALT batch inteiro (Veto 8)
  - Destination not writeable -> SKIP + WARN (Veto 9)
  - Arquivos: `tools/fix-project-configs.js`

- [x] **AC-4: Validacao Profunda settings.json** — Detectar erros conhecidos
  - Check `hooks` como array (erro fatal, ref: `.claude/rules/settings-format.md`)
  - Check matchers incorretos (objeto em vez de string)
  - Check `permissions.allow` e `permissions.deny` existem
  - Severidade por check: CRITICAL / HIGH / MEDIUM
  - Arquivos: `tools/audit-project-configs.js`

### Sprint 2: Critical (~2h)

- [ ] **AC-5: Subprocess Error Handling (Vetos 10-12)** — Capturar e validar output
  - VETO_10: Exit code != 0 -> HALT batch com stderr
  - VETO_11: Arquivo esperado nao criado apos sucesso -> ROLLBACK + HALT
  - VETO_12: Arquivo criado mas JSON/Markdown invalido -> ROLLBACK + HALT
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

- [ ] **AC-6: Validation Layer Separation** — 3 camadas explicitas
  - L1 Structural: Arquivos existem?
  - L2 Semantic: Conteudo valido? (keys, placeholders, hooks format)
  - L3 Temporal: Atualizado? (template version hash)
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

- [ ] **AC-7: Template Structure Docs** — Documentar dependencias externas
  - Adicionar secao "Template Structure" com path tree
  - Listar project types validos (enum)
  - Adicionar tabela de placeholders com exemplos
  - Adicionar Mode Selection Guide (CENTRALIZED vs HYBRID)
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

### Sprint 3: Enhancements (~1.5h)

- [ ] **AC-8: Relatorio Exportavel** — Salvar audit report em arquivo
  - Gerar `docs/reports/audit-{timestamp}.md`
  - Perguntar ao usuario se quer salvar
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

- [ ] **AC-9: Health Score Summary** — Nota geral do ecossistema
  - Linha: `Project Health: 15/20 OK (75%)`
  - Before/After delta quando auto-fix e usado
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

- [ ] **AC-10: Placeholder Detection Context-Aware** — Evitar falsos positivos
  - Ignorar `{{` dentro de code blocks (triple backtick)
  - Ignorar `{{` em comentarios HTML
  - Se ambiguo -> perguntar ao usuario
  - Arquivos: `.aios/skills/audit-project-config/SKILL.md`

---

## Definition of Done

- [ ] Todos os ACs de Sprint 1 implementados (P0 blockers resolvidos)
- [ ] Skill atualizado com vetos, dry-run, e validacoes
- [ ] Report de analise referenciado na story
- [ ] Score @pedro-valerio >= 7.0 (atualmente 4.2)
- [ ] Score Kaizen >= 9.0 (atualmente 7.5)
- [ ] Score Knowledge >= 9.0 (atualmente 8.0)

---

## File List

| Arquivo | Status | Descricao |
|---------|--------|-----------|
| `tools/audit-project-configs.js` | Modificado (v2.0) | Script de audit com vetos + validation layers |
| `tools/fix-project-configs.js` | Modificado (v2.0) | Script de fix com dry-run + first-fix |
| `.aios/skills/audit-project-config/SKILL.md` | Modificado (v2.0) | Skill com docs completos |
| `docs/reports/audit-project-config-analysis.md` | Criado | Relatorio tripartido |
| `docs/reports/project-config-audit.md` | Gerado | Ultimo audit report |

---

## References

- Analise Tripartida: `docs/reports/audit-project-config-analysis.md`
- Settings Format Rules: `.claude/rules/settings-format.md`
- Story similar (vetos): `docs/stories/active/TRANS-2-add-veto-conditions.md`

---

## Axiomas Aplicaveis

### Process (@pedro-valerio)
- PV_PATH_INFERENCE: Path por heuristica sem validar
- PV_BULK_ACTION: Batch sem validacao individual
- PV_USER_CHOICE_BYPASS: Escolha sem validation
- PV_RELATIVE_PATH_HELL: `../` em path computation
- PV_TABLE_PARSE_BLIND: Parse Markdown sem schema

### Knowledge (@oalanicolas)
- AN_KE_001: Domain Boundary via User Consent
- AN_KE_002: External Dependency Documentation
- AN_KE_003: Implicit Knowledge Triage
- AN_KE_004: Validation Layer Separation
- AN_KE_005: Progressive Disclosure for Skills
- AN_KE_006: External Dependency Graph
