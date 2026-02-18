"""Chapter detection — detect topic boundaries in transcription segments.

Uses a sliding-window text similarity approach to find natural break points
where the vocabulary changes significantly, indicating a new topic.
No external dependencies required (pure Python).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .models import Segment, _fmt_time


@dataclass
class Chapter:
    """A detected chapter with title and time range."""

    index: int
    title: str
    start: float
    end: float
    segments: list[Segment] = field(default_factory=list)

    @property
    def start_formatted(self) -> str:
        return _fmt_time(self.start)

    @property
    def end_formatted(self) -> str:
        return _fmt_time(self.end)

    @property
    def duration(self) -> float:
        return self.end - self.start

    @property
    def word_count(self) -> int:
        return sum(len(s.text.split()) for s in self.segments)

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "start_formatted": self.start_formatted,
            "end_formatted": self.end_formatted,
            "duration": round(self.duration, 1),
            "word_count": self.word_count,
        }


# Common stopwords for Portuguese and English (used in vocabulary extraction)
_STOPWORDS = frozenset({
    # Portuguese
    "a", "o", "e", "de", "do", "da", "em", "um", "uma", "que", "com", "para",
    "por", "no", "na", "se", "os", "as", "ao", "dos", "das", "nos", "nas",
    "mais", "mas", "como", "não", "isso", "esse", "essa", "este", "esta",
    "ele", "ela", "eles", "elas", "eu", "nós", "você", "vocês", "muito",
    "tem", "ter", "vai", "foi", "ser", "está", "são", "então", "quando",
    "aqui", "ali", "lá", "já", "também", "ainda", "mesmo", "pode", "todo",
    "toda", "todos", "todas", "tinha", "sobre", "entre", "depois", "antes",
    # English
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "this", "that", "these", "those",
    "it", "its", "he", "she", "they", "we", "you", "i", "my", "your",
    "not", "so", "if", "from", "just", "very", "also", "then", "than",
})


def _tokenize(text: str) -> list[str]:
    """Extract meaningful words from text."""
    words = re.findall(r"[a-záàâãéèêíïóôõúüçñ]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOPWORDS]


def _jaccard_distance(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard distance (1 - similarity) between two word sets."""
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return 1.0 - (intersection / union)


def _generate_title(segments: list[Segment], index: int) -> str:
    """Generate a simple chapter title from the first meaningful words."""
    text = " ".join(s.text.strip() for s in segments[:3] if s.type == "speech")
    words = text.split()
    if len(words) > 8:
        title = " ".join(words[:8]) + "..."
    elif words:
        title = " ".join(words)
    else:
        title = f"Parte {index}"

    # Capitalize first letter
    if title:
        title = title[0].upper() + title[1:]
    return title


def detect_chapters(
    segments: list[Segment],
    *,
    min_chapter_seconds: float = 120.0,
    window_size: int = 15,
    threshold: float = 0.75,
) -> list[Chapter]:
    """Detect chapter boundaries using vocabulary shift analysis.

    Slides a window over the segments and computes Jaccard distance
    between the vocabulary before and after each point. High-distance
    points indicate topic changes.

    Args:
        segments: Cleaned transcription segments.
        min_chapter_seconds: Minimum chapter duration in seconds.
        window_size: Number of segments in each half-window.
        threshold: Jaccard distance threshold to consider a break.

    Returns:
        List of Chapter objects.
    """
    speech_segments = [s for s in segments if s.type == "speech" and s.text.strip()]

    if len(speech_segments) < window_size * 2:
        # Too short — return single chapter
        if speech_segments:
            return [Chapter(
                index=1,
                title=_generate_title(speech_segments, 1),
                start=speech_segments[0].start,
                end=speech_segments[-1].end,
                segments=speech_segments,
            )]
        return []

    # Compute Jaccard distance at each potential boundary
    distances: list[tuple[int, float]] = []
    for i in range(window_size, len(speech_segments) - window_size):
        left_words = set()
        right_words = set()
        for seg in speech_segments[i - window_size:i]:
            left_words.update(_tokenize(seg.text))
        for seg in speech_segments[i:i + window_size]:
            right_words.update(_tokenize(seg.text))

        dist = _jaccard_distance(left_words, right_words)
        distances.append((i, dist))

    # Find peaks above threshold with minimum spacing
    boundaries: list[int] = [0]  # Always start at 0
    last_boundary_time = speech_segments[0].start

    for idx, dist in distances:
        if dist < threshold:
            continue
        current_time = speech_segments[idx].start
        if current_time - last_boundary_time < min_chapter_seconds:
            continue
        boundaries.append(idx)
        last_boundary_time = current_time

    # Build chapters from boundaries
    chapters: list[Chapter] = []
    for i, start_idx in enumerate(boundaries):
        end_idx = boundaries[i + 1] if i + 1 < len(boundaries) else len(speech_segments)
        chapter_segments = speech_segments[start_idx:end_idx]

        if not chapter_segments:
            continue

        chapters.append(Chapter(
            index=i + 1,
            title=_generate_title(chapter_segments, i + 1),
            start=chapter_segments[0].start,
            end=chapter_segments[-1].end,
            segments=chapter_segments,
        ))

    # Merge very short final chapters into the previous one
    if len(chapters) >= 2:
        last = chapters[-1]
        if last.duration < min_chapter_seconds:
            prev = chapters[-2]
            prev.end = last.end
            prev.segments.extend(last.segments)
            chapters.pop()

    return chapters


def save_chapters(chapters: list[Chapter], output_path: Path) -> Path:
    """Save chapters as JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "total_chapters": len(chapters),
        "chapters": [ch.to_dict() for ch in chapters],
    }
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def chapters_to_markdown(chapters: list[Chapter]) -> str:
    """Format chapters as a markdown table of contents."""
    lines: list[str] = ["## Chapters\n"]

    for ch in chapters:
        lines.append(f"- **[{ch.start_formatted}]** {ch.title} ({ch.word_count} words)")

    lines.append("")
    return "\n".join(lines)
