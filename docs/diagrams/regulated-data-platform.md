# Regulated bank data and analytics platform

Private-connected analytics platform with customer-held keys, governed data and security analytics, the shape regulators scrutinize in exit-plan reviews.

Node color = how well that provider's service matches the reference capability: green `exact`, blue `close`, amber `partial`, red dashed `none`. The label repeats the fit as text.

| Provider | Parity for this architecture |
|---|---|
| AWS | 93.9 / 100 |
| Azure | 96.4 / 100 |
| Google Cloud | 96.4 / 100 |
| Oracle Cloud | 88.6 / 100 |

## AWS

```mermaid
flowchart LR
  subgraph G0["Connectivity"]
    n_link["Dedicated private connectivity<br/><b>AWS Direct Connect</b><br/><i>exact</i>"]:::exact
    n_hub["Network transit hub<br/><b>AWS Transit Gateway</b><br/><i>exact</i>"]:::exact
    n_pe["Private service endpoints<br/><b>AWS PrivateLink</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Ingest"]
    n_stream["Event streaming<br/><b>Amazon Kinesis Data Streams</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Storage"]
    n_lake["Object storage<br/><b>Amazon S3</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Processing"]
    n_spark["Managed big-data processing (Spark/Hadoop)<br/><b>Amazon EMR</b><br/><i>exact</i>"]:::exact
    n_dw["Cloud data warehouse<br/><b>Amazon Redshift</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Consumption"]
    n_bi["Business intelligence<br/><b>Amazon QuickSight</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Governance"]
    n_catalog["Data catalog and governance<br/><b>AWS Glue Data Catalog / Amazon DataZone / SageMaker Catalog</b><br/><i>close</i>"]:::close
  end
  subgraph G6["Security"]
    n_kms["Key management service<br/><b>AWS KMS</b><br/><i>exact</i>"]:::exact
    n_xkey["Customer-held external key control<br/><b>AWS KMS External Key Store (XKS)</b><br/><i>exact</i>"]:::exact
    n_iam["Cloud identity and access management<br/><b>AWS IAM / IAM Identity Center</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>AWS CloudTrail</b><br/><i>exact</i>"]:::exact
    n_siem["Cloud-native SIEM / SecOps<br/><b>Amazon Security Lake with partner SIEM / Amazon Detective</b><br/><i>partial</i>"]:::partial
  end
  n_link --> n_hub
  n_hub --> n_pe
  n_pe --> n_lake
  n_stream --> n_lake
  n_lake --> n_spark
  n_spark --> n_dw
  n_dw --> n_bi
  n_catalog --> n_dw
  n_xkey --> n_kms
  n_kms --> n_lake
  n_kms --> n_dw
  n_iam --> n_dw
  n_audit --> n_siem
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G6 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Azure

```mermaid
flowchart LR
  subgraph G0["Connectivity"]
    n_link["Dedicated private connectivity<br/><b>Azure ExpressRoute</b><br/><i>exact</i>"]:::exact
    n_hub["Network transit hub<br/><b>Azure Virtual WAN</b><br/><i>exact</i>"]:::exact
    n_pe["Private service endpoints<br/><b>Azure Private Link</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Ingest"]
    n_stream["Event streaming<br/><b>Azure Event Hubs</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Storage"]
    n_lake["Object storage<br/><b>Azure Blob Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Processing"]
    n_spark["Managed big-data processing (Spark/Hadoop)<br/><b>Azure Databricks / Synapse Spark / HDInsight</b><br/><i>close</i>"]:::close
    n_dw["Cloud data warehouse<br/><b>Microsoft Fabric Warehouse / Azure Synapse Analytics</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Consumption"]
    n_bi["Business intelligence<br/><b>Power BI</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Governance"]
    n_catalog["Data catalog and governance<br/><b>Microsoft Purview</b><br/><i>exact</i>"]:::exact
  end
  subgraph G6["Security"]
    n_kms["Key management service<br/><b>Azure Key Vault (Keys)</b><br/><i>exact</i>"]:::exact
    n_xkey["Customer-held external key control<br/><b>Azure Key Vault Managed HSM / Customer Key controls</b><br/><i>close</i>"]:::close
    n_iam["Cloud identity and access management<br/><b>Microsoft Entra ID with Azure RBAC</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Azure Activity Log</b><br/><i>exact</i>"]:::exact
    n_siem["Cloud-native SIEM / SecOps<br/><b>Microsoft Sentinel</b><br/><i>exact</i>"]:::exact
  end
  n_link --> n_hub
  n_hub --> n_pe
  n_pe --> n_lake
  n_stream --> n_lake
  n_lake --> n_spark
  n_spark --> n_dw
  n_dw --> n_bi
  n_catalog --> n_dw
  n_xkey --> n_kms
  n_kms --> n_lake
  n_kms --> n_dw
  n_iam --> n_dw
  n_audit --> n_siem
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G6 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Google Cloud

```mermaid
flowchart LR
  subgraph G0["Connectivity"]
    n_link["Dedicated private connectivity<br/><b>Cloud Interconnect</b><br/><i>exact</i>"]:::exact
    n_hub["Network transit hub<br/><b>Network Connectivity Center</b><br/><i>close</i>"]:::close
    n_pe["Private service endpoints<br/><b>Private Service Connect</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Ingest"]
    n_stream["Event streaming<br/><b>Pub/Sub</b><br/><i>close</i>"]:::close
  end
  subgraph G2["Storage"]
    n_lake["Object storage<br/><b>Cloud Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Processing"]
    n_spark["Managed big-data processing (Spark/Hadoop)<br/><b>Dataproc / Serverless for Apache Spark</b><br/><i>exact</i>"]:::exact
    n_dw["Cloud data warehouse<br/><b>BigQuery</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Consumption"]
    n_bi["Business intelligence<br/><b>Looker / Looker Studio</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Governance"]
    n_catalog["Data catalog and governance<br/><b>Dataplex Universal Catalog</b><br/><i>exact</i>"]:::exact
  end
  subgraph G6["Security"]
    n_kms["Key management service<br/><b>Cloud KMS</b><br/><i>exact</i>"]:::exact
    n_xkey["Customer-held external key control<br/><b>Cloud External Key Manager (EKM)</b><br/><i>exact</i>"]:::exact
    n_iam["Cloud identity and access management<br/><b>Cloud IAM</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Cloud Audit Logs</b><br/><i>exact</i>"]:::exact
    n_siem["Cloud-native SIEM / SecOps<br/><b>Google Security Operations</b><br/><i>exact</i>"]:::exact
  end
  n_link --> n_hub
  n_hub --> n_pe
  n_pe --> n_lake
  n_stream --> n_lake
  n_lake --> n_spark
  n_spark --> n_dw
  n_dw --> n_bi
  n_catalog --> n_dw
  n_xkey --> n_kms
  n_kms --> n_lake
  n_kms --> n_dw
  n_iam --> n_dw
  n_audit --> n_siem
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G6 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Oracle Cloud

```mermaid
flowchart LR
  subgraph G0["Connectivity"]
    n_link["Dedicated private connectivity<br/><b>OCI FastConnect</b><br/><i>exact</i>"]:::exact
    n_hub["Network transit hub<br/><b>Dynamic Routing Gateway (DRG)</b><br/><i>close</i>"]:::close
    n_pe["Private service endpoints<br/><b>OCI Private Endpoints / Service Gateway</b><br/><i>close</i>"]:::close
  end
  subgraph G1["Ingest"]
    n_stream["Event streaming<br/><b>OCI Streaming</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Storage"]
    n_lake["Object storage<br/><b>OCI Object Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Processing"]
    n_spark["Managed big-data processing (Spark/Hadoop)<br/><b>OCI Data Flow</b><br/><i>exact</i>"]:::exact
    n_dw["Cloud data warehouse<br/><b>Oracle Autonomous Data Warehouse</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Consumption"]
    n_bi["Business intelligence<br/><b>Oracle Analytics Cloud</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Governance"]
    n_catalog["Data catalog and governance<br/><b>OCI Data Catalog</b><br/><i>close</i>"]:::close
  end
  subgraph G6["Security"]
    n_kms["Key management service<br/><b>OCI Vault</b><br/><i>exact</i>"]:::exact
    n_xkey["Customer-held external key control<br/><b>OCI External Key Management Service</b><br/><i>close</i>"]:::close
    n_iam["Cloud identity and access management<br/><b>OCI IAM (identity domains)</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>OCI Audit</b><br/><i>exact</i>"]:::exact
    n_siem["Cloud-native SIEM / SecOps<br/><b>OCI Logging Analytics with partner SIEM</b><br/><i>partial</i>"]:::partial
  end
  n_link --> n_hub
  n_hub --> n_pe
  n_pe --> n_lake
  n_stream --> n_lake
  n_lake --> n_spark
  n_spark --> n_dw
  n_dw --> n_bi
  n_catalog --> n_dw
  n_xkey --> n_kms
  n_kms --> n_lake
  n_kms --> n_dw
  n_iam --> n_dw
  n_audit --> n_siem
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G6 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

