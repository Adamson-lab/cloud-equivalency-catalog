# Lab 2: Assess a real estate and rank the workplan (20 min)

**Scenario:** A bank runs ~$1.3M/month on AWS and the board asked for a credible exit and portability assessment.
`examples/bank-aws-inventory.csv` is an *illustrative* inventory (spend figures are made up) shaped like a Cost Explorer or invoice export.

```bash
cloudequiv assess examples/bank-aws-inventory.csv --to azure --out azure-report.md
cloudequiv assess examples/bank-aws-inventory.csv --to oci   --out oci-report.md
cloudequiv assess examples/bank-aws-inventory.csv --to gcp   --out gcp-report.md
```

Open each report in a Markdown viewer (GitHub renders the Mermaid spend chart).

**Check yourself**
1. How much monthly spend lands on a *partial or none* equivalent for each target? Which target is riskiest?
2. Which two inventory lines are **unmatched**? What would you do about them? (Hint: one is a retired AWS product and one is a service the catalog doesn't cover yet.)
3. Priority = spend x (fit gap + complexity). Why does Aurora outrank Redshift on Azure even though Redshift has an `exact` mapping?

**Your turn: use your own data**
1. Export a service-level cost report from your cloud billing console.
2. Save it as CSV with columns `service,monthly_cost_usd,workload`.
3. Run `cloudequiv assess your.csv --from aws --to azure`. Use `--from azure` or `--from gcp` or `--from oci` for other sources.
4. Add mappings for every unmatched line and open a PR.
