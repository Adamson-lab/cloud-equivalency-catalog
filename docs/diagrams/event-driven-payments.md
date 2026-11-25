# Event-driven payments processing

API-fronted, event-driven payment flow with orchestration, HSM-backed signing and low-latency NoSQL state.

Node color = how well that provider's service matches the reference capability: green `exact`, blue `close`, amber `partial`, red dashed `none`. The label repeats the fit as text.

| Provider | Parity for this architecture |
|---|---|
| AWS | 100.0 / 100 |
| Azure | 97.5 / 100 |
| Google Cloud | 92.5 / 100 |
| Oracle Cloud | 71.5 / 100 |

## AWS

```mermaid
flowchart LR
  subgraph G0["Entry"]
    n_api["API gateway / management<br/><b>Amazon API Gateway</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Compute"]
    n_fn["Serverless functions (FaaS)<br/><b>AWS Lambda</b><br/><i>exact</i>"]:::exact
    n_svc["Serverless containers<br/><b>AWS Fargate / Amazon ECS</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Orchestration"]
    n_flow["Serverless workflow orchestration<br/><b>AWS Step Functions</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Messaging"]
    n_bus["Event bus / event routing<br/><b>Amazon EventBridge</b><br/><i>exact</i>"]:::exact
    n_queue["Message queue<br/><b>Amazon SQS</b><br/><i>exact</i>"]:::exact
    n_fanout["Publish/subscribe notifications<br/><b>Amazon SNS</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Data"]
    n_state["Key-value / wide-column NoSQL<br/><b>Amazon DynamoDB</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Security"]
    n_hsm["Dedicated HSM<br/><b>AWS CloudHSM</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>AWS CloudTrail</b><br/><i>exact</i>"]:::exact
  end
  n_api --> n_fn
  n_fn --> n_bus
  n_bus --> n_flow
  n_flow --> n_queue
  n_queue --> n_svc
  n_svc --> n_state
  n_svc --> n_hsm
  n_flow --> n_fanout
  n_fn --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Azure

```mermaid
flowchart LR
  subgraph G0["Entry"]
    n_api["API gateway / management<br/><b>Azure API Management</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Compute"]
    n_fn["Serverless functions (FaaS)<br/><b>Azure Functions</b><br/><i>exact</i>"]:::exact
    n_svc["Serverless containers<br/><b>Azure Container Apps</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Orchestration"]
    n_flow["Serverless workflow orchestration<br/><b>Azure Logic Apps / Durable Functions</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Messaging"]
    n_bus["Event bus / event routing<br/><b>Azure Event Grid</b><br/><i>exact</i>"]:::exact
    n_queue["Message queue<br/><b>Azure Service Bus Queues / Storage Queues</b><br/><i>exact</i>"]:::exact
    n_fanout["Publish/subscribe notifications<br/><b>Azure Service Bus Topics / Event Grid</b><br/><i>close</i>"]:::close
  end
  subgraph G4["Data"]
    n_state["Key-value / wide-column NoSQL<br/><b>Azure Cosmos DB for NoSQL / Table</b><br/><i>exact</i>"]:::exact
  end
  subgraph G5["Security"]
    n_hsm["Dedicated HSM<br/><b>Azure Dedicated HSM / Managed HSM</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>Azure Activity Log</b><br/><i>exact</i>"]:::exact
  end
  n_api --> n_fn
  n_fn --> n_bus
  n_bus --> n_flow
  n_flow --> n_queue
  n_queue --> n_svc
  n_svc --> n_state
  n_svc --> n_hsm
  n_flow --> n_fanout
  n_fn --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Google Cloud

```mermaid
flowchart LR
  subgraph G0["Entry"]
    n_api["API gateway / management<br/><b>Apigee / API Gateway</b><br/><i>exact</i>"]:::exact
  end
  subgraph G1["Compute"]
    n_fn["Serverless functions (FaaS)<br/><b>Cloud Run functions (formerly Cloud Functions)</b><br/><i>exact</i>"]:::exact
    n_svc["Serverless containers<br/><b>Cloud Run</b><br/><i>exact</i>"]:::exact
  end
  subgraph G2["Orchestration"]
    n_flow["Serverless workflow orchestration<br/><b>Workflows</b><br/><i>exact</i>"]:::exact
  end
  subgraph G3["Messaging"]
    n_bus["Event bus / event routing<br/><b>Eventarc</b><br/><i>exact</i>"]:::exact
    n_queue["Message queue<br/><b>Pub/Sub (pull subscriptions) / Cloud Tasks</b><br/><i>close</i>"]:::close
    n_fanout["Publish/subscribe notifications<br/><b>Pub/Sub</b><br/><i>exact</i>"]:::exact
  end
  subgraph G4["Data"]
    n_state["Key-value / wide-column NoSQL<br/><b>Cloud Bigtable / Firestore</b><br/><i>close</i>"]:::close
  end
  subgraph G5["Security"]
    n_hsm["Dedicated HSM<br/><b>Cloud HSM / Cloud External Key Manager</b><br/><i>close</i>"]:::close
    n_audit["Control-plane audit logging<br/><b>Cloud Audit Logs</b><br/><i>exact</i>"]:::exact
  end
  n_api --> n_fn
  n_fn --> n_bus
  n_bus --> n_flow
  n_flow --> n_queue
  n_queue --> n_svc
  n_svc --> n_state
  n_svc --> n_hsm
  n_flow --> n_fanout
  n_fn --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

## Oracle Cloud

```mermaid
flowchart LR
  subgraph G0["Entry"]
    n_api["API gateway / management<br/><b>OCI API Gateway</b><br/><i>close</i>"]:::close
  end
  subgraph G1["Compute"]
    n_fn["Serverless functions (FaaS)<br/><b>OCI Functions</b><br/><i>close</i>"]:::close
    n_svc["Serverless containers<br/><b>OCI Container Instances</b><br/><i>partial</i>"]:::partial
  end
  subgraph G2["Orchestration"]
    n_flow["Serverless workflow orchestration<br/><b>No first-party equivalent</b><br/><i>none</i>"]:::none
  end
  subgraph G3["Messaging"]
    n_bus["Event bus / event routing<br/><b>OCI Events</b><br/><i>close</i>"]:::close
    n_queue["Message queue<br/><b>OCI Queue</b><br/><i>exact</i>"]:::exact
    n_fanout["Publish/subscribe notifications<br/><b>OCI Notifications</b><br/><i>close</i>"]:::close
  end
  subgraph G4["Data"]
    n_state["Key-value / wide-column NoSQL<br/><b>OCI NoSQL Database</b><br/><i>close</i>"]:::close
  end
  subgraph G5["Security"]
    n_hsm["Dedicated HSM<br/><b>OCI Dedicated KMS (HSM)</b><br/><i>exact</i>"]:::exact
    n_audit["Control-plane audit logging<br/><b>OCI Audit</b><br/><i>exact</i>"]:::exact
  end
  n_api --> n_fn
  n_fn --> n_bus
  n_bus --> n_flow
  n_flow --> n_queue
  n_queue --> n_svc
  n_svc --> n_state
  n_svc --> n_hsm
  n_flow --> n_fanout
  n_fn --> n_audit
  style G0 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G1 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G2 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G3 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G4 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  style G5 fill:none,stroke:#8b949e,stroke-dasharray:3 3
  classDef exact fill:#e3f6ea,stroke:#0a7d3b,color:#0b2e1a;
  classDef close fill:#e4eefc,stroke:#1f5fbf,color:#0d2447;
  classDef partial fill:#fff0d6,stroke:#a15c00,color:#4a2b00;
  classDef none fill:#fde7e5,stroke:#b3261e,color:#4a0f0b,stroke-dasharray:5 3;
```

