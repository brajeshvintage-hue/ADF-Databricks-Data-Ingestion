# 30-day Azure Databricks build workbook

For a separate file with full instructions and learning notes for each day, start with [the daily learning index](../daily-learning/README.md). This document remains the compact overview.

Use the exam outline effective October 9, 2026. One project, increasing operational responsibility. Plan for 90–120 minutes daily; external-service days may need additional setup time. This is an intensive learning sequence, not a substitute for production experience.

Cross-checked against your uploaded October 9 guide. See [the objective coverage audit](exam-alignment.md) for the distinction between supplied code, exercises you implement, and labs needing external access.

## Daily method

Spend 10 minutes retrieving yesterday's concept without notes, 15 minutes reading, 45–60 minutes building, 20 minutes breaking/repairing, and 10–15 minutes explaining. If you only copied a script, mark the day built rather than verified. On days 7, 14, 21 and 28, spend the retrieval time revisiting the previous week's weakest concept.

Every day's completion evidence includes a journal entry using `journal-template.md`. Save small results, plans and run IDs under `evidence/day-NN/`; do not save tokens or sensitive logs. Follow references in `sources.md` and `advanced-labs.md` for details outside Topic 1.

## Day 1 — Python project boundaries

**Concept:** pure business logic versus runtime orchestration; imports and `src/` layout.

**Build:** run the local demo and contract tests from README. Read each source file. Implement a second pure function that validates an order amount: null, negative and nonnumeric values need an explicit policy. Write distinguishing input/output examples first.

**Break:** remove whitespace collapse from `normalize_name`; predict failing cases before testing. Repair it.

**Evidence:** passing tests, before/after failure, and your diagram of the package. **Explain:** why can we test a business rule without starting Spark?

## Day 2 — Package and deploy

**Concept:** wheel versus source archive versus bundle versus running job; target configuration.

**Build:** follow setup to build distributions, inspect the wheel, install it in a fresh venv, and run its entry point. Create the lab namespace in Azure; validate/deploy the bundle and run `retail_names`.

**Break:** change the task entry point to `missing_entry`. Observe whether validation detects it and where the runtime failure appears. Restore and redeploy.

**Evidence:** installed version, distribution contents, successful job run and repair. **Explain:** how do the same modules deploy to a different catalog without changing business logic?

## Day 3 — Dependencies and installation failures

**Concept:** dependency scope, transitive resolution, wheel tags, source builds and serverless cache.

**Build:** use `02_dependencies.py` to install a pinned PyPI library, your wheel and your sdist. Execute the worker probe. Record Python/runtime/library versions. Add a dependency through the serverless task environment and compare with a notebook install. Inspect pipeline environment dependency configuration too.

**Break:** perform the nonexistent-version and conflicting-constraints drills in Topic 1. Explain an incompatible native-wheel failure using its tags; do not damage the shared runtime to manufacture one.

**Evidence:** installation logs, worker output, three failure diagnoses. **Explain:** why can a notebook import succeed while a job fails?

## Day 4 — Python, pandas and native functions

**Concept:** Python execution boundaries, Arrow batches, null safety and explicit return types.

**Build:** run `01_udfs.py`. Check expected output and schema before benchmarking. Repeat trials and explain the formatted plans.

**Break:** remove scalar null handling, then return a pandas Series with the wrong length in a disposable function. Fix both. Test blank strings and nulls against all implementations.

**Evidence:** equivalence assertions, plans and result-consuming timings. **Explain:** when would you choose each implementation? Why is pandas batching not a guarantee of vectorized business logic?

## Day 5 — Test and automate development

**Concept:** contract tests, Spark integration tests, DataFrame.transform and reproducible CI.

**Build:** run `tests/` and the Spark assertions in notebook 01. Add one real edge case. Read the supplied CI workflow; run the same test/build commands locally and, if you use GitHub, in your own repository. Explain an Azure DevOps equivalent if that is your CI platform.

**Break:** change output column type or business behavior and show that an appropriate test catches it. Restore the contract.

**Evidence:** test/build outputs, and Topic 1's completion gate. **Explain:** which failures still require a workspace integration run?

## Day 6 — Batch ingestion and format contracts

**Concept:** parsing, schemas, append-only ingestion and the medallion boundary.

**Build:** run notebook 00 and inspect the JSON files before reading them. Read with an explicit schema; export the same fixture to CSV and Parquet under separate lab-volume subfolders. Read them back and compare schemas and nulls. Run `03_ingest.py` to create bronze. Sketch a Kafka/Event Hubs source with offsets, authentication and schema handling using the linked source documentation.

**Break:** read the CSV without a declared schema and compare numeric/timestamp types. Add a malformed JSON file in a separate scratch directory and compare parser modes.

**Format extension:** use `spark.read.format("binaryFile").load(...)` on the JSON fixture directory to inspect file path, byte length and binary content. Contrast that file-level representation with parsed JSON rows. Implement a bounded Kafka/Event Hubs ingestion if you have an approved test broker; otherwise mark that source exercise as design-only. Compare how Kafka, Kinesis and Pub/Sub expose source progress and credentials rather than assuming one connector configuration works for all three.

**Evidence:** format/schema comparison and bronze count 4 on the initial fixture. **Explain:** why is append-only ingestion not the same as business-key deduplication?

## Day 7 — Auto Loader schema evolution

**Concept:** source schema state, checkpoint state and target Delta schema are separate.

**Build:** run ingestion twice with the same checkpoint and unchanged files; count must remain stable. Add the optional coupon file in notebook 03 and restart ingestion as required. Inspect `_rescued_data` and schema changes.

**Break:** add a type-mismatch example under a new filename. Predict whether it changes schema, is rescued or fails under your options. Compare `rescue` with `addNewColumns` in a separate stream/target/checkpoint.

**Evidence:** restart behavior, schema and source/target row accounting. **Explain:** what happens if you discard the checkpoint? Do not delete the working checkpoint; reason first and use a disposable copy experiment.

## Day 8 — Declarative pipelines

**Concept:** defining a dependency graph versus imperatively executing actions; streaming tables and materialized views.

**Build:** deploy and run `retail_pipeline`. Trace `lp_bronze` → `lp_checked` → `lp_silver`/`lp_quarantine` → `lp_gold`. Inspect which definitions use streaming reads and which use batch reads. Compare operation and ownership with notebook 03's explicit stream.

**Break:** introduce a bad column reference in a development copy, inspect the pipeline error, restore and update.

**Evidence:** graph, update ID and gold totals. **Explain:** why is the gold aggregate a materialized view? When would an append-oriented streaming table be the better choice? Keep `.collect()` and writes out of declarative dataset functions.

## Day 9 — Quality, quarantine and advanced transformations

**Concept:** warn/drop/fail expectations, SQL three-valued logic, deterministic windows and joins.

**Build:** run notebook 04. Reconcile input, valid, duplicate and quarantined counts. Run a SQL window equivalent of the PySpark dedup. Add a small customer dimension and aggregate orders after the join. Inspect `lp_checked` quality metrics.

**Break:** remove `coalesce` from a simplified null-sensitive validity rule and see whether null rows disappear from both branches. In a dev pipeline change one expectation to `expect_or_fail`; observe rollback/failure behavior.

**Evidence:** initial silver count 3, quarantine count 1, gold total 75; record changed totals if you added files. **Explain:** why doesn't dropping invalid data provide a quarantine record automatically?

## Day 10 — CDC, sequencing and SCD

**Concept:** event sequence versus arrival time; SCD1 overwrites, SCD2 preserves versions.

**Build:** inspect the out-of-order CDC fixture from notebook 00. Run the pipeline's two AUTO CDC targets. Query current and historical customer rows; order history by `__START_AT` and inspect `__END_AT`. Append a new event with unique `(customer_id, sequence)` and update again.

**Break:** design a conflicting same-key/same-sequence pair and explain why you need a deterministic ordering policy. Test a late sequence in a separate synthetic key rather than corrupting existing fixtures.

**Evidence:** customer 10 current region US, customer 20 deleted, SCD2 history and interval reasoning. **Explain:** CDC application versus Delta CDF; why doesn't an arbitrary `dropDuplicates` choose the latest update?

## Day 11 — Watermarks and bounded state

**Concept:** event time, progress-driven watermark, state eviction and bounded deduplication.

**Build:** run notebook 05's first section. Append files with a duplicate key and later event time, ingest into bronze and rerun dedup. In a scratch source create events more than ten minutes apart; advance the maximum event time and then submit an old event. Inspect state/watermark progress across triggers.

**Break:** propose dedup without a watermark for an unbounded stream; explain memory growth. Observe that time passing on the wall clock alone does not advance an event-time watermark.

**Evidence:** input and output keys with event times and watermark/state metrics. **Explain:** does a watermark guarantee all older rows are always dropped? Why is a within-threshold guarantee different from a universal duplicate filter?

## Day 12 — Recovery and idempotent sinks

**Concept:** checkpoint recovery, output modes, foreachBatch at-least-once and sink transaction identity.

**Build:** run notebook 05's foreachBatch section on supported compute. Demonstrate the transaction-ID write on the same batch twice in a scratch target; count stays stable. Discuss append/update/complete modes using a windowed aggregation.

**Break:** repeat a plain append without transaction IDs in another scratch target and observe duplicates. Explain why reusing a transaction application ID with a new checkpoint can skip valid writes.

**Evidence:** replay before/after counts and a restart with the original checkpoint. **Explain:** why is a checkpoint insufficient for exactly-once calls to an external API? Avoid assuming atomicity across multiple sinks.

## Day 13 — Jobs, branches, loops and compute

**Concept:** orchestration DAG, task values, retries and resource fit.

**Build:** in Jobs UI create a training job with ingestion → validation → gold. Validation publishes an invalid-row count using `dbutils.jobs.taskValues.set`. Add an If/Else condition and run gold only on the chosen outcome. Add a For Each task over two small region parameters. Export/generate its bundle configuration and compare with the included wheel job.

**Break:** fail validation intentionally; inspect which downstream tasks run, retry or skip. Repair only the failed task after fixing it. Compare serverless settings with a supported high-memory classic notebook task configuration. Locate the job's automatic optimization/retry controls in your workspace.

**Evidence:** task graph, task values, failure and repair run IDs. **Explain:** when should transient failures retry, and when must a data contract failure stop? The kit uses zero retries for its tiny wheel exercise; that is not a production streaming recommendation.

**Performance-mode extension:** where your workspace offers standard and performance-optimized serverless Jobs modes, run the same bounded task in both. Record queue/startup time, execution time and usage, keeping inputs and dependency versions fixed. Explain the latency/cost tradeoff; do not infer a winner from a single cold run. If a mode is unavailable, mark the comparison unverified.

## Day 14 — Managed ingestion and federation

**Concept:** replicating data with Lakeflow Connect versus querying a governed foreign source.

**Build:** follow the prerequisite-gated lab in `advanced-labs.md`. Use a disposable Azure SQL/PostgreSQL source: replicate inserts/updates/deletes with Connect, then query it through a governed federation connection/foreign catalog. Compare freshness and query execution location. Inventory grants at connection, catalog and table scope.

**Break:** with your own disposable connection, revoke the test identity's source read access and diagnose the boundary that fails; restore it.

**Evidence:** source changes and replicated result, federated query, credentials/grant design. If prerequisites are missing, submit the design and mark execution unverified. **Explain:** why is federation not CDC replication?

## Day 15 — Semi-structured data and AI enrichment

**Concept:** VARIANT versus a fixed STRUCT; missing versus JSON null; probabilistic enrichment.

**Build:** run notebook 09's VARIANT section. Extract nested fields, flatten the items array with a supported variant generator, and compare `from_json` with a declared schema. Run the bounded AI lab on five synthetic reviews if an approved endpoint is available; persist source key, prompt/model metadata and result.

**Break:** use malformed JSON and a wrong field type. Simulate endpoint error handling without discarding source rows.

**Evidence:** extracted values, null/error behavior and enrichment lineage. **Explain:** why should inference not be retriggered casually by a row UDF or every dashboard read?

## Day 16 — Delta history and CDF

**Concept:** transaction versions, time travel, change types and incremental downstream processing.

**Build:** run notebook 06's changes section. Read history, choose a valid starting version, query `table_changes` and identify insert, delete, update preimage and postimage. Query an earlier version with `VERSION AS OF`.

**Break:** apply both preimage and postimage as new inserts in a scratch downstream calculation and show double counting. Correct the consumer's change-type handling.

**Evidence:** versioned rows and a correct downstream reconciliation. **Explain:** why is CDF not a permanent independent audit log? What happens when a consumer falls behind retention?

## Day 17 — Table layout and clustering

**Concept:** files, pruning, data skipping and clustering versus partitioning/ZORDER.

**Build:** run the performance table section of notebook 06. Measure a filtered query before/after liquid clustering and OPTIMIZE. Inspect table detail and query profile. Compare fixed clustering with `CLUSTER BY AUTO` where supported. Sketch a large date-partitioned alternative and compare workload assumptions.

**Break:** choose a high-cardinality partitioning key in a small disposable table and count small files; explain why that layout may be poor.

**Evidence:** files/bytes read and layout metadata. **Explain:** why are partitioning/ZORDER not simply additional switches to stack onto a liquid-clustered table? Tiny datasets may show no benefit.

## Day 18 — Deletion vectors and maintenance

**Concept:** write amplification, logical deletion and physical reorganization.

**Build:** create two disposable Delta copies of the performance fixture with supported deletion-vector configurations. Update/delete a small subset; compare history and operation metrics. Inspect table features before enabling them. Compare managed versus external table operational responsibilities and inspect predictive-optimization eligibility/settings.

**Break:** explain why an older unsupported reader might fail after a table feature change; test only if you have an isolated compatible/older client pair.

**Evidence:** operations and feature/protocol metadata. **Explain:** why doesn't a deletion vector mean all deleted bytes have already disappeared? Predictive optimization eligibility is not proof that a particular maintenance run has happened.

## Day 19 — Caching and measured performance

**Concept:** disk cache, result cache, Spark persistence and managed maintenance.

**Build:** run a bounded repeated query. Record compute type and distinguish cold read, warm data read and reused query result. Where supported, persist a Spark DataFrame, consume a derived value, inspect storage, and unpersist it.

**Break:** change input/query or restart disposable compute and predict which caches survive. Do not use a cached result to claim a clustering improvement.

**Evidence:** query IDs, input bytes, cache indicators and repeated timings. **Explain:** which cache is managed automatically, which did you request, and why is cache performance workload-dependent?

## Day 20 — Joins, skew and shuffles

**Concept:** join cardinality, broadcast strategy, aggregation shuffles and skew.

**Build:** use notebook 06's join and create an unhinted comparison. Inspect plans/profile. Add a duplicate dimension key in a scratch view; measure row/revenue inflation. Create a skewed key distribution and inspect task distributions on classic Spark UI or supported serverless query profile.

**Break:** broadcast a dimension that is too large in a design scenario; identify driver/executor memory risks without intentionally exhausting shared compute.

**Evidence:** join counts, plan choice and shuffle observations. **Explain:** when are preaggregation, a corrected join key or adaptive execution preferable to merely adding workers?

## Day 21 — Unity Catalog privileges and functions

**Concept:** catalog/schema/object privileges, inheritance, persistent versus session functions.

**Build:** run notebook 07's SQL function. Match the Python name contract. Have an authorized owner create a lab group and grant the minimum catalog/schema/table privileges to a second identity. Inspect grants; add descriptions/tags.

**Break:** omit `USE SCHEMA` for that identity and distinguish the failure from a missing table `SELECT`. Restore it.

**Evidence:** permission matrix, two-identity query results and function tests. **Explain:** why does having SELECT alone not necessarily make an object usable? Distinguish UC grants from workspace job/notebook ACLs.

## Day 22 — Masks, row filters and ABAC

**Concept:** identity-dependent enforcement versus transformed output; governed tags and policies.

**Build:** run notebook 07's synthetic table/mask/filter. Test with two identities having different lab group memberships. Follow the ABAC lab in `advanced-labs.md` to attach a governed tag policy at schema scope and test a second tagged table.

**Break:** remove a test table's policy-selection tag; record the policy behavior and why unmanaged tags are a control risk. Restore it. Keep table-specific and ABAC experiments on separate tables to avoid overlapping policy ambiguity.

**PII detection extension:** create synthetic text with email-like values, non-PII values and nulls. Implement a documented candidate-detection rule, route flagged records for review, and apply the appropriate governed mask on the published table. Run the same rule against batch input and streaming input; verify that an unauthorized reader cannot see the original value. Record false positives/negatives: a regular expression detects a pattern, not every kind of PII. Keep raw sensitive access restricted in your design.

**Evidence:** before/after authorization matrix and policy audit. **Explain:** why is unsalted hashing of low-entropy PII not automatically anonymization?

## Day 23 — Sharing and Clean Rooms

**Concept:** data-provider versus recipient trust boundary; read sharing versus controlled computation.

**Build:** follow `advanced-labs.md` to share only a synthetic gold object with a disposable recipient. Test allowed and denied access. With an eligible second collaborator, run an approved aggregate-only Clean Rooms notebook and inspect result access.

**Break:** remove the test share grant/recipient access and verify the actual recipient cannot query. Do not assume revocation retracts previously downloaded copies.

**Evidence:** provider/recipient result, grants and clean-room run. Without the extra parties, write the threat model and mark the runtime checks unverified. **Explain:** when does a controlled collaboration workflow solve a different problem from ordinary table sharing?

## Day 24 — Retention and deletion

**Concept:** logical deletion, historical versions, physical file retention and downstream erasure.

**Build:** run the purge-demo section of notebook 07. Observe the current table and history. Trace a synthetic subject through files, bronze, silver, gold, CDF and a consumer. Write an ordered deletion/replay-prevention design.

**Break:** demonstrate that deleting from silver alone leaves the source copy able to reintroduce the subject. Use synthetic fixtures only.

**Evidence:** inventory, deletion verification queries and `VACUUM DRY RUN`. **Explain:** why doesn't a successful DELETE prove end-to-end erasure? Do not shorten retention or disable retention checks to finish the exercise.

## Day 25 — Monitoring and alerts

**Concept:** system tables, usage versus price, freshness and actionable thresholds.

**Build:** run notebook 08's available queries, inspect the compute metadata schema, and attribute one run to its usage where the identifiers exist. Join effective-dated list pricing only after checking its keys/units. Create a SQL/Lakehouse alert on invalid-order count or freshness and use a test destination you control. Also design signals for cost, audit, SQL health and AI failure rate.

**Break:** insert a synthetic invalid order and show a threshold transition, then fix it and show recovery. Account for system-table ingestion latency.

**Evidence:** alert evaluation, query/run identifiers and usage attribution. **Explain:** what action should the alert trigger, and how do you avoid treating every nonzero metric as an incident?

## Day 26 — Debugging and repair

**Concept:** isolate code, environment, permission and data failures using the right evidence.

**Build:** query the actual pipeline event log via notebook 08. Fetch your job state with CLI/API/SDK. Inspect a query profile or Spark UI and correlate it with a run failure. Repair a failed downstream task after a controlled bad-column or parameter error.

**Break:** supply a wrong lab schema parameter and diagnose why upstream data exists but downstream cannot read it. Restore parameters before repair.

**Evidence:** failure timeline, root cause, repaired task/run ID and output reconciliation. **Explain:** when should you repair a task, rerun the whole job, retry a micro-batch or fully refresh a pipeline?

## Day 27 — Deployment promotion and CI/CD

**Concept:** build/test/deploy boundaries, identities, target isolation and configuration drift.

**Build:** validate and deploy the same revision to dev and test after creating the test namespace. Run the wheel smoke test in each. In your CI provider add bundle validation and controlled deployment after test/build using approved workload identity. In a Databricks Git folder inspect branch switching and revision provenance.

**Break:** change the declared test schema to a nonexistent/unauthorized catalog and show the difference between config validation and runtime privilege checks. Restore it. Change a deployed job manually and inspect what redeploy does.

**Evidence:** revision, artifact version, CI log or reproducible local equivalent, dev/test run IDs. **Explain:** why shouldn't an unreviewed branch deploy with a production service principal?

## Day 28 — Iceberg and interoperability

**Concept:** table format versus file format, managed Iceberg versus Delta compatibility features.

**Build:** use the feature-gated Iceberg lab in `advanced-labs.md`: create a tiny managed Iceberg table if enabled, ingest synthetic data, inspect metadata and perform an update/read. Compare governance and layout with Delta. If supported, configure a separate eligible pipeline with an Iceberg target using its current documented settings.

**Break:** try a documented unsupported feature only on an isolated test table and explain the actual format/engine limitation. Do not assume every Delta feature or AUTO CDC mode is available for every Iceberg configuration.

**Evidence:** supported-engine/operation matrix and actual table metadata; external-reader evidence if available. **Explain:** why does having Parquet files alone not make a valid Iceberg table?

## Day 29 — Dimensional model and metrics

**Concept:** grain, surrogate keys, SCD point-in-time joins and reusable measure semantics.

**Build:** run notebook 09's fact/metric view sections with your catalog substituted. Design customer/product/date dimensions. Join an order to the SCD2 customer version valid at order time after mapping sequence to a valid business-time contract. Add a second gold aggregate as a materialized view through the declarative pipeline.

**Break:** join orders to all customer history rows and show revenue inflation; repair the join. Evaluate the same metric at two dimensional groupings.

**Evidence:** grain statement, uniqueness checks, reconciled totals and `MEASURE()` output. **Explain:** why should a global ratio often be recomputed from components rather than averaged from group-level ratios?

## Day 30 — Rebuild, incident and teach-back

**Concept:** integrated correctness under change and failure.

**Build:** from a fresh checkout/environment, run tests, build the wheel, validate/deploy to test, ingest initial files, process CDC, verify silver/quarantine/gold and enforce access with a second identity. Add a late order, a duplicate key, an invalid amount and a new field. Predict all outcomes before running.

**Incident:** choose three earlier failures randomly: missing dependency, schema evolution, denied access, out-of-order CDC, replayed batch, bad join cardinality or a failed task. Diagnose using evidence, repair, and reconcile business totals.

**Evidence:** a runbook someone else can follow and a ten-minute teach-back without notes. For each concept, explain the problem, design choice, rejected alternative, failure behavior and proof. List every admin/service-gated item still unverified; schedule additional practice before claiming mastery.

## Coverage map

These are the official new-outline domain weights; study time also includes shared setup and retrieval practice. Cross-domain days intentionally overlap.

| Domain | Weight | Main days |
|---|---:|---|
| Python/SQL development | 23% | 1–5, 7–13, 21 |
| Ingestion and acquisition | 12% | 6–7, 10, 14, 23, 28 |
| Data manipulation | 12% | 9, 15, 20 |
| Monitoring and alerting | 10% | 25–26 |
| Cost and performance | 15% | 16–20 |
| Security and compliance | 8% | 21–24 |
| Governance | 5% | 21–23 |
| Debugging and deploying | 10% | 2–5, 13, 26–27 |
| Data modeling | 5% | 17, 28–29 |

Source: [official exam guide, new outline](https://www.databricks.com/sites/default/files/2026-09/databricks-certified-data-engineer-professional-exam-guide-oct-2026.pdf). Recheck the official guide two weeks before your exam.

## Readiness rubric

Score each concept 0–3: 0 = unfamiliar; 1 = can describe; 2 = can build with documentation; 3 = can predict, build, diagnose, repair and explain the tradeoffs. Aim for 3 on the core project and no unexamined domain. This is your self-assessment, not an official passing threshold. A blocked external lab is a gap to resolve, not a completed hands-on exercise.
