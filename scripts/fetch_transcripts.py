"""Prefetch YouTube transcripts for catalog items into the private transcripts repo.

YouTube blocks transcript downloads from cloud runners, so this runs locally
(see scripts/com.martinbreuss.ai-syllabus-transcripts.plist) and pushes
timestamped plain-text transcripts that the cloud routine can read.

Usage: uv run scripts/fetch_transcripts.py <path-to-transcripts-repo>
"""

import logging
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

CATALOG_URL = "https://raw.githubusercontent.com/martin-martin/ai-syllabus/main/catalog.yaml"
YOUTUBE_ID = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})")
CUE_START = re.compile(r"^(\d+):(\d{2}):(\d{2})\.\d+ -->")
TAG = re.compile(r"<[^>]+>")
PAUSE_SECONDS = 20  # YouTube rate-limits (HTTP 429) rapid subtitle requests

log = logging.getLogger("fetch_transcripts")


def youtube_ids(catalog: str) -> list[str]:
    """Return unique YouTube video IDs found in the catalog text, in order."""
    return list(dict.fromkeys(YOUTUBE_ID.findall(catalog)))


def vtt_to_text(vtt: str) -> str:
    """Flatten a VTT file to `[hh:mm:ss] text` lines, dropping rolling-caption repeats."""
    lines: list[str] = []
    last = ""
    for block in vtt.split("\n\n"):
        rows = block.strip().splitlines()
        start = next((CUE_START.match(r) for r in rows if CUE_START.match(r)), None)
        if not start:
            continue
        stamp = ":".join(start.groups())
        for row in rows:
            text = TAG.sub("", row).strip()
            if text and "-->" not in row and text != last:
                lines.append(f"[{stamp}] {text}")
                last = text
    return "\n".join(lines) + "\n"


def download_vtt(video_id: str, workdir: Path) -> Path | None:
    """Download English subtitles (manual preferred, auto as fallback) with yt-dlp."""
    cmd = [
        "uvx", "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", "en", "--sub-format", "vtt", "-o", str(workdir / "%(id)s"),
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    vtt = next(workdir.glob(f"{video_id}*.vtt"), None)
    if vtt is None:
        log.warning("No subtitles for %s: %s", video_id, result.stderr.strip()[-300:])
    return vtt


def git(repo: Path, *args: str) -> str:
    """Run a git command in `repo` and return stdout."""
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    repo = Path(sys.argv[1]).expanduser().resolve()
    out_dir = repo / "youtube"
    out_dir.mkdir(exist_ok=True)
    git(repo, "pull", "--ff-only", "-q")

    with urllib.request.urlopen(CATALOG_URL, timeout=30) as response:
        catalog = response.read().decode()
    missing = [v for v in youtube_ids(catalog) if not (out_dir / f"{v}.txt").exists()]
    log.info("%d YouTube transcripts missing", len(missing))

    with tempfile.TemporaryDirectory() as tmp:
        for i, video_id in enumerate(missing):
            if i:
                time.sleep(PAUSE_SECONDS)
            vtt = download_vtt(video_id, Path(tmp))
            if vtt:
                (out_dir / f"{video_id}.txt").write_text(vtt_to_text(vtt.read_text()))
                log.info("Saved %s", video_id)

    if git(repo, "status", "--porcelain"):
        git(repo, "add", "youtube")
        git(repo, "commit", "-q", "-m", "Add transcripts")
        git(repo, "push", "-q")
        log.info("Pushed new transcripts")


if __name__ == "__main__":
    main()
