# video-transcriber

CLI tool that downloads, transcribes, cleans, chunks, and **batch-processes** video/audio content. Includes Whisper hallucination loop cleaning, SRT/VTT captions, chapter detection, extractive summarization, Obsidian integration, glossary extraction, full-text search index, and optional HTML dashboard.

**Version:** 1.3.0

## Install

```bash
pip install -e tools/video-transcriber/
```

For transcription support (Apple Silicon):
```bash
pip3 install mlx-whisper
```

Fallback (CPU):
```bash
pip install openai-whisper
```

System dependencies:
```bash
brew install ffmpeg yt-dlp
pip3 install gdown  # for Google Drive
```

## Usage

### Full pipeline

```bash
video-transcriber process "https://youtube.com/watch?v=xxx" --output /tmp/vt-result/
```

Output:
```
/tmp/vt-result/
├── metadata.json              # title, url, duration, channel
├── transcription.json         # Whisper raw output
├── transcription_clean.json   # Cleaned (no loops, merged)
├── transcription_clean.md     # Markdown with timestamps
├── stats.json                 # Cleaning statistics
└── chunks/
    ├── chunk-001.txt          # ~2000 words each
    ├── chunk-002.txt
    └── manifest.json          # Chunk metadata
```

With all features enabled:
```bash
vt process "https://youtube.com/watch?v=xxx" \
    --srt --vtt --chapters --summarize \
    --obsidian --glossary --index
```

Additional output:
```
/tmp/vt-result/
├── transcription.srt          # SRT subtitles
├── transcription.vtt          # WebVTT subtitles
├── chapters.json              # Detected chapter boundaries
├── chapters.md                # Chapters as markdown TOC
├── summary.json               # Extractive summary
├── summary.md                 # Summary as markdown
├── glossary.json              # Key terms, names, concepts
├── glossary.md                # Glossary as markdown
├── *-obsidian.md              # Obsidian-native with frontmatter
└── vt-search.db               # SQLite FTS5 search index
```

### Download only

```bash
video-transcriber download "https://youtube.com/watch?v=xxx" --output /tmp/
```

### Transcribe local file

```bash
video-transcriber transcribe /path/to/audio.wav --model medium --language pt
```

### Clean existing transcription

```bash
video-transcriber clean /path/to/transcription.json
```

### Batch transcribe a directory

```bash
# Scan and list pending videos
vt batch ~/Dropbox/Cursos/MeuCurso --dry-run

# Transcribe all videos with dashboard
vt batch ~/Dropbox/Cursos/MeuCurso --dashboard

# Custom model and language
vt batch ~/Dropbox/Cursos/MeuCurso --model turbo --language pt --dashboard

# With captions, chapters, and Obsidian output
vt batch ~/Dropbox/Cursos/MeuCurso --srt --chapters --summarize --obsidian --glossary

# With search indexing (builds FTS5 database)
vt batch ~/Dropbox/Cursos/MeuCurso --index
```

Output per video: `{video-stem}-transcricao.md` alongside the original file.

Features:
- Recursive directory scan
- Automatic resume (skips videos with existing `-transcricao.md`)
- Whisper hallucination loop cleaning via `clean_segments()`
- SRT/VTT subtitle generation per video
- Automatic chapter detection via vocabulary shift analysis
- Extractive summarization (no LLM required)
- Obsidian-native markdown with YAML frontmatter, wikilinks, and tags
- Glossary/NER extraction (proper names, technical terms, key concepts)
- SQLite FTS5 full-text search index across all transcriptions
- Atomic status JSON writes (`batch-status.json`)
- Graceful Ctrl+C (re-run to resume)
- Optional HTML dashboard (`--dashboard`)

### Search indexed transcriptions

```bash
# Search across all indexed videos
vt search "machine learning" --db ~/Cursos/vt-search.db

# Search with FTS5 syntax
vt search "python AND framework" --db ./vt-search.db

# View index statistics
vt search-stats --db ./vt-search.db
```

## Options

### Single-file commands

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `medium` | Whisper model: tiny, base, small, medium, large, turbo |
| `--language` | `pt` | Language code (pt, en, auto) |
| `--output` | `/tmp/vt-<hash>/` | Output directory |
| `--max-words` | `2000` | Max words per chunk |
| `--srt` | off | Generate SRT subtitle file |
| `--vtt` | off | Generate VTT subtitle file |
| `--chapters` | off | Detect and generate chapters |
| `--summarize` | off | Generate extractive summary |
| `--obsidian` | off | Generate Obsidian-native markdown |
| `--glossary` | off | Extract glossary of key terms |
| `--index` | off | Index in SQLite FTS5 search database |

### Batch command

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `turbo` | Whisper model |
| `--language` | `pt` | Language code |
| `--output-dir` | alongside video | Centralized output directory |
| `--dashboard` | off | Start HTML dashboard |
| `--port` | `8765` | Dashboard server port |
| `--chunk` | off | Generate chunks per video |
| `--max-words` | `2000` | Max words per chunk |
| `--srt` | off | Generate SRT subtitle per video |
| `--vtt` | off | Generate VTT subtitle per video |
| `--chapters` | off | Detect chapters per video |
| `--summarize` | off | Generate extractive summary per video |
| `--obsidian` | off | Generate Obsidian-native markdown per video |
| `--glossary` | off | Extract glossary per video |
| `--index` | off | Index all videos in FTS5 search database |
| `--dry-run` | off | List videos without processing |

### Search command

| Flag | Default | Description |
|------|---------|-------------|
| `--db` | `~/.vt/vt-search.db` | Path to search database |
| `--limit` | `20` | Maximum results |

## Deprecated Scripts

The following standalone scripts in `tools/` are **deprecated**. Use `vt batch` instead.

| Script | Replacement |
|--------|-------------|
| `batch-transcribe.py` | `vt batch <dir> --model turbo --language pt` |
| `transcription-status-generator.py` | Status JSON generated automatically by `vt batch` |
| `transcription-dashboard.html` | `vt batch --dashboard` |
