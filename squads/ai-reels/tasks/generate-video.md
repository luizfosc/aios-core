# Task: Generate Video

**Agente:** @avatar-director
**Fase:** 4 (Avatar / Lip Sync)
**Gate:** QG-AR-4

## Objetivo

Gerar vídeo com lip sync (talking head) a partir do áudio clonado.

## Input

- `audio_file`: Áudio merged (.wav) da fase 3
- `beat_timestamps`: Timestamps por beat
- `template` (opcional): Template de vídeo específico

## Processo

1. Selecionar template de vídeo (rotação entre 3+ templates/semana)
2. Upload áudio + template para HeyGen
3. Gerar vídeo com lip sync
4. Validar sincronização (especialmente primeiros 10s)
5. Verificar preservação de identidade facial

## Templates

| Requisito | Valor |
|-----------|-------|
| Resolução | 1080x1920 (9:16) |
| Duração mínima | Mesmo do áudio + 2s margem |
| Head movement | Máximo 30° |
| Iluminação | Consistente, sem sombras duras |
| Fundo | Neutro ou contextual |
| Rotação | Mínimo 3 templates diferentes/semana |

## Output

```yaml
video_file: "avatar-raw.mp4"
sync_quality_score: X/10
template_used: "template-{n}"
identity_preserved: true/false
processing_time_s: X
heygen_credits_used: "X min"
heygen_credits_remaining: "X min"
```

## Quality Gate QG-AR-4

| Critério | Obrigatório |
|----------|-------------|
| Lip sync sem dessincronização visível | SIM |
| Identidade facial preservada | SIM |
| Resolução 1080x1920 | SIM |
| Head movement < 30° | SIM |
| Sync especialmente OK nos primeiros 10s | SIM |

## Veto Conditions

- Dessincronização visível nos primeiros 10s → **REPROCESSAR** com ajustes
- Identidade facial não preservada → **TROCAR** template
- Template com head movement > 30° → **REJEITAR** template (não usar)
- HeyGen credits < 3 min restantes → **ALERTAR** Chief, limitar batch
- Resolução ≠ 1080x1920 → **REPROCESSAR**
