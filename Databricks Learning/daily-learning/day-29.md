# Day 29 - Dimensional grain, historical joins and metric views

[All days](README.md) | [Previous day](day-28.md) | [Next day](day-30.md)

**Where:** Azure SQL and the declarative pipeline  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 9 silver data, Day 10 history, supported metric-view compute. Set namespace references in notebook 09, including the fully qualified source inside metric YAML.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Grain states what one fact row represents. Customer/product/date dimensions add analytical context; a historical dimension must match the version valid for the fact's relevant time. Joining all historical versions inflates measures.

A metric view centralizes analytical definitions. A materialized aggregate persists a result for a refresh/performance need. Defining a reusable metric does not automatically make every expensive query precomputed.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Metric-view YAML and semantics](https://learn.microsoft.com/en-us/azure/databricks/uc-semantics/metric-views/yaml-reference)
- [Pipeline materialized views](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev)

## 3. Open today's materials

- [notebooks/09_variant_modeling.sql](../notebooks/09_variant_modeling.sql)
- [pipelines/retail_pipeline.py](../pipelines/retail_pipeline.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run notebook 09's fact and metric-view sections after changing all main/de_pro_lab references, including YAML source. Check fact order_id uniqueness and reconcile revenue to silver.
2. Design a separate business-time SCD2 dimension; the core sequence column is an ordering number, not a timestamp. Test a point-in-time join:

```sql
WITH fact AS (
 SELECT 10 customer_id, TIMESTAMP '2026-10-01 10:00:00' order_time, 25 amount
), dim AS (
 SELECT * FROM VALUES
 (10, 'CA', TIMESTAMP '2026-01-01', TIMESTAMP '2026-10-01 12:00:00'),
 (10, 'US', TIMESTAMP '2026-10-01 12:00:00', CAST(NULL AS TIMESTAMP))
 AS d(customer_id,region,valid_from,valid_to)
)
SELECT f.amount, d.region FROM fact f JOIN dim d
 ON f.customer_id=d.customer_id AND f.order_time>=d.valid_from
 AND (f.order_time<d.valid_to OR d.valid_to IS NULL);
```

3. Remove the interval condition in a scratch query, compare row count/revenue, then restore it. Add boundary-time tests at exactly valid_to/valid_from.
4. Query sales_metrics with MEASURE(Revenue)/MEASURE(Orders) at multiple region groupings. Add a ratio from properly aggregated components.
5. Add a second materialized gold aggregate through the pipeline and compare its refresh/performance role with the metric definition.

## 5. Verify the result

The historical join returns one CA row with amount 25. Without time filtering it returns two matches and can sum to 50. Core fact revenue remains 75 or 87 depending on the supplied files, plus any deliberate later valid additions.

## 6. Break one thing and repair it

Average regional ratios and compare with a global ratio computed from summed numerators/denominators. Explain the weighting difference. Do not repair join inflation by averaging away duplicate fact rows.

## 7. Explain without looking

What is the fact grain? Why use a half-open history interval? Does a metric view always persist preaggregated rows?

<details>
<summary>Answer notes - open after your attempt</summary>

State the real business entity per fact row. Half-open intervals avoid double matches at shared boundaries. Metric definitions and materialized query results have distinct roles; inspect actual materialization configuration.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-29/` if useful.

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

[All days](README.md) | [Previous day](day-28.md) | [Next day](day-30.md)
