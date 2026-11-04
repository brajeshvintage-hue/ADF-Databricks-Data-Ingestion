# Day 19 - Caches and fair performance experiments

[All days](README.md) | [Previous day](day-18.md) | [Next day](day-20.md)

**Where:** Azure SQL warehouse; optional supported classic Spark compute  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 17 perf_orders and access to Query History/profile. Some Spark persistence APIs are unavailable on serverless; use supported classic compute for that optional comparison.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Result caching can avoid executing a query. Disk/data caching can avoid fetching remote files again. Spark persistence stores an explicitly selected intermediate representation. Each caches a different thing and has different lifetime/availability.

A warm query being faster does not prove your code or clustering improved. Measure repeatable inputs, result consumption, engine/startup conditions, cache indicators and scanned work.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Disk caching behavior](https://learn.microsoft.com/en-us/azure/databricks/optimizations/disk-cache)
- [Query profile and cached-query limitations](https://learn.microsoft.com/en-us/azure/databricks/sql/user/queries/query-profile)

## 3. Open today's materials

- [notebooks/06_delta_and_performance.sql](../notebooks/06_delta_and_performance.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

For added Python cells that use `ns` or `root`, run this configuration cell first.
Replace `main` if your training catalog has a different name; the schema must
already exist from notebook 00. This cell only selects names; it creates nothing.

```python
catalog = 'main'
lab_schema = 'de_pro_lab'
ns = f'{catalog}.{lab_schema}'
root = f'/Volumes/{catalog}/{lab_schema}/lab_files'
```

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Execute a filtered aggregate from Day 17 three times and record query IDs, wall time, bytes scanned and cache/profile availability.
2. Inspect whether a result-cache hit bypassed the execution you hoped to measure. If your supported SQL environment allows it, disable cached results for a controlled experiment using the current documented setting; otherwise compare queries with evidence that execution occurred.
3. Change the predicate, then the projected expression, and predict which type of cache may still help. A comment change alone is not reliable proof of cache bypass.
4. Optional supported classic Spark experiment:

```python
from pyspark.sql import functions as F
base = spark.table(f'{ns}.perf_orders').filter('customer_id < 100')
cached = base.persist()
print(cached.agg(F.sum('amount')).first()[0])
print(cached.agg(F.sum('amount')).first()[0])
cached.unpersist()
```

5. Inspect storage/cache evidence; compare before/after unpersist. Explain what happens when a worker is replaced or when underlying table data changes. Do not restart shared compute just to create a cold run.

## 5. Verify the result

Repeated queries return identical values. Timing and cache hits vary by engine; record observations without inventing a universal speedup. Supported Spark persistence is explicitly released by unpersist.

## 6. Break one thing and repair it

Present a deliberately misleading result: a cached run after a code change. List what additional evidence is needed before attributing the speedup to that change, then collect that evidence where available.

## 7. Explain without looking

What did each cache store? Does unpersist clear SQL result caching? Why might a cached query lack an execution profile?

<details>
<summary>Answer notes - open after your attempt</summary>

Caches store query results, file data or selected DataFrame intermediates. Unpersist acts on the persisted Spark object, not every platform cache. A reused result may bypass normal execution and its operator profile.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-19/` if useful.

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

[All days](README.md) | [Previous day](day-18.md) | [Next day](day-20.md)
