# Day 10 - AUTO CDC, out-of-order changes and SCD history

[All days](README.md) | [Previous day](day-09.md) | [Next day](day-11.md)

**Where:** Azure pipeline and SQL notebook  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 8 pipeline and notebook 00's append-only customer_cdc source. Use a pipeline configuration supporting AUTO CDC.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

CDC application turns a change stream into table state. The sequence is a source-order contract, not necessarily arrival order. SCD1 keeps current attributes; SCD2 preserves version intervals. AUTO CDC handles updates/deletes using keys, sequencing and the configured history policy.

The fixture deliberately contains customer 10's sequence 3 before sequence 2. The current state must still reflect sequence 3. Delta CDF exposes committed table changes; it is not the same operation as applying a database CDC feed.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [AUTO CDC and SCD examples](https://learn.microsoft.com/en-us/azure/databricks/ldp/cdc)

## 3. Open today's materials

- [pipelines/retail_pipeline.py](../pipelines/retail_pipeline.py)
- [notebooks/00_setup.py](../notebooks/00_setup.py)

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

1. Read the five fixture CDC records in notebook 00 and predict both target states before querying.
2. Run a normal pipeline update and execute SQL using your catalog/schema:

```sql
SELECT * FROM lp_customer_current ORDER BY customer_id;
SELECT * FROM lp_customer_history ORDER BY customer_id, __START_AT;
```

3. Identify current SCD2 rows with __END_AT IS NULL and explain deleted keys.
4. Append one synthetic update using a NEW key/sequence pair:

```python
spark.createDataFrame([(10, 'Alice', 'UK', 5, 'UPDATE')],
    'customer_id long, name string, region string, sequence long, operation string'
).write.mode('append').saveAsTable(f'{ns}.customer_cdc')
```

Run that append only once, update the pipeline, and inspect the new history interval.
5. Design a same-key/same-sequence conflict. State a source ordering/tie rule before testing it with an isolated key. Do not use an arbitrary dropDuplicates to hide conflicting versions.

## 5. Verify the result

Before the extension: customer 10 has region US; customer 20 is absent from current state after its delete. After sequence 5: customer 10 is UK and history reflects the transition. Sequence intervals are not automatically business timestamps.

## 6. Break one thing and repair it

Append a late lower-sequence event for a separate new synthetic customer after a higher sequence. Verify current state remains consistent with ordering. Explain any history changes rather than assuming the late row is always discarded.

## 7. Explain without looking

Why is arrival-order last-write-wins unsafe? Can SCD sequence intervals be joined directly to order timestamps? How would full refresh affect source retention needs?

<details>
<summary>Answer notes - open after your attempt</summary>

Arrival can reorder events. Only a defined mapping makes a sequence comparable with business time. Rebuilding history requires retaining the source changes needed to reconstruct it.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-10/` if useful.

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

[All days](README.md) | [Previous day](day-09.md) | [Next day](day-11.md)
