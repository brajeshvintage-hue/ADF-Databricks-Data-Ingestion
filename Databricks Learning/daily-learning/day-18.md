# Day 18 - Deletion vectors and managed maintenance

[All days](README.md) | [Previous day](day-17.md) | [Next day](day-19.md)

**Where:** Azure SQL compute and Catalog Explorer  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 17 perf_orders. Use disposable copies and compute supporting the selected Delta table features; inspect protocol before changing features.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Deletion vectors allow supported operations to record changed/deleted rows without immediately rewriting all original file content. Reads apply the relevant metadata to recover the current logical result. Logical deletion and physical removal occur at different stages.

UC managed tables let the platform own more maintenance responsibilities. Predictive optimization can schedule eligible maintenance, but enabled configuration is not proof a maintenance run already occurred.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Deletion vectors](https://learn.microsoft.com/en-us/azure/databricks/tables/features/deletion-vectors)
- [Predictive optimization](https://learn.microsoft.com/en-us/azure/databricks/optimizations/predictive-optimization)
- [Managed tables](https://learn.microsoft.com/en-us/azure/databricks/tables/managed)

## 3. Open today's materials

- [notebooks/06_delta_and_performance.sql](../notebooks/06_delta_and_performance.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Create separate bounded Delta copies; if these names already exist, inspect them before rerunning:

```sql
CREATE TABLE day18_dv_on USING DELTA
TBLPROPERTIES ('delta.enableDeletionVectors' = 'true') AS SELECT * FROM perf_orders;
CREATE TABLE day18_dv_off USING DELTA
TBLPROPERTIES ('delta.enableDeletionVectors' = 'false') AS SELECT * FROM perf_orders;
DELETE FROM day18_dv_on WHERE order_id < 10;
DELETE FROM day18_dv_off WHERE order_id < 10;
DESCRIBE HISTORY day18_dv_on;
DESCRIBE HISTORY day18_dv_off;
```

2. Compare counts, operation metrics, feature/protocol metadata and physical-write observations. An enabled feature does not guarantee identical engines use an identical optimization for every operation.
3. Inspect managed/external table detail and ownership. In Catalog Explorer or documented SQL inspect predictive-optimization settings/inheritance for the lab's managed tables.
4. Record which operations are supported by your actual runtime/readers. Explain the cost/maintenance owner for an external table versus a UC managed table.
5. Distinguish OPTIMIZE, statistics maintenance and retention cleanup. Do not lower retention or change shared catalog settings to force activity.

## 5. Verify the result

Both tables retain 99,990 rows. Logical contents should agree even if operation/file metrics differ. Capture table type, feature settings and any actual maintenance evidence separately.

## 6. Break one thing and repair it

Model an older reader that cannot understand an enabled feature. Test only if you have an isolated supported/older reader pair. Avoid casually upgrading business table protocols or interpreting absence of immediate physical deletion as a failed DELETE.

## 7. Explain without looking

What is write amplification? Can current data be correct while old bytes remain? Who owns external-table cleanup?

<details>
<summary>Answer notes - open after your attempt</summary>

Changing a few rows can cause disproportionately large rewrites. Transactional metadata can define correct current reads while old files remain under retention. External-table owners retain responsibilities that managed services may automate.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-18/` if useful.

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

[All days](README.md) | [Previous day](day-17.md) | [Next day](day-19.md)
