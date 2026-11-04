# Day 09 - Quality rules, quarantine, windows and joins

[All days](README.md) | [Previous day](day-08.md) | [Next day](day-10.md)

**Where:** Azure Python notebook and pipeline UI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Bronze from Day 6/7 and the pipeline from Day 8. Use the current source inventory when reconciling totals.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A quality rule needs an explicit disposition: retain and measure, drop, fail, or route to quarantine. SQL null predicates can escape both WHERE valid and WHERE NOT valid unless you define null handling.

A row_number window chooses one version per key only when ordering is meaningful. Joining a fact to multiple matching dimension rows multiplies the fact. Validation must therefore include grain and cardinality, not just whether the job succeeded.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Pipeline expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations)
- [Query profile and row cardinality](https://learn.microsoft.com/en-us/azure/databricks/sql/user/queries/query-profile)

## 3. Open today's materials

- [notebooks/04_batch_silver_gold.py](../notebooks/04_batch_silver_gold.py)
- [pipelines/retail_pipeline.py](../pipelines/retail_pipeline.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run `04_batch_silver_gold.py`. Inspect how the complete validity rule is coalesced to False.
2. Reconcile input = valid before dedup + quarantine, then count duplicates removed before silver. Distinguish rejected data from duplicate valid versions.
3. Write a SQL equivalent of the window:

```sql
-- Use your catalog and lab schema.
SELECT * EXCEPT(rn) FROM (
  SELECT *, row_number() OVER (
    PARTITION BY order_id ORDER BY event_time DESC, source_file DESC
  ) AS rn
  FROM bronze_orders
  WHERE order_id IS NOT NULL AND customer_id IS NOT NULL
    AND event_time IS NOT NULL AND amount >= 0 AND _rescued_data IS NULL
) WHERE rn = 1;
```

4. Inspect the warning/drop expectations in the pipeline. Change one to expect_or_fail in development, run, and record the failed update's outcome. Restore the original definition.
5. Create a two-row customer lookup, join to valid orders, aggregate revenue and then add a duplicate lookup key. Observe the change in cardinality and repair the lookup/join contract.

## 5. Verify the result

Initial valid revenue is 75, or 87 after the optional coupon order. One supplied negative order is quarantined. A duplicated dimension key can inflate revenue even if all amounts are nonnegative and every task is green.

## 6. Break one thing and repair it

Create a small DataFrame containing amount null and use only amount >= 0 as a filter. Compare WHERE predicate and WHERE NOT predicate, then coalesce the rule. Explain which row was otherwise unaccounted for.

## 7. Explain without looking

Does expect_or_drop automatically preserve rejected rows elsewhere? Why does dedup need a tie policy? Can a join pass all row-level quality tests and still be wrong?

<details>
<summary>Answer notes - open after your attempt</summary>

Dropping needs a separate quarantine branch to preserve rejects. Ambiguous ties cannot reliably choose the intended version. Join multiplicity is a cross-row invariant that per-row rules may miss.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-09/` if useful.

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

[All days](README.md) | [Previous day](day-08.md) | [Next day](day-10.md)
