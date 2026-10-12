<!-- GitHub profile README · BackendArchitectX · October 2026 -->

<div align="center">
  <img src="./assets/pranay-editorial-masthead-v4.svg" alt="Pranay Kadu — Backend and Distributed Systems Engineer" width="100%" />
</div>

<p align="center">
  <a href="https://www.linkedin.com/in/pranaykadu">LinkedIn</a> ·
  <a href="https://backendarchitectx.github.io/">Portfolio</a> ·
  <a href="mailto:pranaykadu.softwareengineer@gmail.com">Email</a> ·
  <a href="https://github.com/BackendArchitectX?tab=repositories">Repositories</a>
</p>

### Hi, I'm Pranay 👋

I'm a software engineer based in India, focused on **Java, Spring Boot, distributed systems, and production reliability**. I enjoy problems where the difficult part is not writing the happy path, but making concurrency, recovery, performance, and operational behavior predictable.

**What I work on:** transactional APIs · event-driven services · Kafka and Redis · SQL performance · JVM diagnostics · fault tolerance · repeatable tests.

## Selected engineering projects

| Project | What I'm building |
| --- | --- |
| **[Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)** | Exact GPU vector search with **CUDA, C++20, JNI, and Spring Boot**. Persistent indexes, FP16 storage, Top-K kernels, and documented benchmarks. |
| **[NUMEN](https://github.com/BackendArchitectX/NUMEN)** | Data-intelligence workflow with a **Java backend**, permitted-source collection, provenance, validation, and a web interface. |
| **[Aegis Insurance Decisioning](https://github.com/BackendArchitectX/Aegis-Insurance-Decision-Platform)** | Full-stack insurance workflows for policies, premiums, claims, renewals, and auditable decisions. |
| **[BedRock](https://github.com/BackendArchitectX/BedRock)** | **Early-stage Go prototype** for local-first AI-assisted software-engineering workflows with bounded edits, verification, and rollback. |
| **[CHAIN//REACTION](https://github.com/BackendArchitectX/CHAIN-REACTION)** | Synthetic infrastructure-resilience simulation with causal dependencies, counterfactual comparisons, and deterministic safety checks. |

Also exploring [distributed transaction internals](https://github.com/BackendArchitectX/distrib-txn-db): hybrid logical clocks, MVCC, transaction conflicts, and deterministic failure scenarios.

## Open-source contributions

I work on reproducible bugs, lifecycle boundaries, race conditions, RPC behavior, and reliable CI—not just code that passes the happy path.

**Merged upstream**

- **[AutoMQ #3493](https://github.com/AutoMQ/automq/pull/3493)** — Prevented the metrics reporter from starting on controller-only nodes.
- **[AutoMQ #3542](https://github.com/AutoMQ/automq/pull/3542)** — Clarified callback ownership and removed redundant topic cleanup logic.

**Under review**

- **[Trino #30973](https://github.com/trinodb/trino/pull/30973)** — Proposed changes to prevent query failure after transaction commit begins.
- **[Apache Fluss #4263](https://github.com/apache/fluss/pull/4263)** — Proposed endpoint-aware identity handling for cached RPC connections.
- **[AutoMQ #3579](https://github.com/AutoMQ/automq/pull/3579)** — Proposed optional Basic authentication for the Prometheus metrics endpoint.
- **[AutoMQ #3555](https://github.com/AutoMQ/automq/pull/3555)** — Proposed guard against restoring blocks after a stream reader closes.

**Investigations and upstream impact**

- **[DJV #919](https://github.com/grizzlypeak3d/DJV/pull/919)** — Investigated Information-panel search, built regression tests and GUI evidence, and identified a PR workflow that could pass without running tests. The maintainer acknowledged the CI finding and independently implemented smaller search and workflow fixes on `main`. **My PR was closed without merging.**

## Toolbox

| Area | Technologies and practices |
| --- | --- |
| **Backend** | Java 8/11/17, Spring Boot, Spring MVC, JPA/Hibernate, REST APIs, SQL |
| **Distributed systems** | Kafka, Redis, messaging, transactions, idempotency, retries, circuit breakers |
| **Data & performance** | PostgreSQL, MySQL, query tuning, caching, JVM profiling, concurrency |
| **Cloud & delivery** | AWS, Docker, Kubernetes, Jenkins, GitHub Actions, CI/CD |
| **Testing & observability** | JUnit 5, Mockito, regression testing, structured logs, Splunk, Dynatrace |
| **Additional languages** | Python, C++, TypeScript/JavaScript, Go |

## How I approach engineering

> **Build for failure. Measure before optimizing. Preserve the invariant.**

I prefer the smallest design that solves the verified problem, with explicit ownership, meaningful regression tests, clear failure semantics, and evidence that survives code review.

## GitHub activity

![Contribution activity for BackendArchitectX](https://ghchart.rshah.org/BackendArchitectX)

---

<p align="center">
  <strong>Open to thoughtful engineering collaboration and open-source reviews.</strong><br/>
  <a href="https://www.linkedin.com/in/pranaykadu">Connect on LinkedIn</a> ·
  <a href="mailto:pranaykadu.softwareengineer@gmail.com">Get in touch</a>
</p>
