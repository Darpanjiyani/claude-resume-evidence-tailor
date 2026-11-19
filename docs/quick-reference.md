# Quick Reference

## 1. Install

**Claude (web, desktop):**
1. Zip the `resume-evidence-tailor` folder. The folder itself must be the root of the ZIP, and the folder name must match the `name` in `SKILL.md`.
2. In Claude, go to **Customize → Skills**, click **+**, then **Create skill → Upload a skill**, and upload the ZIP.
3. See Anthropic's guide: https://support.claude.com/en/articles/12512180-use-skills-in-claude

**Claude Code:** copy the folder to `~/.claude/skills/resume-evidence-tailor/`.

**Needed in the environment:**
- `python3`
- LibreOffice and `pdftotext` (poppler), for the layout check
- Claude's built-in docx skill, for building the Word file

## 2. Fill in the Evidence Bank

Edit `resume-evidence-tailor/evidence_bank.md` before uploading. See `examples/sample_evidence_bank.md` for a filled-in example.

| Rule | Why |
|---|---|
| Real, measured facts only | The skill copies them exactly as written |
| Anything in `[brackets]` = unconfirmed | Never used; it goes to "Confirm Before Sending" instead |
| One entry per project, with Status, Origin, My part, Best for roles, Domain, Link | These drive project scoring and the honesty rules (team work, tutorials, co-authors) |
| Self-study skills in their own section | They go in the Skills line only, never as projects |

Keep your real Evidence Bank private. Commit the template, not your copy.

## 3. Run it

Attach your resume (.docx works best) and paste the job description or a link, then:

```
/resume-evidence-tailor
```

You can add instructions in the same message ("keep the header as is", "drop the streaming project"). Explicit instructions take priority over the skill's defaults.

## 4. Read the output

| Output | What to do with it |
|---|---|
| `<Name>_Resume_<Company>_<Role>.docx` | The tailored resume. Export the PDF from Word, not LibreOffice |
| `<Company>_<Role>_report.md`, sections 2 and 9 | Keyword table and coverage before → after |
| Report section 5 | Why each project was kept or swapped |
| Report section 8 | Gap triage: fix with wording, fix with a project, or hard gap. Ends with an Apply recommendation |
| **Report section 11: Confirm Before Sending** | **Read this every time.** Missing metrics, derived numbers and conflicts between your sources. None of it is in the file until you confirm it |

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| Upload fails | Check that the folder name matches the skill name and that the ZIP has the folder at its root. claude.ai may also reject skill descriptions over 200 characters, so shorten the `description` if needed |
| The PDF is 2 pages but Word shows 1 | LibreOffice lays pages out taller than Word. The layout check compares both files in the same converter, so trust that check and export from Word |
| A fact you know is true keeps getting flagged | Add it to the Evidence Bank. The checks only trust the resume and the bank |
