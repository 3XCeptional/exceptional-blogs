#!/usr/bin/env python3
"""Daily CVE blog pipeline.

Run by launchd at 09:00 / 15:00 / 18:00. Each firing:
  1. Skips silently if a CVE was already posted today (dbcli.posted_today) —
     this is what makes the 3-times-a-day schedule safe: whichever window
     the machine happens to be awake for does the post, the other two are
     no-ops.
  2. Pulls recently published CVEs from the NVD API, picks the
     highest-severity one not already in the tracker DB.
  3. Generates the article body via a headless, tool-less `claude -p` call.
  4. Writes the .mdx file, runs `npm run build` as a compile gate, and only
     then commits + pushes to main (which triggers the GH Pages deploy).
  5. Records the CVE in the tracker DB so it is never posted again.

No new third-party dependencies: stdlib only (urllib, sqlite3 via dbcli).
"""
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
import dbcli  # noqa: E402

LOG_PATH = REPO_ROOT / "scripts" / "data" / "daily_cve_post.log"
ARTICLES_DIR = REPO_ROOT / "src" / "content" / "articles"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
LOOKBACK_DAYS = 5
MIN_CVSS = 7.0
CLAUDE_TIMEOUT_SEC = 600

GENERIC_HERO = {
    "image": "assets/dns-rce-hero.png",
    "imageAlt": "Abstract illustration of interconnected server nodes representing a software vulnerability",
    "imageCaption": "A conceptual illustration of a security vulnerability in software.",
}


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def fetch_candidates() -> list[dict]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=LOOKBACK_DAYS)
    q_start = urllib.parse.quote(start.isoformat(timespec="milliseconds"))
    q_end = urllib.parse.quote(end.isoformat(timespec="milliseconds"))
    url = f"{NVD_API}?pubStartDate={q_start}&pubEndDate={q_end}&resultsPerPage=200"
    req = urllib.request.Request(url, headers={"User-Agent": "exceptional-blogs-cve-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    candidates = []
    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        cve_id = cve.get("id")
        if not cve_id or dbcli.exists(cve_id):
            continue
        desc = next(
            (d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"), None
        )
        if not desc or "** REJECT **" in desc or "** DISPUTED **" in desc:
            continue
        metrics = cve.get("metrics", {})
        cvss_data = None
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if metrics.get(key):
                cvss_data = metrics[key][0]["cvssData"]
                break
        if not cvss_data:
            continue
        score = cvss_data.get("baseScore", 0)
        if score < MIN_CVSS:
            continue
        refs = [r["url"] for r in cve.get("references", [])[:3]]
        candidates.append({
            "cve_id": cve_id,
            "description": desc,
            "cvss": score,
            "severity": cvss_data.get("baseSeverity", "UNKNOWN"),
            "vector": cvss_data.get("vectorString", ""),
            "published": cve.get("published", ""),
            "references": refs,
        })

    candidates.sort(key=lambda c: c["cvss"], reverse=True)
    return candidates


def build_prompt(c: dict) -> str:
    return f"""You are writing a technical blog post explaining a newly published CVE for a public security blog read by developers, students, and CTF/HTB players who want to actually understand and test the bug.

Known facts (starting point only, go deeper):
CVE ID: {c['cve_id']}
Description: {c['description']}
CVSS score: {c['cvss']} ({c['severity']})
CVSS vector: {c['vector']}
Published: {c['published']}
References: {', '.join(c['references']) or 'none provided'}

You have WebFetch and WebSearch. Use them before writing:
- Fetch every URL in References above.
- Search for the vendor advisory, the researcher's own write-up, any GitHub issue/PR/commit that fixed it, and any public PoC or exploit analysis (GHSA, Rapid7, watchTowr, ProjectDiscovery, etc).
- Cross-check the technical mechanism across at least two independent sources when possible. If sources disagree, say so rather than picking one silently.
- Only state technical details you actually found in a source. Never invent a root cause, an offset, a payload, or a version number you have no evidence for.

Output ONLY a single JSON object (no markdown code fences, no commentary before or after) with exactly these keys:
- "title": specific human-readable headline, not just the CVE ID
- "dek": 1-2 sentence subtitle explaining why this vulnerability matters, professional tone
- "excerpt": summary under 200 characters for a card preview
- "read_time": estimate like "6 min read", based on your body length
- "body": the full article body as Markdown (no top-level H1, no frontmatter), 900-1400 words, professional prose, no em dashes, no filler. Use "##" headings. Structure:
  1. What happened - plain-language summary of the bug and why it was disclosed.
  2. Affected software and versions.
  3. Technical root cause - the actual bug class and mechanism (e.g. missing auth check, deserialization gadget, path traversal, race condition), explained precisely enough that a reader understands *why* it works, sourced from what you found.
  4. Exploitability and attack vector - what an attacker needs (network position, auth, user interaction) and what they gain.
  5. "## Reproduce it safely" - a reader-facing walkthrough for testing this **only against a system you own or an authorized lab (a local VM, a Docker container you built, or a HackTheBox/TryHackMe box that specifically hosts this CVE)**. State that framing explicitly at the top of the section. If you found a real public PoC, walk through its actual steps (setup, the request/payload/command, expected result) citing where it came from. If no public PoC or reliable reproduction path exists, say so plainly instead of fabricating one, and instead give a concrete verification method (a version check, a vulnerable-config check, a detection signature, or a relevant existing HTB/THM box that teaches the same bug class) so the reader still has something real to do.
  6. Real-world impact and remediation - patched version, config mitigation, and detection guidance.
  At the end of the body, add a "## Sources" markdown line listing the URLs you actually used (references + anything found via search)."""


def call_claude(prompt: str) -> dict:
    result = subprocess.run(
        [
            "claude", "-p", prompt,
            "--output-format", "text",
            "--allowedTools", "WebFetch,WebSearch",
            "--disallowedTools", "Bash,Edit,Write,Read,Grep,Glob,Agent,NotebookEdit",
        ],
        cwd=str(REPO_ROOT / "scripts" / "data"),
        capture_output=True, text=True, timeout=CLAUDE_TIMEOUT_SEC,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed: {result.stderr.strip()[:500]}")
    text = result.stdout.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"claude -p returned invalid JSON: {e}") from e


def write_article(c: dict, gen: dict, slug: str, today: str) -> Path:
    fm = {
        "title": gen["title"],
        "dek": gen["dek"],
        "date": today,
        "readTime": gen["read_time"],
        "kicker": "Security · CVE Analysis",
        **GENERIC_HERO,
        "excerpt": gen["excerpt"],
        "category": "cve",
        "categoryLabel": "CVE Analysis",
    }
    fm_lines = ",\n".join(f"  {k}: {json.dumps(v)}" for k, v in fm.items())
    content = f"export const frontmatter = {{\n{fm_lines},\n}};\n\n{gen['body']}\n"
    path = ARTICLES_DIR / f"{slug}.mdx"
    path.write_text(content)
    return path


def build_check() -> tuple[bool, str]:
    result = subprocess.run(
        ["npm", "run", "build"], cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=300
    )
    return result.returncode == 0, (result.stdout + result.stderr)[-2000:]


def git_publish(path: Path, cve_id: str, title: str) -> None:
    rel = str(path.relative_to(REPO_ROOT))
    subprocess.run(["git", "add", rel], cwd=str(REPO_ROOT), check=True)
    message = (
        f"Add daily CVE post: {cve_id} - {title}\n\n"
        f"Automated daily CVE pipeline (scripts/daily_cve_post.py).\n\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )
    subprocess.run(["git", "commit", "-m", message], cwd=str(REPO_ROOT), check=True)
    subprocess.run(["git", "push"], cwd=str(REPO_ROOT), check=True)


def main() -> int:
    if dbcli.posted_today():
        log("already posted today, skipping")
        return 0

    try:
        candidates = fetch_candidates()
    except Exception as e:
        log(f"NVD fetch failed: {e}")
        return 1

    if not candidates:
        log("no unposted CVE candidates found today")
        return 0

    chosen = candidates[0]
    today = date.today().isoformat()
    slug = f"{today}-{chosen['cve_id'].lower()}"

    prompt = build_prompt(chosen)
    gen = None
    for attempt in range(2):
        try:
            gen = call_claude(prompt)
            break
        except Exception as e:
            log(f"content generation attempt {attempt + 1} failed for {chosen['cve_id']}: {e}")
    if gen is None:
        return 1

    path = write_article(chosen, gen, slug, today)

    ok, output = build_check()
    if not ok:
        log(f"build check FAILED for {chosen['cve_id']}, reverting: {output}")
        path.unlink(missing_ok=True)
        return 1

    try:
        git_publish(path, chosen["cve_id"], gen["title"])
    except subprocess.CalledProcessError as e:
        log(f"git publish failed for {chosen['cve_id']}: {e}")
        return 1

    dbcli.add_cve(
        cve_id=chosen["cve_id"], title=gen["title"], severity=chosen["severity"],
        cvss=chosen["cvss"], published=chosen["published"], slug=slug, blog_date=today,
    )
    log(f"posted {chosen['cve_id']} ({chosen['cvss']} {chosen['severity']}) as {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
