"""Output renderers: aligned text tables, Markdown, CSV, JSON."""
from __future__ import annotations

import csv
import io
import json
from typing import Iterable

from .loader import PROVIDER_LABELS, PROVIDERS, Entry

FIT_MARK = {"exact": "=", "close": "~", "partial": "!", "none": "x"}


def _cell(e: Entry, p: str, with_fit: bool = True) -> str:
    o = e["offerings"][p]
    return f"{o['service']} [{FIT_MARK[o['fit']]}]" if with_fit else o["service"]


def text_table(rows: list[list[str]], headers: list[str]) -> str:
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)] if rows else [len(h) for h in headers]
    line = lambda r: "  ".join(str(c).ljust(w) for c, w in zip(r, widths)).rstrip()
    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    return "\n".join(out)


def matrix(entries: Iterable[Entry], fmt: str = "table") -> str:
    entries = list(entries)
    if fmt == "json":
        return json.dumps(entries, indent=2, ensure_ascii=False)
    headers = ["Category", "Capability"] + [PROVIDER_LABELS[p] for p in PROVIDERS]
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["id", "category", "capability", "migration_complexity", "lock_in_risk"]
                   + [f"{p}_{k}" for p in PROVIDERS for k in ("service", "fit")])
        for e in entries:
            w.writerow([e["id"], e["category"], e["name"], e["migration_complexity"], e["lock_in_risk"]]
                       + [v for p in PROVIDERS for v in (e["offerings"][p]["service"], e["offerings"][p]["fit"])])
        return buf.getvalue()
    rows = [[e["category"], e["name"]] + [_cell(e, p) for p in PROVIDERS] for e in entries]
    if fmt == "markdown":
        out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
        out += ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in rows]
        out.append("")
        out.append("Fit legend: `[=]` exact, `[~]` close, `[!]` partial, `[x]` no equivalent.")
        return "\n".join(out)
    return text_table(rows, headers) + "\n\nFit legend: [=] exact  [~] close  [!] partial  [x] none"


def translation(results: list[dict]) -> str:
    if not results:
        return "No match found."
    out = []
    for r in results:
        a, b = r["from"], r["to"]
        out.append(f"{r['concept']}  ({r['category']})")
        out.append(f"  {PROVIDER_LABELS[r['from_provider']]}: {a['service']}")
        out.append(f"  {PROVIDER_LABELS[r['to_provider']]}: {b['service']}  [fit: {b['fit']}]")
        if b.get("notes"):
            out.append(f"  Gap / notes: {b['notes']}")
        out.append(f"  Migration complexity: {r['migration_complexity']}   Lock-in risk: {r['lock_in_risk']}")
        if r["exec_note"]:
            out.append(f"  Executive note: {r['exec_note']}")
        out.append("")
    return "\n".join(out).rstrip()


def brief_text(b: dict) -> str:
    L = PROVIDER_LABELS
    out = [
        f"EXECUTIVE BRIEF: {L[b['from']]} -> {L[b['to']]}",
        "=" * 60,
        f"Capabilities in scope : {b['concepts_in_scope']}",
        f"Parity score          : {b['parity_score']} / 100",
        "Fit distribution      : " + ", ".join(f"{k}={v}" for k, v in b["fit_counts"].items()),
        f"Posture               : {b['posture']}",
        "",
    ]

    def section(title: str, items: list[Entry]) -> None:
        out.append(f"{title} ({len(items)})")
        if not items:
            out.append("  none")
        for e in items:
            o = e["offerings"][b["to"]]
            out.append(f"  - {e['name']}: {o['service']}" + (f"  // {o['notes']}" if o.get("notes") else ""))
        out.append("")

    section("BLOCKERS: no equivalent on target", b["blockers"])
    section("REWORK: partial equivalent on target", b["rework"])
    section("HARD MIGRATIONS: high complexity, not an exact match", b["hard_migrations"])
    out.append(f"LOCK-IN HOTSPOTS on source ({len(b['lock_in_hotspots'])})")
    for e in b["lock_in_hotspots"]:
        out.append(f"  - {e['name']}: {e['offerings'][b['from']]['service']}" + (f"  // {e['exec_note']}" if e.get("exec_note") else ""))
    out.append("")
    out.append("Heuristic only. Validate against current vendor documentation before decisions.")
    return "\n".join(out)
