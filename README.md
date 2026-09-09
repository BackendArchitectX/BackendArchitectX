# Hi, I'm Pranay Kadu 👋

📍 **India** | ⚙️ **Backend & Distributed Systems Engineer** | ☕ **Java / Spring Boot** | 🌐 **Open Source Contributor**

![Java](https://img.shields.io/badge/Java-17%2F21-000000?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-000000?style=flat-square&logo=apachekafka&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)

> I work on backend systems where correctness under concurrency, failure recovery, performance, and operability matter.
>
> My current engineering focus is distributed systems, messaging infrastructure, RPC, transactional storage, and production-grade Java.

---

## Open Source

I contribute to infrastructure projects by reproducing failures, tracing lifecycle and concurrency bugs, implementing focused fixes, and adding regression coverage around the actual failure mode.

### AutoMQ

Kafka-compatible diskless streaming infrastructure.

- ✅ [**#3493 — Skip AutoBalancer metrics reporter on controller-only nodes**](https://github.com/AutoMQ/automq/pull/3493) — **merged**
  - Prevented broker-specific reporter initialization on controller-only processes.
  - Added regression coverage across broker, controller-only, combined-role, and missing-role configurations.

- 🔐 [**#3579 — Add optional Basic authentication to the Prometheus endpoint**](https://github.com/AutoMQ/automq/pull/3579)
  - Adds backward-compatible authentication for `/metrics` while keeping health endpoints public.
  - Covers authentication policy, malformed credentials, configuration validation, and exporter lifecycle.

- 🔄 [**#3555 — Prevent closed StreamReader instances from restoring block state**](https://github.com/AutoMQ/automq/pull/3555)
  - Handles in-flight and post-close readahead races around asynchronous metadata loading.

- 🧹 [**#3542 — Remove redundant topic-cleanup notifications**](https://github.com/AutoMQ/automq/pull/3542)
  - Clarifies metadata callback ownership and removes duplicate cleanup behavior.

### Apache Fluss

Streaming storage and real-time analytics infrastructure.

- 🌐 [**#4263 — Handle endpoint changes for cached server connections**](https://github.com/apache/fluss/pull/4263)
  - Makes Netty RPC connection identity endpoint-aware when the same logical server moves to a new host or port.
  - Preserves UID-level lifecycle semantics while preventing stale reachable endpoints from being reused.

- 🔗 [**#4230 — Support custom Paimon lake table paths in Spark reads**](https://github.com/apache/fluss/pull/4230)
  - Enables lake reads when Paimon database/table mappings differ from the Fluss table path.
  - Includes lake-only, lake+log union, predicate-pushdown, and compatibility coverage.

### Trino

Distributed SQL query engine.

- ⚡ [**#30973 — Prevent query failure after transaction commit starts**](https://github.com/trinodb/trino/pull/30973)
  - Fixes a race where an external failure could transition an autocommit query to `FAILED` after transaction commit had already begun.
  - Coordinates commit and failure ownership while preserving genuine commit-failure handling.
  - Adds deterministic regression tests for successful commit, commit failure, and delayed result consumption.

**Contribution areas:** concurrency · lifecycle correctness · RPC · transaction state · asynchronous I/O · Kafka internals · Netty · regression testing · observability

---

## Systems Projects

### [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

A workshop-style distributed transactional key-value store built in Java, progressing from storage primitives to transactional consistency.

`Hybrid Logical Clocks` · `MVCC` · `distributed routing` · `transaction records` · `write intents` · `snapshot isolation` · `clock uncertainty` · `read restart` · `serializable conflict prevention`

### [Aegis Insurance Decisioning Platform](https://github.com/BackendArchitectX/Aegis-Insurance-Decision-Platform)

Java 17 + Spring Boot decisioning platform covering policy servicing, claims, premium calculation, risk evaluation, renewal workflows, and auditable decisions.

`Spring Boot` · `REST APIs` · `business rules` · `auditability` · `JUnit` · `Docker` · `Angular`

### [PragyaShield AI Intelligence Platform](https://github.com/BackendArchitectX/PragyaShield-AI-Intelligence-Platform)

Production-minded AI application architecture with deterministic workflows around LLM-assisted features.

`RAG` · `tool routing` · `prompt guardrails` · `PII redaction` · `audit trails` · `fallbacks` · `human-in-the-loop`

---

## What I Work On

- **Distributed systems** — transactions, consistency, metadata, coordination, failure modes, and lifecycle boundaries
- **Backend engineering** — Java, Spring Boot, REST/gRPC APIs, concurrency, SQL, caching, and asynchronous processing
- **Messaging & streaming** — Kafka internals, event-driven systems, backpressure, and reliable processing
- **Performance & reliability** — latency, throughput, database tuning, resource lifecycle, observability, and graceful degradation
- **Cloud-native systems** — Docker, Kubernetes, AWS, CI/CD, health checks, metrics, and production operations
- **AI-backed applications** — using LLMs behind deterministic contracts, guardrails, auditability, and fallback paths rather than treating AI as the system of record

---

## Engineering Principles

```text
Correctness before cleverness.
Failures are part of the design, not edge cases.
Concurrency bugs deserve deterministic tests.
Own resource lifecycle explicitly.
Measure performance before optimizing it.
Keep critical paths observable and reversible.
Prefer boring, maintainable code over fragile sophistication.
```

---

## GitHub Activity

![GitHub contribution graph](https://ghchart.rshah.org/BackendArchitectX)

---

## Connect

📧 **Email:** [pranayp.kadu@gmail.com](mailto:pranayp.kadu@gmail.com)  
🔗 **GitHub:** [github.com/BackendArchitectX](https://github.com/BackendArchitectX)
