# Product Strategy

## Overview

The Identity Operating System (Identity OS) is a platform-layer product. It does not compete at the application layer. It enables application builders to embed trusted, agent-aware identity into their products with minimal friction.

Our strategy is to win the **identity infrastructure layer** for the agentic AI era, the same way Linux won the server OS layer and TCP/IP won the networking layer: by being open, composable, and indispensable.

---

## Market Context

### The Agentic AI Shift

Large language model (LLM) capabilities have crossed a threshold. AI agents can now autonomously plan, act, and collaborate across multi-step tasks. This shift creates a critical gap:

- Traditional IAM was designed for human users making synchronous requests.
- AI agents are asynchronous, delegating authority, and operating at machine speed.
- No broadly adopted open standard governs *agent identity* — who the agent is, who it acts on behalf of, and what it is authorised to do.

### The Identity Gap

| Dimension | Human IAM today | Agent IAM today | Identity OS target |
|-----------|----------------|-----------------|-------------------|
| Authentication | Strong (MFA, FIDO2) | Weak (API keys, tokens) | Cryptographic identity for all participants |
| Authorisation | Role-based | Ad-hoc | Delegated, contextual, time-bounded |
| Auditability | Partial | Near-zero | Full, tamper-evident, exportable |
| Federation | Mature (OIDC, SAML) | Absent | Protocol-level federation for agents |

---

## Strategic Bets

### Bet 1: Identity is the atom, not the molecule

Other platforms treat identity as one feature among many. We bet that identity — human and agent — is *the* foundational primitive. Every other capability (collaboration, delegation, audit) is derived from it.

### Bet 2: Open source drives adoption, commercial services drive revenue

The core platform is Apache-licensed. Enterprise capabilities (hosted infrastructure, compliance tooling, SLA-backed support) are offered as a managed service. This is the proven playbook for infrastructure platforms (HashiCorp, Elastic, Confluent).

### Bet 3: Agentic AI is a greenfield identity market

Human IAM is a mature, competitive market. Agent IAM is not. We focus there first, then extend backward to improve human identity experiences powered by agent capabilities (e.g., an AI-assisted identity governance agent).

### Bet 4: Developer experience is a moat

Developers choose identity infrastructure based on time-to-working-prototype. We invest heavily in SDKs, documentation, and zero-config defaults. A developer should be able to register an agent identity in 10 lines of code.

---

## Go-to-Market

### Phase 1 — Developer Adoption (Year 1)
- Release open-source Python and TypeScript SDKs.
- Publish end-to-end tutorials for common agentic AI frameworks (LangChain, AutoGen, CrewAI).
- Build a Discord community and open RFC process for protocol design.
- Target: 1,000 GitHub stars, 100 active contributors, 10 reference integrations.

### Phase 2 — Enterprise Pilot (Year 2)
- Launch a managed cloud service with SOC 2 Type II compliance.
- Integrate with enterprise IdPs (Okta, Azure AD, Ping Identity).
- Offer compliance-focused features: GDPR-aware audit export, agent lifecycle management.
- Target: 10 enterprise pilots, $1M ARR.

### Phase 3 — Platform Ecosystem (Year 3+)
- Open a marketplace for certified agent identity providers.
- Launch an industry working group to formalise the Agent Identity Protocol (AIP).
- Target: 50 enterprise customers, $10M ARR, AIP adopted by ≥3 major AI frameworks.

---

## Key Metrics

| Metric | Definition | Year 1 Target |
|--------|-----------|--------------|
| SDK downloads | Total pip/npm installs | 50,000 |
| Active projects | GitHub repos importing identity-os | 500 |
| Agent identities registered | Via all deployments | 10,000 |
| Community contributors | PRs merged from community | 100 |
| Enterprise pilots | Paid or design-partner pilots | 10 |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Large cloud provider launches a competing service | High | High | Focus on open standard + community moat; be protocol-first |
| Standards fragmentation (W3C DID, OpenID for VCs, SPIFFE) | Medium | Medium | Design as an integration layer; adopt and extend existing standards |
| Developer fatigue with yet another identity SDK | Medium | High | Radical simplicity in developer experience; 5-minute quickstart |
| Security vulnerability in core identity primitives | Low | Critical | Formal security review, bug bounty, independent audit |
