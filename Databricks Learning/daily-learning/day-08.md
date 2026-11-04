# Day 08 - Declarative pipelines and materialized results

[All days](README.md) | [Previous day](day-07.md) | [Next day](day-09.md)

**Where:** Azure Lakeflow Pipeline; launch from local CLI or the pipeline UI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Notebook 00 has run; bundle deploy is complete; permission and compute for serverless pipelines. This file runs in a pipeline, not with local python.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Declarative functions describe datasets and dependencies; the engine plans execution. A streaming read describes incremental input processing, whereas a batch read can describe a query whose materialized result must reflect the current source.

The project's lp_ tables are separately owned pipeline outputs. lp_gold is a materialized aggregate over lp_silver. The operational tradeoff includes refresh needs, late changes and cost, not just API syntax.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Pipeline Python development](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev)
- [Pipeline concepts](https://learn.microsoft.com/en-us/azure/databricks/ldp/)

## 3. Open today's materials

- [pipelines/retail_pipeline.py](../pipelines/retail_pipeline.py)
- [resources/retail_pipeline.yml](../resources/retail_pipeline.yml)

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

1. Read the source file and identify every dataset name and read dependency before launching.
2. Check `resources/retail_pipeline.yml`: catalog, schema, source volume and CDC table must match notebook 00.
3. In the authenticated project shell:

```powershell
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev retail_pipeline
```

4. Open the pipeline graph. Trace lp_bronze → lp_checked → lp_silver/lp_quarantine → lp_gold. The customer CDC branch can be inspected today; Day 10 explains its semantics.
5. Query lp_gold and compare it with a batch GROUP BY over lp_silver. Inspect which functions return streaming DataFrames and which return batch DataFrames.
6. Add a small new immutable file, run another normal update, and observe incremental source progress. Compare this with notebook 03's explicit query/checkpoint management.

## 5. Verify the result

For batch_001 only: four bronze, three valid silver, one quarantine, valid revenue 75. If Day 7 added batch_002: five bronze, four valid, one quarantine, revenue 87. Additional experimental files change the baseline; inventory them before asserting counts.

## 6. Break one thing and repair it

Introduce a missing-column reference in the development pipeline, inspect the reported graph/update error, restore the column and update again. Avoid collect(), arbitrary writes and external side effects inside dataset definitions.

## 7. Explain without looking

Who schedules a declarative function? Which output needs a maintained full aggregate? When is Structured Streaming preferable?

<details>
<summary>Answer notes - open after your attempt</summary>

The pipeline engine plans execution. A materialized result serves the aggregate query over changing source data. Explicit Structured Streaming is useful when you need supported custom sinks or operational control beyond the declarative graph.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-08/` if useful.

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

[All days](README.md) | [Previous day](day-07.md) | [Next day](day-09.md)
