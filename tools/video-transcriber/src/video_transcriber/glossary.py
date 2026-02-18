"""Glossary/NER extraction — extract key terms, proper names, and concepts.

Uses frequency analysis, capitalization patterns, and multi-word detection
to identify important terms without external NLP dependencies.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .models import Segment


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
    "essa", "esse", "isso", "aquilo", "nessa", "nesse", "nisso", "disso",
    "dessa", "desse", "dela", "dele", "minha", "meu", "sua", "seu",
    "nossa", "nosso", "outra", "outro", "outras", "outros", "onde", "cada",
    # English
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "this", "that", "these", "those",
    "it", "its", "he", "she", "they", "we", "you", "i", "my", "your",
    "not", "so", "if", "from", "just", "very", "also", "then", "than",
    "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "once", "here",
    "there", "when", "where", "why", "how", "all", "both", "each",
    "few", "more", "most", "other", "some", "such", "only", "own",
    "same", "too", "which", "who", "whom",
})

# Pattern for capitalized multi-word sequences (likely proper names)
_PROPER_NAME_RE = re.compile(
    r"\b([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÚÜÇÑ][a-záàâãéèêíïóôõúüçñ]+(?:\s+[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÚÜÇÑ][a-záàâãéèêíïóôõúüçñ]+)+)\b"
)

# Pattern for technical terms (words with special chars or patterns)
_TECHNICAL_RE = re.compile(
    r"\b([A-Z][A-Za-z]*(?:\.[A-Za-z]+)+|[A-Z]{2,}(?:\s+[A-Z]{2,})*|[a-z]+(?:-[a-z]+)+)\b"
)


@dataclass
class GlossaryEntry:
    """A single glossary entry."""

    term: str
    count: int
    category: str  # "concept", "proper_name", "technical"
    first_seen: float = 0.0  # timestamp of first occurrence

    def to_dict(self) -> dict:
        return {
            "term": self.term,
            "count": self.count,
            "category": self.category,
            "first_seen": self.first_seen,
        }


@dataclass
class Glossary:
    """Full glossary extracted from transcription."""

    entries: list[GlossaryEntry] = field(default_factory=list)
    total_terms: int = 0

    @property
    def concepts(self) -> list[GlossaryEntry]:
        return [e for e in self.entries if e.category == "concept"]

    @property
    def proper_names(self) -> list[GlossaryEntry]:
        return [e for e in self.entries if e.category == "proper_name"]

    @property
    def technical_terms(self) -> list[GlossaryEntry]:
        return [e for e in self.entries if e.category == "technical"]

    def to_dict(self) -> dict:
        return {
            "total_terms": self.total_terms,
            "entries": [e.to_dict() for e in self.entries],
            "by_category": {
                "concepts": len(self.concepts),
                "proper_names": len(self.proper_names),
                "technical": len(self.technical_terms),
            },
        }


def _extract_proper_names(segments: list[Segment]) -> dict[str, dict]:
    """Extract capitalized multi-word sequences as proper names."""
    names: dict[str, dict] = {}
    for seg in segments:
        if seg.type != "speech":
            continue
        for match in _PROPER_NAME_RE.finditer(seg.text):
            name = match.group(1).strip()
            # Filter out sentence-start false positives
            words = name.split()
            if len(words) < 2:
                continue
            # Skip if all words are common
            if all(w.lower() in _STOPWORDS for w in words):
                continue
            key = name.lower()
            if key not in names:
                names[key] = {"term": name, "count": 0, "first_seen": seg.start}
            names[key]["count"] += 1
    return names


def _extract_technical_terms(segments: list[Segment]) -> dict[str, dict]:
    """Extract technical terms (acronyms, dotted names, hyphenated terms)."""
    terms: dict[str, dict] = {}
    for seg in segments:
        if seg.type != "speech":
            continue
        for match in _TECHNICAL_RE.finditer(seg.text):
            term = match.group(1).strip()
            if len(term) < 2:
                continue
            key = term.lower()
            if key not in terms:
                terms[key] = {"term": term, "count": 0, "first_seen": seg.start}
            terms[key]["count"] += 1
    return terms


def _extract_key_concepts(
    segments: list[Segment],
    *,
    min_count: int = 3,
    min_word_length: int = 4,
) -> dict[str, dict]:
    """Extract frequently used meaningful words as key concepts."""
    word_freq: dict[str, dict] = {}
    for seg in segments:
        if seg.type != "speech":
            continue
        words = re.findall(r"[a-záàâãéèêíïóôõúüçñ]+", seg.text.lower())
        for w in words:
            if len(w) < min_word_length or w in _STOPWORDS:
                continue
            if w not in word_freq:
                word_freq[w] = {"term": w, "count": 0, "first_seen": seg.start}
            word_freq[w]["count"] += 1

    # Filter by minimum frequency
    return {k: v for k, v in word_freq.items() if v["count"] >= min_count}


def _extract_bigrams(
    segments: list[Segment],
    *,
    min_count: int = 3,
) -> dict[str, dict]:
    """Extract frequent two-word phrases as compound concepts."""
    bigram_freq: dict[str, dict] = {}
    for seg in segments:
        if seg.type != "speech":
            continue
        words = re.findall(r"[a-záàâãéèêíïóôõúüçñ]+", seg.text.lower())
        words = [w for w in words if len(w) > 2 and w not in _STOPWORDS]
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram not in bigram_freq:
                bigram_freq[bigram] = {"term": bigram, "count": 0, "first_seen": seg.start}
            bigram_freq[bigram]["count"] += 1

    return {k: v for k, v in bigram_freq.items() if v["count"] >= min_count}


def extract_glossary(
    segments: list[Segment],
    *,
    max_entries: int = 50,
    min_concept_count: int = 3,
) -> Glossary:
    """Extract a glossary from transcription segments.

    Combines proper name detection, technical term extraction,
    and frequency-based concept identification.

    Args:
        segments: Cleaned transcription segments.
        max_entries: Maximum glossary entries.
        min_concept_count: Minimum occurrences for a concept.

    Returns:
        Glossary object with categorized entries.
    """
    entries: list[GlossaryEntry] = []
    seen_keys: set[str] = set()

    # 1. Proper names (highest priority)
    proper_names = _extract_proper_names(segments)
    for key, data in proper_names.items():
        if data["count"] >= 2 and key not in seen_keys:
            entries.append(GlossaryEntry(
                term=data["term"],
                count=data["count"],
                category="proper_name",
                first_seen=data["first_seen"],
            ))
            seen_keys.add(key)

    # 2. Technical terms
    technical = _extract_technical_terms(segments)
    for key, data in technical.items():
        if data["count"] >= 2 and key not in seen_keys:
            entries.append(GlossaryEntry(
                term=data["term"],
                count=data["count"],
                category="technical",
                first_seen=data["first_seen"],
            ))
            seen_keys.add(key)

    # 3. Key bigrams (compound concepts)
    bigrams = _extract_bigrams(segments, min_count=min_concept_count)
    for key, data in bigrams.items():
        if key not in seen_keys:
            entries.append(GlossaryEntry(
                term=data["term"],
                count=data["count"],
                category="concept",
                first_seen=data["first_seen"],
            ))
            seen_keys.add(key)

    # 4. Single-word key concepts
    concepts = _extract_key_concepts(segments, min_count=min_concept_count)
    for key, data in concepts.items():
        if key not in seen_keys:
            entries.append(GlossaryEntry(
                term=data["term"],
                count=data["count"],
                category="concept",
                first_seen=data["first_seen"],
            ))
            seen_keys.add(key)

    # Sort by count descending, cap at max_entries
    entries.sort(key=lambda e: e.count, reverse=True)
    entries = entries[:max_entries]

    return Glossary(entries=entries, total_terms=len(entries))


def save_glossary(glossary: Glossary, output_path: Path) -> Path:
    """Save glossary as JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(glossary.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def glossary_to_markdown(glossary: Glossary) -> str:
    """Format glossary as markdown."""
    lines: list[str] = ["## Glossary\n"]

    if glossary.proper_names:
        lines.append("### People & Names\n")
        for e in sorted(glossary.proper_names, key=lambda x: x.count, reverse=True):
            lines.append(f"- **{e.term}** ({e.count}x)")
        lines.append("")

    if glossary.technical_terms:
        lines.append("### Technical Terms\n")
        for e in sorted(glossary.technical_terms, key=lambda x: x.count, reverse=True):
            lines.append(f"- **{e.term}** ({e.count}x)")
        lines.append("")

    if glossary.concepts:
        lines.append("### Key Concepts\n")
        for e in sorted(glossary.concepts, key=lambda x: x.count, reverse=True):
            lines.append(f"- **{e.term}** ({e.count}x)")
        lines.append("")

    lines.append(f"*{glossary.total_terms} terms extracted*\n")
    return "\n".join(lines)
