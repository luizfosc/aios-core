# Task: Compose Reel

**Agente:** @video-composer
**Fase:** 5 (Edição / Composição)
**Gate:** QG-AR-5

## Objetivo

Editar e compor o reel final com 8 camadas visuais via Remotion.

## Input

- `video_raw`: Vídeo com lip sync da fase 4
- `performance_10D`: Direção de performance da fase 2
- `beat_timestamps`: Timestamps dos beats
- `captions_json`: Legendas word-by-word (Whisper)

## 8 Camadas Visuais

| Camada | Componente | Detalhes |
|--------|-----------|----------|
| 8 | Film Grain | noise3D, opacity 0.05 |
| 7 | Progress Bar | 3px topo, cor do accent |
| 6 | Lower Third | Nome + @handle, slide-in com spring |
| 5 | Keyword Overlays | Texto animado em timestamps |
| 4 | Auto Captions | TikTok-style word-by-word |
| 3 | Vignette | Radial gradient cinematográfico |
| 2 | Cut Flash | Flash branco nos pontos de corte |
| 1 | OffthreadVideo | Avatar com punch-in/out (auto-cuts) |

## Processo

1. Gerar `reel-config.json` a partir dos inputs
2. Configurar auto-cuts (intervalS ~4s, alternando normal/close-up)
3. Adicionar captions TikTok-style (max 3 words/line, word-by-word highlight)
4. Aplicar grain + vignette + progress bar
5. Normalizar áudio (-14 LUFS via FFmpeg)
6. Render via Remotion
7. Validar output specs

## Output

```yaml
reel_file: "reel-edited.mp4"
composition_report:
  resolution: "1080x1920"
  fps: 25
  duration_s: X
  codec: "H.264"
  audio_lufs: -14
  layers_active: [1,2,3,4,5,6,7,8]
  auto_cuts_count: X
  captions_synced: true
```

## Quality Gate QG-AR-5

| Critério | Obrigatório |
|----------|-------------|
| 1080x1920 9:16 | SIM |
| 25 fps | SIM |
| H.264 codec | SIM |
| Áudio -14 LUFS | SIM |
| Captions sincronizadas (< 0.2s desvio) | SIM |
| Grain aplicado | SIM |
| Safe zones respeitadas | SIM |
| Duração 15-90s | SIM |

## Veto Conditions

- Resolução ≠ 1080x1920 → **REJEITAR** e re-render
- Captions dessincronizadas > 0.2s → **REFAZER** alinhamento
- Áudio não normalizado → **REPROCESSAR** com FFmpeg
- Conteúdo em safe zones (200px bottom, 150px top) → **REPOSICIONAR**
- Grain ausente → **ADICIONAR** (obrigatório por heurística VC-02)
- Arquivo > 100MB → **OTIMIZAR** bitrate
