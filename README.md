<div align="center">

<img src="./assets/distributed-systems-command-center.svg" width="100%" alt="Production systems command center" />

<br>

**`BACKEND ARCHITECT X // BACKEND & DISTRIBUTED SYSTEMS ENGINEER`**

[GitHub](https://github.com/BackendArchitectX) · [Email](mailto:pranayp.kadu@gmail.com)

<sub>Java-first backend engineering across distributed systems, multi-runtime services, performance and production reliability.</sub>

</div>

---

## `01 // ENGINEERING PROOF`

| SIGNAL | ENGINEERING PROBLEM | PROOF | STATUS |
|:--|:--|:--|:--|
| [**AutoMQ #3493**](https://github.com/AutoMQ/automq/pull/3493) | controller-only reporter lifecycle | process-role regression tests + maintainer design review | **MERGED** |
| [**Trino #30973**](https://github.com/trinodb/trino/pull/30973) | commit/failure finalization race | explicit state ownership + deterministic blocking-commit tests | **UNDER REVIEW** |
| [**Fluss #4263**](https://github.com/apache/fluss/pull/4263) | stale physical endpoint reuse | endpoint-aware connection identity + two-server regression | **UNDER REVIEW** |
| [**AutoMQ #3579**](https://github.com/AutoMQ/automq/pull/3579) | Prometheus endpoint authentication | configuration, policy and lifecycle coverage | **UNDER REVIEW** |
| [**Fluss #4230**](https://github.com/apache/fluss/pull/4230) | custom Paimon table paths | lake-only + lake/log + predicate-path tests | **UNDER REVIEW** |

**Strongest signal:** AutoMQ #3493 was refined through maintainer feedback, approved and merged. Open PRs are presented as work under review—not as equivalent external validation.

<details>
<summary><code>EXPAND // CORE INVARIANTS</code></summary>
<br>

- **AutoMQ:** runtime lifecycle must respect Kafka process-role semantics.
- **Trino:** once commit owns finalization, unrelated failure cannot steal terminal state.
- **Fluss:** logical server identity must not silently imply physical endpoint identity.
- **Lifecycle:** threads, permits, connections and native handles require explicit ownership.
- **Testing:** race windows should be forced deterministically, not discovered by chance.

</details>

---

## `02 // SYSTEMS LAB`

### `VORTEX // GPU VECTOR ENGINE`

<img src="./assets/vortex-memory-pipeline.svg" width="100%" alt="Vortex Java JNI CUDA execution pipeline" />

[**Vortex CUDA →**](https://github.com/BackendArchitectX/Vortex-CUDA)

`Spring Boot → Java API → JNI → pinned host memory → CUDA streams → GPU-resident index → exact Top-K`

**Documented workload:** RTX 3050 6GB Laptop GPU · 500K×128 · FP32 P50 ~**1.67–1.72 ms** · ~**1,641–1,662 QPS** @ batch 32 · FP16 **50% storage reduction** · **99.6875% Recall@10** on the specified FP16 workload.

### `DISTRIB-TXN-DB // DISTRIBUTED STATE LAB`

[**distrib-txn-db →**](https://github.com/BackendArchitectX/distrib-txn-db)

`HLC → MVCC → routing → transaction records → write intents → snapshot isolation → clock uncertainty → read restart → serializable guards`

**Purpose:** expose the anomaly first, then introduce the mechanism that removes it. `EDUCATIONAL SYSTEMS MODEL`.

---

## `03 // ENGINEERING STACK`

<img src="./assets/full-stack-skills-console.svg" width="100%" alt="Resume-grounded multi-runtime engineering stack" />

```text
PRIMARY      Java · J2EE · Spring · Spring Boot · Spring MVC · REST APIs
PYTHON       Python 3 · FastAPI · Flask
WEB / API    TypeScript · JavaScript · Node.js · Express.js · ReactJS · JSP
SYSTEMS      Microservices · distributed systems · event-driven architecture · async processing
NATIVE       C++ · STL
DATA         MySQL · PostgreSQL · MongoDB · Redis · Kafka · message queues · SQL optimization
PERFORMANCE  multithreading · concurrency · caching · parallel processing · JFR · connection pooling
QUALITY      JUnit · TDD · OOP · SOLID · Agile
PLATFORM     AWS · EKS · PCF · Docker · Kubernetes · Jenkins · CI/CD
OPERABILITY  CloudWatch · Splunk · Dynatrace · Git · GitHub · Bitbucket · Jira
AI TOOLING   Claude Sonnet · Claude Opus · GitHub Copilot · agent-based coding tools
```

**Positioning:** Java/JVM remains the primary depth. Python services, Node/TypeScript/JavaScript, ReactJS and C++/STL broaden the execution surface without diluting the backend/distributed-systems identity.

---

## `04 // ENGINEERING MODEL`

```text
OBSERVE → ISOLATE → MODEL INVARIANT → CHANGE → PROVE → MEASURE → OPERATE
```

**Principles:** correctness before cleverness · explicit failure states · logical identity ≠ physical location · own resource lifecycle · idempotent retries · deterministic race tests · measure before/after optimization · operability is part of design.

---

<div align="center">

**`DISTRIBUTED SYSTEMS · STORAGE · STREAMING · CONCURRENCY · RELIABILITY · PERFORMANCE`**

<br>

![Profile views](https://komarev.com/ghpvc/?username=BackendArchitectX&label=SYSTEM%20VISITS&style=flat-square)

</div>
