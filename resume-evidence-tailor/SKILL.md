---
name: "resume-evidence-tailor"
description: "Tailor Darpan's resume to a specific job posting using his Evidence Bank and Project Library, so it passes ATS screening, reads as human-written, and stays on one page. Use whenever the user shares a job description (JD) or a job posting link with their resume, or asks to customize, optimize, tailor, or \"ATS-proof\" a resume for a role. Picks the best projects from the library for each job, adds only facts that are on file, and produces a .docx plus a report file (keyword table, project scores, gap triage) and a Confirm Before Sending list."
---

# Resume Evidence Tailor

## Auto-Run Mode

When this skill is invoked, run the full workflow end to end without waiting for further instructions.

### Inputs (load automatically)

1. **Job description:** Use the JD in the user's message. If the message gives a job link instead of the text, fetch the posting (WebFetch, or the Indeed connector's job-details tool for Indeed links when it is available) and use the full posting text. If the page can't be read (sign-in wall, expired posting), ask for the pasted JD once and stop. If no JD or link is provided, ask for it once and stop.
2. **Resume:** The user attaches their current resume every time. Use the resume attached in the current message. If none is attached, ask for it once and stop; do not tailor from memory or from an earlier conversation. The attached resume also sets how many project slots and bullets the output has.
3. **Evidence Bank:** Always read `evidence_bank.md` from this skill folder. Lines that are still template placeholders (text in `[square brackets]`, `__` blanks, or lines starting with "e.g.") are unfilled and are **not** facts. Never use them as evidence; if one would have helped, add it to the Confirm Before Sending list.
4. **Profiles:** After Step 0, read only the matching sections of `references/role_profiles.md` and `references/industry_profiles.md`.

### Execution order

1. Step 00 → Load evidence
2. Step 0 → Analyze JD, classify role type and industry
3. Priorities 0–5 (including 2.5) → Tailor headline, skills, bullets, business impact, projects, summary, relevance pass
4. Generate the tailored resume as a .docx file using ATS-safe formatting (section 12). Read the docx skill's SKILL.md before building the file (find it in the skills list; its path differs between environments). If the attached resume is already a .docx, edit a copy of it in place so the original layout is kept. Name it `Darpan_Jiyani_Resume_<Company>_<Role>.docx`.
5. Final Quality Check, including the AI-wording check (`scripts/ai_tells.py`), the unique opening verbs check, and the resume check (`scripts/check_resume.py`: facts, layout, links). Fix what they flag and re-run until they pass.
6. Write the full report (Output Format sections 1–11) to `<Company>_<Role>_report.md`, send it together with the .docx, and reply in chat with the short summary described under Output Format.

### Questions

- Do not ask questions mid-workflow. Collect anything uncertain (missing metrics, derived numbers, unclear facts) into a **"Confirm Before Sending"** list at the end of the output.
- Exclude unconfirmed or derived facts from the .docx; list them in the Confirm Before Sending list instead.

---

## Goal

Make the resume reflect the job posting's exact language without inventing experience.

Make the fewest edits that create the greatest improvement in ATS keyword coverage, recruiter relevance, and clarity. Prioritize strong evidence over keyword quantity.

The tailored resume must remain truthful, natural, concise, and defensible in an interview.

## Step 00 — Load Evidence Sources

Before analyzing the JD, gather evidence from three sources:

1. **Resume:** The current tailored or base resume.
2. **Evidence Bank:** The candidate's master list of true facts, metrics, projects, coursework, and domain exposure that may not appear on the one-page resume. Its **Project Library** lists every project the candidate has built; Priority 3 chooses from it. If no Evidence Bank is available, note this in the Confirm Before Sending list.
3. **Role and Industry Profiles:** Stored in `references/`.

A requirement may be marked ❌ only after checking both the resume and the Evidence Bank.

If a fact exists in the Evidence Bank but not the resume, mark it ⚠️ and pull it into the resume when it is relevant.

**Conflicts:** If the resume and the Evidence Bank disagree on a fact (a degree name, a date, a number, a tool, a project's scope), do not pick one. Keep the resume's wording in the file, don't build new content on the disputed fact, and list both versions in Confirm Before Sending so the user can fix the wrong source.

---

## Step 0 — Analyze the Job Posting

1. Pull out the **top 5–8 requirements**.

2. Rank the requirements based on:

   - How often they are repeated in the JD
   - Whether they appear under "Required" or "Preferred"
   - Whether they appear in the job title
   - Whether they appear in the first lines of the posting
   - How central they are to the role's responsibilities

3. Record the **exact phrasing** used in the JD.

   Examples:

   - "Cross-functional collaboration"
   - "ETL pipelines"
   - "Stakeholder management"
   - "Data quality"
   - "Machine learning models"

4. Note the **exact target job title** from the posting.

5. Compare each top requirement against the resume and mark it as:

   - ✅ **Already shown:** Clearly demonstrated using the same or very similar wording
   - ⚠️ **Present but worded differently:** The candidate has the experience, but the resume does not use the JD's terminology
   - ❌ **Missing:** The resume does not provide evidence that the candidate has this qualification

6. Do not treat every item in the JD as equally important. Prioritize the core responsibilities and required qualifications over minor preferred qualifications.

7. Classify the **role type**: Data Engineer, Analytics Engineer, Data Analyst, BI Analyst, Business Data Analyst, Data Scientist, AI / ML Engineer, Financial Analyst, or Software Engineer. If the role is a hybrid, choose a primary and a secondary type.

8. Classify the **industry or domain**: Finance/Banking, Healthcare/Pharmacy, Manufacturing/Semiconductor, Retail/E-commerce, Transportation/Mobility, SaaS/GTM (B2B software, sales and go-to-market analytics), Tech/General, or Other. These names are also what a project's "Domain" is matched against in Priority 3. Note any domain-specific terms the JD repeats, such as "risk," "claims," "yield," or "compliance."

9. After classifying the role type and industry, read only the matching section of `references/role_profiles.md` and `references/industry_profiles.md`. Do not load profiles for other roles or industries. Use them to decide what to put first and which vocabulary to use.

---

## Priority 0 — Professional Headline: Title Alignment

Compare the candidate's current or most recent job title with the target job title.

### If the titles match or nearly match

Skip this step. A professional headline is not required solely for title alignment.

### If the titles do not match

Add a one-line professional headline directly under the candidate's name and contact information.

A headline adds a line. Add it only if it replaces content of the same height (see One-Page Layout Rules). If nothing can give up a line, recommend the headline in section 1 of the output instead of adding it to the file.

The headline should connect the candidate's real title and background to the target field without changing or misrepresenting the candidate's official job title.

### Format

`[Current Title] | [Target Field 1], [Target Field 2] & [Target Field 3]`

### Example

If the candidate's current title is "Data Engineer" and the target role is Data Scientist, Analytics Engineer, or AI Engineer:

**Data Engineer | Data Science, Analytics & AI**

### Headline rules

- Use the posting's terminology for the target fields.
- If the JD says "Machine Learning," do not automatically replace it with "AI."
- Keep the headline to one line.
- Use no more than three focus areas.
- Keep it specific enough to communicate the target direction.
- Align the headline with the Summary, Skills, Experience, and Projects sections so they tell one consistent story.
- Do not place the headline inside a page header, footer, table, text box, or graphic.

---

## Priority 1 — Skills and Keyword Alignment

Make sure every top requirement the candidate genuinely has appears **verbatim or nearly verbatim** somewhere on the resume.

### Keyword distribution rule

Distribute keywords naturally across the **Summary, Skills, Experience, Projects, and Education** sections where they are genuinely supported.

Do not concentrate all JD keywords in the Skills section.

A keyword listed in Skills should ideally be supported by evidence in Experience, Projects, or Education when that evidence is available.

Do not force a keyword into every section. Place it in the section where it is most credible and natural.

### Keyword placement hierarchy

For each important keyword, use the strongest available placement:

1. **Experience:** The skill was used in a professional role
2. **Projects:** The skill was applied in a substantive project
3. **Education:** The skill was covered through relevant coursework, research, or an academic project
4. **Skills:** The candidate knows the skill and can confidently discuss it
5. **Summary:** The skill is central to the candidate's fit for the target role and is supported elsewhere

### Skills section rules

- Use the JD's exact wording when it accurately describes the candidate's experience. This applies to tools, platforms, methods and core technical nouns ("ETL pipelines," "data quality," "Apache Airflow"). Soft phrases ("cross-functional collaboration," "stakeholder management") follow the Plain, Human Wording rules instead.
- If the JD says "ETL pipelines," prefer "ETL pipelines" over a vague substitute such as "data flows."
- Include both the acronym and full term where useful.

Example:

**Extract, Transform, Load (ETL)**

- Keep the attached resume's skill categories and its number of Skills lines (see One-Page Layout Rules). A category may be renamed toward the JD's wording (for example "Cloud" → "Cloud and Data Warehouses") only if the line still fits. Do not add or split categories.
- Order categories by the matching Role Profile's "Skills order" where the existing lines allow it.
- Put the most JD-relevant skills first within each category.
- Swap out or move down skills that are not relevant to the target role, replacing them with relevant ones in the same line.
- Do not add unsupported tools, technologies, methodologies, or domain knowledge.
- Do not repeat the same keyword unnecessarily.
- Avoid keyword lists that do not connect to demonstrated experience.

---

## Priority 2 — Experience Bullets

Rewrite **2–3 bullets** to reflect the posting's language. Choose them from whichever role holds the strongest evidence for the JD's top requirements, not only the most recent role. For example, a manufacturing JD may get more from the Keysight or Cerebulb bullets than from the current role. Bullets can come from more than one role.

Prioritize bullets that can demonstrate the JD's highest-ranked requirements. Bullets stay under the role where the work happened; never move a bullet to another employer.

### Bullet structure

Use this structure whenever the available information supports it:

**Action verb + what the candidate did + tool or method + scope, outcome, or measurable result**

The action verb must not open any other bullet on the page (see Unique Opening Verbs).

### Example

JD phrase:

**Cross-functional collaboration**

Original resume wording:

> Worked with different teams to improve reporting.

Tailored wording:

> Worked with operations and engineering teams to automate reporting, cutting manual processing time by 30%

The JD's soft phrase is shown by naming the actual teams, not pasted in. Recruiters read "Coordinated cross-functional collaboration" as copied from the posting.

(The 30% and the automation are only allowed because they come from the resume or Evidence Bank. If no source exists, drop them and add a request to Confirm Before Sending.)

### Experience bullet rules

- Preserve every original fact, metric, tool, responsibility, and scope.
- Change the wording and emphasis, not the underlying facts.
- Use the JD's wording only when it accurately describes the work performed.
- Pair important keywords with an action, result, scope, metric, or business outcome whenever possible.
- Do not add numbers that are not present in the source resume or supporting information.
- Do not make a responsibility sound larger than it was.
- Do not repeat the same keyword more than 2–3 times across the entire resume unless repetition is necessary and natural.
- Prefer specific evidence over generic claims.
- Do not mechanically insert keywords into unrelated bullets.

---

## Priority 2.5 — Business Impact Translation

For analyst, scientist, and finance-leaning roles, rewrite 2–3 bullets so the business outcome comes before the tools. These can be the same bullets chosen in Priority 2; aim for no more than 5 changed experience bullets in total, so the resume still reads as the candidate's own.

### Structure

**Business outcome + for whom + how (tool or method) + evidence**

### Example

Before: Automated shift reporting with Power Automate, saving 30+ min/shift

After: Saved 30+ minutes per shift for 50+ supervisors by automating shift reporting with Power Automate, removing formatting errors from daily operations reviews

(This example assumes "50+ supervisors" and "formatting errors" already appear elsewhere in the resume or Evidence Bank. Never add an audience size or outcome that has no source.)

### Rules

- Calculations from existing facts are allowed only when the math is direct and simple. Label them **"Derived — confirm with user"** in the output, and do not put them in the final resume until the user confirms.
- Never estimate dollar values, savings, or revenue without a source number.
- If an impact claim has no number (for example, "cut unplanned downtime"), add a request for the real figure to the Confirm Before Sending list instead of inventing one.
- Name the stakeholder or decision-maker whenever possible: operators, supervisors, plant managers, clients, engineering teams.
- Use industry vocabulary only as allowed by the matching Industry Profile.
- A result-first bullet still needs a unique opening word ("Saved", "Cut", "Reduced" can each open only one bullet).

---

## Priority 3 — Relevant Project Alignment

Review the Projects section and determine whether a project demonstrates a top JD requirement more convincingly than the candidate's professional experience.

Use project bullets when the candidate has genuine hands-on experience with a required technology, tool, methodology, or responsibility that is not strongly represented in the Experience section.

### Choose projects from the Project Library

The candidate's resume shows only a few projects. The **Project Library** in `evidence_bank.md` holds all of them. For every JD, pick the best set from both sources:

1. **Build the candidate list:** every project on the current resume plus every filled-in project in the Project Library. Skip library entries whose Status or Ready-to-use bullets are still placeholders in `[square brackets]`, unless the project is already on the resume.
   - **A project on both the resume and in the library is one candidate,** matched by title or GitHub link. It is always a candidate, whatever its library Status says, because the user already presents it. Its resume bullets are confirmed facts. Its library entry adds facts only from fields that are not in brackets.
   - When rewording such a project, start from its resume bullets and keep the same bullet count. Library facts (a metric, a tool) may replace weaker wording in the same lines.
2. **Apply the role filters first.** "Best for roles" restrictions are hard filters, not bonuses:
   - "X only" (for example "Software Engineer only"): drop the project unless the role type from Step 0, primary or secondary, is X.
   - A condition (for example "use for Data Engineer roles only when the JD asks for Kafka, Docker or Kubernetes"): drop the project unless the JD meets the condition.
   - Note every filtered-out project in the Project Selection table as "Not used (filtered)".
3. **Score each remaining project** against the top 5–8 JD requirements from Step 0:
   - +3 for each top requirement the project clearly demonstrates (tool, method, or responsibility)
   - +2 if its "Best for roles" includes the role type classified in Step 0
   - +1 if its "Domain" matches the JD's industry (use the Step 0 industry names; "Finance-adjacent" counts as Finance/Banking)
   - +1 if it has a real metric in "Results and metrics"
   - +1 if it covers a requirement that the Experience section does not already show (fills a gap rather than repeating evidence)
   - −1 if its Origin is "Tutorial-based"
4. **Pick one slot at a time,** for the same number of project slots the current resume has. Keep the one-page limit; do not add slots.
   - Take the highest-scoring project first.
   - Before each next pick, re-score the rest: the +3 counts only for top requirements that no project already picked demonstrates. This stops two projects that show the same thing (for example two Databricks medallion builds) from taking both slots, unless nothing else covers more.
   - Ties go to the project whose ready bullets match the slot's bullet count, then to the one with a real metric.
5. **Swap, don't stack:** a library project replaces the lowest-scoring resume project. Use the same number of bullets per project as the slot it replaces.
   - **Entry has more ready bullets than the slot:** use the ones that show the most top requirements.
   - **Entry has fewer ready bullets than the slot:** write the missing bullet from that entry's own fields only (Tools and tech, Methods and concepts, Data and scale, Results and metrics), and mark it "new bullet from library fields" in section 5. If the fields can't support another true, specific bullet, use the next-best project instead.
   - **Check what depends on the outgoing project first.** Search the Summary, headline and Skills for anything only that project supports: a metric, a named system, a tool. Either rewrite those lines in the same pass, or, if the outgoing project carries the Summary's headline achievement and the score gap is small, keep it and explain the trade-off in section 5.
6. **Build bullets from the library entry only:** start from its "Ready-to-use bullets" and adjust wording toward the JD. Every tool, number, and scale must appear in that project's entry. Bullets in `[square brackets]` are unconfirmed; skip them and list them in Confirm Before Sending.
   - **Library bullets often open with "Built" or "Designed".** When a swapped-in project's bullet repeats an opening verb already on the page, change it following Unique Opening Verbs.
   - **Team projects:** a bullet may say "Built", "Implemented" or "Designed" only for work listed under "My part". Describe other team work as team work ("Contributed to a 5-person team that..."). If "My part" is still in brackets, use only bullets that clearly describe shared work, and ask for the user's part in Confirm Before Sending.
   - **"Co-authors listed" projects:** the candidate built all of the work, so bullets may claim it. Never write "solo", "independently", "single-handedly", "led a team" or a team size; the submitted report lists other names, and the resume must not contradict it.
   - **Tutorial-based projects:** describe only what was built, never claim original design ("Designed an architecture..."). Prefer bullets about anything the user added beyond the tutorial. (The −1 in scoring already ranks a self-designed project above it when both cover the same requirement.)
   - **Results marked "team results":** never present them as the user's individual result.
7. **Status rules:** a "Completed" project can be used as is. An "In progress" project may be used only if its bullets describe work already done, and its title must say "(In Progress)". Never use a "Planned" project on the resume; it may only appear in Gap Triage as a suggestion.
8. Show the scores in Output section 5 so the user can see why each project was chosen, including the re-scored values for the second and later picks.

### Project selection rules

- Prioritize projects that demonstrate the JD's required technologies or responsibilities.
- Keep the most relevant projects and move them higher within the Projects section.
- Swap out (Priority 3 step 5) or move down projects that do not strengthen the candidate's fit for the target role. Never leave a project slot empty.
- Do not force every project to match the JD.
- For an early-career candidate, use substantive projects as evidence when relevant professional experience is limited.

### Project bullet rules

Rewrite selected project bullets using this structure:

**Action verb + system or problem + technology or methodology + scale, result, or demonstrated capability**

Example:

> Built an incremental ETL pipeline using Python, SQL, and Snowflake Streams and Tasks to process 50M+ records while handling late-arriving data.

### Project keyword rules

- Use the JD's exact phrase when the project genuinely demonstrates it.
- Connect keywords to implementation details, scale, architecture, measurable results, or technical decisions.
- Do not list a tool in a project unless the candidate actually used it.
- Do not convert tutorial exposure into professional-level project experience.
- If the candidate learned a skill through self-study, describe it at the appropriate level.
- Do not invent project metrics, users, data volumes, accuracy results, performance improvements, or business impact.

---

## Priority 4 — Summary or Objective

Rewrite the Summary or Objective for every application.

If the attached resume has no Summary, do not add one unless it replaces content of the same height (see One-Page Layout Rules). Otherwise, suggest it once in section 7 of the output, naming what it could replace. Write in implied first person (no "I").

The Summary should immediately communicate the candidate's relevance to the target role. It should not simply repeat the Skills section.

### Length

Use 2–3 concise lines.

### Structure

1. Target job title matching the posting, plus years or type of relevant experience
2. Two or three top JD requirements tied to the candidate's genuine strengths
3. One concrete achievement, area of impact, or value statement

### Summary rules

- Write the Summary only after Priority 3 is final, and rewrite every sentence of it. Do not keep sentences from the old Summary without checking them against the final page.
- Every number, named project and named system in the Summary must appear in a bullet on the final page. A fact that is true but no longer on the page does not count, and a Skills line alone never supports a metric.
- Use the exact target title when appropriate.
- Include only keywords supported by Experience, Projects, Education, or Skills.
- Prioritize two or three high-value keywords rather than listing every JD requirement.
- Keep the language natural and readable.
- Avoid generic filler, including:
  - "Passionate"
  - "Hardworking"
  - "Results-driven professional"
  - "Dynamic individual"
  - "Go-getter"
- Avoid exaggerated claims such as "expert" unless the candidate's background clearly supports that level.
- Do not repeat the headline word for word.

---

## Priority 5 — Relevance and Removal Pass

After tailoring the content, review every section of the resume for relevance.

Tailoring is not only about adding keywords. It also requires reducing content that distracts from the target role.

**What this pass may change in the file:** the order of items within a section, the wording of a bullet (keeping its line count), swapping one skill for another within a line, and replacing a low-value line with the headline or Summary (see One-Page Layout Rules). **What it may not do:** delete bullets, projects or lines, or add them. Every removal or shortening is a recommendation in section 7, which the user applies to their base resume if they agree.

### Review each item

Evaluate every:

- Experience bullet
- Project
- Skill
- Certification
- Coursework item
- Summary phrase

Ask:

1. Does this item provide evidence for a core target-role requirement?
2. Does it demonstrate a useful transferable skill?
3. Does it contain a meaningful tool, method, result, or metric?
4. Would removing it create space for stronger and more relevant evidence?

### Relevance pass rules

- Keep content that strengthens the candidate's fit for the target role.
- Replace the wording of low-value bullets with stronger true evidence when it fits the same lines; otherwise recommend shortening or removing them in section 7.
- Move highly relevant bullets, projects, and skills higher.
- Move secondary or preferred qualifications lower.
- Reword duplicate information that appears in multiple sections without adding evidence, or recommend removing it in section 7.
- Do not remove important achievements simply because their wording differs from the JD.
- Do not sacrifice readability to maximize keyword coverage.
- Preserve the candidate's strongest measurable accomplishments.
- The resume stays exactly one page (One-Page Layout Rules).

---

## One-Page Layout Rules

The attached resume is tuned to fill exactly one page. The tailored resume must occupy the same footprint: not spill onto a second page, and not leave a gap at the bottom.

- **Same sections, same order, same bullet count** under every role and project. Replacing a bullet's content, or swapping a Project Library project into an existing slot, is allowed. Adding or removing bullets is not.
- **Line-for-line parity.** A one-line bullet stays one line; a two-line bullet stays two lines, with the second line at least half full. Fill space with real facts (a number, a tool, who used it, what was slow or broken before), never filler words. If nothing true fits, let the line end a little short; that does not change the page length.
- **Skills section keeps the same number of lines.** Reorder and swap items within lines; do not add lines.
- **Headline and Summary** add lines. Add them only by replacing content of the same height, such as a low-value coursework line or the weakest bullet.
- **Zero spacing changes.** No blank paragraphs or extra line breaks, and no changes to margins, font sizes or paragraph spacing, especially below the Skills section.
- **Edit .docx files in place.** Work on a copy of the attached file. Inline bold splits a sentence into several runs in the XML; edit the plain runs and leave the bold runs where they are.
- **Keep non-text runs.** Runs that hold only a `<w:br/>`, tab or field create the gaps between sections. When replacing a paragraph's text, delete only the old text runs, never these.
- **Project links follow the project.** Every project on the final page shows its GitHub link in the same way the attached resume shows project links: same display text (e.g. "GitHub" or the URL), same position on the title line, same font, size, color and underline. Copy the formatting of an existing link run instead of building a new style.
  - **Swapping a project in:** take the URL from that project's **Link** field in the Project Library and point the slot's hyperlink at it. In the .docx, change the `Target` of the hyperlink's relationship in `word/_rels/document.xml.rels` (or add a new relationship with `TargetMode="External"` if the slot had no link) and keep the `<w:hyperlink r:id=...>` run formatting as is. Never leave the outgoing project's URL on the incoming project.
  - **Kept projects:** if a kept project's link on the resume differs from its library Link, use the library Link and note the change in section 5.
  - **No confirmed link:** when a swapped-in project's Link is empty or still in `[square brackets]`, remove the old hyperlink (and its relationship) rather than leaving a link to the wrong repo, and ask for the link in Confirm Before Sending.
  - **Check after building:** `scripts/check_resume.py` lists every hyperlink in the final .docx with its display text and target, and flags any that don't match the project they sit next to.
- **Trust footprint parity over a converter's page count.** LibreOffice-based converters often lay a page out taller than Word does, so the user's own one-page resume can render as two pages. Never trim content to satisfy a converter. `scripts/check_resume.py` checks parity: it renders the original and the tailored file with the same converter and compares each line's page number and vertical position. Identical positions mean the footprint is unchanged; it names the first line that moved, and the element just above it (which grew, shrank or lost spacing) gets fixed.
- **PDF or text resumes:** rebuild as .docx as faithfully as the format allows, say the formatting is approximated, and ask for the Word source in Confirm Before Sending.

---

## Education and Coursework Keyword Rules

Use the Education section for keywords only when they are genuinely supported by:

- A completed degree
- Relevant coursework
- Academic research
- A capstone
- A thesis
- A substantive academic project

Do not place unrelated JD keywords in Education merely to increase keyword coverage.

Do not rename degrees, courses, universities, majors, or credentials.

If relevant coursework is included, prioritize courses that support the target role and swap less relevant course names for relevant ones within the same line. A whole coursework line may only be replaced by the headline or Summary (One-Page Layout Rules).

---

## Plain, Human Wording

A recruiter who suspects AI usually goes by feel: stock phrases, every bullet built the same way, wording lifted from the posting. AI detectors are unreliable on short text like resume bullets, so no wording can guarantee a pass. What works is writing the way an engineer describes their own work, with details only the person who did it would know. Test every line: would the candidate say it this way if an interviewer asked "tell me about that"?

Every line written or rewritten in this skill follows these rules.

**Write like this:**
- **Plain verbs:** built, wrote, set up, moved, cut, fixed, replaced, added, ran, merged, automated, trained, deployed. Technical verbs are fine when literal ("orchestrated Airflow DAGs," "partitioned by date").
- **Concrete nouns:** the actual system, data and people ("plant managers," "a 30-person team," "RF test files") instead of "stakeholders," "insights" and "solutions."
- **What was slow or broken, and what changed:** "refresh took 15 min; now under 15 sec" instead of "enabling near real-time monitoring."
- **Different shapes:** some bullets lead with the result ("Cut X from A to B by…"), some with the work ("Wrote…"), and some are short. Every bullet starts with a different word (Unique Opening Verbs below).
- **"so" or "which" instead of a trailing -ing clause:** "…, so new test types don't break the pipeline" reads human; "…, enabling seamless onboarding of new test types" doesn't.
- **Numbers the way engineers say them:** "under 15 sec," "2M+ rows," "60+ stations."
- **Keep the searchable terms.** Plain wording changes the sentence shape, not the keywords: tool names and technical nouns stay.

**Avoid:**
- **Stock AI words:** leveraged, utilized, spearheaded, fostered, championed, streamlined, seamless, robust, cutting-edge, state-of-the-art, innovative, pivotal, instrumental, meticulous, comprehensive, actionable insights, data-driven decisions, transformative, empowered, facilitated, harnessed, delved, elevated, impactful, synergy, holistic, results-driven, proven track record, passionate, adept, detail-oriented, fast-paced.
- **Trailing -ing results** (", enabling…," ", ensuring…," ", driving…," ", resulting in…") on more than two bullets per page.
- **Filler adjective pairs:** "clean, reliable data," "structured, reusable datasets."
- **"via" more than twice per page.** Use "with," "using" or "by."
- **Em dashes inside bullets, and semicolons in more than two bullets.**
- **JD soft phrases pasted into bullets** ("cross-functional collaboration," "translate business requirements," "stakeholder management"). Show them with concrete facts instead. A soft phrase may appear at most once, in Skills or Summary, and only when it is a top requirement.
- **Self-praise in the Summary** ("passionate," "proven," "highly motivated," "seeking to leverage").

**Plain wording never changes a fact.** When a line is simplified, every number, tool and claim stays the same. Don't add a detail (who used it, what it replaced) unless the resume, Evidence Bank or user supplies it.

### Unique Opening Verbs

Every bullet on the final page, across Experience and Projects, starts with a different word. No verb opens more than one bullet, "Built" and "Designed" included. A recruiter skimming the left edge of the page should see a different action on every line.

- **Whole page, not just changed lines.** If a rewrite would repeat a verb an untouched bullet already uses, pick another. If the attached resume itself repeats an opening verb, fix it in this run by changing only the first word (plus "a"/"an" if the grammar needs it). This is the one change to an original line that the JD doesn't have to call for; show it in section 4 or 5 like any other change.
- **Change the bullet that has room.** A new verb changes the line length. Of the two bullets sharing a verb, change the one whose last line has the most space left: a two-line bullet with a short second line, or a one-line bullet that ends well before the margin. A longer verb there costs nothing. If neither has room, use a replacement of the same length or shorter ("Built" → "Coded", "Made", "Wired"). Line-for-line parity (One-Page Layout Rules) beats a stronger verb; never let a verb swap push a bullet onto an extra line.
- **The verb must be literally true.** It describes the same action as before (built → delivered, launched, coded, set up is fine; built → led or owned is not, unless the sources say so). The Priority 3 team-project rules still apply: "Built", "Implemented" and "Designed" only for work under "My part".
- **No stock words as replacements.** "Streamlined", "Spearheaded", "Leveraged", "Utilized", "Facilitated" and the rest of the stock list are out, even as a way to avoid a repeat.
- **Spare verbs to draw from:** Wrote, Set up, Shipped, Delivered, Launched, Coded, Created, Implemented, Engineered, Developed, Modeled, Merged, Joined, Streamed, Moved, Replaced, Migrated, Cut, Reduced, Raised, Added, Fixed, Ran, Tuned, Automated, Deployed, Partnered, Blocked, Transformed, Resolved, Handled, Scheduled, Validated, Profiled, Indexed, Partitioned, Orchestrated (only when literal).

**Check:** write every bullet on the final page (Experience and Projects; no headline, Summary or bullet character), one per line, to `bullets.txt`, then run:

`python3 -c "import sys,collections as c;n=c.Counter(l.split()[0].lower() for l in open(sys.argv[1],encoding='utf-8') if l.strip());d={v:k for v,k in n.items() if k>1};print(d or 'opening verbs: all unique')" bullets.txt`

It must print `opening verbs: all unique`. (`ai_tells.py` only flags a verb used three or more times, so it misses pairs; this check is the one that counts.) After any verb swap, re-run `check_resume.py` to confirm the line positions didn't move.

### AI-wording check

Before producing the output, write the headline, Summary and every bullet of the tailored resume to a text file, one per line, and run:

`python3 scripts/ai_tells.py lines.txt` (the script is in this skill's folder)

Targets: no stock words (unless one is a literal technical term); "insight" and "stakeholder" at most once each; "via" at most twice; trailing -ing clauses on at most two lines; no filler adjective pairs; no em dashes; semicolons on at most two lines; every bullet's first word used only once on the page (run the Unique Opening Verbs check above, since the script only catches a verb used three or more times).

Fix every line you wrote that misses a target. For lines from the original resume that you did not change, report the misses in section 10 instead of rewriting them, so the user can fix them once in their base resume. The exception is a repeated opening verb, which is always fixed in the file (Unique Opening Verbs).

### Resume check

After building the .docx, run:

`python3 scripts/check_resume.py <attached resume> <tailored .docx> --bank evidence_bank.md` (paths to this skill's folder)

It checks three things and exits non-zero if any needs a look:

1. **Facts:** every number, and the noun it counts, plus every tool-like term in the tailored file, must appear in the attached resume or the Evidence Bank. "40+ engineers" is flagged when the sources only say "20+ engineers", even if a 40 appears elsewhere.
2. **Layout:** line-by-line page and height comparison with the original (only when the original is a .docx).
3. **Links:** each hyperlink, the line it sits on, and the Project Library project that owns its URL.

For every flag: back it with a source, move it to Confirm Before Sending and take it out of the file, or fix the layout or link. A flag can be a false alarm (a JD term the candidate truly has on file under a different spelling); say so in section 10. Re-run until the only flags left are explained false alarms.

---

## Guardrails: Non-Negotiable

- **Never change the candidate's actual job title** in the Experience section to match the target role. Employment titles may be checked during background verification. Use the professional headline to communicate the connection instead.

- **Never add skills, tools, responsibilities, metrics, or experience the candidate does not have.**

- If a top requirement is missing, mark it as ❌ and flag it to the user. Do not insert it into the resume.

- Skills learned through tutorials or self-study may appear in the Skills section only if the candidate can confidently explain and demonstrate them in an interview.

- When possible, recommend supporting self-taught skills with a genuine project.

- Do not present tutorial-only exposure as professional experience.

- Do not invent or estimate:
  - Metrics
  - Percentages
  - Data volumes
  - Cost savings
  - Time savings
  - Accuracy results
  - Team sizes
  - User counts
  - Performance improvements
  - Business outcomes

- Preserve the candidate's original facts, scope, and level of responsibility.

- Keep ATS-safe formatting:
  - Standard section headings
  - No tables
  - No columns
  - No text boxes
  - No graphics
  - No icons used as essential information
  - No important information inside headers or footers
  - Simple, readable fonts
  - Consistent dates and formatting

- Keep the wording natural and human: follow Plain, Human Wording and pass the AI-wording check.

- Every bullet starts with a different word: follow Unique Opening Verbs.

- Keep the one-page footprint: follow the One-Page Layout Rules.

- Do not optimize for ATS keywords at the expense of recruiter readability.

- Every important keyword should connect to evidence whenever possible.

- The final resume must be defensible in an interview.

- Industry translation must describe concepts the candidate actually worked with; never imply employment in an industry the candidate has not worked in.

- Derived metrics must be marked for confirmation and excluded from the final resume until confirmed.

- Facts from the Evidence Bank must be used exactly as written; do not inflate their scope during tailoring.

---

## Final Quality Check

Before providing the tailored content, verify:

1. The target job title is accurate.
2. The top 5–8 requirements were correctly identified.
3. Every added keyword is supported by the candidate's background.
4. Important keywords are distributed naturally across relevant sections.
5. Keywords are not concentrated only in the Skills section.
6. Experience and project bullets contain evidence, not just keywords.
7. Original facts, metrics, tools, and scope were preserved.
8. No unsupported claims were introduced.
9. The most relevant content appears first.
10. Low-relevance or repetitive content was reworded within its lines, moved down, or listed for removal in section 7.
11. The Summary, headline, Skills, Experience, and Projects sections tell one consistent story.
12. Dates, punctuation, capitalization, tense, and bullet formatting are consistent.
13. Technology names are written correctly.
14. The content sounds natural rather than AI-generated.
15. The resume remains ATS-safe and appropriate in length.
16. Industry vocabulary is used only where the underlying work matches.
17. No derived or unconfirmed numbers appear in the .docx.
18. Every line written in this run passes the AI-wording check targets, and `check_resume.py` passes or every flag left is explained in section 10.
19. JD soft phrases are shown with concrete facts, not pasted into bullets.
20. Same sections, bullet counts and line counts as the attached resume; no spacing, margin or font changes.
21. Every metric, named project and named system in the Summary and headline matches a bullet on the final page. Re-run this check after any project swap.
22. Every project on the final page carries its own GitHub link from the Project Library, formatted like the attached resume's links; no project points at another project's repo.
23. Every bullet on the page starts with a different word (the Unique Opening Verbs check prints "all unique"), no replacement verb is on the stock list, and every verb swap kept the bullet's line count.

---

## Output Format

The run produces three things:

- **The tailored resume** (`Darpan_Jiyani_Resume_<Company>_<Role>.docx`, section 12).
- **The full report** (`<Company>_<Role>_report.md`): sections 1–11 below, in order. Send it with the .docx.
- **A short chat reply.** The user reads this first, so keep it to about 15 lines:
  - One line naming the role and the file.
  - **Fit:** the Apply recommendation from section 8 and the main reason.
  - **Coverage:** before → after from section 9.
  - **Projects:** which projects are on the page, and each swap in one line ("Transportation Lakehouse replaces Football Analytics: shows streaming and CDC").
  - **Headline and Summary:** whether a headline was added and what it replaced.
  - **Confirm Before Sending:** the full list from section 11, since nothing there can go out unchecked.
  - One line pointing to the report for the keyword table, before/after bullets and gap triage.

  Do not paste the report's tables or before/after bullets into chat.

### Report sections

### 1. Title Check

Show:

- Candidate's current or most recent title
- Target title from the JD
- Whether the titles match or nearly match
- Whether a professional headline is needed
- Recommended headline, if needed

### 2. Keyword Match Table

Use these columns:

| Requirement | Exact JD Phrase | Status | Current Evidence | Where It Was Added or Strengthened |
|---|---|---|---|---|

Use:

- ✅ Already shown
- ⚠️ Present but worded differently
- ❌ Missing

Do not claim a missing requirement was added unless the candidate provided supporting experience.

### 3. Updated Skills Section

Provide a complete replacement Skills section with:

- Logical categories
- JD-relevant skills listed first
- Exact JD terminology where truthful
- Irrelevant skills swapped out or moved down, same number of lines
- No unsupported skills

### 4. Rewritten Experience Bullets

For every changed bullet, show:

**Before:**
Original bullet

**After:**
Tailored bullet

**Reason:**
One sentence explaining which JD requirement was emphasized and why the revision is stronger. For an opening-verb-only change, say which bullet shared the verb.

**Lines:** before → after (must match, e.g., 1 → 1)

### 5. Rewritten Project Bullets

For every changed project bullet, show:

**Before:**
Original project bullet

**After:**
Tailored project bullet

**Reason:**
One sentence explaining how the project demonstrates a target requirement. For an opening-verb-only change, say which bullet shared the verb.

If no project changes are needed, explicitly state that the existing projects already support the target role or that no project provides relevant evidence.

Before the bullets, show a **Project Selection table** covering every candidate project (resume and Project Library):

| Project | Source (Resume / Library) | Requirements it shows | Score (re-score after earlier picks) | Decision (Keep / Add / Swap out / Not used / Not used (filtered) / Skipped (unconfirmed Status)) |
|---|---|---|---|---|

For each swap, add one line: "[Library project] replaces [resume project] because ..."

Then list the link on each final project: "[Project] → [URL] (kept / swapped in / changed / removed, no confirmed link)".

### 6. New Tailored Summary

Provide a concise 2–3 line Summary aligned with:

- Target title
- Top JD requirements
- Candidate's strongest supported achievement or value

### 7. Relevance and Removal Recommendations

List:

- Content to keep
- Content to move higher
- Content to move lower
- Content to shorten
- Content to remove

Provide a short reason for each recommendation. Say which of these were applied in the file (only moves and same-line rewording) and which are recommendations only (shortening and removal are always recommendations; the file keeps every bullet).

Do not remove content only because it lacks an exact JD keyword. Consider transferable value and measurable impact.

### 8. Gap Triage

Classify every ❌ requirement into exactly one category:

| Gap | Required / Preferred | Category | Why | Action |
|---|---|---|---|---|

**Categories:**

- 🟢 **Fix with wording:** The evidence exists in the resume or Evidence Bank but is not visible. Fix it in this tailoring pass.
- 🟡 **Fix with a project:** The skill can be learned and demonstrated within weeks. First check the Project Library for an "In progress" or "Planned" project that would cover it and recommend finishing that one. Only if none fits, recommend one new, specific, scoped project with suggested data, method, and metric to report.
- 🔴 **Hard gap:** It requires years of direct industry experience, a license, a certification, or a degree the candidate does not have. Suggest addressing it in a cover letter or interview, or deprioritizing the role.

Do not suggest claiming the skill before the candidate has learned or applied it.

After the table, give a one-line **Apply recommendation**:

- **Strong fit:** Apply now
- **Reasonable fit:** Apply now and address gaps in the cover letter
- **Stretch:** Apply only after completing the recommended project

### 9. Estimated Keyword Coverage

Show:

- Before tailoring: requirements clearly covered out of the top requirements
- After tailoring: requirements clearly covered out of the top requirements

Example:

**Before: 4/8 clearly covered**
**After: 7/8 clearly covered**
**Remaining gaps that need a project: 1**

This is a keyword and evidence coverage estimate, not a guaranteed ATS score, interview probability, or hiring outcome.

### 10. Final Consistency Check

Briefly confirm:

- No experience was invented
- No official job title was changed
- No unsupported skill was added
- Keywords were distributed naturally
- Experience and Projects provide supporting evidence
- Formatting remains ATS-safe
- AI-wording check result, plus any misses in original lines that were left unchanged
- Unique Opening Verbs check result ("all unique"), plus any opening verbs changed in original lines and why
- Resume check (`check_resume.py`) result for facts, layout and links, with any remaining flag explained
- Summary-to-evidence check: each metric or named project in the Summary, and the bullet that backs it

### 11. Confirm Before Sending

List every derived number, missing metric, or unclear fact that needs the user's confirmation. None of these items may appear in the .docx until confirmed.

### 12. Tailored Resume File

Generate the tailored resume as an ATS-safe .docx file named `Darpan_Jiyani_Resume_<Company>_<Role>.docx` (short company and role names, underscores, no spaces). For a PDF, tell the user to export it from Word: LibreOffice-made PDFs often lay out taller than Word and can spill onto a second page.