# Pranay Kadu

**Backend & Distributed Systems Engineer** · Java · Streaming · Transactions · Reliability

[![Java](https://img.shields.io/badge/Java-17%2F21-000?style=flat-square&logo=openjdk&logoColor=white)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![Kafka](https://img.shields.io/badge/Kafka-000?style=flat-square&logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)

I build and debug backend systems where **concurrency, failure recovery, resource lifecycle, throughput, and operability** matter.

My current focus is distributed systems and production-grade Java: Kafka-compatible infrastructure, RPC, transactional state, asynchronous I/O, observability, and deterministic regression testing.

---

## Selected Open Source Work

### AutoMQ — Kafka-compatible streaming infrastructure

- ✅ [**#3493 — controller-only AutoBalancer reporter fix**](https://github.com/AutoMQ/automq/pull/3493) — merged
  Prevented broker-only metrics reporter initialization from breaking controller-only nodes and added role-specific regression coverage.

- 🔐 [**#3579 — Prometheus endpoint authentication**](https://github.com/AutoMQ/automq/pull/3579)
  Added optional backward-compatible Basic authentication with endpoint policy, configuration validation, credential handling, and lifecycle tests.

- 🔄 [**#3555 — StreamReader close/readahead race**](https://github.com/AutoMQ/automq/pull/3555)
  Prevents asynchronous readahead from restoring block state after a reader has crossed its close lifecycle boundary.

### Apache Fluss — streaming storage

- 🌐 [**#4263 — endpoint-aware Netty connection caching**](https://github.com/apache/fluss/pull/4263)
  Prevents a cached RPC connection from continuing to target a stale-but-reachable TabletServer endpoint after metadata changes.

- 🔗 [**#4230 — custom Paimon lake paths for Spark reads**](https://github.com/apache/fluss/pull/4230)
  Supports independent Fluss/Paimon table paths across lake-only reads, lake+log reads, and predicate pushdown.

### Trino — distributed SQL

- ⚡ [**#30973 — transaction commit/failure race**](https://github.com/trinodb/trino/pull/30973)
  Coordinates commit and failure ownership so unrelated failures cannot mark an autocommit query failed after commit has begun.

**Areas:** concurrency · asynchronous lifecycle · RPC · transactions · metadata · Kafka internals · Netty · regression testing

---

## Systems Lab

### [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

A Java workshop that builds a distributed transactional key-value store from first principles:

`HLC` → `MVCC` → `distributed routing` → `transaction records` → `write intents` → `snapshot isolation` → `clock uncertainty` → `read restart` → `serializable conflict prevention`

The project intentionally demonstrates anomalies before introducing the mechanism that fixes them.

---

## Product Engineering

### [Aegis Insurance Decisioning Platform](https://github.com/BackendArchitectX/Aegis-Insurance-Decision-Platform)

Java 17 + Spring Boot decisioning platform for claims, premium calculation, risk evaluation, renewals, and auditable business decisions.

### [PragyaShield AI Intelligence Platform](https://github.com/BackendArchitectX/PragyaShield-AI-Intelligence-Platform)

AI-assisted insurance architecture built around deterministic workflows, RAG, tool routing, guardrails, auditability, fallbacks, and human review.

---

## Engineering Focus

```text
Java / Spring Boot        Distributed systems
Kafka / event streaming   REST / gRPC / Netty
Concurrency               SQL / Redis / caching
Performance tuning        Failure recovery
Docker / Kubernetes       AWS / CI/CD
Observability             Production operations
```

> Correctness before cleverness. Make failure states explicit. Test races deterministically. Own resource lifecycle.

---

## Activity

![GitHub contribution graph](https://ghchart.rshah.org/BackendArchitectX)

---

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)
