"""Check a tailored resume against its sources before sending it.

Usage:
    python3 check_resume.py ORIGINAL TAILORED.docx --bank evidence_bank.md [--skip-layout]

ORIGINAL is the resume the user attached (.docx, .pdf, .txt or .md).
TAILORED is the .docx this run produced.

Three checks, each printed as PASS or CHECK:
  1. Facts:  every number and every technical-looking term in the tailored
             resume must appear in the original resume or the Evidence Bank.
  2. Layout: both .docx files are rendered with the same converter and every
             line's page and vertical position is compared (needs LibreOffice
             and pdftotext; only when ORIGINAL is a .docx).
  3. Links:  every hyperlink in the tailored resume is listed with the line it
             sits on, and matched to the Project Library entry that owns its URL.

Exit code 0 when everything passes, 1 when something needs a look.
A CHECK is not always an error (a number from the JD's job title, a JD term the
candidate truly has); the person running the skill decides, but must decide.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

# Lowercase technical terms that the capitalisation test below would miss.
LOWER_TECH = {
    "dbt", "pandas", "numpy", "pytest", "pyspark", "kafka", "spark", "airflow",
    "docker", "kubernetes", "terraform", "scikit-learn", "sklearn", "tensorflow",
    "pytorch", "keras", "mlflow", "langchain", "faiss", "redis", "postgres",
    "postgresql", "mysql", "mongodb", "snowflake", "databricks", "tableau",
    "looker", "git", "github", "jenkins", "helm", "fastapi", "flask", "django",
    "streamlit", "jinja", "dax", "excel", "vba", "hadoop", "hive", "presto",
    "trino", "flink", "beam", "dagster", "prefect", "bigquery", "redshift",
    "athena", "glue", "lambda", "emr", "s3", "gcs", "etl", "elt", "cdc", "scd",
    "api", "apis", "rest", "graphql", "nosql", "sql", "llm", "llms", "rag",
}
# Capitalised words that are ordinary English, months or resume headings.
COMMON_CAPS = {
    "a", "an", "the", "and", "or", "for", "with", "to", "of", "in", "on", "by",
    "at", "as", "from", "into", "per", "via", "using", "built", "i",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "jan", "feb", "mar", "apr",
    "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "present",
    "summary", "skills", "experience", "projects", "education", "github",
    "linkedin", "languages", "tools", "certifications", "coursework",
}


# ---------------------------------------------------------------- text loading

def docx_paragraphs(path):
    """Paragraph texts of a .docx, in order, including text inside hyperlinks."""
    from xml.etree import ElementTree as ET
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    paras = []
    for p in root.iter(W + "p"):
        parts = []
        for node in p.iter():
            if node.tag == W + "t" and node.text:
                parts.append(node.text)
            elif node.tag == W + "tab":
                parts.append(" ")
        paras.append("".join(parts))
    return paras


def load_text(path):
    path = Path(path)
    suf = path.suffix.lower()
    if suf == ".docx":
        return "\n".join(docx_paragraphs(path))
    if suf == ".pdf":
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                             capture_output=True, text=True)
        return out.stdout
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------- 1. facts

NUM_RE = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*([%+KkMmBbx×]*)")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z-]*")
FILLER = {"to", "of", "and", "the", "a", "an", "in", "on", "for", "per", "across", "with",
          "from", "over", "under", "about", "than", "more", "less", "or", "by", "at"}


def norm_num(s):
    s = s.replace(",", "")
    if "." in s:
        s = s.rstrip("0").rstrip(".") or "0"
    return s


def number_mentions(text):
    """[(number, noun after it or '')]; the noun says what the number counts."""
    out = []
    for m in NUM_RE.finditer(text):
        after = text[m.end():m.end() + 60]
        noun = ""
        for w in WORD_RE.findall(after)[:3]:
            if w.lower() not in FILLER:
                noun = w.lower()
                break
        out.append((norm_num(m.group(1)), noun))
    return out


def number_backed(num, noun, source_mentions, source_nums):
    """Backed when the same number appears in a source next to the same kind of noun."""
    if num not in source_nums:
        return False
    if not noun or len(noun) < 3:
        return True
    stem = noun[:4] if len(noun) >= 4 else noun
    return any(n == num and (not sn or sn.startswith(stem[:3]) or noun.startswith(sn[:3]))
               for n, sn in source_mentions)


TERM_RE = re.compile(r"[A-Za-z][A-Za-z0-9+#./-]*[A-Za-z0-9+#]|[A-Za-z]")


def tech_terms(line):
    """Words in a line that look like tools, systems or acronyms."""
    found = set()
    toks = list(TERM_RE.finditer(line))
    for i, m in enumerate(toks):
        w = m.group(0).strip(".-/")
        lw = w.lower()
        if not w or lw in COMMON_CAPS:
            continue
        if lw in LOWER_TECH:
            found.add(w)
            continue
        first_word = i == 0 or line[:m.start()].rstrip().endswith((":", "|", "•", "-"))
        mixed = any(c.isupper() for c in w[1:])           # PySpark, AWS, dbtCloud
        has_digit = any(c.isdigit() for c in w)            # S3, GPT-4, EfficientNetV2
        capital = w[0].isupper() and not first_word        # Snowflake mid-sentence
        if mixed or has_digit or capital:
            found.add(w)
    return found


def check_facts(orig_text, tailored_lines, bank_text):
    source = orig_text + "\n" + bank_text
    src_mentions = number_mentions(source)
    src_nums = {n for n, _ in src_mentions}
    src_lower = source.lower()
    issues = []
    for line in tailored_lines:
        if not line.strip():
            continue
        bad_nums = sorted({f"{n} {noun}".strip() for n, noun in number_mentions(line)
                           if not number_backed(n, noun, src_mentions, src_nums)})
        bad_terms = sorted(t for t in tech_terms(line)
                           if t.lower() not in src_lower)
        if bad_nums or bad_terms:
            issues.append((line, bad_nums, bad_terms))
    print("\n== 1. Facts ==")
    if not issues:
        print("PASS: every number and technical term is found in the resume or Evidence Bank.")
        return True
    print("CHECK: these lines contain numbers or terms not found in the resume or Evidence Bank.")
    print("Each one must be backed by a source, moved to Confirm Before Sending, or removed.")
    for line, n, t in issues:
        print(f"- {line[:110]}")
        if n:
            print(f"    numbers: {', '.join(n)}")
        if t:
            print(f"    terms:   {', '.join(t)}")
    return False


# ---------------------------------------------------------------- 2. layout

def to_pdf(docx, outdir):
    profile = tempfile.mkdtemp(prefix="lo_profile_")
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    cmd = ["soffice", f"-env:UserInstallation={Path(profile).as_uri()}",
           "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(docx)]
    subprocess.run(cmd, env=env, capture_output=True, timeout=180)
    pdf = Path(outdir) / (Path(docx).stem + ".pdf")
    if not pdf.exists():
        # Fall back to the docx skill's wrapper, which handles sandboxed sockets.
        for root in ("/mnt/skills/public/docx/scripts", "/mnt/skills/docx/scripts"):
            if Path(root, "office", "soffice.py").exists():
                sys.path.insert(0, root)
                from office.soffice import run_soffice  # noqa: E402
                run_soffice(["--headless", "--convert-to", "pdf", "--outdir",
                             str(outdir), str(docx)], capture_output=True, timeout=180)
                break
    shutil.rmtree(profile, ignore_errors=True)
    return pdf if pdf.exists() else None


def pdf_lines(pdf):
    """(page, yMin, text) for every text line, using pdftotext -bbox-layout."""
    out = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"],
                         capture_output=True, text=True).stdout
    lines, page = [], 0
    for tag in re.finditer(r"<page |<line xMin=\"[\d.]+\" yMin=\"([\d.]+)\"[^>]*>(.*?)</line>",
                           out, re.S):
        if tag.group(0).startswith("<page"):
            page += 1
            continue
        words = re.findall(r">([^<]*)</word>", tag.group(2))
        lines.append((page, float(tag.group(1)), " ".join(words)))
    return lines, page


def check_layout(orig_docx, tailored_docx):
    print("\n== 2. Layout ==")
    if not (shutil.which("soffice") and shutil.which("pdftotext")):
        print("CHECK: LibreOffice or pdftotext is not installed, so layout was not compared.")
        return False
    tmp = Path(tempfile.mkdtemp(prefix="layout_"))
    a_dir, b_dir = tmp / "orig", tmp / "tailored"
    a_dir.mkdir()
    b_dir.mkdir()
    a_pdf, b_pdf = to_pdf(orig_docx, a_dir), to_pdf(tailored_docx, b_dir)
    if not a_pdf or not b_pdf:
        print("CHECK: could not render one of the files to PDF.")
        return False
    a, a_pages = pdf_lines(a_pdf)
    b, b_pages = pdf_lines(b_pdf)
    print(f"Pages (same converter, both files): original {a_pages}, tailored {b_pages}")
    print(f"Text lines: original {len(a)}, tailored {len(b)}")
    if a_pages != 1:
        print("Note: the original also renders as more than one page here. That is the "
              "converter, not the resume; only the comparison below matters.")
    ok = a_pages == b_pages and len(a) == len(b)
    first_diff = None
    for i, (la, lb) in enumerate(zip(a, b)):
        if la[0] != lb[0] or abs(la[1] - lb[1]) > 1.0:
            first_diff = (i, la, lb)
            break
    if first_diff:
        ok = False
        i, la, lb = first_diff
        print(f"First line that moved (line {i + 1}):")
        print(f"    original: page {la[0]}, y={la[1]:.1f}  {la[2][:80]}")
        print(f"    tailored: page {lb[0]}, y={lb[1]:.1f}  {lb[2][:80]}")
        print("    The element just above this line grew, shrank or lost spacing; fix it.")
    elif len(a) != len(b):
        longer = a if len(a) > len(b) else b
        extra = longer[min(len(a), len(b))]
        print(f"Lines match until the end, then {'the original' if longer is a else 'the tailored file'} "
              f"has extra lines, starting: {extra[2][:80]}")
    if ok:
        print("PASS: every line sits on the same page at the same height as in the original.")
    else:
        print("CHECK: the footprint changed; see above.")
    shutil.rmtree(tmp, ignore_errors=True)
    return ok


# ---------------------------------------------------------------- 3. links

def bank_projects(bank_text):
    """{url: project title} from the Project Library's Link fields."""
    projects = {}
    title = None
    for line in bank_text.splitlines():
        m = re.match(r"###\s+\d+\.\s+(.*)", line)
        if m:
            title = m.group(1).strip()
            continue
        m = re.match(r"\s*-\s+\*\*Link:\*\*\s+(\S+)", line)
        if m and title and m.group(1).startswith("http"):
            projects[m.group(1).rstrip("/").lower()] = title
    return projects


def docx_links(path):
    """[(paragraph text, display text, target)] for every hyperlink."""
    from xml.etree import ElementTree as ET
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        rels_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    rels = {r.get("Id"): r.get("Target") for r in rels_root}
    out = []
    for p in root.iter(W + "p"):
        ptext = "".join(t.text or "" for t in p.iter(W + "t"))
        for h in p.iter(W + "hyperlink"):
            rid = h.get(R + "id")
            if not rid:
                continue
            disp = "".join(t.text or "" for t in h.iter(W + "t"))
            out.append((ptext, disp, rels.get(rid, "(missing relationship)")))
        # Field-code hyperlinks: HYPERLINK "url"
        instr = "".join(t.text or "" for t in p.iter(W + "instrText"))
        for url in re.findall(r'HYPERLINK\s+"([^"]+)"', instr):
            out.append((ptext, "(field link)", url))
    return out


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def check_links(tailored_docx, bank_text):
    print("\n== 3. Links ==")
    projects = bank_projects(bank_text)
    links = docx_links(tailored_docx)
    if not links:
        print("No hyperlinks found in the tailored resume.")
        return True
    ok = True
    seen = {}
    for ptext, disp, target in links:
        key = target.rstrip("/").lower()
        owner = projects.get(key)
        line = f"- {ptext[:70]!r} | shows {disp!r} -> {target}"
        if "github.com" in key and key.count("/") >= 4:
            if not owner:
                line += "\n    CHECK: this repo is not any project's Link in the Project Library."
                ok = False
            else:
                # Does the line the link sits on look like the owning project?
                scores = {t: len(words(t) & words(ptext)) for t in projects.values()}
                best = max(scores, key=scores.get)
                line += f"\n    belongs to: {owner}"
                if scores[best] > scores[owner]:
                    line += f"\n    CHECK: this line looks more like '{best}'. Wrong repo?"
                    ok = False
            if key in seen:
                line += f"\n    CHECK: the same repo is also linked on {seen[key]!r}."
                ok = False
            seen[key] = ptext[:50]
        print(line)
    print("PASS: every project link points at its own repo." if ok
          else "CHECK: fix the links flagged above.")
    return ok


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("original")
    ap.add_argument("tailored")
    ap.add_argument("--bank", required=True, help="path to evidence_bank.md")
    ap.add_argument("--skip-layout", action="store_true")
    args = ap.parse_args()

    bank = Path(args.bank).read_text(encoding="utf-8")
    orig_text = load_text(args.original)
    tailored_lines = docx_paragraphs(args.tailored)

    results = [check_facts(orig_text, tailored_lines, bank)]
    if args.skip_layout:
        print("\n== 2. Layout ==\nSkipped.")
    elif Path(args.original).suffix.lower() != ".docx":
        print("\n== 2. Layout ==\nSkipped: the original is not a .docx, so there is no "
              "footprint to match. Say the formatting is approximated.")
    else:
        results.append(check_layout(args.original, args.tailored))
    results.append(check_links(args.tailored, bank))

    print("\nRESULT:", "PASS" if all(results) else "CHECK (see above)")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
