<div align="center">

# Pranay Kadu

### Backend & Distributed Systems Engineer

**Java · Distributed Systems · Streaming · Transactions · Reliability**

I build backend and infrastructure systems where **correctness under concurrency, failure recovery, resource lifecycle, throughput, and operability** matter.

`Java` · `Spring Boot` · `Kafka` · `Netty` · `REST/gRPC` · `SQL` · `Redis` · `Docker` · `Kubernetes` · `AWS`

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)

</div>

---

## Open-source engineering

### ✅ Merged upstream

#### [AutoMQ #3493 — controller-only AutoBalancer reporter fix](https://github.com/AutoMQ/automq/pull/3493)

**Merged after maintainer review and approval**

Prevented broker-only metrics reporter initialization on controller-only nodes. The final implementation reused Kafka's own `ConfigDef` parsing semantics and retained focused regression coverage for real process-role inputs and reporter lifecycle behavior.

> **Signal:** Kafka internals · configuration semantics · lifecycle correctness · regression testing

### 🔍 Under review

| Project | Change | Engineering focus |
|---|---|---|
| **AutoMQ** | [#3579 — Prometheus endpoint authentication](https://github.com/AutoMQ/automq/pull/3579) | Backward-compatible auth policy · credential validation · endpoint security · lifecycle coverage |
| **Apache Fluss** | [#4263 — endpoint-aware Netty connection caching](https://github.com/apache/fluss/pull/4263) | RPC identity · stale endpoint handling · connection lifecycle · Netty |
| **Apache Fluss** | [#4230 — custom Paimon lake paths](https://github.com/apache/fluss/pull/4230) | Metadata mapping · Spark lake reads · predicate pushdown |
| **Trino** | [#30973 — transaction commit/failure race](https://github.com/trinodb/trino/pull/30973) | Atomic finalization ownership · concurrency · transaction correctness · deterministic tests |

<details>
<summary><strong>Technical context</strong></summary>
<br>

**AutoMQ #3579** proposes opt-in Basic authentication for the built-in Prometheus endpoint with backward-compatible defaults, endpoint-level access policy, configuration validation, credential handling, lifecycle coverage, and the OpenTelemetry compatibility change required by the authenticator API.

**Fluss #4263** proposes changing physical RPC connection identity from logical server UID alone to `UID + host + port`, preventing stale-but-reachable endpoints from being reused when a TabletServer moves while preserving UID-level disconnect semantics.

**Fluss #4230** proposes resolving configured Paimon table paths independently of Fluss table identity across lake-only reads, lake+log reads, and predicate pushdown.

**Trino #30973** proposes explicit finalization ownership between commit and failure paths so unrelated failures cannot transition an autocommit query to `FAILED` after commit has already begun, while genuine commit failures remain visible.

</details>

---

## Selected systems work

<table>
<tr>
<td width="50%" valign="top">

### ⚡ [Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)

**GPU-accelerated exact vector search** built from CUDA kernels through a Java/Spring API boundary.

- Persistent GPU-resident indexes
- Hierarchical and fused GPU Top-K
- FP16 storage with FP32 accumulation
- Pinned host memory + dual CUDA streams
- JNI lifecycle ownership with `AutoCloseable`
- Spring Boot API with health, metrics and capacity guards
- Reproducible latency, throughput and recall benchmarks

The benchmark documentation reports hardware, workload shape, repeatability and recall while explicitly separating the scalar CPU reference from optimized production vector databases.

</td>
<td width="50%" valign="top">

### 🧭 [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

**Java systems workshop** for distributed transaction mechanics from first principles.

`HLC` → `MVCC` → `routing` → `transaction records` → `write intents` → `snapshot isolation` → `clock uncertainty` → `read restart` → `serializable conflict prevention`

The project intentionally exposes anomalies and failure modes before introducing the mechanism that addresses them.

**Educational by design — not presented as production-complete infrastructure.**

</td>
</tr>
</table>

---

## Engineering principles

> **Correctness before cleverness.** Make failure states explicit. Test races deterministically. Own resource lifecycle.

```text
Concurrency & lifecycle     Distributed transactions
Kafka & event streaming     RPC / gRPC / Netty
Performance engineering     SQL / Redis / caching
Failure recovery            Observability
Docker / Kubernetes         AWS / CI/CD
Production operations       Deterministic regression testing
```

---

<div align="center">

### Current engineering direction

**Distributed systems · storage & streaming internals · concurrency · reliability · performance**

<br>

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=Profile%20views&style=flat-square)

</div>
