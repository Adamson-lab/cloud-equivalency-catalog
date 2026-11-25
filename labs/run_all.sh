#!/usr/bin/env bash
# Runs every lab command end to end, failing fast. Use as a smoke test or a live demo.
set -euo pipefail
cd "$(dirname "$0")/.."
step() { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
step "Validate catalog + architectures";   cloudequiv validate
step "Coverage and parity";                cloudequiv stats
step "Translate DynamoDB -> Azure";        cloudequiv translate "DynamoDB" --to azure
step "Gaps on OCI";                        cloudequiv gaps oci
step "AWS -> Azure executive brief";       cloudequiv brief --from aws --to azure
step "Blueprint: bank data platform -> OCI"; cloudequiv blueprint regulated-data-platform --from aws --to oci
step "Assess the sample bank inventory";   cloudequiv assess examples/bank-aws-inventory.csv --to azure --out /tmp/azure-report.md && head -12 /tmp/azure-report.md
step "Diagrams are up to date";            cloudequiv diagrams --check
echo; echo "All labs ran clean."
