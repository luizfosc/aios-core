"""Obsidian integration — generate Obsidian-native markdown with frontmatter.

Produces markdown files with YAML frontmatter, wikilinks for
cross-referencing, and auto-generated tags from content analysis.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .models import Segment, _fmt_time


def _extract_tags(segments: list[Segment], max_tags: int = 10) -> list[str]:
    """Extract topic tags from segment text using word frequency analysis."""
    # Stopwords for tag extraction
    stopwords = frozenset({
        "a", "o", "e", "de", "do", "da", "em", "um", "uma", "que", "com", "para",
        "por", "no", "na", "se", "os", "as", "ao", "dos", "das", "nos", "nas",
        "mais", "mas", "como", "não", "isso", "esse", "essa", "este", "esta",
        "ele", "ela", "eles", "elas", "eu", "nós", "você", "vocês", "muito",
        "tem", "ter", "vai", "foi", "ser", "está", "são", "então", "quando",
        "aqui", "ali", "lá", "já", "também", "ainda", "mesmo", "pode", "todo",
        "toda", "todos", "todas", "tinha", "sobre", "entre", "depois", "antes",
        "porque", "coisa", "gente", "assim", "tipo", "acho", "fazer", "falar",
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "this", "that", "these", "those",
        "it", "its", "he", "she", "they", "we", "you", "not", "so", "if",
        "from", "just", "very", "also", "then", "than",
    })

    word_freq: dict[str, int] = {}
    for seg in segments:
        if seg.type != "speech":
            continue
        words = re.findall(r"[a-záàâãéèêíïóôõúüçñ]+", seg.text.lower())
        for w in words:
            if len(w) > 3 and w not in stopwords:
                word_freq[w] = word_freq.get(w, 0) + 1

    # Sort by frequency, take top N
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_tags]]


def _build_frontmatter(
    title: str,
    *,
    source: str = "",
    language: str = "",
    model: str = "",
    duration: float = 0.0,
    segments_count: int = 0,
    word_count: int = 0,
    tags: list[str] | None = None,
    chapters: list[dict] | None = None,
) -> str:
    """Build YAML frontmatter block."""
    lines: list[str] = ["---"]
    lines.append(f"title: \"{title}\"")
    lines.append(f"type: transcription")
    lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    if source:
        lines.append(f"source: \"{source}\"")
    if language:
        lines.append(f"language: {language}")
    if model:
        lines.append(f"model: {model}")
    if duration > 0:
        lines.append(f"duration: {_fmt_time(duration)}")
    if segments_count > 0:
        lines.append(f"segments: {segments_count}")
    if word_count > 0:
        lines.append(f"words: {word_count}")
    if tags:
        lines.append("tags:")
        for tag in tags:
            lines.append(f"  - {tag}")
    if chapters:
        lines.append("chapters:")
        for ch in chapters:
            lines.append(f"  - \"[{ch.get('start_formatted', '')}] {ch.get('title', '')}\"")
    lines.append("---")
    return "\n".join(lines)


def segments_to_obsidian(
    segments: list[Segment],
    *,
    title: str = "Untitled",
    source: str = "",
    language: str = "",
    model: str = "",
    chapters: list[dict] | None = None,
    summary_text: str = "",
    glossary_terms: list[dict] | None = None,
) -> str:
    """Convert segments to Obsidian-native markdown.

    Args:
        segments: Cleaned transcription segments.
        title: Document title.
        source: Source URL or file path.
        language: Language code.
        model: Whisper model used.
        chapters: Optional chapter data (list of dicts with start_formatted, title).
        summary_text: Optional summary to include.
        glossary_terms: Optional glossary entries (list of dicts with term, count).

    Returns:
        Obsidian-formatted markdown string.
    """
    speech_segs = [s for s in segments if s.type == "speech" and s.text.strip()]

    word_count = sum(len(s.text.split()) for s in speech_segs)
    duration = speech_segs[-1].end if speech_segs else 0.0
    tags = _extract_tags(segments)

    # Build frontmatter
    fm = _build_frontmatter(
        title,
        source=source,
        language=language,
        model=model,
        duration=duration,
        segments_count=len(speech_segs),
        word_count=word_count,
        tags=tags,
        chapters=chapters,
    )

    lines: list[str] = [fm, ""]

    # Title
    lines.append(f"# {title}")
    lines.append("")

    # Summary callout
    if summary_text:
        lines.append("> [!summary] Summary")
        for summary_line in summary_text.split("\n"):
            lines.append(f"> {summary_line}")
        lines.append("")

    # Chapters as linked TOC
    if chapters:
        lines.append("## Chapters")
        lines.append("")
        for ch in chapters:
            ts = ch.get("start_formatted", "")
            ch_title = ch.get("title", "")
            lines.append(f"- `[{ts}]` {ch_title}")
        lines.append("")

    # Glossary as wikilinks
    if glossary_terms:
        lines.append("## Key Terms")
        lines.append("")
        for entry in glossary_terms[:20]:
            term = entry.get("term", "")
            count = entry.get("count", 0)
            # Wikilink format for Obsidian cross-referencing
            lines.append(f"- [[{term}]] ({count}x)")
        lines.append("")

    # Transcription body
    lines.append("## Transcription")
    lines.append("")

    current_hour = -1
    for seg in speech_segs:
        hour = int(seg.start // 3600)
        if hour != current_hour:
            current_hour = hour
            if hour == 0:
                lines.append("### Start")
                lines.append("")
            else:
                lines.append(f"### Hour {hour}")
                lines.append("")

        ts = _fmt_time(seg.start)
        lines.append(f"`[{ts}]` {seg.text.strip()}")
        lines.append("")

    # Footer with tags
    if tags:
        lines.append("---")
        lines.append("")
        lines.append("Tags: " + " ".join(f"#{tag}" for tag in tags))
        lines.append("")

    return "\n".join(lines)


def save_obsidian(
    segments: list[Segment],
    output_path: Path,
    **kwargs: str | list,
) -> Path:
    """Write segments as Obsidian-native markdown file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = segments_to_obsidian(segments, **kwargs)
    output_path.write_text(content, encoding="utf-8")
    return output_path
