# Task: QA Review

**Agente:** @qa-sentinel
**Fase:** 7 (QA Final)
**Gate:** QG-AR-7

## Objetivo

Validação final binária (14/14 checklist) + Devil's Advocate + gate humano.

## Input

- `reel_file`: Reel editado final (fase 5)
- `caption`: Caption Instagram (fase 6)
- `all_phase_outputs`: Outputs de todas as 6 fases anteriores

## Processo

1. Assistir reel frame-by-frame (heurística QS-03)
2. Executar checklist 14 itens (binário: PASS ou FAIL cada)
3. Se 14/14 → executar Devil's Advocate
4. DA DEVE encontrar 3+ weak points (DA que não encontra = inválido, refazer)
5. Compilar relatório e apresentar para gate humano

## Checklist 14 Itens

### Hook (4 itens)
1. Primeiros 3s capturam atenção
2. Fórmula comprovada identificável
3. Curiosity gap presente
4. Viável visualmente (não só texto)

### Storytelling (3 itens)
5. 7 beats presentes e na ordem correta
6. Insight depois da ação (não antes)
7. Arco narrativo completo (não termina no ar)

### Copy (3 itens)
8. Voice DNA consistente (tom, vocabulário)
9. CTA específico e claro
10. Caption alinhada com conteúdo do reel

### Posicionamento (3 itens)
11. Conteúdo reflete expertise real
12. Não promete resultados irreais
13. Diferenciação clara (não genérico)

### Técnico (1 item)
14. Specs OK (1080x1920, -14 LUFS, legendas sync, grain)

## Devil's Advocate

Após 14/14 PASS, o QA Sentinel DEVE:
- Identificar 3+ pontos fracos com fonte referenciada
- Sugerir melhoria concreta por ponto
- **Regra:** DA que não encontra falhas = inválido → refazer DA
- Fontes: hook-formulas.md, positioning.md, voice-dna.md, ai-writing-guardrail.md

## Output

```yaml
qa_report:
  checklist_score: "X/14"
  items:
    - id: 1
      description: "Primeiros 3s capturam atenção"
      result: "PASS/FAIL"
      note: "..."
    # ... (14 itens)
  devils_advocate:
    weak_points:
      - point: "..."
        source: "..."
        suggestion: "..."
    # ... (3+ pontos)
  recommendation: "PUBLICAR / REVISAR (fase X) / DESCARTAR"
  human_decision: "PENDENTE"
```

## Quality Gate QG-AR-7

| Critério | Obrigatório |
|----------|-------------|
| 14/14 checklist PASS | SIM |
| Devil's Advocate com 3+ weak points | SIM |
| Aprovação humana (Tiago) | SIM — BLOCKING |

## Veto Conditions

- Checklist < 14/14 → **GATE-FAIL** (retornar à fase correspondente ao item que falhou)
- DA sem weak points → **DA INVÁLIDO** (refazer — impossível que tudo seja perfeito)
- Sem aprovação humana → **NUNCA PUBLICAR** (gate blocking, sem exceção)
- Reel não assistido frame-by-frame → **QA INVÁLIDO** (refazer assistindo)
