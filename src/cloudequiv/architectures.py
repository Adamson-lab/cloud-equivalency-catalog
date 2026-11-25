"""Reference architectures: load, validate, and render as Mermaid diagrams."""
from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from .loader import FIT_WEIGHT, PROVIDER_LABELS, PROVIDERS, catalog_dir

CLASS_DEFS = (
    "classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;\n"
    "classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;\n"
    "classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;\n"
    "classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;"
)


def arch_dir(catalog: str | os.PathLike | None = None) -> Path:
    env = os.environ.get("CLOUDEQUIV_ARCHITECTURES")
    return Path(env) if env else catalog_dir(catalog).parent / "architectures"


def load_architectures(catalog: str | os.PathLike | None = None) -> list[dict]:
    d = arch_dir(catalog)
    out = []
    for f in sorted(d.glob("*.yaml")) if d.is_dir() else []:
        out.append(yaml.safe_load(f.read_text(encoding="utf-8")) | {"_file": f.name})
    return out


def validate_architectures(archs: list[dict], entries: list[dict]) -> list[str]:
    ids = {e["id"] for e in entries}
    errors, seen = [], set()
    for a in archs:
        n = a.get("_file", "?")
        for k in ("id", "title", "description", "components", "edges"):
            if k not in a:
                errors.append(f"{n}: missing '{k}'")
        if errors and any(e.startswith(f"{n}: missing") for e in errors):
            continue
        if a["id"] in seen:
            errors.append(f"{n}: duplicate architecture id {a['id']}")
        seen.add(a["id"])
        keys = set()
        for c in a["components"]:
            if c["key"] in keys:
                errors.append(f"{n}: duplicate component key '{c['key']}'")
            keys.add(c["key"])
            if c["capability"] not in ids:
                errors.append(f"{n}: component '{c['key']}' uses unknown capability '{c['capability']}'")
        for e in a["edges"]:
            if len(e) != 2 or e[0] not in keys or e[1] not in keys:
                errors.append(f"{n}: bad edge {e}")
    return errors


def _q(s: str) -> str:
    return s.replace('"', "#quot;")


def mermaid(arch: dict, entries: list[dict], provider: str) -> str:
    """Mermaid flowchart of the architecture using `provider` service names, colored by fit."""
    by_id = {e["id"]: e for e in entries}
    lines = ["flowchart LR"]
    groups: dict[str, list[dict]] = {}
    for c in arch["components"]:
        groups.setdefault(c.get("group", "Other"), []).append(c)
    for gi, (g, comps) in enumerate(groups.items()):
        lines.append(f'  subgraph G{gi}["{_q(g)}"]')
        for c in comps:
            e = by_id[c["capability"]]
            o = e["offerings"][provider]
            lines.append(f'    n_{c["key"]}["{_q(e["name"])}<br/><b>{_q(o["service"])}</b><br/><i>{o["fit"]}</i>"]:::{o["fit"]}')
        lines.append("  end")
    for a, b in arch["edges"]:
        lines.append(f"  n_{a} --> n_{b}")
    for gi in range(len(groups)):
        lines.append(f"  style G{gi} fill:none,stroke:#8b949e,stroke-dasharray:3 3")
    lines.append("  " + CLASS_DEFS.replace("\n", "\n  "))
    return "\n".join(lines)


def blueprint_rows(arch: dict, entries: list[dict], src: str, dst: str) -> list[dict]:
    by_id = {e["id"]: e for e in entries}
    rows = []
    for c in arch["components"]:
        e = by_id[c["capability"]]
        rows.append({"key": c["key"], "capability": e["name"], "from": e["offerings"][src], "to": e["offerings"][dst],
                     "complexity": e["migration_complexity"], "lock_in": e["lock_in_risk"], "exec_note": e.get("exec_note", "")})
    return rows


def blueprint_score(rows: list[dict]) -> float:
    return round(100 * sum(FIT_WEIGHT[r["to"]["fit"]] for r in rows) / len(rows), 1)


def diagram_doc(arch: dict, entries: list[dict]) -> str:
    """Markdown page with one Mermaid diagram per provider (renders natively on GitHub)."""
    out = [f"# {arch['title']}", "", arch["description"], "",
           "Node color = how well that provider's service matches the reference capability: "
           "green `exact`, blue `close`, amber `partial`, red dashed `none`. The label repeats the fit as text.", ""]
    by_id = {e["id"]: e for e in entries}
    out += ["| Provider | Parity for this architecture |", "|---|---|"]
    for p in PROVIDERS:
        w = sum(FIT_WEIGHT[by_id[c["capability"]]["offerings"][p]["fit"]] for c in arch["components"])
        out.append(f"| {PROVIDER_LABELS[p]} | {round(100 * w / len(arch['components']), 1)} / 100 |")
    out.append("")
    for p in PROVIDERS:
        out += [f"## {PROVIDER_LABELS[p]}", "", "```mermaid", mermaid(arch, entries, p), "```", ""]
    return "\n".join(out)
