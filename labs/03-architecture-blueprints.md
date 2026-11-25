# Lab 3: Move a whole architecture, not just a service (15 min)

**Scenario:** Regulators ask your bank for a *stressed-exit* plan for the data platform.

```bash
cloudequiv architectures
cloudequiv blueprint regulated-data-platform --from aws --to oci
cloudequiv blueprint regulated-data-platform --from aws --to azure --mermaid
cloudequiv diagram gov-hybrid-enclave --provider gcp      # paste output into https://mermaid.live
```

Then read the committed, always-up-to-date diagrams in `docs/diagrams/` (GitHub renders them): one diagram per provider per architecture, nodes colored and labeled by fit.

**Check yourself**
1. In `regulated-data-platform`, which component is the single gap moving to OCI? What does the catalog say to do about it?
2. Which architecture has the **lowest** parity when moved to Google Cloud? Why?
3. In `gov-hybrid-enclave`, why is the fit for the government-cloud component not `exact` on Google Cloud, and what should an executive do with that information?

**Your turn:** copy `architectures/three-tier-web.yaml`, model *your* system using capability ids from `catalog/`, run `cloudequiv validate`, then `cloudequiv diagrams` to regenerate docs.
