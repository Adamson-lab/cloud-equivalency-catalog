"""Query logic: search, translate, coverage, gaps, and executive briefs."""
from __future__ import annotations

import re
from typing import Iterable

from .loader import FIT_WEIGHT, FITS, PROVIDERS, Entry


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def search(entries: Iterable[Entry], text: str, category: str | None = None) -> list[Entry]:
    """Free-text search across concept names, descriptions and every provider's service name."""
    q = norm(text)
    out = []
    for e in entries:
        if category and e["category"] != category:
            continue
        hay = " ".join(
            [e["id"], e["name"], e["description"]] + [o["service"] for o in e["offerings"].values()]
        )
        if q in norm(hay):
            out.append(e)
    return out


def find_by_service(entries: Iterable[Entry], service: str, provider: str | None = None) -> list[tuple[Entry, str]]:
    """Find concepts containing a given provider service name. Returns (entry, provider) pairs."""
    q = norm(service)
    hits = []
    for e in entries:
        for p in PROVIDERS:
            if provider and p != provider:
                continue
            if q and q in norm(e["offerings"][p]["service"]):
                hits.append((e, p))
    return hits


def translate(entries: Iterable[Entry], service: str, src: str | None, dst: str) -> list[dict]:
    """Translate a service from `src` provider (or any) to `dst` provider."""
    results = []
    for e, p in find_by_service(entries, service, src):
        if p == dst:
            continue
        results.append(
            {
                "concept": e["name"],
                "id": e["id"],
                "category": e["category"],
                "from_provider": p,
                "from": e["offerings"][p],
                "to_provider": dst,
                "to": e["offerings"][dst],
                "migration_complexity": e["migration_complexity"],
                "lock_in_risk": e["lock_in_risk"],
                "exec_note": e.get("exec_note", ""),
            }
        )
    return results


def coverage(entries: Iterable[Entry]) -> dict[str, dict[str, int]]:
    """Per provider: count of entries by fit."""
    entries = list(entries)
    out = {p: {f: 0 for f in FITS} for p in PROVIDERS}
    for e in entries:
        for p in PROVIDERS:
            out[p][e["offerings"][p]["fit"]] += 1
    return out


def parity_score(entries: Iterable[Entry], provider: str) -> float:
    """Weighted 0-100 score of how fully a provider covers the reference concepts."""
    entries = list(entries)
    if not entries:
        return 0.0
    total = sum(FIT_WEIGHT[e["offerings"][provider]["fit"]] for e in entries)
    return round(100 * total / len(entries), 1)


def gaps(entries: Iterable[Entry], provider: str, include_partial: bool = True) -> list[Entry]:
    bad = {"none", "partial"} if include_partial else {"none"}
    return [e for e in entries if e["offerings"][provider]["fit"] in bad]


def brief(entries: Iterable[Entry], src: str, dst: str) -> dict:
    """Executive migration brief for moving workloads from `src` to `dst`.

    Only concepts where `src` actually has an offering are in scope.
    """
    scope = [e for e in entries if e["offerings"][src]["fit"] != "none"]
    fit_counts = {f: 0 for f in FITS}
    for e in scope:
        fit_counts[e["offerings"][dst]["fit"]] += 1
    score = parity_score(scope, dst)
    blockers = [e for e in scope if e["offerings"][dst]["fit"] == "none"]
    rework = [e for e in scope if e["offerings"][dst]["fit"] == "partial"]
    hard = [
        e
        for e in scope
        if e["migration_complexity"] == "high" and e["offerings"][dst]["fit"] != "exact"
    ]
    lock_in = [e for e in scope if e["lock_in_risk"] == "high"]
    if score >= 85 and not blockers:
        posture = "LOW RISK: broad parity; focus on execution and skills."
    elif score >= 65:
        posture = "MODERATE RISK: plan compensating controls for gaps before committing."
    else:
        posture = "HIGH RISK: material capability gaps; validate with a proof of concept first."
    return {
        "from": src,
        "to": dst,
        "concepts_in_scope": len(scope),
        "fit_counts": fit_counts,
        "parity_score": score,
        "posture": posture,
        "blockers": blockers,
        "rework": rework,
        "hard_migrations": hard,
        "lock_in_hotspots": lock_in,
    }
