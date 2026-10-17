# Daily pick routine

**GitHub access:** `gh` is not authenticated in cloud runs, don't use it. Use the built-in GitHub tools (`mcp__github__*`, load via ToolSearch: e.g. `list_issues`, `issue_read`, `issue_write`, `add_issue_comment`) for all issue work. When creating an issue, pass the actual file content as the body, not a shell expression. Commit and push with plain `git` to `main` (if HEAD is detached, `git push origin HEAD:main`).

**Manual / off-schedule runs:** if this run was started manually (any day, including weekends) still produce a pick. If `picks/<today>.md` already exists, use `picks/<today>-b.md` (then `-c`, ...).

Instructions for the scheduled Claude run (weekdays, ~12:00 Europe/Vienna). Martin posts around 15:00 to 16:00 Vienna time (US East Coast morning).

## 1. Read feedback

- Read `voice.md` and `catalog.yaml`.
- List recent issues labeled `daily-pick` (state all, last 10) and read comments on any you haven't processed.
- Apply feedback in `catalog.yaml`:
  - "posted" (optionally with final text, or "posted A/B/C"): set `status: posted`, `posted_on`, and `posted_text` (Martin's final text if given, otherwise the chosen variant).
  - "skip" or reasons against: set `status: skipped` and note the reason.
  - Style corrections: propose a dated line for "Additions from review rounds" in `voice.md` in today's issue. Don't edit `voice.md` without approval, unless Martin's comment says to add it.
  - Whenever Martin shares his posted text, add it to "Posted examples" in `voice.md` (that counts as approved). Note briefly what differed from the drafts.
  - Reply on the issue with a one-line comment saying what you recorded, then close it.

## 2. Keep the catalog healthy

- If fewer than ~15 `candidate` items remain, research and add 5 to 10 new ones. Use `people.yaml` and web search, and aim for a mix:
  - About 50/50 `foundational` (history that led to today, any decade) and `current` (roughly the last 18 months).
  - All formats: talks, course lectures, podcasts, papers, essays, blog posts.
  - Freely accessible only, no paywalls.
- You may add people to `people.yaml` with a one-line `why`. Mention additions in the issue.

## 3. Pick one

- Prefer candidates whose full text or transcript is available (papers, posts, podcast pages with transcripts, prefetched YouTube transcripts).
- Choose a `candidate` that differs from the last 5 picks in person and format, and alternates eras.
- Verify it: fetch the URL and confirm the title, speaker and date. Set `verified: true`. If the URL is dead or wrong, fix it or mark it skipped and pick another.
- Get the actual content:
  - YouTube: YouTube blocks cloud downloads. Read the prefetched transcript from the private repo `martin-martin/ai-syllabus-transcripts` (cloned next to this repo, or fetch `youtube/<video_id>.txt` via the GitHub tools). Format: `[hh:mm:ss] text` lines. Martin's Mac fills it on weekdays at 17:30 Vienna for every YouTube URL in `catalog.yaml`, so newly added videos become usable the next day. Never commit transcripts to this public repo.
  - If no transcript exists for a video, prefer another candidate. Pick a video without transcript only if it's clearly the best choice, then use its chapters/description and mark the quote unverified.
  - Papers and posts: fetch the page or PDF text.
- Select one section worth 2 to 5 minutes (or a few paragraphs): a clear explanation, a surprising claim, a historical insight. For video, record the start timestamp and build a deep link (`&t=<seconds>s` or `?t=` for youtu.be).
- Extract a short verbatim quote (1 to 3 sentences) from that section. **Quote only text present in the transcript or source.** If no transcript is obtainable, say so in the issue, give the best section guess from chapters or description, and mark the quote as unverified. Never invent one.

## 4. Draft

Write 2 to 3 variants (see `voice.md`) that are clearly different from each other in angle, structure and length (e.g. short, medium, longer). Each variant:
- Names the person and includes the deep link in the body.
- Follows every rule in `voice.md`, including no em dashes and no hype.

## 5. Deliver

- Write `picks/YYYY-MM-DD.md` using `picks/TEMPLATE.md`.
- Update the catalog entry: `status: picked`, `picked_on`, `timestamp`, `quote`, `issue` (after creating it).
- Commit to `main` with message `Daily pick: <title>` and push.
- Open an issue titled `Daily pick YYYY-MM-DD: <person>, <short title>`, labeled `daily-pick`, whose body is the pick file's content. Martin is notified by GitHub.
- Delete `tmp/`.

If anything blocks the run (e.g. transcripts fail everywhere), still open an issue explaining what happened, so Martin knows the run happened.
