# Design Decisions

The main choices behind the skill, and the problem each one solves.

## A separate Evidence Bank instead of "just use the resume"
A one-page resume can't hold everything. Without a source of extra facts, a model either leaves out relevant work or invents it. The Evidence Bank holds every project, metric and self-study skill. The rule is strict: text in `[brackets]` is unconfirmed and is never used. That makes "don't invent anything" something the model can follow and a script can check.

## Honesty rules written into the project fields
- **"My part":** limits which team work can be described as the candidate's own.
- **"Origin: Tutorial-based":** blocks claims of original design.
- **"Co-authors listed":** blocks words like "solo" or "independently" that would contradict a public report.

These are written as fields, so they're applied the same way every time instead of left to judgment.

## Profiles loaded on demand
Role and industry guidance lives in `references/`. After classifying the job, only the matching sections are read, which keeps the context small. Industry "translations" are allowed only when the underlying fact is on file: "built anomaly alerting" is fine, "worked in banking" is not.

## Scripts for the checks that matter most
`check_resume.py` compares every number, and the noun it counts, against the sources. So "40+ engineers" is flagged when the sources say "20+ engineers". It also compares line positions with the original and matches each GitHub link to its project. `ai_tells.py` counts stock AI words and sentence patterns. The model must fix flags and re-run until they pass, or explain each remaining flag in the report.

## Layout parity instead of page count
LibreOffice often lays out a Word resume taller than Word does, so a one-page resume can render as two pages. Trimming content to satisfy the converter would be wrong. Instead, the original and the tailored file are rendered with the same converter, and each line's position is compared. If the positions match, the footprint hasn't changed.

## Edit in place, not rebuild
The tailored resume is an edited copy of the attached .docx: same styles, margins, spacing runs and link formatting. Rebuilding from scratch loses the small spacing tricks that make a resume fit exactly one page.

## "Confirm Before Sending" instead of mid-run questions
The skill doesn't stop to ask. Anything uncertain (missing metrics, derived numbers, conflicts between the resume and the bank) is kept out of the file and listed at the end. The user gets a usable file right away and a short list of things to check before sending.

## Plain, human wording
Recruiters tend to spot AI-written resumes by feel: stock phrases, every bullet with the same shape, wording lifted from the posting. The skill bans a list of stock words and limits trailing "-ing" clauses. It also requires every bullet to start with a different verb, and it shows soft JD phrases ("cross-functional collaboration") through concrete facts instead of pasting them in.
