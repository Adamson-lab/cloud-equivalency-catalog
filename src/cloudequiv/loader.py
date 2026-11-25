"""Load and validate the YAML catalog (stdlib + PyYAML only)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

PROVIDERS = ("aws", "azure", "gcp", "oci")
PROVIDER_LABELS = {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud", "oci": "Oracle Cloud"}
FITS = ("exact", "close", "partial", "none")
LEVELS = ("low", "medium", "high")
# How much of the reference capability the offering delivers (used for parity scoring).
FIT_WEIGHT = {"exact": 1.0, "close": 0.75, "partial": 0.4, "none": 0.0}

Entry = dict[str, Any]


def catalog_dir(path: str | os.PathLike | None = None) -> Path:
    """Resolve the catalog directory: explicit arg > $CLOUDEQUIV_CATALOG > repo checkout > ./catalog."""
    if path:
        return Path(path)
    env = os.environ.get("CLOUDEQUIV_CATALOG")
    if env:
        return Path(env)
    repo = Path(__file__).resolve().parents[2] / "catalog"
    if repo.is_dir():
        return repo
    return Path.cwd() / "catalog"


def load_documents(path: str | os.PathLike | None = None) -> list[tuple[Path, dict]]:
    root = catalog_dir(path)
    files = sorted(root.glob("*.yaml"))
    if not files:
        raise FileNotFoundError(f"No *.yaml catalog files found in {root}")
    docs = []
    for f in files:
        with f.open("r", encoding="utf-8") as fh:
            docs.append((f, yaml.safe_load(fh)))
    return docs


def load_entries(path: str | os.PathLike | None = None) -> list[Entry]:
    """Return a flat list of entries; each gets `category` and `category_title` injected."""
    entries: list[Entry] = []
    for _, doc in load_documents(path):
        for e in doc["entries"]:
            item = dict(e)
            item["category"] = doc["category"]
            item["category_title"] = doc["title"]
            entries.append(item)
    return entries


def _check_offering(where: str, off: Any, errors: list[str]) -> None:
    if not isinstance(off, dict):
        errors.append(f"{where}: offering must be a mapping")
        return
    extra = set(off) - {"service", "fit", "notes"}
    if extra:
        errors.append(f"{where}: unknown keys {sorted(extra)}")
    if not isinstance(off.get("service"), str) or not off["service"].strip():
        errors.append(f"{where}: 'service' must be a non-empty string")
    if off.get("fit") not in FITS:
        errors.append(f"{where}: 'fit' must be one of {FITS}, got {off.get('fit')!r}")
    if "notes" in off and not isinstance(off["notes"], str):
        errors.append(f"{where}: 'notes' must be a string")
    if off.get("fit") in ("partial", "none") and not off.get("notes"):
        errors.append(f"{where}: fit '{off.get('fit')}' requires 'notes' explaining the gap")


def validate_documents(docs: list[tuple[Path, dict]]) -> list[str]:
    """Return a list of human-readable errors (empty list == valid)."""
    errors: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_cats: dict[str, str] = {}
    for path, doc in docs:
        name = path.name
        if not isinstance(doc, dict):
            errors.append(f"{name}: top level must be a mapping")
            continue
        missing = {"category", "title", "entries"} - set(doc)
        if missing:
            errors.append(f"{name}: missing keys {sorted(missing)}")
            continue
        if doc["category"] in seen_cats:
            errors.append(f"{name}: category '{doc['category']}' already used in {seen_cats[doc['category']]}")
        seen_cats[doc["category"]] = name
        if not isinstance(doc["entries"], list) or not doc["entries"]:
            errors.append(f"{name}: 'entries' must be a non-empty list")
            continue
        for i, e in enumerate(doc["entries"]):
            eid = e.get("id", f"#{i}") if isinstance(e, dict) else f"#{i}"
            where = f"{name}:{eid}"
            if not isinstance(e, dict):
                errors.append(f"{where}: entry must be a mapping")
                continue
            allowed = {"id", "name", "description", "migration_complexity", "lock_in_risk", "exec_note", "offerings"}
            extra = set(e) - allowed
            if extra:
                errors.append(f"{where}: unknown keys {sorted(extra)}")
            for key in ("id", "name", "description"):
                if not isinstance(e.get(key), str) or not e[key].strip():
                    errors.append(f"{where}: '{key}' must be a non-empty string")
            if e.get("migration_complexity") not in LEVELS:
                errors.append(f"{where}: migration_complexity must be one of {LEVELS}")
            if e.get("lock_in_risk") not in LEVELS:
                errors.append(f"{where}: lock_in_risk must be one of {LEVELS}")
            if isinstance(e.get("id"), str):
                if e["id"] in seen_ids:
                    errors.append(f"{where}: duplicate id (also in {seen_ids[e['id']]})")
                seen_ids[e["id"]] = name
            offerings = e.get("offerings")
            if not isinstance(offerings, dict):
                errors.append(f"{where}: 'offerings' must be a mapping")
                continue
            for p in PROVIDERS:
                if p not in offerings:
                    errors.append(f"{where}: missing provider '{p}'")
                else:
                    _check_offering(f"{where}.{p}", offerings[p], errors)
            unknown = set(offerings) - set(PROVIDERS)
            if unknown:
                errors.append(f"{where}: unknown providers {sorted(unknown)}")
    return errors


def validate(path: str | os.PathLike | None = None) -> list[str]:
    return validate_documents(load_documents(path))
