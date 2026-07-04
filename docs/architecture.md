# System Architecture

## Overview

The Identity OS is structured as a layered platform. Each layer builds on the one below it, and all layers are independently consumable.

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│   (developer apps, AI agent frameworks, enterprise UIs) │
├─────────────────────────────────────────────────────────┤
│                 Collaboration Layer                      │
│         Sessions · Delegation · Intent Graphs           │
├─────────────────────────────────────────────────────────┤
│                   Agent Layer                            │
│       Agent Identity · Lifecycle · Capabilities         │
├─────────────────────────────────────────────────────────┤
│                  Identity Layer                          │
│    Identity Primitives · Attestation · Federation        │
├─────────────────────────────────────────────────────────┤
│                  Platform Core                           │
│       Registry · Event Bus · Audit Log · Storage        │
└─────────────────────────────────────────────────────────┘
```

---

## Layer Descriptions

### Platform Core

The lowest layer provides infrastructure primitives:

- **Registry** — a pluggable store for identity and agent records. Default: in-memory; production: PostgreSQL or any key-value store.
- **Event Bus** — an asynchronous event stream. Every identity lifecycle event (created, verified, delegated, revoked) is published. Default: in-process; production: Kafka, Redis Streams, or NATS.
- **Audit Log** — append-only, tamper-evident log of all actions. Structured as OTEL-compatible spans.
- **Storage** — abstract storage interface for credentials, trust anchors, and agent state.

### Identity Layer

The identity layer defines the core data model:

- **`Identity`** — the atomic unit. Carries a unique ID, kind (`HUMAN`, `ORGANISATION`, `AI_AGENT`, `SERVICE`), metadata, and one or more credentials.
- **`Credential`** — a verifiable assertion about an identity (e.g., email verified, domain ownership, organisational affiliation).
- **`TrustAssertion`** — a time-bounded, contextual statement that one identity trusts another to perform a specific set of actions.
- **Federation** — adapters that translate external identity tokens (OIDC JWTs, SAML assertions, W3C DIDs) into `Identity` objects.

### Agent Layer

Extends the identity layer for AI agents:

- **`Agent`** — an `Identity` of kind `AI_AGENT`. Carries additional metadata: model provider, capability manifest, owning human identity.
- **`Capability`** — a declared action or resource scope an agent is designed to exercise. Capabilities must be granted by a human identity before use.
- **`AgentLifecycle`** — state machine: `PENDING → ACTIVE → SUSPENDED → REVOKED`. Lifecycle transitions are event-sourced.

### Collaboration Layer

Provides primitives for multi-participant interactions:

- **`Session`** — a bounded context in which a set of identities (human and agent) collaborate toward a declared goal.
- **`DelegationChain`** — an auditable chain showing how authority flows from a root human identity through any number of agents.
- **`IntentGraph`** — a directed acyclic graph of declared intents, sub-tasks, and outcomes. Provides traceability from high-level goal to atomic action.

### Application Layer

The application layer is not owned by this platform. It is where developers, enterprises, and AI frameworks integrate the Identity OS. SDKs provide idiomatic bindings for Python and TypeScript.

---

## Data Model

```
Identity
├── id: UUID
├── name: str
├── kind: IdentityKind (HUMAN | ORGANISATION | AI_AGENT | SERVICE)
├── credentials: List[Credential]
├── created_at: datetime
└── metadata: Dict[str, Any]

Agent (extends Identity, kind=AI_AGENT)
├── owner: Identity          ← the human who registered this agent
├── model_provider: str      ← e.g. "openai", "anthropic", "local"
├── capabilities: List[Capability]
└── lifecycle: AgentLifecycle

Session
├── id: UUID
├── participants: List[Identity]
├── goal: str
├── delegation_chain: DelegationChain
├── intent_graph: IntentGraph
├── started_at: datetime
└── ended_at: Optional[datetime]
```

---

## Security Model

### Threat Model

The Identity OS assumes an **adversarial environment**:

- API clients may be compromised.
- Agent identities may be stolen or spoofed.
- Delegation chains may be forged if not cryptographically bound.

### Defences

| Threat | Defence |
|--------|---------|
| Identity spoofing | Cryptographic signing of identity tokens (Ed25519 by default) |
| Delegation forgery | Delegation assertions are signed by the delegating identity |
| Privilege escalation | Capabilities are additive but bounded by the owner's own authority |
| Replay attacks | All tokens are time-bounded with a `jti` (JWT ID) nonce |
| Audit tampering | Append-only log with cryptographic chaining (hash of previous entry) |

---

## Extensibility

The platform is designed for extensibility at every layer:

- **Pluggable storage backends** — implement `StorageBackend` to use any database.
- **Pluggable event transports** — implement `EventTransport` to use any message broker.
- **Pluggable federation adapters** — implement `FederationAdapter` to add new external IdP support.
- **Custom capability verifiers** — implement `CapabilityVerifier` to define domain-specific capability checks.

---

## Deployment Topologies

### Embedded (development / testing)
All components run in-process. No external dependencies.

### Containerised (production)
Platform Core services run as Docker containers, orchestrated by Kubernetes. The Python/TypeScript SDKs communicate over gRPC.

### Managed (cloud service)
Platform Core is hosted and operated by the Identity OS team. Customers interact exclusively through the SDK.
