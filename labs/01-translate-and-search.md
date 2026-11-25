# Lab 1: Translate services and find gaps (10 min)

**Scenario:** Your CTO says "we're evaluating Azure for the payments stack." You need answers in minutes, not weeks.

```bash
cloudequiv translate "DynamoDB" --to azure
cloudequiv translate "Cloud Spanner" --to aws        # what has no clean match?
cloudequiv lookup "key vault"                        # search by any provider's name
cloudequiv gaps oci                                  # where is Oracle Cloud partial/none?
cloudequiv stats
```

**Check yourself**
1. Which capability has **no** first-party equivalent on OCI, and what's the workaround the catalog suggests?
2. For `Cloud Spanner` -> AWS, what fit rating comes back and why isn't it `exact`?
3. Which provider has the lowest parity score, and why is that number *not* a vendor ranking? (Read the caveat `stats` prints.)

**Your turn:** pick a service your organization uses that isn't in the catalog, add an entry to the right `catalog/*.yaml`, run `cloudequiv validate`, and confirm `translate` finds it.
