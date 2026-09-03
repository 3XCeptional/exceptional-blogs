#!/usr/bin/env python3
"""CRUD CLI for the CVE tracker DB (scripts/data/cve_tracker.db).

Tracks which CVEs have already been turned into a blog post so the daily
pipeline (scripts/daily_cve_post.py) never posts the same CVE twice.

Usage:
    python3 dbcli.py init
    python3 dbcli.py add --cve-id CVE-2026-1234 --title "..." --severity CRITICAL --cvss 9.8 --published 2026-09-01 --slug 2026-09-03-cve-2026-1234
    python3 dbcli.py get --cve-id CVE-2026-1234
    python3 dbcli.py list [--status posted]
    python3 dbcli.py update --cve-id CVE-2026-1234 --set status=retracted --set slug=new-slug
    python3 dbcli.py delete --cve-id CVE-2026-1234
    python3 dbcli.py exists --cve-id CVE-2026-1234
    python3 dbcli.py today
"""
import argparse
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "scripts" / "data" / "cve_tracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS cves (
    cve_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    severity TEXT,
    cvss REAL,
    published TEXT,
    slug TEXT,
    blog_date TEXT,
    status TEXT NOT NULL DEFAULT 'posted',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

FIELDS = ["cve_id", "title", "severity", "cvss", "published", "slug", "blog_date", "status"]


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def init_db() -> None:
    connect().close()


def add_cve(cve_id: str, title: str, severity: str = None, cvss: float = None,
            published: str = None, slug: str = None, blog_date: str = None,
            status: str = "posted") -> None:
    blog_date = blog_date or date.today().isoformat()
    with connect() as conn:
        conn.execute(
            "INSERT INTO cves (cve_id, title, severity, cvss, published, slug, blog_date, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (cve_id, title, severity, cvss, published, slug, blog_date, status),
        )


def get_cve(cve_id: str) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute("SELECT * FROM cves WHERE cve_id = ?", (cve_id,)).fetchone()


def list_cves(status: str = None) -> list[sqlite3.Row]:
    with connect() as conn:
        if status:
            return conn.execute(
                "SELECT * FROM cves WHERE status = ? ORDER BY blog_date DESC", (status,)
            ).fetchall()
        return conn.execute("SELECT * FROM cves ORDER BY blog_date DESC").fetchall()


def update_cve(cve_id: str, **fields) -> bool:
    fields = {k: v for k, v in fields.items() if k in FIELDS and k != "cve_id"}
    if not fields:
        return False
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    with connect() as conn:
        cur = conn.execute(
            f"UPDATE cves SET {set_clause} WHERE cve_id = ?",
            (*fields.values(), cve_id),
        )
        return cur.rowcount > 0


def delete_cve(cve_id: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM cves WHERE cve_id = ?", (cve_id,))
        return cur.rowcount > 0


def exists(cve_id: str) -> bool:
    return get_cve(cve_id) is not None


def posted_today() -> sqlite3.Row | None:
    today = date.today().isoformat()
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM cves WHERE blog_date = ? AND status = 'posted' LIMIT 1", (today,)
        ).fetchone()


def _print_rows(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("(none)")
        return
    for r in rows:
        print(f"{r['cve_id']}  {r['severity'] or '-':8}  cvss={r['cvss'] or '-':4}  "
              f"blog_date={r['blog_date']}  status={r['status']}  slug={r['slug']}")
        print(f"    {r['title']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="CRUD CLI for the CVE tracker DB")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create the DB/table if missing")

    p_add = sub.add_parser("add", help="Insert a new CVE record")
    p_add.add_argument("--cve-id", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--severity")
    p_add.add_argument("--cvss", type=float)
    p_add.add_argument("--published")
    p_add.add_argument("--slug")
    p_add.add_argument("--blog-date")
    p_add.add_argument("--status", default="posted")

    p_get = sub.add_parser("get", help="Fetch one CVE record")
    p_get.add_argument("--cve-id", required=True)

    p_list = sub.add_parser("list", help="List CVE records")
    p_list.add_argument("--status")

    p_update = sub.add_parser("update", help="Update fields on a CVE record")
    p_update.add_argument("--cve-id", required=True)
    p_update.add_argument("--set", action="append", default=[], metavar="field=value",
                           help="Repeatable. e.g. --set status=retracted")

    p_delete = sub.add_parser("delete", help="Delete a CVE record")
    p_delete.add_argument("--cve-id", required=True)

    p_exists = sub.add_parser("exists", help="Exit 0 if the CVE is already tracked, else 1")
    p_exists.add_argument("--cve-id", required=True)

    sub.add_parser("today", help="Show the CVE posted today, if any")

    args = parser.parse_args()

    if args.command == "init":
        init_db()
        print(f"DB ready at {DB_PATH}")
        return 0

    if args.command == "add":
        add_cve(args.cve_id, args.title, args.severity, args.cvss, args.published,
                args.slug, args.blog_date, args.status)
        print(f"added {args.cve_id}")
        return 0

    if args.command == "get":
        row = get_cve(args.cve_id)
        if not row:
            print(f"not found: {args.cve_id}", file=sys.stderr)
            return 1
        _print_rows([row])
        return 0

    if args.command == "list":
        _print_rows(list_cves(args.status))
        return 0

    if args.command == "update":
        updates = {}
        for pair in args.set:
            if "=" not in pair:
                print(f"invalid --set value (need field=value): {pair}", file=sys.stderr)
                return 1
            k, v = pair.split("=", 1)
            updates[k] = v
        ok = update_cve(args.cve_id, **updates)
        print("updated" if ok else f"not found: {args.cve_id}")
        return 0 if ok else 1

    if args.command == "delete":
        ok = delete_cve(args.cve_id)
        print("deleted" if ok else f"not found: {args.cve_id}")
        return 0 if ok else 1

    if args.command == "exists":
        found = exists(args.cve_id)
        print("yes" if found else "no")
        return 0 if found else 1

    if args.command == "today":
        row = posted_today()
        if not row:
            print("no CVE posted today")
            return 1
        _print_rows([row])
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
