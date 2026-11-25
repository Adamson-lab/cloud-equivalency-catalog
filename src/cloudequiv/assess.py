"""Assess a real service inventory (CSV) for migration from one provider to another."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from .loader import FIT_WEIGHT, PROVIDER_LABELS, Entry
from .query import norm

COMPLEXITY_W = {"low": 1.0, "medium": 2.0, "high": 3.0}


def _parts(service: str) -> list[str]:
    parts = re.split(r"\s*/\s*", service)
    return [norm(re.sub(r"\(.*?\)", "", p)) for p in parts if p.strip()] + [norm(service)]


def match_service(entries: list[Entry], service: str, provider: str) -> Entry | None:
    """Best catalog entry for a service name as it appears on `provider`'s invoice or inventory."""
    q = norm(re.sub(r"\(.*?\)", "", service))
    if not q:
        return None
    best, best_score = None, 0.0
    for e in entries:
        for part in _parts(e["offerings"][provider]["service"]):
            if not part:
                continue
            if part == q:
                score = 3.0
            elif q in part:
                score = 2.0 - min(len(part) - len(q), 40) / 100  # prefer the tightest name
            elif part in q:
                score = 1.0 + min(len(part), 40) / 100  # inventory name is more verbose
            else:
                continue
            if score > best_score:
                best, best_score = e, score
    return best


def read_inventory(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "service" not in rows[0]:
        raise ValueError("inventory CSV needs a 'service' column (optional: monthly_cost_usd, workload)")
    for r in rows:
        try:
            r["cost"] = float(r.get("monthly_cost_usd") or 0)
        except ValueError:
            r["cost"] = 0.0
    return rows


def assess(entries: list[Entry], inventory: list[dict], src: str, dst: str) -> dict:
    lines, unmatched = [], []
    for r in inventory:
        e = match_service(entries, r["service"], src)
        if not e:
            unmatched.append(r)
            continue
        to = e["offerings"][dst]
        # Priority: spend x (how bad the fit is + how hard the move is).
        gap = 1.0 - FIT_WEIGHT[to["fit"]]
        priority = round(r["cost"] * (gap + 0.25 * COMPLEXITY_W[e["migration_complexity"]]), 2)
        lines.append({"row": r, "entry": e, "to": to, "priority": priority})
    lines.sort(key=lambda x: (-x["priority"], x["row"]["service"]))
    total = sum(r["cost"] for r in inventory)
    matched = sum(x["row"]["cost"] for x in lines)
    spend_by_fit = {f: 0.0 for f in FIT_WEIGHT}
    for x in lines:
        spend_by_fit[x["to"]["fit"]] += x["row"]["cost"]
    at_risk = spend_by_fit["partial"] + spend_by_fit["none"]
    hard = sum(x["row"]["cost"] for x in lines if x["entry"]["migration_complexity"] == "high" and x["to"]["fit"] != "exact")
    return {"src": src, "dst": dst, "lines": lines, "unmatched": unmatched, "total": total, "matched": matched,
            "spend_by_fit": spend_by_fit, "at_risk": at_risk, "hard": hard}


def report_markdown(a: dict) -> str:
    L, usd = PROVIDER_LABELS, lambda v: f"${v:,.0f}"
    pct = lambda v: f"{(100 * v / a['total']):.0f}%" if a["total"] else "n/a"
    out = [f"# Migration assessment: {L[a['src']]} -> {L[a['dst']]}", "",
           f"- Inventory lines: **{len(a['lines']) + len(a['unmatched'])}** ({len(a['lines'])} matched, {len(a['unmatched'])} unmatched)",
           f"- Monthly spend in inventory: **{usd(a['total'])}**; matched to catalog: **{usd(a['matched'])}** ({pct(a['matched'])})",
           f"- Spend with only a **partial or no** equivalent on target: **{usd(a['at_risk'])}** ({pct(a['at_risk'])})",
           f"- Spend that is **high-complexity and not an exact match**: **{usd(a['hard'])}** ({pct(a['hard'])})", "",
           "```mermaid", "pie showData title Monthly spend by fit on " + L[a["dst"]]]
    for f in ("exact", "close", "partial", "none"):
        if a["spend_by_fit"][f] > 0:
            out.append(f'  "{f}" : {round(a["spend_by_fit"][f])}')
    out += ["```", "", "## Priority-ranked workplan",
            "Priority = monthly spend x (fit gap + migration complexity). Start at the top: it is where money and risk concentrate.", "",
            "| # | Source service | Workload | $/mo | Target service | Fit | Complexity | Lock-in | Notes |", "|---|---|---|---|---|---|---|---|---|"]
    for i, x in enumerate(a["lines"], 1):
        r, e, to = x["row"], x["entry"], x["to"]
        note = (to.get("notes") or e.get("exec_note") or "").replace("|", "/")
        out.append(f"| {i} | {r['service']} | {r.get('workload', '')} | {usd(r['cost'])} | {to['service']} | {to['fit']} | "
                   f"{e['migration_complexity']} | {e['lock_in_risk']} | {note} |")
    if a["unmatched"]:
        out += ["", "## Unmatched inventory lines (not in catalog: review manually or contribute a mapping)", ""]
        out += [f"- {r['service']} ({usd(r['cost'])}/mo)" for r in a["unmatched"]]
    out += ["", "_Heuristic output from curated data. Validate with vendor documentation and a proof of concept before committing._"]
    return "\n".join(out)
