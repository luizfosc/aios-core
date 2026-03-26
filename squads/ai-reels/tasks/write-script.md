# Task: Write Script

**Agente:** @script-director
**Fase:** 2 (Script)
**Gate:** QG-AR-2

## Objetivo

Escrever roteiro completo com 7 beats + direção de performance 10D por beat.

## Input

- `selected_hook`: Hook aprovado da fase 1
- `trigger_type`: Tipo de trigger psicológico
- `retention_strategy`: Estratégia de retenção
- `duration_target`: Duração alvo (default: 60s)

## Processo

1. Estruturar os 7 beats do Eight-Point Arc (Blackman)
2. Distribuir timing por beat (~150 palavras/min PT-BR)
3. Escrever direção de performance 10D por beat
4. Validar fluxo narrativo e timing total

## 7 Beats (para reel de 60s)

| Beat | Tempo | Função |
|------|-------|--------|
| HOOK | 0-3s | Capturar atenção (da fase 1) |
| STASIS | 3-8s | Estabelecer contexto/mundo |
| TRIGGER | 8-15s | Evento que muda tudo |
| RISING | 15-30s | Construir tensão/argumento |
| INSIGHT | 30-42s | Revelação/ponto alto |
| RESOLUTION | 42-50s | Consequência/proof |
| CTA | 50-60s | Call to action específico |

## Output

```yaml
script:
  beats:
    - beat: HOOK
      text: "..."
      duration_s: 3
      direction_10D: "Close-up, olhar direto câmera, tom urgente..."
    # ... (7 beats)
  total_words: X
  estimated_duration_s: X
  performance_notes: "..."
```

## Quality Gate QG-AR-2

| Critério | Obrigatório |
|----------|-------------|
| 7 beats completos | SIM |
| Direção 10D por beat | SIM |
| Timing validado (~150 wpm PT-BR) | SIM |
| Duração total 15-90s | SIM |
| Insight DEPOIS da ação (beat order) | SIM |

## Veto Conditions

- Script com < 7 beats → **VETO** (completar beats faltantes)
- Sem direção 10D → **VETO** (adicionar performance direction)
- Timing > 90s → **VETO** (cortar ou dividir em 2 reels)
- Insight antes da ação → **VETO** (reordenar beats)
- Overrun > 10% do target → **VETO** (ajustar wording)
