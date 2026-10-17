# ai-syllabus

A growing, curated list of freely accessible lectures, talks, papers and posts by the people who built modern AI, from early neural network research to current work.

Every weekday a scheduled Claude Code run picks one piece, finds a worthwhile section (with timestamp and verified quote), and drafts a few short LinkedIn post variants for me (Martin Breuss) to edit and share. Picks are delivered as GitHub issues.

## Files

- `people.yaml`: researchers and educators, with why they matter.
- `catalog.yaml`: candidate pieces and their status (`candidate`, `picked`, `posted`, `skipped`).
- `picks/`: one Markdown file per daily pick.
- `voice.md`: style guide for the drafts.
- `ROUTINE.md`: instructions the scheduled run follows.

## Feedback loop

Comment on a daily issue with `posted B` (plus the final text if edited), `skip: <reason>`, or style notes. The next run updates the catalog and proposes voice guide changes.

## Transcripts

YouTube blocks transcript downloads from cloud runners, so `scripts/fetch_transcripts.py` runs locally on weekdays at 17:30 (launchd job in `scripts/`) and pushes transcripts for catalog videos to a separate private repo.

Install the job:

```sh
cp scripts/com.martinbreuss.ai-syllabus-transcripts.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.martinbreuss.ai-syllabus-transcripts.plist
```

Run it by hand: `uv run --no-project scripts/fetch_transcripts.py <path-to-transcripts-repo>`. Logs go to `~/Library/Logs/ai-syllabus-transcripts.log`.
