"""CLI interface for video-transcriber using Typer."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .audio import extract_audio
from .chunker import chunk_transcription, save_chunks
from .cleaner import clean_segments, clean_transcription_file, generate_clean_markdown
from .config import (
    AUDIO_EXTENSIONS,
    BATCH_DASHBOARD_PORT,
    BATCH_DEFAULT_MODEL,
    CHAPTER_MIN_SECONDS,
    CHAPTER_THRESHOLD,
    CHAPTER_WINDOW_SIZE,
    CHUNK_MAX_WORDS,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    MEDIA_EXTENSIONS,
    SUMMARY_MAX_SENTENCES,
    TEXT_EXTENSIONS,
    VIDEO_EXTENSIONS,
    WHISPER_MODELS,
)
from .downloader import download_youtube_audio, download_youtube_metadata
from .models import Segment
from .transcriber import load_transcription, save_transcription, transcribe

app = typer.Typer(
    name="video-transcriber",
    help="Download, transcribe, clean, chunk, and ingest video/audio/text content.",
    no_args_is_help=True,
)

console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"video-transcriber {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """Video Transcriber — Download, transcribe, clean, and chunk media content."""


@app.command()
def process(
    source: str = typer.Argument(help="URL or local file path"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory. Defaults to /tmp/vt-<hash>/",
    ),
    model: str = typer.Option(
        DEFAULT_MODEL, "--model", "-m",
        help=f"Whisper model size ({', '.join(WHISPER_MODELS)})",
    ),
    language: str = typer.Option(
        DEFAULT_LANGUAGE, "--language", "-l",
        help="Language code (e.g., 'pt', 'en', 'auto')",
    ),
    max_words: int = typer.Option(
        CHUNK_MAX_WORDS, "--max-words",
        help="Max words per chunk",
    ),
    srt: bool = typer.Option(
        False, "--srt",
        help="Generate SRT subtitle file",
    ),
    vtt: bool = typer.Option(
        False, "--vtt",
        help="Generate VTT subtitle file",
    ),
    chapters: bool = typer.Option(
        False, "--chapters",
        help="Detect and generate chapters",
    ),
    summarize: bool = typer.Option(
        False, "--summarize",
        help="Generate extractive summary",
    ),
    obsidian: bool = typer.Option(
        False, "--obsidian",
        help="Generate Obsidian-native markdown with frontmatter",
    ),
    glossary: bool = typer.Option(
        False, "--glossary",
        help="Extract glossary of key terms and proper names",
    ),
    index: bool = typer.Option(
        False, "--index",
        help="Index transcription in SQLite FTS5 search database",
    ),
) -> None:
    """Full pipeline: download + transcribe + clean + chunk."""
    # Determine output directory
    if output is None:
        hash_str = hashlib.md5(source.encode()).hexdigest()[:8]
        output = Path(tempfile.gettempdir()) / f"vt-{hash_str}"
    output.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold]Output:[/bold] {output}\n")

    is_youtube = "youtube.com" in source or "youtu.be" in source
    is_local = Path(source).exists() if not is_youtube else False

    # Step 1: Get metadata + audio
    metadata = None
    audio_path: Path | None = None

    if is_youtube:
        console.print("[bold blue]Step 1/5:[/bold blue] Fetching metadata...")
        metadata = download_youtube_metadata(source)
        console.print(f"  Title: {metadata.title}")
        console.print(f"  Channel: {metadata.channel}")
        console.print(f"  Duration: {metadata.duration_formatted}")

        # Save metadata
        meta_path = output / "metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata.to_dict(), f, ensure_ascii=False, indent=2)

        console.print("\n[bold blue]Step 2/5:[/bold blue] Downloading audio...")
        audio_path = download_youtube_audio(source, output)

    elif is_local:
        local_path = Path(source).resolve()
        ext = local_path.suffix.lower()

        if ext not in MEDIA_EXTENSIONS:
            console.print(f"[red]Unsupported format: {ext}[/red]")
            raise typer.Exit(1)

        console.print(f"[bold blue]Step 1/5:[/bold blue] Local file: {local_path.name}")

        if ext in VIDEO_EXTENSIONS:
            console.print("\n[bold blue]Step 2/5:[/bold blue] Extracting audio...")
            audio_path = extract_audio(local_path, output / f"{local_path.stem}.wav")
        else:
            audio_path = local_path
            console.print("  Audio file — skipping extraction")
    else:
        console.print(f"[red]Source not recognized: {source}[/red]")
        console.print("Provide a YouTube URL or a local file path.")
        raise typer.Exit(1)

    # Step 3: Transcribe
    console.print(f"\n[bold blue]Step 3/5:[/bold blue] Transcribing ({model})...")
    result = transcribe(audio_path, model_name=model, language=language)

    word_count = len(result.full_text.split())
    console.print(f"  [green]Done:[/green] {len(result.segments)} segments, {word_count:,} words")
    console.print(f"  Language: {result.language}")

    # Save raw transcription
    raw_json = output / "transcription.json"
    save_transcription(result, raw_json)

    # Step 4: Clean
    console.print(f"\n[bold blue]Step 4/5:[/bold blue] Cleaning transcription...")
    cleaned_segs, stats = clean_segments(result.segments)
    console.print(
        f"  [green]Cleaned:[/green] {stats.original_count} \u2192 {stats.final_count} segments"
    )
    console.print(f"  Removed: {stats.removed_total} ({stats.loop_segments_removed} loops)")

    # Save cleaned outputs
    clean_data = {
        "language": result.language,
        "original_segments": stats.original_count,
        "cleaned_segments": stats.final_count,
        "segments": [s.to_dict() for s in cleaned_segs],
    }
    clean_json = output / "transcription_clean.json"
    with open(clean_json, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=2)

    title = metadata.title if metadata else Path(source).stem
    md_content = generate_clean_markdown(cleaned_segs, stats, title)
    clean_md = output / "transcription_clean.md"
    with open(clean_md, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Save stats
    stats_path = output / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats.to_dict(), f, ensure_ascii=False, indent=2)

    # Step 5: Chunk
    console.print(f"\n[bold blue]Step 5/5:[/bold blue] Chunking (max {max_words} words)...")
    chunks = chunk_transcription(cleaned_segs, max_words=max_words)
    save_chunks(chunks, output)

    # Optional: Captions (SRT/VTT)
    if srt or vtt:
        from .captions import save_srt, save_vtt

        caption_title = metadata.title if metadata else Path(source).stem
        if srt:
            srt_path = output / "transcription.srt"
            save_srt(cleaned_segs, srt_path)
            console.print(f"  [green]SRT:[/green] {srt_path.name}")
        if vtt:
            vtt_path = output / "transcription.vtt"
            save_vtt(cleaned_segs, vtt_path, title=caption_title)
            console.print(f"  [green]VTT:[/green] {vtt_path.name}")

    # Optional: Chapters
    detected_chapters = None
    if chapters:
        from .chapters import chapters_to_markdown, detect_chapters, save_chapters

        console.print("\n[bold cyan]Chapters:[/bold cyan] Detecting topic boundaries...")
        detected_chapters = detect_chapters(cleaned_segs)
        if detected_chapters:
            save_chapters(detected_chapters, output / "chapters.json")
            ch_md = chapters_to_markdown(detected_chapters)
            (output / "chapters.md").write_text(ch_md, encoding="utf-8")
            console.print(f"  [green]Found {len(detected_chapters)} chapters[/green]")
            for ch in detected_chapters:
                console.print(f"    [{ch.start_formatted}] {ch.title}")
        else:
            console.print("  No chapters detected (content too short or uniform)")

    # Optional: Summarize
    generated_summary = None
    if summarize:
        from .summarizer import save_summary, summarize_segments, summary_to_markdown

        console.print("\n[bold cyan]Summary:[/bold cyan] Generating extractive summary...")
        sum_title = metadata.title if metadata else Path(source).stem
        generated_summary = summarize_segments(cleaned_segs, title=sum_title)
        if generated_summary.full_summary:
            save_summary(generated_summary, output / "summary.json")
            sum_md = summary_to_markdown(generated_summary)
            (output / "summary.md").write_text(sum_md, encoding="utf-8")
            console.print(f"  [green]{generated_summary.word_count} words, "
                          f"{len(generated_summary.key_points)} key points[/green]")
        else:
            console.print("  No summary generated (not enough content)")

    # Optional: Glossary
    generated_glossary = None
    if glossary:
        from .glossary import extract_glossary, glossary_to_markdown, save_glossary

        console.print("\n[bold cyan]Glossary:[/bold cyan] Extracting key terms...")
        generated_glossary = extract_glossary(cleaned_segs)
        if generated_glossary.entries:
            save_glossary(generated_glossary, output / "glossary.json")
            gl_md = glossary_to_markdown(generated_glossary)
            (output / "glossary.md").write_text(gl_md, encoding="utf-8")
            console.print(
                f"  [green]{generated_glossary.total_terms} terms:[/green] "
                f"{len(generated_glossary.proper_names)} names, "
                f"{len(generated_glossary.technical_terms)} technical, "
                f"{len(generated_glossary.concepts)} concepts"
            )
        else:
            console.print("  No terms extracted (not enough content)")

    # Optional: Obsidian
    if obsidian:
        from .obsidian import save_obsidian

        console.print("\n[bold cyan]Obsidian:[/bold cyan] Generating Obsidian-native markdown...")
        obs_title = metadata.title if metadata else Path(source).stem
        obs_kwargs: dict = {
            "title": obs_title,
            "source": source,
            "language": result.language,
            "model": model,
        }
        if detected_chapters:
            obs_kwargs["chapters"] = [ch.to_dict() for ch in detected_chapters]
        if generated_summary and generated_summary.full_summary:
            obs_kwargs["summary_text"] = generated_summary.full_summary
        if generated_glossary and generated_glossary.entries:
            obs_kwargs["glossary_terms"] = [e.to_dict() for e in generated_glossary.entries[:20]]
        obs_path = output / f"{Path(source).stem if not metadata else obs_title}.md"
        # Sanitize filename
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', obs_path.stem)
        obs_path = output / f"{safe_name}-obsidian.md"
        save_obsidian(cleaned_segs, obs_path, **obs_kwargs)
        console.print(f"  [green]Saved:[/green] {obs_path.name}")

    # Optional: Search index
    indexed_count = 0
    if index:
        from .search import SearchIndex

        console.print("\n[bold cyan]Index:[/bold cyan] Adding to search database...")
        idx_title = metadata.title if metadata else Path(source).stem
        db_path = output / "vt-search.db"
        with SearchIndex(db_path) as idx:
            indexed_count = idx.index_transcription(
                cleaned_segs,
                title=idx_title,
                source_path=source,
                language=result.language,
                model=model,
            )
            idx_stats = idx.stats()
        console.print(
            f"  [green]Indexed {indexed_count} segments[/green] "
            f"({idx_stats['documents']} docs in DB)"
        )

    # Results summary
    console.print("\n" + "=" * 50)
    console.print("[bold green]COMPLETE[/bold green]")
    console.print("=" * 50)

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Output", str(output))
    if metadata:
        table.add_row("Title", metadata.title)
    table.add_row("Segments", f"{stats.original_count} \u2192 {stats.final_count}")
    table.add_row("Words", f"{word_count:,}")
    table.add_row("Chunks", str(len(chunks)))
    table.add_row("Language", result.language)
    if detected_chapters:
        table.add_row("Chapters", str(len(detected_chapters)))
    if generated_summary:
        table.add_row("Summary", f"{generated_summary.word_count} words")
    if generated_glossary:
        table.add_row("Glossary", f"{generated_glossary.total_terms} terms")
    if indexed_count:
        table.add_row("Indexed", f"{indexed_count} segments")
    console.print(table)
    console.print()


@app.command()
def download(
    url: str = typer.Argument(help="YouTube URL to download"),
    output: Path = typer.Option(
        Path(tempfile.gettempdir()), "--output", "-o",
        help="Output directory",
    ),
) -> None:
    """Download audio from YouTube."""
    output.mkdir(parents=True, exist_ok=True)
    audio_path = download_youtube_audio(url, output)
    console.print(f"\n[green]Downloaded:[/green] {audio_path}")


@app.command(name="transcribe")
def transcribe_cmd(
    file: Path = typer.Argument(help="Path to audio or video file"),
    model: str = typer.Option(
        DEFAULT_MODEL, "--model", "-m",
        help=f"Whisper model ({', '.join(WHISPER_MODELS)})",
    ),
    language: str = typer.Option(
        DEFAULT_LANGUAGE, "--language", "-l",
        help="Language code",
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output JSON path",
    ),
) -> None:
    """Transcribe a local audio/video file."""
    file = file.resolve()
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    ext = file.suffix.lower()
    audio_path = file

    if ext in VIDEO_EXTENSIONS:
        console.print("Extracting audio...")
        audio_path = extract_audio(file)

    console.print(f"Transcribing with model={model}, language={language}...")
    result = transcribe(audio_path, model_name=model, language=language)

    if output is None:
        output = file.parent / f"{file.stem}_transcription.json"

    save_transcription(result, output)
    console.print(f"\n[green]Saved:[/green] {output}")
    console.print(f"Segments: {len(result.segments)}, Language: {result.language}")


@app.command()
def batch(
    source_dir: Path = typer.Argument(help="Directory containing videos to transcribe"),
    model: str = typer.Option(
        BATCH_DEFAULT_MODEL, "--model", "-m",
        help=f"Whisper model ({', '.join(WHISPER_MODELS)})",
    ),
    language: str = typer.Option(
        DEFAULT_LANGUAGE, "--language", "-l",
        help="Language code (e.g., 'pt', 'en')",
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output-dir", "-o",
        help="Centralized output directory (default: alongside each video)",
    ),
    dashboard: bool = typer.Option(
        False, "--dashboard",
        help="Start an HTML dashboard for monitoring progress",
    ),
    port: int = typer.Option(
        BATCH_DASHBOARD_PORT, "--port",
        help="Dashboard server port",
    ),
    do_chunk: bool = typer.Option(
        False, "--chunk",
        help="Generate chunks per video (off by default)",
    ),
    max_words: int = typer.Option(
        CHUNK_MAX_WORDS, "--max-words",
        help="Max words per chunk (requires --chunk)",
    ),
    srt: bool = typer.Option(
        False, "--srt",
        help="Generate SRT subtitle per video",
    ),
    vtt: bool = typer.Option(
        False, "--vtt",
        help="Generate VTT subtitle per video",
    ),
    chapters: bool = typer.Option(
        False, "--chapters",
        help="Detect chapters per video",
    ),
    do_summarize: bool = typer.Option(
        False, "--summarize",
        help="Generate extractive summary per video",
    ),
    do_obsidian: bool = typer.Option(
        False, "--obsidian",
        help="Generate Obsidian-native markdown per video",
    ),
    do_glossary: bool = typer.Option(
        False, "--glossary",
        help="Extract glossary per video",
    ),
    do_index: bool = typer.Option(
        False, "--index",
        help="Index all transcriptions in SQLite FTS5 search database",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="List videos without processing",
    ),
) -> None:
    """Batch transcribe all videos in a directory.

    Scans recursively for video files, skips already-transcribed ones,
    and writes '-transcricao.md' files with cleaned transcriptions.
    """
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

    from .batch import BatchEngine

    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        console.print(f"[red]Not a directory: {source_dir}[/red]")
        raise typer.Exit(1)

    engine = BatchEngine(
        source_dir,
        model=model,
        language=language,
        output_dir=output_dir,
        chunk=do_chunk,
        max_words=max_words,
        generate_srt=srt,
        generate_vtt=vtt,
        generate_chapters=chapters,
        generate_summary=do_summarize,
        generate_obsidian=do_obsidian,
        generate_glossary=do_glossary,
        generate_index=do_index,
    )

    # Scan
    console.print(f"\n[bold]Scanning:[/bold] {source_dir}")
    state = engine.scan()

    console.print(f"  Total videos: {state.total_videos}")
    console.print(f"  Already done: {state.skipped}")
    console.print(f"  To process:   {state.remaining}")

    if state.remaining == 0:
        console.print("\n[green]All videos already transcribed![/green]")
        raise typer.Exit(0)

    # Dry run — list and exit
    if dry_run:
        console.print(f"\n[bold]Pending videos ({len(engine.pending)}):[/bold]")
        for i, video in enumerate(engine.pending, 1):
            rel = video.relative_to(source_dir)
            console.print(f"  {i:3d}. {rel}")
        raise typer.Exit(0)

    # Start dashboard if requested
    dashboard_server = None
    if dashboard:
        from .dashboard import DashboardServer

        serve_dir = output_dir or source_dir
        dashboard_server = DashboardServer(serve_dir, port=port)
        actual_port = dashboard_server.start()
        console.print(
            f"\n[bold green]Dashboard:[/bold green] http://localhost:{actual_port}/dashboard.html"
        )

    # Run with Rich progress
    console.print(f"\n[bold]Starting batch transcription[/bold]")
    console.print(f"  Model: {model} | Language: {language}")
    console.print(f"  Ctrl+C to pause (resume by re-running)\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Transcribing", total=len(engine.pending))

        completed_count = 0

        def on_progress(batch_state):  # noqa: ANN001
            nonlocal completed_count
            new_completed = batch_state.completed - state.skipped + batch_state.errors
            advance = new_completed - completed_count
            if advance > 0:
                completed_count = new_completed
                progress.advance(task, advance)
            progress.update(task, description=f"[cyan]{batch_state.current_video or 'Done'}[/cyan]")

        final_state = engine.run(progress_callback=on_progress)

    # Summary
    console.print("\n" + "=" * 60)
    if not engine._is_running and final_state.remaining > 0:
        console.print("[yellow]PAUSED[/yellow] — re-run to resume")
    else:
        console.print("[bold green]COMPLETE[/bold green]")
    console.print("=" * 60)

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Directory", str(source_dir))
    table.add_row("Completed", str(final_state.completed))
    table.add_row("Errors", str(final_state.errors))
    table.add_row("Remaining", str(final_state.remaining))
    table.add_row("Model", model)
    console.print(table)
    console.print()

    if dashboard_server:
        dashboard_server.stop()


@app.command()
def clean(
    file: Path = typer.Argument(help="Path to transcription JSON file"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory",
    ),
) -> None:
    """Clean a transcription JSON (remove loops, merge segments)."""
    file = file.resolve()
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    result_path = clean_transcription_file(file, output)
    console.print(f"\n[green]Cleaned:[/green] {result_path}")


# ---------------------------------------------------------------------------
# Helpers for text ingestion
# ---------------------------------------------------------------------------

_VTT_TIMESTAMP = re.compile(
    r"^\d{2}:\d{2}[:.]\d{3}\s*-->\s*\d{2}:\d{2}[:.]\d{3}",
)
_SRT_TIMESTAMP = re.compile(
    r"^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}",
)
_VTT_HEADER = re.compile(r"^(WEBVTT|Kind:|Language:)")
_SRT_INDEX = re.compile(r"^\d+$")
_VTT_TAG = re.compile(r"<[^>]+>")


def _parse_subtitles(file_path: Path) -> str:
    """Extract plain text from a VTT or SRT file, stripping timestamps and cues."""
    raw = file_path.read_text(encoding="utf-8")
    lines: list[str] = []
    prev_line = ""

    for line in raw.splitlines():
        stripped = line.strip()

        # Skip empty, headers, timestamps, SRT numeric indices
        if not stripped:
            continue
        if _VTT_HEADER.match(stripped):
            continue
        if _VTT_TIMESTAMP.match(stripped) or _SRT_TIMESTAMP.match(stripped):
            continue
        if _SRT_INDEX.match(stripped):
            continue

        # Remove inline VTT tags like <c>, </c>, <v Name>
        cleaned = _VTT_TAG.sub("", stripped)
        if not cleaned:
            continue

        # Deduplicate consecutive identical lines (common in VTT)
        if cleaned == prev_line:
            continue

        lines.append(cleaned)
        prev_line = cleaned

    return "\n\n".join(lines)


def _text_to_segments(text: str) -> list[Segment]:
    """Convert plain text into Segment objects using paragraph breaks.

    Assigns synthetic sequential timestamps (1s per 3 words) so the
    chunker can still operate on segment boundaries.
    """
    # Split on double newlines (paragraphs) or treat as single block
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    if not paragraphs:
        return []

    segments: list[Segment] = []
    cursor = 0.0
    words_per_second = 3.0  # rough estimate for timestamp generation

    for para in paragraphs:
        word_count = len(para.split())
        duration = max(word_count / words_per_second, 1.0)
        segments.append(Segment(
            start=cursor,
            end=cursor + duration,
            text=para,
            type="speech",
        ))
        cursor += duration

    return segments


# ---------------------------------------------------------------------------
# Commands: chunk & ingest
# ---------------------------------------------------------------------------

@app.command()
def chunk(
    file: Path = typer.Argument(help="Path to transcription JSON file"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory (default: same as input file)",
    ),
    max_words: int = typer.Option(
        CHUNK_MAX_WORDS, "--max-words",
        help="Max words per chunk",
    ),
) -> None:
    """Chunk an existing transcription JSON into text files."""
    file = file.resolve()
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    if file.suffix.lower() != ".json":
        console.print("[red]Expected a .json transcription file[/red]")
        raise typer.Exit(1)

    out_dir = output or file.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"Loading: {file.name}")
    result = load_transcription(file)
    console.print(f"  Segments: {len(result.segments)}, Language: {result.language}")

    console.print(f"Chunking (max {max_words} words)...")
    chunks = chunk_transcription(result.segments, max_words=max_words)
    chunks_dir = save_chunks(chunks, out_dir)

    console.print(f"\n[green]Done:[/green] {len(chunks)} chunks saved to {chunks_dir}")


@app.command()
def ingest(
    file: Path = typer.Argument(help="Path to VTT, SRT, TXT, MD, or JSON file"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory (default: same as input file)",
    ),
    max_words: int = typer.Option(
        CHUNK_MAX_WORDS, "--max-words",
        help="Max words per chunk",
    ),
) -> None:
    """Parse a text file (VTT/SRT/TXT/MD/JSON) and produce chunks.

    This is the entry point for 'ready text' — content that is already
    transcribed or written and just needs to be chunked for LLM processing.
    """
    file = file.resolve()
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    ext = file.suffix.lower()
    if ext not in TEXT_EXTENSIONS:
        console.print(f"[red]Unsupported format: {ext}[/red]")
        console.print(f"Supported: {', '.join(sorted(TEXT_EXTENSIONS))}")
        raise typer.Exit(1)

    out_dir = output or file.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold]Ingesting:[/bold] {file.name} ({ext})")

    # --- Parse based on format ---
    if ext == ".json":
        # Assume transcription JSON — load, clean, chunk
        result = load_transcription(file)
        console.print(f"  Segments: {len(result.segments)}, Language: {result.language}")

        console.print("  Cleaning...")
        cleaned_segs, stats = clean_segments(result.segments)
        console.print(
            f"  Cleaned: {stats.original_count} → {stats.final_count} segments"
        )
        segments = cleaned_segs

    elif ext in {".vtt", ".srt"}:
        # Parse subtitles → plain text → segments
        console.print("  Parsing subtitles...")
        text = _parse_subtitles(file)
        word_count = len(text.split())
        console.print(f"  Extracted: {word_count:,} words")
        segments = _text_to_segments(text)

    else:
        # Plain text (.txt, .md) — read and convert
        text = file.read_text(encoding="utf-8")
        word_count = len(text.split())
        console.print(f"  Words: {word_count:,}")
        segments = _text_to_segments(text)

    # --- Chunk ---
    console.print(f"  Chunking (max {max_words} words)...")
    chunks = chunk_transcription(segments, max_words=max_words)
    chunks_dir = save_chunks(chunks, out_dir)

    # --- Summary ---
    total_words = sum(c.word_count for c in chunks)
    console.print(f"\n[green]Done:[/green] {len(chunks)} chunks, {total_words:,} words")
    console.print(f"  Output: {chunks_dir}")
    console.print(f"  Manifest: {chunks_dir / 'manifest.json'}")


@app.command()
def search(
    query: str = typer.Argument(help="Search query (supports FTS5 syntax: AND, OR, NOT, \"phrases\")"),
    db: Path = typer.Option(
        Path.home() / ".vt" / "vt-search.db", "--db",
        help="Path to search database",
    ),
    limit: int = typer.Option(
        20, "--limit", "-n",
        help="Maximum results",
    ),
) -> None:
    """Search across all indexed transcriptions."""
    from .search import SearchIndex

    db = db.resolve()
    if not db.exists():
        console.print(f"[red]No search database found at: {db}[/red]")
        console.print("Use --index flag with process/batch to build the index.")
        raise typer.Exit(1)

    with SearchIndex(db) as idx:
        results = idx.search(query, limit=limit)
        idx_stats = idx.stats()

    if not results:
        console.print(f"No results for: [bold]{query}[/bold]")
        console.print(f"  Database: {idx_stats['documents']} documents, {idx_stats['total_words']:,} words")
        raise typer.Exit(0)

    console.print(f"\n[bold]Results for:[/bold] {query} ({len(results)} matches)\n")

    for i, r in enumerate(results, 1):
        snippet = r.snippet.replace(">>>", "[bold yellow]").replace("<<<", "[/bold yellow]")
        console.print(f"  [dim]{i:2d}.[/dim] [bold]{r.title}[/bold]")
        console.print(f"      [{r.timestamp_formatted}] {snippet}")
        console.print()

    console.print(f"[dim]Database: {idx_stats['documents']} docs, {idx_stats['total_words']:,} words[/dim]")


@app.command(name="search-stats")
def search_stats(
    db: Path = typer.Option(
        Path.home() / ".vt" / "vt-search.db", "--db",
        help="Path to search database",
    ),
) -> None:
    """Show search index statistics."""
    from .search import SearchIndex

    db = db.resolve()
    if not db.exists():
        console.print(f"[red]No search database found at: {db}[/red]")
        raise typer.Exit(1)

    with SearchIndex(db) as idx:
        s = idx.stats()
        docs = idx.list_documents()

    console.print(f"\n[bold]Search Index Stats[/bold]\n")
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Database", str(db))
    table.add_row("Size", f"{s['db_size_mb']} MB")
    table.add_row("Documents", str(s['documents']))
    table.add_row("Segments", str(s['segments']))
    table.add_row("Total Words", f"{s['total_words']:,}")
    console.print(table)

    if docs:
        console.print(f"\n[bold]Indexed Documents ({len(docs)}):[/bold]\n")
        for d in docs:
            console.print(f"  - {d['title']} ({d['word_count']:,} words, {d['segment_count']} segments)")

    console.print()


if __name__ == "__main__":
    app()
