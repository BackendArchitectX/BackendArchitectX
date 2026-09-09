# Pranay Kadu

**Backend & Distributed Systems Engineer** · Java · Streaming · Transactions · Reliability

I work on backend and infrastructure systems where **concurrency, failure recovery, resource lifecycle, throughput, and operability** matter.

`Java` · `Spring Boot` · `Kafka` · `Netty` · `REST/gRPC` · `SQL` · `Redis` · `Docker` · `Kubernetes` · `AWS`

---

## Open Source

### Merged upstream

- **AutoMQ #3493 — controller-only AutoBalancer reporter fix**  
  [PR](https://github.com/AutoMQ/automq/pull/3493) · merged after maintainer review and approval  
  Prevented broker-only metrics reporter initialization on controller-only nodes and added focused regression coverage across process-role inputs and lifecycle behavior.

### Under review

- **AutoMQ #3579 — Prometheus endpoint authentication**  
  [PR](https://github.com/AutoMQ/automq/pull/3579) · open  
  Proposed optional Basic authentication for the built-in Prometheus endpoint with backward-compatible defaults, endpoint policy, credential validation, lifecycle coverage, and an OpenTelemetry compatibility upgrade.

- **Apache Fluss #4263 — endpoint-aware Netty connection caching**  
  [PR](https://github.com/apache/fluss/pull/4263) · open  
  Proposed endpoint-aware RPC connection identity for same-UID TabletServers whose host or port changes while an older endpoint remains reachable.

- **Apache Fluss #4230 — custom Paimon lake paths for Spark reads**  
  [PR](https://github.com/apache/fluss/pull/4230) · open  
  Proposed support for independently mapped Fluss/Paimon table paths across lake-only reads, lake+log reads, and predicate pushdown.

- **Trino #30973 — transaction commit/failure race**  
  [PR](https://github.com/trinodb/trino/pull/30973) · open  
  Proposed coordination of commit and failure ownership so unrelated failures cannot override an autocommit query once commit has begun.

**Contribution areas:** concurrency · asynchronous lifecycle · RPC · transactions · metadata · Kafka internals · regression testing

---

## Selected Engineering Work

### [Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)

GPU-accelerated exact vector search built with CUDA, C++20, JNI, Java, and Spring Boot.

Highlights include persistent GPU indexes, hierarchical/fused Top-K search, FP16 storage with FP32 accumulation, pinned memory, dual CUDA streams, JNI lifecycle handling, and a reproducible benchmark harness with latency, throughput, and recall measurements.

### [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

A Java workshop for exploring distributed transaction mechanics from first principles:

`HLC` → `MVCC` → `distributed routing` → `transaction records` → `write intents` → `snapshot isolation` → `clock uncertainty` → `read restart` → `serializable conflict prevention`

The project is intentionally educational rather than production-complete.

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

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)
