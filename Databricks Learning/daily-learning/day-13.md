# Day 13 - Jobs, conditions, loops, retries and compute

[All days](README.md) | [Previous day](day-12.md) | [Next day](day-14.md)

**Where:** Azure Jobs UI, notebook tasks and authenticated CLI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 2 deployment and bronze data. Permission to create training Jobs; supported serverless or policy-approved classic compute. Leave schedules disabled.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Jobs coordinate task dependencies and run conditions. A task value is small orchestration metadata, not a substitute for a data table. Branches choose which outcomes run; For Each applies a task to a parameter set.

Compute configuration belongs to the execution environment. Standard serverless performance mode and performance-optimized mode trade usage against startup/execution latency. Retrying a transient failure can help; retrying an invalid data contract without a fix repeats the problem.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Bundle task types and control flow](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/job-task-types)
- [Serverless Jobs and performance modes](https://learn.microsoft.com/en-us/azure/databricks/jobs/run-serverless-jobs)

## 3. Open today's materials

- [resources/retail_job.yml](../resources/retail_job.yml)
- [notebooks/04_batch_silver_gold.py](../notebooks/04_batch_silver_gold.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. In Jobs & Pipelines create a manual training job with ingestion → validation → gold. Use the imported source notebooks; configure the same catalog/schema widgets.
2. Create a validation notebook with:

```python
invalid = spark.table('YOUR_CATALOG.de_pro_lab.quarantine_orders').count()
dbutils.jobs.taskValues.set(key='invalid_orders', value=invalid)
```

3. Add an If/Else task comparing `{{tasks.validation.values.invalid_orders}}` with your threshold. Set gold's dependency to the chosen condition outcome.
4. Add For Each over `["CA", "US"]`. In its nested notebook read the region parameter and query only that region. Export/generate the job's bundle definition and inspect the resulting task graph.
5. Toggle Performance optimized for the same bounded serverless job where available. Run comparable trials and record startup, task execution and usage. Compare with the configuration needed for a high-memory classic notebook task; use real policy/node choices from your workspace.
6. Locate retry/automatic-optimization settings. For a disposable task choose an intentional failure and configure the retry behavior. Generate a second minimal job through the current API/SDK schema to compare with UI creation.

## 5. Verify the result

The invalid-count branch is predictable from actual quarantine. CA/US loop tasks receive different parameters. A failed upstream task changes downstream eligibility. Record actual mode/usage, not an assumed universal cost reduction.

## 6. Break one thing and repair it

Fail the validation task once, inspect retries/skips and repair the failed section after fixing it. Distinguish a repair from a completely new run. Keep bundle-managed and API-created demonstration jobs separate.

## 7. Explain without looking

Does depends_on mean a task always runs? What is max_retries protecting against? Why keep For Each parameters small?

<details>
<summary>Answer notes - open after your attempt</summary>

Run-if/condition outcomes also control eligibility. Retries address supported transient/recoverable attempts, not arbitrary correctness flaws. Task parameters/values coordinate work; large datasets belong in durable data assets.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-13/` if useful.

- **Status:** not started / built / verified / needs access / repeat
- **The problem this concept solves, in my words:**
- **My prediction:**
- **What I actually observed (values/schema/plan/run ID):**
- **The failure I introduced and its root cause:**
- **The repair and how I verified it:**
- **When I would choose a different approach:**
- **Runtime, environment and revision used:**
- **Still uncertain / missing prerequisites:**

## Completion check

- [ ] I stated the input/output or operational contract before running.
- [ ] I built the main exercise and checked its actual result.
- [ ] I diagnosed and repaired the controlled failure.
- [ ] I answered the questions in my own words.
- [ ] I marked unavailable service/identity/feature checks as pending.
- [ ] I will revisit this concept tomorrow and again after 3 and 7 days.

[All days](README.md) | [Previous day](day-12.md) | [Next day](day-14.md)
