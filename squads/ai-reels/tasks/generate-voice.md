# Task: Generate Voice

**Agente:** @voice-engineer
**Fase:** 3 (Voz)
**Gate:** QG-AR-3

## Objetivo

Gerar áudio com clone de voz PT-BR via ElevenLabs (beat-by-beat, não bloco único).

## Input

- `script`: Roteiro com 7 beats marcados
- `beat_timestamps`: Timing por beat
- `voice_id`: Clone de voz (default: `YenbYX8x7myujzTnQhXP`)

## Processo

1. Separar script em 7 blocos (1 por beat)
2. Configurar parâmetros por beat (stability, similarity, style)
3. Gerar áudio beat-by-beat via ElevenLabs API
4. Merge beats em arquivo único com timestamps
5. Verificar fidelidade e artefatos

## Parâmetros por Beat

| Beat | Stability | Similarity | Style | Velocidade |
|------|-----------|------------|-------|------------|
| HOOK | 0.40 | 0.85 | 0.60 | 1.15x |
| STASIS | 0.60 | 0.80 | 0.30 | 1.10x |
| TRIGGER | 0.35 | 0.85 | 0.70 | 1.15x |
| RISING | 0.45 | 0.80 | 0.50 | 1.15x |
| INSIGHT | 0.50 | 0.85 | 0.40 | 1.10x |
| RESOLUTION | 0.55 | 0.80 | 0.35 | 1.10x |
| CTA | 0.45 | 0.85 | 0.55 | 1.15x |

## Output

```yaml
audio_file: "voice-merged.wav"
beat_timestamps:
  - beat: HOOK
    start_s: 0.0
    end_s: 3.2
  # ... (7 beats)
total_duration_s: X
chars_consumed: X
credits_remaining: X
fidelity_score: X%
```

## Quality Gate QG-AR-3

| Critério | Obrigatório |
|----------|-------------|
| Fidelidade >= 80% | SIM |
| Zero artefatos audíveis | SIM |
| Pronúncia PT-BR correta | SIM |
| Beat-by-beat (não bloco único) | SIM |
| Timestamps por beat | SIM |

## Veto Conditions

- Script recebido como bloco único (sem beats marcados) → **DEVOLVER** para fase 2
- Artefatos audíveis em qualquer beat → **REGERAR** beat específico
- Fidelidade < 80% → **AJUSTAR** parâmetros e regerar
- Credits insuficientes → **FALLBACK** para XTTS-v2 local
- Budget < 20% restante do mês → **ALERTAR** Chief antes de gerar
