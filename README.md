<div align="center">

<img src="./assets/distributed-systems-command-center.svg" width="100%" alt="Animated distributed systems command center" />

<br>

**Backend & Distributed Systems Engineer**

`Java` · `Spring Boot` · `Kafka` · `Netty` · `REST/gRPC` · `SQL` · `Redis` · `Docker` · `Kubernetes` · `AWS`

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)

</div>

---

## `01 // UPSTREAM`

### `STATUS: MERGED`

#### [AutoMQ #3493 — controller-only AutoBalancer reporter fix](https://github.com/AutoMQ/automq/pull/3493)

**Merged after maintainer review and approval**

Prevented broker-only metrics reporter initialization on controller-only nodes. The final implementation reused Kafka's own `ConfigDef` parsing semantics and retained focused regression coverage for real process-role inputs and reporter lifecycle behavior.

```text
DOMAIN      Kafka internals
FAILURE     Invalid reporter initialization on controller-only nodes
FIX         Process-role-aware lifecycle guard
VALIDATION  Maintainer review + regression tests
STATE       MERGED
```

### `STATUS: UNDER REVIEW`

| System | Change | Failure boundary / engineering focus |
|---|---|---|
| **AutoMQ** | [#3579 — Prometheus endpoint authentication](https://github.com/AutoMQ/automq/pull/3579) | Backward-compatible auth policy · credential validation · endpoint lifecycle |
| **Apache Fluss** | [#4263 — endpoint-aware Netty connection caching](https://github.com/apache/fluss/pull/4263) | RPC identity · stale endpoint reuse · connection lifecycle · Netty |
| **Apache Fluss** | [#4230 — custom Paimon lake paths](https://github.com/apache/fluss/pull/4230) | Metadata mapping · Spark lake reads · predicate pushdown |
| **Trino** | [#30973 — transaction commit/failure race](https://github.com/trinodb/trino/pull/30973) | Finalization ownership · concurrency · transaction correctness · deterministic tests |

<details>
<summary><strong>Open technical traces</strong></summary>
<br>

**AutoMQ #3579** proposes opt-in Basic authentication for the built-in Prometheus endpoint with backward-compatible defaults, endpoint-level access policy, configuration validation, credential handling, lifecycle coverage, and the OpenTelemetry compatibility change required by the authenticator API.

**Fluss #4263** proposes changing physical RPC connection identity from logical server UID alone to `UID + host + port`, preventing stale-but-reachable endpoints from being reused when a TabletServer moves while preserving UID-level disconnect semantics.

**Fluss #4230** proposes resolving configured Paimon table paths independently of Fluss table identity across lake-only reads, lake+log reads, and predicate pushdown.

**Trino #30973** proposes explicit finalization ownership between commit and failure paths so unrelated failures cannot transition an autocommit query to `FAILED` after commit has already begun, while genuine commit failures remain visible.

</details>

---

## `02 // SYSTEMS LAB`

<table>
<tr>
<td width="50%" valign="top">

### ⚡ [Vortex CUDA](https://github.com/BackendArchitectX/Vortex-CUDA)

**GPU-accelerated exact vector search** built from CUDA kernels through a Java/Spring API boundary.

```text
PATH
Spring Boot → JNI → CUDA → GPU-resident index
```

- Persistent GPU-resident indexes
- Hierarchical and fused GPU Top-K
- FP16 storage with FP32 accumulation
- Pinned host memory + dual CUDA streams
- JNI lifecycle ownership with `AutoCloseable`
- Health, metrics and capacity guards
- Reproducible latency, throughput and recall benchmarks

The benchmark documentation reports hardware, workload shape, repeatability and recall while explicitly separating the scalar CPU reference from optimized production vector databases.

</td>
<td width="50%" valign="top">

### 🧭 [distrib-txn-db](https://github.com/BackendArchitectX/distrib-txn-db)

**Java systems workshop** for distributed transaction mechanics from first principles.

```text
HLC → MVCC → routing → txn records
    → write intents → snapshot isolation
    → clock uncertainty → read restart
    → serializable conflict prevention
```

The project intentionally exposes anomalies and failure modes before introducing the mechanism that addresses them.

**Educational by design — not presented as production-complete infrastructure.**

</td>
</tr>
</table>

---

## `03 // ENGINEERING MATRIX`

```text
RUNTIME / BACKEND          DISTRIBUTED SYSTEMS
Java / Spring Boot         Transactions / consistency
Kafka / event streaming    RPC / gRPC / Netty
SQL / Redis / caching      Failure recovery

PERFORMANCE                OPERABILITY
JFR / profiling            Observability
Concurrency                Docker / Kubernetes
Resource lifecycle         AWS / CI/CD
Deterministic testing      Production operations
```

> **Correctness before cleverness.** Make failure states explicit. Test races deterministically. Own resource lifecycle.

---

## `04 // CURRENT VECTOR`

<div align="center">

**Distributed systems · storage & streaming internals · concurrency · reliability · performance**

<sub>Tracing races, failure boundaries, resource ownership and state transitions across real systems.</sub>

</div>

---

<div align="center">

`SYSTEM CONSOLE // END OF TRANSMISSION`

<br>

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=Profile%20views&style=flat-square)

</div>
