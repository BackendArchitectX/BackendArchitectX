# Pranay Kadu

**Backend & Distributed Systems Engineer** · Java · Streaming · Transactions · Reliability

I work on backend and infrastructure systems where **correctness under concurrency, failure recovery, resource lifecycle, throughput, and operability** matter.

`Java` · `Spring Boot` · `Kafka` · `Netty` · `REST/gRPC` · `SQL` · `Redis` · `Docker` · `Kubernetes` · `AWS`

---

## Open Source

### Merged upstream

- **AutoMQ #3493 — controller-only AutoBalancer reporter fix**  
  [PR](https://github.com/AutoMQ/automq/pull/3493) · **merged after maintainer review and approval**  
  Prevented broker-only metrics reporter initialization on controller-only nodes. The final implementation reused Kafka's own `ConfigDef` parsing semantics and kept focused regression coverage for real process-role inputs and reporter lifecycle behavior.

### Under review

- **AutoMQ #3579 — Prometheus endpoint authentication**  
  [PR](https://github.com/AutoMQ/automq/pull/3579) · open  
  Proposed opt-in Basic authentication for the built-in Prometheus endpoint with backward-compatible defaults, endpoint-level access policy, configuration validation, credential handling, lifecycle coverage, and the OpenTelemetry compatibility change required by the authenticator API.

- **Apache Fluss #4263 — endpoint-aware Netty connection caching**  
  [PR](https://github.com/apache/fluss/pull/4263) · open  
  Proposed changing physical RPC connection identity from logical server UID alone to `UID + host + port`, preventing stale-but-reachable endpoints from being reused when a TabletServer moves while preserving UID-level disconnect semantics.

- **Apache Fluss #4230 — custom Paimon lake paths for Spark reads**  
  [PR](https://github.com/apache/fluss/pull/4230) · open  
  Proposed resolving configured Paimon table paths independently of Fluss table identity across lake-only reads, lake+log reads, and predicate pushdown.

- **Trino #30973 — transaction commit/failure race**  
  [PR](https://github.com/trinodb/trino/pull/30973) · open  
  Proposed explicit finalization ownership between commit and failure paths so unrelated failures cannot transition an autocommit query to `FAILED` after commit has already begun, while genuine commit failures remain visible.

**Contribution areas:** concurrency · asynchronous lifecycle · RPC · transactions · metadata · Kafka internals · regression testing

---

## Selected Engineering Work

### [Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)

GPU-accelerated **exact vector search** built from CUDA kernels through a Java/Spring API boundary.

- persistent GPU-resident indexes
- hierarchical and fused GPU Top-K search
- FP16 storage with FP32 accumulation
- pinned host memory and dual CUDA streams
- JNI lifecycle ownership with Java `AutoCloseable`
- Spring Boot API with validation, health, metrics, and capacity guards
- reproducible benchmark harness with latency, throughput, storage, and recall measurements

The benchmark documentation reports hardware, workload shape, repeatability, recall, and explicitly distinguishes the project's scalar CPU reference from optimized production vector databases.

### [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

A Java systems workshop for exploring distributed transaction mechanics from first principles:

`HLC` → `MVCC` → `distributed routing` → `transaction records` → `write intents` → `snapshot isolation` → `clock uncertainty` → `read restart` → `serializable conflict prevention`

The project intentionally demonstrates failure modes and anomalies before introducing the mechanism that addresses them. It is educational by design rather than production-complete.

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

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=Profile%20views&style=flat-square)
