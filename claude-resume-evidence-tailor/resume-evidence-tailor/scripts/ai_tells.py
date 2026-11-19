import re, sys
from collections import Counter

# Usage: python3 ai_tells.py lines.txt  (the summary plus every bullet, one per line)
lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
text = "\n".join(lines)

stock = [r"leverag\w*", r"utiliz\w*", r"spearhead\w*", r"foster\w*", r"champion\w*",
         r"streamlin\w*", r"seamless\w*", r"robust", r"cutting-edge", r"state-of-the-art",
         r"innovative", r"pivotal", r"instrumental", r"meticulous\w*", r"comprehensive",
         r"actionable", r"data-driven", r"transformative", r"empower\w*", r"facilitat\w*",
         r"harness(?:ed|ing)", r"delv\w*", r"elevat\w*", r"impactful", r"synerg\w*",
         r"holistic", r"results-driven", r"track record", r"passionate", r"adept",
         r"detail-oriented", r"fast-paced", r"highly motivated"]
nouns = r"(?!engineering\b|including\b|string\b|testing\b|monitoring\b|reporting\b|processing\b|streaming\b|modeling\b|computing\b|caching\b|partitioning\b)"

report = {
    "stock words (target 0)": {m.group(0).lower(): 1 for p in stock
                               for m in re.finditer(r"\b" + p + r"\b", text, re.I)},
    "insights/stakeholders (target <=1 each)": Counter(
        w.lower().rstrip("s") for w in re.findall(r"\b(insights?|stakeholders?)\b", text, re.I)),
    "via (target <=2)": len(re.findall(r"\bvia\b", text, re.I)),
    "trailing -ing clauses (target <=2 lines)": [
        l[:60] for l in lines if re.search(r",\s+(?:and\s+)?" + nouns + r"\w+ing\b", l)],
    "filler adjective pairs (target 0)": re.findall(
        r"\b(?:clean|reliable|reusable|structured|trusted|scalable|robust|efficient|accurate|"
        r"consistent|high-quality|analysis-ready|queryable|actionable),\s+\w+", text, re.I),
    "em dashes (target 0)": text.count("—"),
    "lines with semicolons (target <=2)": sum(";" in l for l in lines),
    "first verb used 3+ times (target none)": {
        v: n for v, n in Counter(l.split()[0].lower() for l in lines).items() if n > 2},
}
for k, v in report.items():
    print(f"{k}: {v}")
