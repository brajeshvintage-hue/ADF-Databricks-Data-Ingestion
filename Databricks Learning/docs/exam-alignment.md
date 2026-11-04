# Coverage audit against your uploaded exam guide

Compared October 27, 2026 against the 11-page PDF you supplied:
[October 9 exam guide](C:/Users/braje/Downloads/Databricks-Certified-Data-Engineer-Professional-Exam-Guide-9-Oct-2026.pdf).

The document identifies its publication and update date as October 9, 2026. Its outline is on PDF pages 3–6. All nine domains and weights match the existing workbook. The earlier web reference contained both old and new outlines; this uploaded document presents the October 9 outline on its own.

## How to read the map

- **Code + exercise:** starter implementation exists; you must run, extend and verify it.
- **Exercise:** explicit build instructions exist; you write the implementation as part of learning.
- **External:** execution also needs an additional service, feature, identity or administrative grant.

These labels describe the learning materials, not your mastery or successful Azure execution. No live workspace verification has happened here. Core Python tests have local verification only.

| Domain / objective, paraphrased | Days | Material level |
|---|---|---|
| **1. Python/SQL development — 23%** | | |
| Modular Python project and bundle structure | 1–2, 5, 27 | Code + exercise |
| PyPI/wheel/sdist conflict and install diagnosis across environments | 3 | Code + exercise; pipeline installation extension |
| Python, pandas, SQL and governed UC functions | 4, 21 | Code + exercise; governed Python implementation is a follow-up below |
| Streaming pipelines with Auto Loader | 7–8 | Code + exercise |
| Jobs through UI, API and CLI | 2, 13, 26 | Code + exercise; API creation extension below |
| Streaming-table versus materialized-view choice | 8, 29 | Code + exercise |
| AUTO CDC, sequence, SCD1/SCD2 | 10 | Code + exercise |
| Structured Streaming versus declarative pipeline choice | 8, 11–12 | Code + exercise |
| If/Else and For Each | 13 | Exercise |
| Compute, serverless dependencies/performance mode, memory and retries | 3, 13 | Exercise + external compute availability |
| Unit/integration tests, DataFrame/schema assertions, transform | 1, 4–5 | Code + exercise |
| Watermarks, output modes, foreachBatch and checkpoint recovery | 11–12 | Code + exercise; aggregation extension below |
| **2. Ingestion and acquisition — 12%** | | |
| Delta/Parquet/JSON/Iceberg/CSV/Binary, cloud and message sources | 6–7, 28 | Code + exercise; real broker external |
| Incremental CDC into Delta or Iceberg | 10, 28 | Delta code + exercise; Iceberg feature-gated external |
| SQL Server/MySQL/PostgreSQL managed Connect ingestion | 14 | External; one source recipe, source comparison below |
| D2D/open sharing and Clean Rooms | 23 | External |
| Governed federation and connection credentials | 14 | External |
| **3. Data manipulation — 12%** | | |
| Windows, joins and aggregations | 9, 20 | Code + exercise |
| VARIANT modeling and extraction | 15 | Code + exercise |
| AI inference/enrichment | 15 | External endpoint + SQL starter |
| Expectations and quarantine/drop/fail behavior | 9 | Code + exercise |
| **4. Monitoring and alerting — 10%** | | |
| Billing/compute/access/lakeflow system tables | 25 | Code + exercise; access may require grants |
| REST/CLI/SDK observation | 26 | Command/code recipes + exercise |
| Pipeline event logs | 8–9, 26 | Query recipe + exercise |
| Business/quality/cost/SQL/audit/AI/branching alerts | 25 | One implemented alert exercise; broader scenarios below |
| Jobs status and performance | 13, 25–26 | Exercise |
| **5. Cost and performance — 15%** | | |
| Managed tables and predictive maintenance | 18–19 | Exercise; feature/access gated |
| Deletion vectors, fixed/automatic liquid clustering | 17–18 | Code + exercise |
| Repeated-read data caching | 19 | Exercise |
| CDF for incremental downstream processing | 16 | Code + exercise |
| Query-profile diagnosis of skipping/joins/shuffles | 17, 20 | Code + exercise |
| Clustering versus partitioning/ZORDER | 17 | Exercise |
| **6. Security and compliance — 8%** | | |
| Least privilege on UC and workspace objects | 21, 27 | Exercise; second identity/grantor needed |
| Governed-tag ABAC filters/masks | 22 | Policy starter + external privileges |
| Hash/token/suppress/generalize techniques | 22 | Concepts + implementation extension below |
| Batch/stream PII detection and enforced masking | 22 | Exercise; policy/identity access needed |
| Deletion and retention strategy | 24 | Code + exercise; full inventory required |
| **7. Governance — 5%** | | |
| Tags/comments for discoverability | 21–22 | Code + exercise |
| Privilege inheritance | 21 | Exercise; future-object test below |
| **8. Debugging and deploying — 10%** | | |
| Spark UI/logs/system tables/query profiles | 20, 26 | Exercise; diagnostics differ by compute |
| Job repair and parameter overrides | 13, 26 | Exercise |
| Bundle deployment | 2, 27 | Code + exercise |
| Git folders and CI/CD | 5, 27 | CI starter + exercise; remote identity needed |
| **9. Modeling — 5%** | | |
| Delta/Iceberg grain, layout and balanced files | 17, 28–29 | Code + exercise; Iceberg feature gated |
| Dimensions, materialized aggregates and UC metric definitions | 29 | Code + exercise |

## Add these follow-ups within the assigned days

These make smaller clauses of the objectives observable without adding more days. If time is short, extend the calendar instead of marking a design-only activity as hands-on complete.

**Day 3 — pipeline dependency scope:** in a disposable development pipeline add a small compatible third-party package to the pipeline's declared environment. Import and use it in a dataset expression/UDF, run the pipeline, then remove the declaration and diagnose the missing-dependency boundary. A notebook installation is not evidence for this objective.

**Day 13 — API creation:** after generating the UI job, create a separate minimal job through the documented Jobs API or SDK using its supported schema. Disable schedules, run once, inspect its run, and compare with the bundle-managed resource. Avoid mixing API edits and bundle ownership on the same job.

**Days 11–12 — real stateful aggregation:** add a windowed event-time sum to a scratch streaming query. Inspect update and append behavior on supported sinks, advance event time, restart from the same checkpoint, and reconcile totals. The supplied dedup query alone does not exercise every aggregation/output-mode contract.

**Day 14 — database source comparison:** execute one available managed connector end to end. For SQL Server, MySQL and PostgreSQL separately document source-side change capture prerequisites, required privileges, connectivity and recovery assumptions using the current connector guide. Mark the other sources as design-only until actually tested.

**Day 21 — governed Python function:** create a tiny UC Python function on supported compute using the current CREATE FUNCTION documentation. Test nulls, declared result type, EXECUTE access and any supported dependency/environment restrictions. Compare its lifetime and authorization with the supplied SQL UC function and session Python UDF.

**Day 21 — inherited access to future objects:** grant the lab group an appropriate scoped SELECT privilege plus namespace-use privileges, create a new synthetic table afterward, and verify its access as the second identity. Inspect the effective grants and revoke the training grant after recording the outcome.

**Day 22 — privacy transformations:** implement hash, lookup-based token, suppression and generalization on synthetic data. State which preserve joins, which require protected mapping material, and what reidentification risk remains. These are technique experiments, not a declaration of regulatory compliance.

**Day 25 — alert breadth:** implement one real alert and exercise its firing and recovery. For business metric, data quality, anomaly, cost, SQL health, audit/security and AI-quality scenarios, write the query/signal, threshold, identity, data latency and intended response. Connect one alert result to a job condition in a disposable orchestration lab if the workspace supports it.

## Adjustments from this comparison

The workbook now explicitly includes binary-file reading on Day 6, serverless performance-mode measurement on Day 13, and batch/stream candidate-PII detection before publication on Day 22. The calendar does not need a domain reorder. The distinction between supplied starter code and exercises requiring your implementation or external access is now explicit.
