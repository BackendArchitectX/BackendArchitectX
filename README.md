# Pranay Kadu

**Backend & Distributed Systems Engineer** · Java · Streaming · Transactions · Reliability

I work on systems where **concurrency, lifecycle boundaries, failure recovery, throughput, and operability** matter.

`Java 17/21` · `Spring Boot` · `Kafka` · `Netty/gRPC` · `SQL/Redis` · `Docker/Kubernetes` · `AWS`

---

## Open Source — Selected Work

| Project | Work | Status |
|---|---|---|
| **AutoMQ** | [#3493 — Skip AutoBalancer metrics reporter on controller-only nodes](https://github.com/AutoMQ/automq/pull/3493) | **Merged** |
| **AutoMQ** | [#3579 — Optional Basic auth for Prometheus metrics](https://github.com/AutoMQ/automq/pull/3579) | Open PR |
| **AutoMQ** | [#3555 — Prevent closed StreamReader from restoring block state](https://github.com/AutoMQ/automq/pull/3555) | Open PR |
| **Apache Fluss** | [#4263 — Endpoint-aware Netty connection caching](https://github.com/apache/fluss/pull/4263) | Open PR |
| **Apache Fluss** | [#4230 — Custom Paimon lake paths for Spark reads](https://github.com/apache/fluss/pull/4230) | Open PR |
| **Trino** | [#30973 — Prevent query failure after transaction commit starts](https://github.com/trinodb/trino/pull/30973) | Open PR |

The recurring themes are **race conditions, asynchronous lifecycle, RPC identity, transaction state, metadata ownership, and regression tests that reproduce the failure mode deterministically**.

---

## Original Systems Work

### [Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)

GPU-accelerated exact vector search built across **CUDA → C++20 → JNI → Java → Spring Boot**.

- Persistent GPU-resident FP32/FP16 indexes
- Hierarchical/fused Top-K kernels and query-tiled batched search
- Pinned memory and asynchronous CUDA streams
- JNI lifecycle management with `AutoCloseable`
- Reproducible latency, throughput, storage, and recall benchmarks
- REST API with validation, health, metrics, request IDs, and capacity guards

Validated on an RTX 3050 with a documented benchmark harness; the repository explicitly separates measured results from broader performance claims.

### [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

A workshop-style Java transactional key-value store that builds the mechanisms in stages:

`HLC` → `MVCC` → `distributed routing` → `transaction records` → `write intents` → `snapshot isolation` → `clock uncertainty` → `read restart` → `serializable conflict prevention`

The project demonstrates anomalies first, then introduces the mechanism that prevents them.

---

## Engineering Focus

```text
Distributed systems      Concurrency & async lifecycle
Kafka / streaming        RPC / Netty / gRPC
Transactions & MVCC      Java / Spring Boot
Performance engineering  SQL / Redis / caching
Observability            Docker / Kubernetes / AWS
Production operations    Deterministic regression testing
```

> Correctness before cleverness. Make failure states explicit. Own resource lifecycle. Test races deterministically.

---

![GitHub contribution graph](https://ghchart.rshah.org/BackendArchitectX)

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)
