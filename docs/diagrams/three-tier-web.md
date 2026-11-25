# Internet-facing three-tier web application

Customer-facing web platform with edge protection, containerized services, managed data stores and secrets.

Node color = how well that provider's service matches the reference capability: green `exact`, blue `close`, amber `partial`, red dashed `none`. The label repeats the fit as text.

| Provider | Parity for this architecture |
|---|---|
| AWS | 100.0 / 100 |
| Azure | 100.0 / 100 |
| Google Cloud | 100.0 / 100 |
| Oracle Cloud | 87.5 / 100 |

## AWS

```mermaid
flowchart LR
  subgraph G0["Edge"]
    n_edge["Content delivery network<br/><b>Amazon CloudFront</b><br/><i>exact</i>"]:::exact
    n_waf["Web application firewall<br/><b>AWS WAF</b><br/><i>exact</i>"]:::exact
    n_lb["Layer-7 load balancer<br/><b>Application Load Balancer</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Application"]
    n_k8s["Managed Kubernetes<br/><b>Amazon EKS</b><br/><i>exact</i>"]:::exact
    n_secrets["Secrets management<br/><b>AWS Secrets Manager</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Data"]
    n_db["Managed relational database<br/><b>Amazon RDS</b><br/><i>exact</i>"]:::exact
    n_cache["Managed in-memory cache<br/><b>Amazon ElastiCache / MemoryDB</b><br/><i>exact</i>"]:::exact
    n_objects["Object storage<br/><b>Amazon S3</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Operations"]
    n_metrics["Metrics and monitoring<br/><b>Amazon CloudWatch</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>AWS CloudTrail</b><br/><i>exact</i>"]:::exact
  end
  n_edge --> n_waf
  n_waf --> n_lb
  n_lb --> n_k8s
  n_k8s --> n_db
  n_k8s --> n_cache
  n_k8s --> n_objects
  n_k8s --> n_secrets
  n_k8s --> n_metrics
  n_k8s --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Azure

```mermaid
flowchart LR
  subgraph G0["Edge"]
    n_edge["Content delivery network<br/><b>Azure Front Door</b><br/><i>exact</i>"]:::exact
    n_waf["Web application firewall<br/><b>Azure Web Application Firewall</b><br/><i>exact</i>"]:::exact
    n_lb["Layer-7 load balancer<br/><b>Azure Application Gateway</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Application"]
    n_k8s["Managed Kubernetes<br/><b>Azure Kubernetes Service (AKS)</b><br/><i>exact</i>"]:::exact
    n_secrets["Secrets management<br/><b>Azure Key Vault (Secrets)</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Data"]
    n_db["Managed relational database<br/><b>Azure SQL Database / Azure Database for PostgreSQL and MySQL</b><br/><i>exact</i>"]:::exact
    n_cache["Managed in-memory cache<br/><b>Azure Managed Redis (successor to Azure Cache for Redis)</b><br/><i>exact</i>"]:::exact
    n_objects["Object storage<br/><b>Azure Blob Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Operations"]
    n_metrics["Metrics and monitoring<br/><b>Azure Monitor</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Azure Activity Log</b><br/><i>exact</i>"]:::exact
  end
  n_edge --> n_waf
  n_waf --> n_lb
  n_lb --> n_k8s
  n_k8s --> n_db
  n_k8s --> n_cache
  n_k8s --> n_objects
  n_k8s --> n_secrets
  n_k8s --> n_metrics
  n_k8s --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Google Cloud

```mermaid
flowchart LR
  subgraph G0["Edge"]
    n_edge["Content delivery network<br/><b>Cloud CDN</b><br/><i>exact</i>"]:::exact
    n_waf["Web application firewall<br/><b>Cloud Armor</b><br/><i>exact</i>"]:::exact
    n_lb["Layer-7 load balancer<br/><b>Cloud Load Balancing (Application Load Balancer)</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Application"]
    n_k8s["Managed Kubernetes<br/><b>Google Kubernetes Engine (GKE)</b><br/><i>exact</i>"]:::exact
    n_secrets["Secrets management<br/><b>Secret Manager</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Data"]
    n_db["Managed relational database<br/><b>Cloud SQL</b><br/><i>exact</i>"]:::exact
    n_cache["Managed in-memory cache<br/><b>Memorystore (Redis / Valkey)</b><br/><i>exact</i>"]:::exact
    n_objects["Object storage<br/><b>Cloud Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Operations"]
    n_metrics["Metrics and monitoring<br/><b>Cloud Monitoring</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Cloud Audit Logs</b><br/><i>exact</i>"]:::exact
  end
  n_edge --> n_waf
  n_waf --> n_lb
  n_lb --> n_k8s
  n_k8s --> n_db
  n_k8s --> n_cache
  n_k8s --> n_objects
  n_k8s --> n_secrets
  n_k8s --> n_metrics
  n_k8s --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Oracle Cloud

```mermaid
flowchart LR
  subgraph G0["Edge"]
    n_edge["Content delivery network<br/><b>No first-party general-purpose CDN</b><br/><i>none</i>"]:::none
    n_waf["Web application firewall<br/><b>OCI Web Application Firewall</b><br/><i>exact</i>"]:::exact
    n_lb["Layer-7 load balancer<br/><b>OCI Load Balancer</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Application"]
    n_k8s["Managed Kubernetes<br/><b>Oracle Container Engine for Kubernetes (OKE)</b><br/><i>exact</i>"]:::exact
    n_secrets["Secrets management<br/><b>OCI Vault (Secrets)</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Data"]
    n_db["Managed relational database<br/><b>OCI Database with MySQL HeatWave / PostgreSQL</b><br/><i>close</i>"]:::close
    n_cache["Managed in-memory cache<br/><b>OCI Cache</b><br/><i>exact</i>"]:::exact
    n_objects["Object storage<br/><b>OCI Object Storage</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Operations"]
    n_metrics["Metrics and monitoring<br/><b>OCI Monitoring</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>OCI Audit</b><br/><i>exact</i>"]:::exact
  end
  n_edge --> n_waf
  n_waf --> n_lb
  n_lb --> n_k8s
  n_k8s --> n_db
  n_k8s --> n_cache
  n_k8s --> n_objects
  n_k8s --> n_secrets
  n_k8s --> n_metrics
  n_k8s --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

