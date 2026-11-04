# Day 26 - Diagnose failures and repair job runs

[All days](README.md) | [Previous day](day-25.md) | [Next day](day-27.md)

**Where:** Azure Jobs/pipeline UI, SQL and authenticated local CLI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** A known training job/run and pipeline ID from previous days. Permission to monitor them; Spark UI availability depends on compute.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Classify the failed boundary before changing code: parameter, missing object, dependency, privilege, bad input, memory/resource pressure or external system. Logs, plans and task state provide different evidence.

Job lifecycle success does not prove business correctness. Repairing selected tasks can save work, but their input assumptions must still hold. A pipeline full refresh has different reconstruction implications from an ordinary update.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Pipeline event log](https://learn.microsoft.com/en-us/azure/databricks/ldp/monitor-event-logs)
- [Spark UI troubleshooting](https://learn.microsoft.com/en-us/azure/databricks/optimizations/spark-ui-guide/)
- [Databricks CLI Jobs commands](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/reference/jobs-commands)

## 3. Open today's materials

- [notebooks/08_observability.sql](../notebooks/08_observability.sql)
- [docs/advanced-labs.md](../docs/advanced-labs.md)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

Before local commands, open PowerShell in the project root (not inside this
daily-learning folder):

```powershell
cd 'C:\Users\braje\OneDrive\Desktop\Documents\ChatGPT\Databricks Learning'
```

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Select one completed run and record its job ID, run ID, task states and output counts. Fetch the same run from your authenticated local shell:

```powershell
databricks jobs get YOUR_JOB_ID
databricks jobs get-run YOUR_RUN_ID
```

Replace the IDs with numeric values from your own job. Inspect equivalent monitoring through the current REST API/SDK reference, using configured authentication rather than a pasted token.
2. Query your actual pipeline event log:

```sql
SELECT timestamp, event_type, message, details
FROM event_log('YOUR_PIPELINE_ID')
ORDER BY timestamp DESC LIMIT 50;
```

3. If the documented regional pipeline-events system table is enabled, compare it with per-pipeline events and its access/latency requirements. Do not assume a beta system table is present everywhere.
4. Introduce a wrong schema parameter in a disposable downstream task. Locate the failure in task output, classify the boundary, fix the parameter and repair the relevant failed tasks.
5. Inspect one relevant SQL profile or classic Spark stage/task/log. Reconcile the repaired output to expected keys and revenue, not only a green task indicator.

## 5. Verify the result

UI and CLI identify the same run/task state. The wrong schema produces a diagnosable missing-object/access boundary rather than a new business rule. A repaired run has both successful task state and reconciled data.

## 6. Break one thing and repair it

Write a timeline: change → first failure → diagnostic evidence → root cause → correction → repair → output proof. Explain why rerunning everything or increasing memory would not repair a wrong schema parameter.

## 7. Explain without looking

When is repair appropriate? Why preserve the source revision/run ID? When might a full refresh require retained raw history?

<details>
<summary>Answer notes - open after your attempt</summary>

Repair is appropriate when corrected tasks can safely reuse the relevant upstream outputs. Revision/run IDs connect evidence to actual code. Reconstructing targets needs adequate retained source data and correct refresh semantics.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-26/` if useful.

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

[All days](README.md) | [Previous day](day-25.md) | [Next day](day-27.md)
