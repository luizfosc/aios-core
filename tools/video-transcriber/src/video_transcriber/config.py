"""Configuration and default settings for video-transcriber."""

from pathlib import Path

# Output paths
YOUTUBE_OUTPUT = Path.home() / "Dropbox" / "Downloads" / "YT"
COURSES_OUTPUT = Path.home() / "Dropbox" / "Downloads" / "Cursos"

# Whisper defaults
DEFAULT_MODEL = "medium"
DEFAULT_LANGUAGE = "pt"
WHISPER_MODELS = ("tiny", "base", "small", "medium", "large", "turbo", "large-v3-turbo")

# Chunking
CHUNK_MAX_WORDS = 2000

# Batch defaults
BATCH_DEFAULT_MODEL = "turbo"
BATCH_OUTPUT_SUFFIX = "-transcricao.md"
BATCH_STATUS_FILE = "batch-status.json"
BATCH_DASHBOARD_PORT = 8765
BATCH_SENTENCES_PER_PARAGRAPH = 5

# Chapter detection defaults
CHAPTER_MIN_SECONDS = 120.0
CHAPTER_WINDOW_SIZE = 15
CHAPTER_THRESHOLD = 0.75

# Summarization defaults
SUMMARY_MAX_SENTENCES = 10

# Supported formats
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".wma", ".opus"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".wmv", ".flv", ".m4v"}
MEDIA_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS
TEXT_EXTENSIONS = {".vtt", ".srt", ".txt", ".md", ".json"}
