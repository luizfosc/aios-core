"""Extractive summarization — generate summaries from transcription segments.

Uses a TF-IDF-like scoring approach to select the most representative
sentences from the transcription. No external LLM required.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

from .models import Segment


# Reuse stopwords from chapters (avoid duplication)
_STOPWORDS = frozenset({
    # Portuguese
    "a", "o", "e", "de", "do", "da", "em", "um", "uma", "que", "com", "para",
    "por", "no", "na", "se", "os", "as", "ao", "dos", "das", "nos", "nas",
    "mais", "mas", "como", "não", "isso", "esse", "essa", "este", "esta",
    "ele", "ela", "eles", "elas", "eu", "nós", "você", "vocês", "muito",
    "tem", "ter", "vai", "foi", "ser", "está", "são", "então", "quando",
    "aqui", "ali", "lá", "já", "também", "ainda", "mesmo", "pode", "todo",
    "toda", "todos", "todas", "tinha", "sobre", "entre", "depois", "antes",
    "porque", "coisa", "gente", "assim", "tipo", "acho", "fazer", "falar",
    # English
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "this", "that", "these", "those",
    "it", "its", "he", "she", "they", "we", "you", "i", "my", "your",
    "not", "so", "if", "from", "just", "very", "also", "then", "than",
})


@dataclass
class Summary:
    """A generated summary."""

    title: str
    key_points: list[str]
    full_summary: str
    word_count: int
    source_segments: int

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "key_points": self.key_points,
            "full_summary": self.full_summary,
            "word_count": self.word_count,
            "source_segments": self.source_segments,
        }


def _tokenize(text: str) -> list[str]:
    """Extract meaningful words."""
    words = re.findall(r"[a-záàâãéèêíïóôõúüçñ]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOPWORDS]


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def _compute_tf(words: list[str]) -> dict[str, float]:
    """Compute term frequency."""
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    total = len(words) if words else 1
    return {w: c / total for w, c in freq.items()}


def _compute_idf(sentences_words: list[list[str]]) -> dict[str, float]:
    """Compute inverse document frequency across sentences."""
    n = len(sentences_words) if sentences_words else 1
    df: dict[str, int] = {}
    for words in sentences_words:
        seen: set[str] = set()
        for w in words:
            if w not in seen:
                df[w] = df.get(w, 0) + 1
                seen.add(w)
    return {w: math.log(n / (1 + count)) for w, count in df.items()}


def _score_sentence(sentence: str, idf: dict[str, float]) -> float:
    """Score a sentence by TF-IDF relevance."""
    words = _tokenize(sentence)
    if not words:
        return 0.0
    tf = _compute_tf(words)
    score = sum(tf.get(w, 0) * idf.get(w, 0) for w in words)
    # Normalize by sentence length (prefer medium-length sentences)
    length_factor = min(len(words) / 10, 1.0)  # penalty for very short
    long_penalty = min(30 / max(len(words), 1), 1.0)  # penalty for very long
    return score * length_factor * long_penalty


def _add_position_bonus(scores: list[tuple[int, float]], total: int) -> list[tuple[int, float]]:
    """Add position bonus — first and last sentences tend to be more important."""
    if total == 0:
        return scores
    result: list[tuple[int, float]] = []
    for idx, score in scores:
        position = idx / max(total - 1, 1)
        # Boost first 10% and last 10%
        if position < 0.1 or position > 0.9:
            score *= 1.3
        result.append((idx, score))
    return result


def summarize_segments(
    segments: list[Segment],
    *,
    max_sentences: int = 10,
    title: str = "",
) -> Summary:
    """Generate an extractive summary from transcription segments.

    Selects the most representative sentences using TF-IDF scoring
    with position bonuses.

    Args:
        segments: Transcription segments (should be cleaned).
        max_sentences: Maximum sentences in the summary.
        title: Optional title for the content.

    Returns:
        Summary object with key points and full summary.
    """
    speech_segments = [s for s in segments if s.type == "speech" and s.text.strip()]

    if not speech_segments:
        return Summary(
            title=title or "Untitled",
            key_points=[],
            full_summary="",
            word_count=0,
            source_segments=0,
        )

    # Combine all text and split into sentences
    full_text = " ".join(s.text.strip() for s in speech_segments)
    sentences = _split_sentences(full_text)

    if not sentences:
        return Summary(
            title=title or "Untitled",
            key_points=[full_text[:200]],
            full_summary=full_text[:500],
            word_count=len(full_text.split()),
            source_segments=len(speech_segments),
        )

    # Compute IDF across all sentences
    sentences_words = [_tokenize(s) for s in sentences]
    idf = _compute_idf(sentences_words)

    # Score each sentence
    scored: list[tuple[int, float]] = [
        (i, _score_sentence(s, idf))
        for i, s in enumerate(sentences)
    ]

    # Add position bonus
    scored = _add_position_bonus(scored, len(sentences))

    # Select top sentences, maintaining original order
    scored.sort(key=lambda x: x[1], reverse=True)
    selected_indices = sorted([idx for idx, _ in scored[:max_sentences]])

    key_points = [sentences[i] for i in selected_indices[:5]]
    summary_sentences = [sentences[i] for i in selected_indices]
    full_summary = " ".join(summary_sentences)

    return Summary(
        title=title or "Untitled",
        key_points=key_points,
        full_summary=full_summary,
        word_count=len(full_summary.split()),
        source_segments=len(speech_segments),
    )


def save_summary(summary: Summary, output_path: Path) -> Path:
    """Save summary as JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def summary_to_markdown(summary: Summary) -> str:
    """Format summary as markdown."""
    lines: list[str] = [f"## Summary: {summary.title}\n"]

    if summary.key_points:
        lines.append("### Key Points\n")
        for point in summary.key_points:
            lines.append(f"- {point}")
        lines.append("")

    if summary.full_summary:
        lines.append("### Full Summary\n")
        lines.append(summary.full_summary)
        lines.append("")

    lines.append(f"*{summary.word_count} words from {summary.source_segments} segments*\n")
    return "\n".join(lines)
