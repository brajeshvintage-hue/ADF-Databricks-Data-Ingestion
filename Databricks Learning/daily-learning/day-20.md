# Day 20 - Join strategy, skew and shuffle diagnosis

[All days](README.md) | [Previous day](day-19.md) | [Next day](day-21.md)

**Where:** Azure SQL query profile or classic Spark UI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 17 perf_orders. Choose profile tools supported by your compute. Use bounded experiments rather than intentionally exhausting memory.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A shuffle redistributes records for grouping or joins. Skew means some keys/partitions carry far more work. Broadcast can avoid a large-side shuffle when the other side is small enough, but an oversized broadcast can create memory pressure.

Cardinality bugs and resource problems are different: a duplicate dimension key can inflate revenue with perfect execution speed. Check business grain before tuning the plan.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Spark UI diagnosis](https://learn.microsoft.com/en-us/azure/databricks/optimizations/spark-ui-guide/)
- [SQL query profile](https://learn.microsoft.com/en-us/azure/databricks/sql/user/queries/query-profile)

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

1. Run notebook 06's dimension-view and broadcast join section. Compare hinted/unhinted formatted plans and actual query profiles; adaptive planning can affect the final strategy.
2. Use this deterministic cardinality experiment:

```sql
WITH facts AS (SELECT * FROM VALUES (1,10),(2,20) AS f(customer_id,amount)),
dims AS (SELECT * FROM VALUES (1,'A'),(1,'B'),(2,'C') AS d(customer_id,name))
SELECT COUNT(*) AS joined_rows, SUM(amount) AS joined_amount
FROM facts JOIN dims USING(customer_id);
```

3. Repair by defining the intended unique dimension state before joining; do not just SELECT DISTINCT the final revenue.
4. Create a bounded skewed DataFrame using many rows with one customer_id, group/join it and inspect task distributions or profile operators. Compare with uniform Day 17 data.
5. Propose preaggregation, corrected key logic, supported adaptive handling or a different layout. For each proposal state the evidence that would make it appropriate.

## 5. Verify the result

The tiny duplicate-dimension join returns 3 rows and sum 40, while original fact sum is 30. A valid unique-dimension repair preserves 30. Capture shuffle/scan/operator metrics from real runs rather than guessing from the source code alone.

## 6. Break one thing and repair it

Design a broadcast of a dimension larger than memory and explain the likely pressure boundary. Do not deliberately crash shared compute. Identify whether the actual bottleneck is scan, shuffle, join expansion or a straggling partition.

## 7. Explain without looking

Why does more compute not fix a many-to-many mistake? What makes a broadcast safe? Which observation suggests skew?

<details>
<summary>Answer notes - open after your attempt</summary>

Resources cannot repair wrong multiplicity. Broadcast must fit the actual execution memory/strategy constraints. Disproportionately slow or large partitions/tasks suggest skew and require investigation.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-20/` if useful.

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

[All days](README.md) | [Previous day](day-19.md) | [Next day](day-21.md)
