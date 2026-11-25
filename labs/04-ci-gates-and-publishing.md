# Lab 4: Treat the catalog like production code (15 min)

**Scenario:** Your architecture review board wants the mapping to be auditable, versioned and never silently wrong.

1. **Break the data on purpose.** In `catalog/storage.yaml`, change one `fit: exact` to `fit: none` and run `cloudequiv validate`. It must fail: gaps need explanatory `notes`. Add notes and watch it pass.
2. **Break a diagram contract.** Run `cloudequiv diagrams --check`: it fails because the committed docs are now stale. Regenerate with `cloudequiv diagrams` and re-check.
3. **Break a reference.** In an `architectures/*.yaml`, use a nonexistent `capability`. Validation names the file and component.
4. **Run the full gate** exactly as CI does:
   ```bash
   cloudequiv validate && cloudequiv diagrams --check && python -m pytest -q
   ```
5. **Publish live:** push to GitHub, set Pages source to *GitHub Actions*, and open the generated site. Search `S3`, filter *Has no equivalent*.

**Check yourself:** why does the repo refuse a `partial`/`none` rating without notes? (Answer: an unexplained "no" is the most dangerous thing an executive can be handed.)
