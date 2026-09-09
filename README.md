<div align="center">

<img src="./assets/distributed-systems-command-center.svg" width="100%" alt="Animated distributed systems command center" />

<br>

**`BACKEND ARCHITECT X // DISTRIBUTED SYSTEMS ENGINEER`**

`JAVA` · `SPRING BOOT` · `KAFKA` · `NETTY` · `REST/gRPC` · `SQL` · `REDIS` · `KUBERNETES` · `AWS`

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)

<sub>Concurrency · correctness · failure recovery · resource lifecycle · performance · operability</sub>

</div>

---

## `00 // OPERATOR PROFILE`

```text
OPERATOR      Pranay Kadu / BackendArchitectX
ROLE          Backend & Distributed Systems Engineer
PRIMARY       Java / JVM / Spring Boot
SYSTEMS       Kafka / Netty / gRPC / transactions / streaming
DATA          SQL / Redis / metadata / durable state
RUNTIME       Docker / Kubernetes / AWS / CI-CD
METHOD        invariants / ownership / deterministic tests / observable failure boundaries
```

> I am most interested in backend problems where correctness depends on **who owns state, which endpoint is real, which resource must be released, and which transition is still legal after failure begins**.

<img src="./assets/architecture-topology-console.svg" width="100%" alt="Animated failure-aware backend topology" />

### `SYSTEM DESIGN LENS`

```text
INGRESS      → validate identity / authorization / rate limits
COMPUTE      → keep state ownership explicit
STATE        → distinguish hot-path cache from durable truth
STREAMING    → make delivery / retry / idempotency semantics visible
REMOTE RPC   → define timeout / fallback / circuit-breaker behavior
RESOURCES    → own threads / permits / connections / native handles
OBSERVATION  → logs / metrics / traces / profiling
FINALIZATION → release resources before declaring terminal state complete
PROOF        → force race windows and failure paths deterministically
```

**Operating invariant:** every asynchronous resource, state transition and remote dependency must have a clear owner and a defined failure path.

---

<img src="./assets/evidence-ladder-console.svg" width="100%" alt="Engineering evidence ladder" />

## `01 // EVIDENCE POLICY`

This profile deliberately separates four levels of proof:

```text
LEVEL 04  EXTERNAL VALIDATION   → maintainer-reviewed and merged upstream
LEVEL 03  UPSTREAM REVIEW       → submitted with focused implementation and tests
LEVEL 02  REPRODUCIBLE PROOF    → benchmarks / deterministic regression / test harnesses
LEVEL 01  DESIGN INTENT         → architecture / invariants / implementation direction
```

**Rule:** presentation must never outrun validation. A merged upstream fix is stronger evidence than an open PR; a reproducible benchmark is stronger evidence than a polished architecture diagram.

---

<img src="./assets/systems-dossier-console.svg" width="100%" alt="Unified systems engineering dossier" />

## `02 // PRIMARY ENGINEERING SIGNALS`

### `AUTOMQ #3493 // EXTERNALLY VALIDATED`

[**controller-only AutoBalancer reporter fix →**](https://github.com/AutoMQ/automq/pull/3493)

```text
PROBLEM     Broker-only reporter logic initialized on controller-only nodes
INVARIANT   Reporter lifecycle must respect Kafka process-role semantics
CHANGE      Guard reporter initialization for controller-only processes
DETAIL      Reuse Kafka ConfigDef LIST parsing for real role inputs
PROOF       Focused process-role and lifecycle regression tests
STATUS      Maintainer feedback incorporated → revised → approved → merged
```

<img src="./assets/automq-role-console.svg" width="100%" alt="AutoMQ process-role lifecycle diagnostic" />

**Why this signal matters:** the implementation survived external design feedback. The final version became simpler, reused Kafka's own parsing semantics, retained lifecycle coverage and was then approved upstream.

### `TRINO #30973 // FINALIZATION OWNERSHIP`

[**Prevent query failure after transaction commit starts →**](https://github.com/trinodb/trino/pull/30973)

<img src="./assets/txn-state-machine-console.svg" width="100%" alt="Animated transaction finalization state machine" />

```text
PROBLEM     External failure could race with autocommit finalization
INVARIANT   Once COMMITTING owns finalization, unrelated failure cannot steal it
MODEL       OPEN → COMMITTING → FINISHED
            OPEN → COMMITTING → FAILED   only for genuine commit failure
MECHANISM   Atomic finalization-state ownership
PROOF       Blocking transaction manager creates deterministic race windows
STATUS      Open / under review
```

The important part is not adding another boolean. It is modeling **who is allowed to own terminal-state transition** and proving that ownership under forced timing rather than probabilistic stress.

### `FLUSS #4263 // CONNECTION IDENTITY`

[**Handle endpoint changes for cached server connections →**](https://github.com/apache/fluss/pull/4263)

```text
PROBLEM     Stable logical UID could reuse a stale physical endpoint
INVARIANT   Logical server identity is not the same as physical connection identity
CHANGE      Connection key: UID → UID + host + port
PROOF       Two live Netty servers using the same UID and different endpoints
STATUS      Open / under review
RISK        Maintainers may prefer stronger endpoint replacement / eviction semantics
```

<img src="./assets/oss-race-console.svg" width="100%" alt="Animated Trino and Fluss diagnostics" />

### `OTHER OPEN REVIEW CHANNELS`

| SYSTEM | CHANGE | ENGINEERING BOUNDARY | CURRENT PROOF |
|:--|:--|:--|:--|
| `AUTOMQ` | [#3579](https://github.com/AutoMQ/automq/pull/3579) | Prometheus authentication · credential validation · endpoint lifecycle | config / endpoint / lifecycle tests |
| `FLUSS` | [#4230](https://github.com/apache/fluss/pull/4230) | Paimon metadata mapping · Spark lake reads · predicate pushdown | lake-only + lake/log test suites |

---

## `03 // FAILURE MODEL`

<img src="./assets/failure-trace-console.svg" width="100%" alt="Animated failure boundary and recovery trace" />

```text
REQUEST
  ↓
VALIDATE / AUTH / RATE LIMIT
  ↓
CLAIM OWNERSHIP
  ↓
REMOTE / STORAGE / STREAMING WORK
  ↓
PARTIAL FAILURE?
  ├─ no  → FINALIZE → EMIT / PERSIST TERMINAL STATE
  └─ yes → CONTAIN / RETRY / FALLBACK / ABORT
                 ↓
        RELEASE OWNED RESOURCES
                 ↓
       PRESERVE LEGAL STATE TRANSITIONS
                 ↓
       DETERMINISTIC REGRESSION PROOF
```

### `FAILURE CLASSES`

| CLASS | FAILURE SHAPE | INVARIANT | RESPONSE |
|:--|:--|:--|:--|
| `CONCURRENCY` | commit vs failure · cancellation · duplicate completion | only one path owns terminal transition | atomic ownership · monotonic transitions · controlled race tests |
| `RPC` | stale endpoint reuse · retained timeouts · reconnect ambiguity | physical route identity must be current | endpoint-aware identity · disconnect semantics · timeout cleanup |
| `LIFECYCLE` | event-loop leaks · scheduler survival · callbacks after close | creator owns shutdown unless ownership is transferred | idempotent close · permit/thread/connection release verification |
| `CONFIGURATION` | role mismatch · unsafe defaults · inconsistent parsing | semantics must match the source system | reuse source-of-truth parser · validate early · preserve compatibility |
| `METADATA` | logical/physical divergence · stale mapping | logical identity cannot silently imply physical location | isolate mapping layer · explicit resolution |
| `PERFORMANCE` | allocation pressure · N+1 · cache misses · sync bottlenecks | optimization must be measurable | profile · benchmark · batch · cache · bound concurrency |

---

## `04 // SYSTEMS LAB`

### `VORTEX // GPU VECTOR ENGINE`

[**Vortex CUDA →**](https://github.com/BackendArchitectX/Vortex-CUDA)

<img src="./assets/vortex-memory-pipeline.svg" width="100%" alt="Animated Vortex memory and execution pipeline" />

<img src="./assets/vortex-telemetry-console.svg" width="100%" alt="Vortex CUDA benchmark telemetry" />

```text
REQUEST → SPRING BOOT → JAVA API → JNI HANDLE → PINNED HOST MEMORY
        → CUDA STREAMS → GPU-RESIDENT INDEX → FUSED TOP-K → RESULT
```

**Systems explored:** persistent GPU indexes · exact squared-L2 search · hierarchical/fused Top-K · FP16 storage with FP32 accumulation · vectorized memory access · FMA · pinned host memory · dual CUDA streams · JNI opaque-handle ownership · health/metrics/capacity guards.

**Lifecycle boundary:** Java `AutoCloseable` owns the native handle lifecycle; native ownership must eventually release GPU-resident state. The project therefore exercises correctness at the Java/native/device boundary, not only kernel speed.

**Documented benchmark signal:** RTX 3050 6GB Laptop GPU · 500K×128 workload · FP32 P50 ~**1.67–1.72 ms** · ~**1,641–1,662 QPS** at batch 32 · **50%** vector-storage reduction with FP16 · **99.6875% Recall@10** on the specified FP16 workload.

**Benchmark discipline:** latency, throughput, recall, storage and repeatability are treated as separate dimensions. The scalar CPU reference is explicitly not presented as an optimized production vector database.

### `DISTRIB-TXN-DB // DISTRIBUTED STATE LAB`

[**distrib-txn-db →**](https://github.com/BackendArchitectX/distrib-txn-db)

```text
PHYSICAL TIME
   ↓
HLC
   ↓
MVCC VISIBILITY
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
SERIALIZABLE CONFLICT PREVENTION
```

**What the project is for:** understanding why each mechanism exists by first exposing the anomaly that appears without it.

```text
ANOMALY        → MECHANISM
stale version  → MVCC visibility rules
partial txn    → transaction records + intents
write conflict → isolation / conflict handling
clock skew     → uncertainty window
unsafe read    → read restart
serialization  → conflict prevention
```

`EDUCATIONAL SYSTEMS MODEL // NOT PRESENTED AS PRODUCTION-COMPLETE INFRASTRUCTURE`

---

<img src="./assets/engineering-matrix-console.svg" width="100%" alt="Engineering capability matrix" />

## `05 // ENGINEERING MATRIX`

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

### `ENGINEERING PRINCIPLES`

```text
01  CORRECTNESS BEFORE CLEVERNESS
02  MAKE FAILURE STATES EXPLICIT
03  MODEL OWNERSHIP BEFORE WRITING RECOVERY LOGIC
04  SEPARATE LOGICAL IDENTITY FROM PHYSICAL LOCATION
05  ASSUME CALLBACKS CAN ARRIVE AFTER CLOSE
06  OWN THREADS / PERMITS / CONNECTIONS / NATIVE HANDLES YOU CREATE
07  DESIGN RETRIES AROUND IDEMPOTENCY AND BOUNDED FAILURE
08  TEST RACES BY CONTROLLING TIME — NOT BY HOPING TO HIT THEM
09  MEASURE PERFORMANCE BEFORE AND AFTER OPTIMIZATION
10  TREAT OPERABILITY AS PART OF THE SYSTEM DESIGN
11  PREFER SOURCE-OF-TRUTH PARSING OVER PARALLEL SEMANTICS
12  DISTINGUISH EXTERNAL VALIDATION FROM WORK STILL UNDER REVIEW
```

---

## `06 // OPERATING MODEL`

```text
OBSERVE
  └─ logs / metrics / traces / profiling
       ↓
ISOLATE
  └─ smallest resource, ownership or state boundary
       ↓
MODEL
  └─ invariants / legal transitions / failure semantics
       ↓
CHANGE
  └─ smallest production-safe correction
       ↓
PROVE
  └─ unit / integration / deterministic regression
       ↓
MEASURE
  └─ latency / throughput / resource behavior
       ↓
OPERATE
  └─ alerts / dashboards / runbooks / rollback awareness
```

### `WHAT I OPTIMIZE FOR`

| DIMENSION | QUESTION |
|:--|:--|
| `CORRECTNESS` | Can two actors believe they own the same state transition? |
| `FAILURE` | What happens after the happy path has partially completed? |
| `LIFECYCLE` | Who shuts down the resource and what if close races with callback completion? |
| `IDENTITY` | Is the identifier logical, physical, cached or authoritative? |
| `PERFORMANCE` | What measurement proves the optimization actually helped? |
| `OPERABILITY` | How will the failure be detected, diagnosed and recovered in production? |

> **Engineering policy:** correctness before cleverness. Make failure states explicit. Test races deterministically. Own resource lifecycle.

---

<img src="./assets/current-vector-console.svg" width="100%" alt="Current engineering vector" />

## `07 // CURRENT VECTOR`

<div align="center">

**`DISTRIBUTED SYSTEMS · STORAGE · STREAMING · CONCURRENCY · RELIABILITY · PERFORMANCE`**

<sub>Races · failure boundaries · endpoint identity · resource ownership · state transitions · recovery semantics</sub>

<br><br>

<img src="./assets/telemetry-footer.svg" width="100%" alt="Animated systems telemetry footer" />

<br>

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=SYSTEM%20VISITS&style=flat-square)

</div>
