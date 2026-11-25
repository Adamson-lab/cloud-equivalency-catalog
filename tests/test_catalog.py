import json
import tempfile
import unittest
from pathlib import Path

import yaml

from cloudequiv import query, render
from cloudequiv.cli import main
from cloudequiv.loader import PROVIDERS, load_documents, load_entries, validate_documents
from cloudequiv.site import build_site

ENTRIES = load_entries()


class CatalogIntegrity(unittest.TestCase):
    def test_catalog_validates(self):
        self.assertEqual(validate_documents(load_documents()), [])

    def test_ids_unique_and_kebab(self):
        ids = [e["id"] for e in ENTRIES]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, r"^[a-z][a-z0-9-]*$")

    def test_every_entry_covers_every_provider(self):
        for e in ENTRIES:
            self.assertEqual(set(e["offerings"]), set(PROVIDERS), e["id"])

    def test_minimum_size(self):
        self.assertGreaterEqual(len(ENTRIES), 50)

    def test_schema_file_matches_when_jsonschema_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = json.loads((Path(__file__).parents[1] / "schema" / "catalog.schema.json").read_text())
        for path, doc in load_documents():
            jsonschema.validate(doc, schema)


class ValidatorRejectsBadData(unittest.TestCase):
    def _doc(self, **over):
        entry = {
            "id": "x", "name": "X", "description": "d",
            "migration_complexity": "low", "lock_in_risk": "low",
            "offerings": {p: {"service": "S", "fit": "exact"} for p in PROVIDERS},
        }
        entry.update(over)
        return [(Path("t.yaml"), {"category": "t", "title": "T", "entries": [entry]})]

    def test_gap_without_notes_rejected(self):
        offs = {p: {"service": "S", "fit": "exact"} for p in PROVIDERS}
        offs["oci"] = {"service": "S", "fit": "none"}
        errs = validate_documents(self._doc(offerings=offs))
        self.assertTrue(any("requires 'notes'" in e for e in errs))

    def test_missing_provider_rejected(self):
        offs = {p: {"service": "S", "fit": "exact"} for p in PROVIDERS if p != "gcp"}
        errs = validate_documents(self._doc(offerings=offs))
        self.assertTrue(any("missing provider 'gcp'" in e for e in errs))

    def test_bad_enum_rejected(self):
        errs = validate_documents(self._doc(lock_in_risk="extreme"))
        self.assertTrue(any("lock_in_risk" in e for e in errs))

    def test_duplicate_id_rejected(self):
        d = self._doc()
        d.append((Path("u.yaml"), {"category": "u", "title": "U", "entries": [dict(d[0][1]["entries"][0])]}))
        self.assertTrue(any("duplicate id" in e for e in validate_documents(d)))


class Queries(unittest.TestCase):
    def test_translate_s3_to_azure(self):
        res = query.translate(ENTRIES, "S3", "aws", "azure")
        self.assertTrue(any("Blob Storage" in r["to"]["service"] for r in res))

    def test_translate_from_any_provider(self):
        res = query.translate(ENTRIES, "BigQuery", None, "aws")
        self.assertTrue(any("Redshift" in r["to"]["service"] for r in res))

    def test_search_matches_service_names(self):
        hits = query.search(ENTRIES, "key vault")
        self.assertTrue(hits)

    def test_parity_bounds(self):
        for p in PROVIDERS:
            self.assertTrue(0 <= query.parity_score(ENTRIES, p) <= 100)

    def test_brief_blockers_are_none_fit(self):
        b = query.brief(ENTRIES, "aws", "oci")
        for e in b["blockers"]:
            self.assertEqual(e["offerings"]["oci"]["fit"], "none")
        self.assertIn("RISK", b["posture"])

    def test_gaps_only_returns_gaps(self):
        for e in query.gaps(ENTRIES, "oci"):
            self.assertIn(e["offerings"]["oci"]["fit"], ("none", "partial"))


class Outputs(unittest.TestCase):
    def test_csv_has_header_and_rows(self):
        out = render.matrix(ENTRIES, "csv").splitlines()
        self.assertEqual(len(out), len(ENTRIES) + 1)
        self.assertTrue(out[0].startswith("id,category"))

    def test_json_roundtrip(self):
        self.assertEqual(len(json.loads(render.matrix(ENTRIES, "json"))), len(ENTRIES))

    def test_site_embeds_data_safely(self):
        evil = [dict(ENTRIES[0])]
        evil[0]["description"] = "</script><script>alert(1)</script>"
        with tempfile.TemporaryDirectory() as d:
            index = build_site(evil, Path(d))
            html = index.read_text()
            self.assertNotIn("</script><script>alert(1)", html)
            self.assertTrue((Path(d) / "catalog.json").exists())

    def test_cli_exit_codes(self):
        self.assertEqual(main(["validate"]), 0)
        self.assertEqual(main(["translate", "nonexistent-xyz", "--to", "aws"]), 1)
        self.assertEqual(main(["brief", "--from", "aws", "--to", "aws"]), 2)


if __name__ == "__main__":
    unittest.main()


class ArchitecturesAndAssess(unittest.TestCase):
    def setUp(self):
        from cloudequiv import architectures as arch
        self.arch = arch
        self.archs = arch.load_architectures()

    def test_architectures_valid_and_present(self):
        self.assertGreaterEqual(len(self.archs), 4)
        self.assertEqual(self.arch.validate_architectures(self.archs, ENTRIES), [])

    def test_validator_catches_unknown_capability_and_edge(self):
        bad = [{"_file": "t.yaml", "id": "t", "title": "T", "description": "d",
                "components": [{"key": "a", "capability": "does-not-exist"}], "edges": [["a", "zzz"]]}]
        errs = self.arch.validate_architectures(bad, ENTRIES)
        self.assertTrue(any("unknown capability" in e for e in errs))
        self.assertTrue(any("bad edge" in e for e in errs))

    def test_mermaid_for_every_architecture_and_provider(self):
        for a in self.archs:
            for p in PROVIDERS:
                m = self.arch.mermaid(a, ENTRIES, p)
                self.assertTrue(m.startswith("flowchart LR"))
                self.assertEqual(m.count(":::") , len(a["components"]))
                self.assertEqual(m.count(" --> "), len(a["edges"]))

    def test_committed_diagrams_are_current(self):
        root = Path(__file__).parents[1] / "docs" / "diagrams"
        for a in self.archs:
            self.assertEqual((root / f"{a['id']}.md").read_text(encoding="utf-8"),
                             self.arch.diagram_doc(a, ENTRIES) + "\n", f"stale: {a['id']}")

    def test_assess_matching_and_unmatched(self):
        from cloudequiv import assess
        self.assertEqual(assess.match_service(ENTRIES, "Amazon S3", "aws")["id"], "object-storage")
        self.assertEqual(assess.match_service(ENTRIES, "Amazon S3 Glacier", "aws")["id"], "archive-storage")
        self.assertEqual(assess.match_service(ENTRIES, "Amazon RDS for PostgreSQL", "aws")["id"], "managed-relational")
        self.assertIsNone(assess.match_service(ENTRIES, "Totally Made Up Service", "aws"))

    def test_assess_sample_inventory(self):
        from cloudequiv import assess
        inv = assess.read_inventory(Path(__file__).parents[1] / "examples" / "bank-aws-inventory.csv")
        a = assess.assess(ENTRIES, inv, "aws", "oci")
        self.assertGreater(len(a["lines"]), 35)
        self.assertEqual(len(a["unmatched"]), 2)
        self.assertAlmostEqual(sum(a["spend_by_fit"].values()), a["matched"])
        prios = [x["priority"] for x in a["lines"]]
        self.assertEqual(prios, sorted(prios, reverse=True))
        self.assertIn("```mermaid", assess.report_markdown(a))

    def test_cli_new_commands(self):
        self.assertEqual(main(["architectures"]), 0)
        self.assertEqual(main(["blueprint", "three-tier-web", "--from", "aws", "--to", "azure"]), 0)
        self.assertEqual(main(["diagrams", "--check"]), 0)
