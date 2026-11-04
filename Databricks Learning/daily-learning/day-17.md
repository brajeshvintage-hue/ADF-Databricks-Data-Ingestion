# Day 17 - Liquid clustering, file layout and pruning

[All days](README.md) | [Previous day](day-16.md) | [Next day](day-18.md)

**Where:** Azure SQL compute with supported liquid clustering  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Isolated schema. Start at 100,000 rows; use larger data only with a chosen budget. Record query cache state and actual engine.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Layout changes the physical work needed for a query. Liquid clustering organizes records around useful access keys without traditional fixed directory partitioning. Statistics and file skipping reduce scanned data when a predicate can exploit the layout.

Partitioning, ZORDER and liquid clustering are choices with compatibility constraints, not switches to stack blindly. A tiny table may show no measurable benefit even when a design is appropriate at larger scale.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Liquid clustering and compatibility](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering)
- [Query profile metrics](https://learn.microsoft.com/en-us/azure/databricks/sql/user/queries/query-profile)

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

1. In notebook 06 run the bounded perf_orders creation and filtered query before the clustering commands.
2. Record query ID, files/bytes scanned, rows returned, plan and runtime. Then enable customer_id clustering, run OPTIMIZE and repeat.
3. Verify a business invariant:

```sql
SELECT COUNT(*) AS n, SUM(amount) AS total FROM perf_orders;
SELECT SUM(amount) AS filtered_total FROM perf_orders WHERE customer_id = 42;
DESCRIBE DETAIL perf_orders;
```

4. Where supported, compare fixed keys with CLUSTER BY AUTO and inspect how eligibility/optimization works. Do not assume automatic keys are chosen immediately on this small workload.
5. In a separate small disposable table compare a date-like partition key with a high-cardinality identifier. Inspect file counts. Write which query patterns justify each choice.
6. Use the Query History profile, not only wall-clock time. Keep a saved before/after record with cache conditions.

## 5. Verify the result

The fixture has 100,000 rows and total amount 9,950,000. customer_id 42 has 100 rows and filtered total 4,200. Layout work must preserve values; performance improvement is not guaranteed at this size.

## 6. Break one thing and repair it

Propose partitioning by unique order_id and explain the small-file/directory consequence. Test only at a small bounded size. If a command rejects mixing clustering and partitioning, use the error to identify the supported layout contract.

## 7. Explain without looking

Why can a faster query be misleading? When does clustering help skipping? Does changing keys rewrite every existing file immediately?

<details>
<summary>Answer notes - open after your attempt</summary>

Caches and startup can dominate timings. Skipping needs an exploitable predicate and useful file organization/statistics. Metadata/key changes and physical maintenance are separate events; inspect actual operations.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-17/` if useful.

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

[All days](README.md) | [Previous day](day-16.md) | [Next day](day-18.md)
