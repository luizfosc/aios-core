"""Caption generation — SRT and VTT subtitle files from transcription segments."""

from __future__ import annotations

from pathlib import Path

from .models import Segment


def _fmt_srt_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS,mmm for SRT."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _fmt_vtt_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS.mmm for VTT."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def segments_to_srt(segments: list[Segment]) -> str:
    """Convert segments to SRT subtitle format.

    Args:
        segments: List of transcription segments with start/end timestamps.

    Returns:
        SRT-formatted string.
    """
    lines: list[str] = []
    idx = 1

    for seg in segments:
        if seg.type != "speech" or not seg.text.strip():
            continue
        lines.append(str(idx))
        lines.append(f"{_fmt_srt_time(seg.start)} --> {_fmt_srt_time(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
        idx += 1

    return "\n".join(lines)


def segments_to_vtt(segments: list[Segment], title: str = "") -> str:
    """Convert segments to WebVTT subtitle format.

    Args:
        segments: List of transcription segments with start/end timestamps.
        title: Optional title for the VTT header.

    Returns:
        VTT-formatted string.
    """
    lines: list[str] = ["WEBVTT"]
    if title:
        lines[0] = f"WEBVTT - {title}"
    lines.append("")

    for seg in segments:
        if seg.type != "speech" or not seg.text.strip():
            continue
        lines.append(f"{_fmt_vtt_time(seg.start)} --> {_fmt_vtt_time(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")

    return "\n".join(lines)


def save_srt(segments: list[Segment], output_path: Path) -> Path:
    """Write segments as an SRT file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = segments_to_srt(segments)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def save_vtt(segments: list[Segment], output_path: Path, title: str = "") -> Path:
    """Write segments as a VTT file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = segments_to_vtt(segments, title=title)
    output_path.write_text(content, encoding="utf-8")
    return output_path
