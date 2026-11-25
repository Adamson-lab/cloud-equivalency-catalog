# Contributing

The catalog is only valuable if it is **accurate and current**. Corrections are the most valuable contribution.

## Add or change an entry
1. Edit the relevant file in `catalog/` (or add a new `catalog/<category>.yaml` with `category`, `title`, `entries`).
2. Every entry needs all four providers: `aws`, `azure`, `gcp`, `oci`.
3. Run `cloudequiv validate`, then `python -m pytest`. CI runs both.

## Fit definitions (be strict)
| fit | meaning |
|---|---|
| `exact` | Delivers the reference capability with no material functional gap |
| `close` | Same job, with differences a team will notice (features, limits, operating model) |
| `partial` | Covers only part of the capability, or needs significant extra tooling. **`notes` required** |
| `none` | No first-party equivalent. **`notes` required**, naming the usual workaround |

## Rules
- **Cite vendor documentation** in your PR description for any new or changed fit. No marketing pages or blog posts as the sole source.
- Use the current product name; note renames or retirements in `notes`.
- `migration_complexity` and `lock_in_risk` describe moving *workloads* off the capability, not the vendor's quality.
- Keep `exec_note` to one factual sentence a non-engineer can act on. No opinions about vendors.
- Never claim a compliance authorization (FedRAMP, IL levels, etc.). Point readers to the authoritative registry.
