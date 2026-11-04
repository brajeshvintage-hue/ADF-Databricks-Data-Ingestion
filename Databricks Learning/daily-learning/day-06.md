# Day 06 - Batch formats, binary files and bronze ingestion

[All days](README.md) | [Previous day](day-05.md) | [Next day](day-07.md)

**Where:** Azure Python notebook  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Run notebook 00 first with your catalog/schema. It defines ns and root and seeds four orders. Import all Python notebooks into the same workspace folder so their relative %run paths resolve.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

File encoding and table semantics are different layers. JSON and CSV need parsing; Parquet carries a columnar schema. binaryFile returns file-level content and metadata, so it does not parse each JSON order into a row.

Bronze preserves an ingestion boundary. Auto Loader's cloudFiles source processes newly discovered files incrementally. Neither a successful file read nor append-only ingestion proves uniqueness of order_id.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Auto Loader source and behavior](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/)
- [File formats and ingestion](https://learn.microsoft.com/en-us/azure/databricks/ingestion/)

## 3. Open today's materials

- [notebooks/00_setup.py](../notebooks/00_setup.py)
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

1. Run `00_setup.py` and inspect the source file. Use the values of `ns` and `root` it prints.
2. In the same notebook/session compare encodings:

```python
schema = 'order_id long, customer_id long, customer_name string, amount double, event_time timestamp, region string'
orders = spark.read.schema(schema).json(f'{root}/orders')
orders.write.mode('overwrite').option('header', True).csv(f'{root}/formats/csv')
orders.write.mode('overwrite').parquet(f'{root}/formats/parquet')
csv = spark.read.option('header', True).csv(f'{root}/formats/csv')
parquet = spark.read.parquet(f'{root}/formats/parquet')
csv.printSchema()
parquet.printSchema()
display(spark.read.format('binaryFile').load(f'{root}/orders')
        .select('path', 'length'))
```

3. Re-read CSV with the explicit schema and compare types/nulls.
4. Run `03_ingest.py` to create bronze. Run its ingestion cell again with the same checkpoint; verify count is unchanged.
5. If an approved broker exists, build a bounded Kafka/Event Hubs read using the source's documented authentication and offset options. Otherwise draw the design and mark broker execution pending. Compare connector-specific offset/credential concepts for Kafka, Kinesis and Pub/Sub; they are not interchangeable configurations.

## 5. Verify the result

With only batch_001, parsed data has four rows; binaryFile has one file row. Header-only CSV reading produces string columns while Parquet retains declared types. Bronze stays at four rows when unchanged files are reprocessed with the same checkpoint.

## 6. Break one thing and repair it

In a scratch folder create malformed JSON and compare PERMISSIVE/FAILFAST parsing. Do not place this experiment in the working orders directory. Separate malformed syntax from a valid JSON value with the wrong business type.

## 7. Explain without looking

Why isn't binaryFile equivalent to JSON reading? Where is source progress stored? Does count 4 prove unique business keys?

<details>
<summary>Answer notes - open after your attempt</summary>

Binary ingestion preserves bytes per file, while JSON parsing produces records. Streaming checkpoints preserve progress. Row count alone cannot establish business uniqueness.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-06/` if useful.

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

[All days](README.md) | [Previous day](day-05.md) | [Next day](day-07.md)
