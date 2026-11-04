# Day 07 - Auto Loader schema changes and rescued data

[All days](README.md) | [Previous day](day-06.md) | [Next day](day-08.md)

**Where:** Azure Python notebook  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 6 bronze/checkpoint exists. Keep the original source files immutable. New experiments use new filenames, not overwrites of consumed files.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

There are three separate persisted concerns: Auto Loader's schema, streaming progress/checkpoint state, and the target table schema. A new column can evolve the discovered schema and stop the stream so it can restart using that schema. The target must also accept the new column.

Rescued data records fields that do not conform to the parsing contract. It provides investigation context; it does not make those fields valid business values. A type mismatch is different from adding a new column.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Schema inference, evolution and rescue](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/schema)

## 3. Open today's materials

- [notebooks/03_ingest.py](../notebooks/03_ingest.py)

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

1. Run notebook 03's ingestion again and record the baseline count/schema.
2. In that notebook uncomment the optional `batch_002.json` creation lines and execute them once. Do not set overwrite=True.
3. Run ingestion. If it stops for a schema-evolution change, capture the message and rerun with the same schema/checkpoint locations. Verify coupon appears in the source and target schemas.
4. Inspect bronze:

```python
display(spark.table(f'{ns}.bronze_orders')
        .select('order_id', 'amount', 'coupon', '_rescued_data'))
```

5. Under a separate scratch input path create an amount='not-a-number' record. Create a separate cloudFiles stream with amount DOUBLE hints and rescue mode, its own schema path, checkpoint and target. Inspect the rescued JSON. Keep this experiment out of the core bronze stream.
6. Write a three-column inventory: source schema path, checkpoint path, destination table. Explain why none is a substitute for the others.

## 5. Verify the result

With the two supplied files, bronze contains five rows and total valid order amount becomes 87. New-file creation should fail if blindly repeated; inspect existing files instead. A rescued type mismatch should remain visible for investigation.

## 6. Break one thing and repair it

Point a scratch stream at a new checkpoint and predict replay before executing into a new scratch target. Do not discard the working checkpoint. Compare counts and explain why downstream dedup may still be necessary.

## 7. Explain without looking

Why can schema evolution require restart? Why might target mergeSchema be required too? What would a new checkpoint forget?

<details>
<summary>Answer notes - open after your attempt</summary>

The running query was planned for an earlier schema. The sink has a separate schema contract. A new checkpoint lacks prior progress and state, so it cannot stand in for recovery of the old query.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-07/` if useful.

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

[All days](README.md) | [Previous day](day-06.md) | [Next day](day-08.md)
