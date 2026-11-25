"""Command-line interface: `cloudequiv <command>`."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, architectures as arch, assess as asm, query, render
from .loader import PROVIDER_LABELS, PROVIDERS, load_documents, load_entries, validate_documents


def _entries(args):
    return load_entries(args.catalog)


def cmd_validate(args) -> int:
    docs = load_documents(args.catalog)
    errors = validate_documents(docs)
    if not errors:
        errors = arch.validate_architectures(arch.load_architectures(args.catalog), load_entries(args.catalog))
    if errors:
        print(f"INVALID: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    n = sum(len(d["entries"]) for _, d in docs)
    na = len(arch.load_architectures(args.catalog))
    print(f"OK: {len(docs)} files, {n} capabilities, {n * len(PROVIDERS)} offerings, {na} reference architectures validated.")
    return 0


def cmd_lookup(args) -> int:
    hits = query.search(_entries(args), args.text, args.category)
    if not hits:
        print("No match found.")
        return 1
    print(render.matrix(hits, args.format))
    return 0


def cmd_translate(args) -> int:
    res = query.translate(_entries(args), args.service, args.src, args.dst)
    if args.format == "json":
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(render.translation(res))
    return 0 if res else 1


def cmd_matrix(args) -> int:
    entries = _entries(args)
    if args.category:
        entries = [e for e in entries if e["category"] == args.category]
    print(render.matrix(entries, args.format))
    return 0


def cmd_gaps(args) -> int:
    rows = query.gaps(_entries(args), args.provider, include_partial=not args.hard_only)
    if not rows:
        print("No gaps.")
        return 0
    for e in rows:
        o = e["offerings"][args.provider]
        print(f"[{o['fit']:7}] {e['name']}: {o['service']}\n          {o.get('notes', '')}")
    return 0


def cmd_stats(args) -> int:
    entries = _entries(args)
    cov = query.coverage(entries)
    rows = []
    for p in PROVIDERS:
        c = cov[p]
        rows.append([PROVIDER_LABELS[p], c["exact"], c["close"], c["partial"], c["none"], query.parity_score(entries, p)])
    print(f"{len(entries)} capabilities across {len({e['category'] for e in entries})} categories\n")
    print(render.text_table([[str(x) for x in r] for r in rows], ["Provider", "Exact", "Close", "Partial", "None", "Parity/100"]))
    print("\nParity is measured against the catalog's neutral capability list, not against any one vendor.")
    return 0


def cmd_brief(args) -> int:
    if args.src == args.dst:
        print("--from and --to must differ", file=sys.stderr)
        return 2
    b = query.brief(_entries(args), args.src, args.dst)
    if args.format == "json":
        slim = {k: ([e["id"] for e in v] if isinstance(v, list) else v) for k, v in b.items()}
        print(json.dumps(slim, indent=2))
    else:
        print(render.brief_text(b))
    return 0


def cmd_site(args) -> int:
    from .site import build_site

    out = build_site(_entries(args), Path(args.out))
    print(f"Wrote {out}")
    return 0


def _arch(args, key):
    for a in arch.load_architectures(args.catalog):
        if a["id"] == key:
            return a
    ids = ", ".join(a["id"] for a in arch.load_architectures(args.catalog))
    raise SystemExit(f"unknown architecture '{key}'. Available: {ids}")


def cmd_architectures(args) -> int:
    for a in arch.load_architectures(args.catalog):
        print(f"{a['id']:26} {a['title']}")
    return 0


def cmd_diagram(args) -> int:
    print(arch.mermaid(_arch(args, args.arch), _entries(args), args.provider))
    return 0


def cmd_diagrams(args) -> int:
    entries, out, stale = _entries(args), Path(args.out), []
    out.mkdir(parents=True, exist_ok=True)
    for a in arch.load_architectures(args.catalog):
        target, text = out / f"{a['id']}.md", arch.diagram_doc(a, entries) + "\n"
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != text:
                stale.append(target.name)
        else:
            target.write_text(text, encoding="utf-8")
            print(f"Wrote {target}")
    if stale:
        print("Stale diagrams (run `cloudequiv diagrams`): " + ", ".join(stale), file=sys.stderr)
        return 1
    return 0


def cmd_blueprint(args) -> int:
    a, entries = _arch(args, args.arch), _entries(args)
    rows = arch.blueprint_rows(a, entries, args.src, args.dst)
    print(f"{a['title']}: {PROVIDER_LABELS[args.src]} -> {PROVIDER_LABELS[args.dst]}")
    print(f"Architecture parity on target: {arch.blueprint_score(rows)} / 100\n")
    table = [[r["capability"], r["from"]["service"], r["to"]["service"], r["to"]["fit"], r["complexity"], r["lock_in"]] for r in rows]
    print(render.text_table(table, ["Component", PROVIDER_LABELS[args.src], PROVIDER_LABELS[args.dst], "Fit", "Complexity", "Lock-in"]))
    risks = [r for r in rows if r["to"]["fit"] in ("partial", "none")]
    if risks:
        print("\nGaps to resolve before committing:")
        for r in risks:
            print(f"  - {r['capability']}: {r['to']['notes']}")
    if args.mermaid:
        print("\n" + arch.mermaid(a, entries, args.dst))
    return 0


def cmd_assess(args) -> int:
    a = asm.assess(_entries(args), asm.read_inventory(args.inventory), args.src, args.dst)
    text = asm.report_markdown(a)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.out}  (matched {len(a['lines'])}, unmatched {len(a['unmatched'])})")
    else:
        print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cloudequiv", description="AWS / Azure / GCP / OCI service equivalency catalog")
    p.add_argument("--version", action="version", version=f"cloudequiv {__version__}")
    p.add_argument("--catalog", help="catalog directory (default: $CLOUDEQUIV_CATALOG or ./catalog)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("validate", help="validate every YAML file; non-zero exit on error (use in CI)")
    s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("lookup", help="free-text search across capabilities and service names")
    s.add_argument("text")
    s.add_argument("--category")
    s.add_argument("--format", choices=["table", "markdown", "csv", "json"], default="table")
    s.set_defaults(fn=cmd_lookup)

    s = sub.add_parser("translate", help="translate a service name to another provider")
    s.add_argument("service", help='e.g. "S3", "Cosmos DB", "BigQuery"')
    s.add_argument("--from", dest="src", choices=PROVIDERS, help="restrict source provider")
    s.add_argument("--to", dest="dst", choices=PROVIDERS, required=True)
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.set_defaults(fn=cmd_translate)

    s = sub.add_parser("matrix", help="print the full comparison matrix")
    s.add_argument("--category")
    s.add_argument("--format", choices=["table", "markdown", "csv", "json"], default="table")
    s.set_defaults(fn=cmd_matrix)

    s = sub.add_parser("gaps", help="list capabilities a provider covers only partially or not at all")
    s.add_argument("provider", choices=PROVIDERS)
    s.add_argument("--hard-only", action="store_true", help="only show 'none'")
    s.set_defaults(fn=cmd_gaps)

    s = sub.add_parser("stats", help="coverage and parity score per provider")
    s.set_defaults(fn=cmd_stats)

    s = sub.add_parser("brief", help="executive migration brief between two providers")
    s.add_argument("--from", dest="src", choices=PROVIDERS, required=True)
    s.add_argument("--to", dest="dst", choices=PROVIDERS, required=True)
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.set_defaults(fn=cmd_brief)

    s = sub.add_parser("architectures", help="list reference architectures")
    s.set_defaults(fn=cmd_architectures)

    s = sub.add_parser("diagram", help="print a Mermaid diagram of a reference architecture on one provider")
    s.add_argument("arch")
    s.add_argument("--provider", choices=PROVIDERS, default="aws")
    s.set_defaults(fn=cmd_diagram)

    s = sub.add_parser("diagrams", help="write Markdown+Mermaid diagram pages for every architecture")
    s.add_argument("--out", default="docs/diagrams")
    s.add_argument("--check", action="store_true", help="fail if committed diagrams are stale (CI)")
    s.set_defaults(fn=cmd_diagrams)

    s = sub.add_parser("blueprint", help="bill of materials for an architecture moved between providers")
    s.add_argument("arch")
    s.add_argument("--from", dest="src", choices=PROVIDERS, required=True)
    s.add_argument("--to", dest="dst", choices=PROVIDERS, required=True)
    s.add_argument("--mermaid", action="store_true", help="also print the target diagram")
    s.set_defaults(fn=cmd_blueprint)

    s = sub.add_parser("assess", help="assess a real service inventory CSV and rank the migration workplan")
    s.add_argument("inventory", help="CSV with columns: service[, monthly_cost_usd, workload]")
    s.add_argument("--from", dest="src", choices=PROVIDERS, default="aws")
    s.add_argument("--to", dest="dst", choices=PROVIDERS, required=True)
    s.add_argument("--out", help="write the Markdown report to this file")
    s.set_defaults(fn=cmd_assess)

    s = sub.add_parser("site", help="generate a static, searchable HTML site (GitHub Pages ready)")
    s.add_argument("--out", default="site")
    s.set_defaults(fn=cmd_site)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except BrokenPipeError:  # e.g. `cloudequiv matrix | head`
        sys.stderr.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
