# Migration assessment: AWS -> Azure

- Inventory lines: **43** (41 matched, 2 unmatched)
- Monthly spend in inventory: **$1,348,000**; matched to catalog: **$1,300,000** (96%)
- Spend with only a **partial or no** equivalent on target: **$47,000** (3%)
- Spend that is **high-complexity and not an exact match**: **$142,000** (11%)

```mermaid
pie showData title Monthly spend by fit on Azure
  "exact" : 1056000
  "close" : 197000
  "partial" : 47000
```

## Priority-ranked workplan
Priority = monthly spend x (fit gap + migration complexity). Start at the top: it is where money and risk concentrate.

| # | Source service | Workload | $/mo | Target service | Fit | Complexity | Lock-in | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | Amazon Aurora | payments ledger | $142,000 | Azure SQL Hyperscale / Azure Database for PostgreSQL Flexible Server | close | high | high | Wire-compatible, but performance features, replication and tooling are proprietary. |
| 2 | Amazon Redshift | enterprise warehouse | $128,000 | Microsoft Fabric Warehouse / Azure Synapse Analytics | exact | high | high | Microsoft is steering new analytics investment toward Fabric; verify Synapse roadmap. |
| 3 | Amazon SageMaker | fraud models | $76,000 | Azure Machine Learning | exact | high | high | Pipelines, feature stores and model registries are proprietary; models themselves (ONNX, PyTorch) are portable. |
| 4 | Amazon RDS for PostgreSQL | customer master | $96,000 | Azure SQL Database / Azure Database for PostgreSQL and MySQL | exact | medium | low | Standard engines migrate with native tooling; the risk is in extensions, versions and operational tooling. |
| 5 | Amazon EC2 | core banking batch + legacy apps | $184,000 | Azure Virtual Machines | exact | low | low | Commodity capability; the lift is in images, licensing and networking, not the VM itself. |
| 6 | Amazon DynamoDB | session and idempotency state | $61,000 | Azure Cosmos DB for NoSQL / Table | exact | high | high | Data models and access patterns are proprietary; plan application rewrite. |
| 7 | Amazon MSK | transaction streaming | $47,000 | Event Hubs Kafka endpoint / HDInsight Kafka | partial | low | low | Kafka-protocol endpoint on a different engine; some Kafka features are unsupported. |
| 8 | Amazon EMR | risk model batch | $52,000 | Azure Databricks / Synapse Spark / HDInsight | close | medium | low |  |
| 9 | AWS Glue | ETL | $39,000 | Azure Data Factory / Fabric Data Factory | exact | high | high |  |
| 10 | Amazon EKS | digital channels | $54,000 | Azure Kubernetes Service (AKS) | exact | medium | medium | Kubernetes API is portable; ingress, IAM integration, storage classes and networking plugins are not. |
| 11 | AWS Lambda | event glue and notifications | $33,000 | Azure Functions | exact | high | high | Triggers, bindings, IAM and event payload formats are proprietary; expect rewrite of glue code. |
| 12 | AWS CloudHSM | card PIN and signing keys | $24,000 | Azure Dedicated HSM / Managed HSM | exact | high | medium |  |
| 13 | Amazon CloudWatch | observability | $31,000 | Azure Monitor | exact | medium | medium |  |
| 14 | Amazon Bedrock | agent assist | $29,000 | Azure AI Foundry (including Azure OpenAI) | exact | medium | high | Model availability differs sharply by provider and region; prompts, guardrails and evaluation sets need re-validation after any move. |
| 15 | Amazon S3 | data lake landing zone | $48,000 | Azure Blob Storage | exact | low | low | S3 API compatibility is widespread; data egress fees, not technology, dominate exit cost. |
| 16 | AWS Fargate | internal APIs | $21,000 | Azure Container Apps | exact | medium | medium |  |
| 17 | AWS Step Functions | loan origination workflow | $14,000 | Azure Logic Apps / Durable Functions | exact | high | high | Workflow definition languages are proprietary and embed service integrations; treat as a rewrite. |
| 18 | Amazon EBS | VM volumes | $37,000 | Azure Managed Disks | exact | low | low |  |
| 19 | Amazon Kinesis Data Streams | clickstream | $18,000 | Azure Event Hubs | exact | medium | medium |  |
| 20 | Amazon QuickSight | exec dashboards | $11,000 | Power BI | exact | high | high |  |
| 21 | AWS Direct Connect | data center links | $16,000 | Azure ExpressRoute | exact | medium | low |  |
| 22 | AWS Network Firewall | egress inspection | $13,000 | Azure Firewall | exact | medium | medium |  |
| 23 | Amazon EFS | shared batch files | $12,000 | Azure Files / Azure NetApp Files | exact | medium | low |  |
| 24 | Amazon CloudFront | online banking edge | $22,000 | Azure Front Door | exact | low | low |  |
| 25 | AWS Backup | backups | $10,000 | Azure Backup | exact | medium | medium |  |
| 26 | AWS WAF | web protection | $9,000 | Azure Web Application Firewall | exact | medium | medium |  |
| 27 | Amazon EventBridge | domain events | $6,000 | Azure Event Grid | exact | high | high |  |
| 28 | Amazon GuardDuty | threat detection | $8,000 | Microsoft Defender for Cloud | exact | medium | medium |  |
| 29 | Amazon Textract | KYC document intake | $8,000 | Azure AI Document Intelligence | exact | medium | medium |  |
| 30 | AWS Transit Gateway | network hub | $7,000 | Azure Virtual WAN | exact | medium | medium |  |
| 31 | AWS Config | config compliance | $6,000 | Azure Policy / Azure Resource Graph | exact | medium | medium |  |
| 32 | AWS KMS | encryption keys | $6,000 | Azure Key Vault (Keys) | exact | medium | medium | Keys generated inside a managed KMS generally cannot be exported; plan key import or re-encryption. |
| 33 | AWS Security Hub | posture management | $5,000 | Microsoft Defender for Cloud (CSPM) | exact | medium | medium |  |
| 34 | Amazon SQS | payment queues | $5,000 | Azure Service Bus Queues / Storage Queues | exact | medium | medium |  |
| 35 | Amazon S3 Glacier | 7-year record retention | $9,000 | Blob Storage Archive tier | exact | low | low |  |
| 36 | Amazon SNS | alerts fan-out | $3,000 | Azure Service Bus Topics / Event Grid | close | medium | medium |  |
| 37 | AWS PrivateLink | private service access | $4,000 | Azure Private Link | exact | medium | medium |  |
| 38 | AWS CloudTrail | audit trail | $4,000 | Azure Activity Log | exact | low | low | Examiners ask for this first. Confirm retention, immutability and export to your archive. |
| 39 | AWS Secrets Manager | app credentials | $2,000 | Azure Key Vault (Secrets) | exact | low | low |  |
| 40 | AWS CloudFormation | provisioning | $0 | Azure Resource Manager (ARM) / Bicep | exact | high | high | Native IaC templates do not port. Terraform/OpenTofu is the usual neutral layer but providers and resources still differ. |
| 41 | AWS Organizations | account governance | $0 | Management Groups / Azure Policy / Landing Zones | exact | high | high | Hierarchy models differ (accounts vs subscriptions vs projects vs compartments); your org structure must be redesigned, not copied. |

## Unmatched inventory lines (not in catalog: review manually or contribute a mapping)

- Amazon Quantum Ledger Database ($3,000/mo)
- AWS Mainframe Modernization ($45,000/mo)

_Heuristic output from curated data. Validate with vendor documentation and a proof of concept before committing._
