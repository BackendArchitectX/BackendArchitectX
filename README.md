<div align="center">

<img src="./assets/distributed-systems-command-center.svg" width="100%" alt="Animated distributed systems command center" />

<br>

**`BACKEND ARCHITECT X // DISTRIBUTED SYSTEMS ENGINEER`**

`JAVA` · `SPRING BOOT` · `KAFKA` · `NETTY` · `REST/gRPC` · `SQL` · `REDIS` · `KUBERNETES` · `AWS`

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)

<sub>Engineering for correctness under concurrency, failure recovery, resource lifecycle, throughput and operability.</sub>

</div>

---

## `00 // MISSION PROFILE`

```text
OPERATOR      Pranay Kadu / BackendArchitectX
ROLE          Backend & Distributed Systems Engineer
PRIMARY       Java / JVM / Spring Boot
SYSTEMS       Kafka / Netty / gRPC / transactions / streaming
DATA          SQL / Redis / metadata / durable state
RUNTIME       Docker / Kubernetes / AWS / CI-CD
FOCUS         concurrency / correctness / failure recovery / performance
METHOD        explicit state ownership / deterministic tests / observable failure boundaries
```

> I am most interested in the points where systems stop being simple: concurrent finalization, stale endpoints, process-role mismatches, resource ownership, asynchronous shutdown, metadata indirection and state transitions that must remain correct under failure.

---

<img src="./assets/proof-ledger-console.svg" width="100%" alt="Animated engineering proof ledger" />

## `01 // UPSTREAM SIGNAL`

### `MERGED // EXTERNALLY VALIDATED`

#### [AutoMQ #3493 — controller-only AutoBalancer reporter fix](https://github.com/AutoMQ/automq/pull/3493)

**Merged after maintainer review and approval.**

```text
FAULT       Broker-only metrics reporter initialized on controller-only process
BOUNDARY    Kafka process-role configuration / reporter lifecycle
CHANGE      Skip reporter initialization for controller-only nodes
DETAIL      Reuse Kafka ConfigDef LIST parsing semantics for real role inputs
TESTING     Focused process-role + lifecycle regression coverage
SIGNAL      Maintainer feedback incorporated → approved → merged
```

This is the strongest external engineering signal on the profile because the implementation was not only submitted — it went through maintainer design feedback, revision and approval.

### `OPEN REVIEW CHANNELS`

| SYSTEM | TRACE | PROBLEM CLASS | VALIDATION PATH |
|:--|:--|:--|:--|
| `AUTOMQ` | [#3579](https://github.com/AutoMQ/automq/pull/3579) | Prometheus endpoint authentication · credential policy · lifecycle | configuration validation · endpoint policy · lifecycle tests |
| `FLUSS` | [#4263](https://github.com/apache/fluss/pull/4263) | stale TabletServer endpoint reuse · RPC connection identity | two live Netty servers · same UID / different endpoint regression |
| `FLUSS` | [#4230](https://github.com/apache/fluss/pull/4230) | custom Paimon path mapping · Spark lake reads | lake-only + lake/log suites · predicate pushdown coverage |
| `TRINO` | [#30973](https://github.com/trinodb/trino/pull/30973) | autocommit commit/failure race · finalization ownership | deterministic blocking commit manager · race-path tests |

<details>
<summary><code>EXPAND // TECHNICAL TRACE BUFFER</code></summary>
<br>

**AutoMQ #3579** proposes opt-in Basic authentication for the built-in Prometheus endpoint while preserving unauthenticated defaults. The change isolates endpoint policy, validates configuration and credentials, covers lifecycle behavior and includes the OpenTelemetry compatibility change required by the authenticator API.

**Fluss #4263** changes physical RPC connection identity from logical server UID alone to `UID + host + port`. The target failure is a stale-but-still-reachable TabletServer endpoint being reused after a server moves. Regression coverage uses separate live endpoints sharing the same logical UID.

**Fluss #4230** separates configured Paimon table-path resolution from Fluss table identity so custom mappings work across lake-only reads, lake+log reads and predicate pushdown paths.

**Trino #30973** introduces explicit finalization ownership between commit and failure paths so unrelated failures cannot mark an autocommit query failed after commit has begun, while true commit failures remain reportable. Tests deliberately block commit to force otherwise timing-sensitive race windows.

</details>

---

<img src="./assets/failure-trace-console.svg" width="100%" alt="Animated failure boundary and recovery trace" />

## `02 // FAILURE MODEL`

My preferred way to reason about backend systems is not feature-first. It is boundary-first:

```text
REQUEST
  ↓
VALIDATE INPUT / AUTH / RATE LIMIT
  ↓
CLAIM STATE OWNERSHIP
  ↓
PERFORM REMOTE / STORAGE / STREAMING WORK
  ↓
HANDLE PARTIAL FAILURE
  ↓
RELEASE RESOURCES / PERMITS / THREADS / CONNECTIONS
  ↓
PERSIST OR EMIT FINAL STATE
  ↓
VERIFY WITH DETERMINISTIC REGRESSION TESTS
```

### `FAILURE CLASSES I CARE ABOUT`

| CLASS | EXAMPLES | ENGINEERING RESPONSE |
|:--|:--|:--|
| `CONCURRENCY` | commit vs failure · cancellation races · duplicate completion | atomic ownership · monotonic state transitions · deterministic race tests |
| `RPC` | stale endpoint reuse · timeout retention · reconnect ambiguity | endpoint-aware identity · explicit disconnect semantics · timeout cleanup |
| `LIFECYCLE` | leaked event loops · scheduler survival · post-close callbacks | clear ownership · idempotent close · shutdown verification |
| `CONFIGURATION` | process-role mismatch · unsafe defaults · ambiguous parsing | source-of-truth parsing · validation · backwards-compatible guards |
| `METADATA` | identity/path divergence · stale mapping · wrong table resolution | explicit mapping layer · isolation of physical vs logical identity |
| `PERFORMANCE` | hot-path allocation · N+1 access · cache misses · sync bottlenecks | profiling · batching · caching · bounded concurrency · measured benchmarks |

---

<img src="./assets/systems-lab-console.svg" width="100%" alt="Animated systems lab execution paths" />

## `03 // SYSTEMS LAB`

<table>
<tr>
<td width="50%" valign="top">

### `VORTEX // GPU VECTOR ENGINE`

[**Repository →**](https://github.com/BackendArchitectX/Vortex-CUDA)

```text
REST REQUEST
    ↓
SPRING BOOT
    ↓
JAVA API
    ↓
JNI OWNERSHIP
    ↓
CUDA KERNELS
    ↓
GPU-RESIDENT INDEX
    ↓
EXACT TOP-K
```

**What it explores**

- persistent GPU-resident vector indexes
- exact squared-L2 search
- hierarchical + fused GPU Top-K
- FP16 storage with FP32 accumulation
- vectorized access and FMA paths
- pinned host memory + dual CUDA streams
- JNI opaque-handle lifecycle with `AutoCloseable`
- benchmark harness for latency, throughput, storage and recall
- Spring Boot health, metrics, validation and capacity guards

**Why it matters:** it forces performance work across language/runtime boundaries rather than stopping at application code.

</td>
<td width="50%" valign="top">

### `TXN-DB // DISTRIBUTED STATE LAB`

[**Repository →**](https://github.com/BackendArchitectX/distrib-txn-db)

```text
HLC
 ↓
MVCC
 ↓
DISTRIBUTED ROUTING
 ↓
TXN RECORDS
 ↓
WRITE INTENTS
 ↓
SNAPSHOT ISOLATION
 ↓
CLOCK UNCERTAINTY
 ↓
READ RESTART
 ↓
SERIALIZABLE GUARDS
```

**What it explores**

- logical time and hybrid clocks
- MVCC visibility
- transaction records and write intents
- snapshot-isolation anomalies
- uncertainty windows and restart semantics
- distributed routing
- conflict prevention

**Design rule:** expose the anomaly first, then introduce the mechanism that removes it.

`EDUCATIONAL SYSTEMS MODEL // NOT PRESENTED AS PRODUCTION-COMPLETE`

</td>
</tr>
</table>

---

<img src="./assets/engineering-matrix-console.svg" width="100%" alt="Animated engineering capability matrix" />

## `04 // ENGINEERING MATRIX`

```text
RUNTIME / BACKEND          DISTRIBUTED SYSTEMS        PERFORMANCE              OPERABILITY
────────────────────       ─────────────────────      ───────────────────      ───────────────────
Java / Spring Boot         Kafka / streaming          JFR / profiling          Observability
REST / gRPC / Netty        Transactions               Concurrency              Docker / Kubernetes
SQL / Redis / caching      Consistency                Resource lifecycle       AWS / CI-CD
JPA / Hibernate            Failure recovery           Async execution          Jenkins
API design                 Idempotency                Connection pooling       Cloud monitoring
Authentication             Rate limiting              Query tuning             Production support
```

### `SYSTEMS PRINCIPLES`

```text
01  CORRECTNESS BEFORE CLEVERNESS
02  MAKE FAILURE STATES EXPLICIT
03  SEPARATE LOGICAL IDENTITY FROM PHYSICAL LOCATION
04  ASSUME CALLBACKS CAN ARRIVE AFTER CLOSE
05  OWN THREADS / PERMITS / CONNECTIONS YOU CREATE
06  DESIGN RETRIES AROUND IDEMPOTENCY
07  TEST RACES BY CONTROLLING TIME — NOT BY HOPING TO HIT THEM
08  MEASURE PERFORMANCE BEFORE AND AFTER OPTIMIZATION
09  TREAT OPERABILITY AS PART OF THE DESIGN
10  DISTINGUISH EXTERNAL VALIDATION FROM WORK STILL UNDER REVIEW
```

---

## `05 // OPERATING MODEL`

```text
OBSERVE       logs / metrics / traces / profiling
ISOLATE       reduce failure to smallest ownership or state boundary
MODEL         define invariants and legal transitions
CHANGE        smallest production-safe correction
PROVE         targeted unit / integration / deterministic regression tests
MEASURE       latency / throughput / resource behavior where relevant
OPERATE       alerts / dashboards / runbooks / rollback awareness
```

> **Engineering policy:** correctness before cleverness. Make failure states explicit. Test races deterministically. Own resource lifecycle.

---

<img src="./assets/current-vector-console.svg" width="100%" alt="Animated current engineering vector" />

## `06 // CURRENT VECTOR`

<div align="center">

**`DISTRIBUTED SYSTEMS · STORAGE · STREAMING · CONCURRENCY · RELIABILITY · PERFORMANCE`**

<sub>Tracing races, failure boundaries, resource ownership, endpoint identity, state transitions and recovery semantics across real systems.</sub>

<br><br>

`BACKEND ARCHITECT X // SYSTEM CONSOLE ONLINE`

<br><br>

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=SYSTEM%20VISITS&style=flat-square)

</div>
