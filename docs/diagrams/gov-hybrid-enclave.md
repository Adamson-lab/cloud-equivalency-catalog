# Federal hybrid enclave

Government-cloud enclave extended to on-premises infrastructure with HSM-backed keys and centralized security monitoring.

Node color = how well that provider's service matches the reference capability: green `exact`, blue `close`, amber `partial`, red dashed `none`. The label repeats the fit as text.

| Provider | Parity for this architecture |
|---|---|
| AWS | 100.0 / 100 |
| Azure | 100.0 / 100 |
| Google Cloud | 91.5 / 100 |
| Oracle Cloud | 95.0 / 100 |

## AWS

```mermaid
flowchart LR
  subgraph G0["Hybrid"]
    n_onprem["Cloud-managed on-premises infrastructure<br/><b>AWS Outposts</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Connectivity"]
    n_vpn["Site-to-site VPN<br/><b>AWS Site-to-Site VPN</b><br/><i>exact</i>"]:::exact
    n_link["Dedicated private connectivity<br/><b>AWS Direct Connect</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Enclave"]
    n_gov["US government cloud environment<br/><b>AWS GovCloud (US) / AWS Secret and Top Secret regions</b><br/><i>exact</i>"]:::exact
    n_fw["Managed network firewall<br/><b>AWS Network Firewall</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Security"]
    n_iam["Cloud identity and access management<br/><b>AWS IAM / IAM Identity Center</b><br/><i>exact</i>"]:::exact
    n_kms["Key management service<br/><b>AWS KMS</b><br/><i>exact</i>"]:::exact
    n_hsm["Dedicated HSM<br/><b>AWS CloudHSM</b><br/><i>exact</i>"]:::exact
    n_threat["Cloud threat detection<br/><b>Amazon GuardDuty</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>AWS CloudTrail</b><br/><i>exact</i>"]:::exact
  end
  n_onprem --> n_link
  n_onprem --> n_vpn
  n_link --> n_fw
  n_vpn --> n_fw
  n_fw --> n_gov
  n_iam --> n_gov
  n_kms --> n_gov
  n_hsm --> n_kms
  n_gov --> n_threat
  n_gov --> n_audit
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
  subgraph G0["Hybrid"]
    n_onprem["Cloud-managed on-premises infrastructure<br/><b>Azure Local with Azure Arc</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Connectivity"]
    n_vpn["Site-to-site VPN<br/><b>Azure VPN Gateway</b><br/><i>exact</i>"]:::exact
    n_link["Dedicated private connectivity<br/><b>Azure ExpressRoute</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Enclave"]
    n_gov["US government cloud environment<br/><b>Azure Government / Azure Government Secret and Top Secret</b><br/><i>exact</i>"]:::exact
    n_fw["Managed network firewall<br/><b>Azure Firewall</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Security"]
    n_iam["Cloud identity and access management<br/><b>Microsoft Entra ID with Azure RBAC</b><br/><i>exact</i>"]:::exact
    n_kms["Key management service<br/><b>Azure Key Vault (Keys)</b><br/><i>exact</i>"]:::exact
    n_hsm["Dedicated HSM<br/><b>Azure Dedicated HSM / Managed HSM</b><br/><i>exact</i>"]:::exact
    n_threat["Cloud threat detection<br/><b>Microsoft Defender for Cloud</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Azure Activity Log</b><br/><i>exact</i>"]:::exact
  end
  n_onprem --> n_link
  n_onprem --> n_vpn
  n_link --> n_fw
  n_vpn --> n_fw
  n_fw --> n_gov
  n_iam --> n_gov
  n_kms --> n_gov
  n_hsm --> n_kms
  n_gov --> n_threat
  n_gov --> n_audit
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
  subgraph G0["Hybrid"]
    n_onprem["Cloud-managed on-premises infrastructure<br/><b>Google Distributed Cloud</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Connectivity"]
    n_vpn["Site-to-site VPN<br/><b>Cloud VPN</b><br/><i>exact</i>"]:::exact
    n_link["Dedicated private connectivity<br/><b>Cloud Interconnect</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Enclave"]
    n_gov["US government cloud environment<br/><b>Assured Workloads / Google Distributed Cloud air-gapped</b><br/><i>partial</i>"]:::partial
    n_fw["Managed network firewall<br/><b>Cloud Next Generation Firewall</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Security"]
    n_iam["Cloud identity and access management<br/><b>Cloud IAM</b><br/><i>exact</i>"]:::exact
    n_kms["Key management service<br/><b>Cloud KMS</b><br/><i>exact</i>"]:::exact
    n_hsm["Dedicated HSM<br/><b>Cloud HSM / Cloud External Key Manager</b><br/><i>close</i>"]:::close
    n_threat["Cloud threat detection<br/><b>Security Command Center (Event Threat Detection)</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Cloud Audit Logs</b><br/><i>exact</i>"]:::exact
  end
  n_onprem --> n_link
  n_onprem --> n_vpn
  n_link --> n_fw
  n_vpn --> n_fw
  n_fw --> n_gov
  n_iam --> n_gov
  n_kms --> n_gov
  n_hsm --> n_kms
  n_gov --> n_threat
  n_gov --> n_audit
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
  subgraph G0["Hybrid"]
    n_onprem["Cloud-managed on-premises infrastructure<br/><b>OCI Dedicated Region Cloud@Customer / Compute Cloud@Customer</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Connectivity"]
    n_vpn["Site-to-site VPN<br/><b>OCI Site-to-Site VPN</b><br/><i>exact</i>"]:::exact
    n_link["Dedicated private connectivity<br/><b>OCI FastConnect</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Enclave"]
    n_gov["US government cloud environment<br/><b>Oracle Cloud Government (US Government regions)</b><br/><i>close</i>"]:::close
    n_fw["Managed network firewall<br/><b>OCI Network Firewall</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Security"]
    n_iam["Cloud identity and access management<br/><b>OCI IAM (identity domains)</b><br/><i>exact</i>"]:::exact
    n_kms["Key management service<br/><b>OCI Vault</b><br/><i>exact</i>"]:::exact
    n_hsm["Dedicated HSM<br/><b>OCI Dedicated KMS (HSM)</b><br/><i>exact</i>"]:::exact
    n_threat["Cloud threat detection<br/><b>OCI Threat Intelligence / Cloud Guard</b><br/><i>close</i>"]:::close
    n_audit["Control-plane audit logging<br/><b>OCI Audit</b><br/><i>exact</i>"]:::exact
  end
  n_onprem --> n_link
  n_onprem --> n_vpn
  n_link --> n_fw
  n_vpn --> n_fw
  n_fw --> n_gov
  n_iam --> n_gov
  n_kms --> n_gov
  n_hsm --> n_kms
  n_gov --> n_threat
  n_gov --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

