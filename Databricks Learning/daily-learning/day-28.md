# Day 28 - Iceberg, table formats and interoperability

[All days](README.md) | [Previous day](day-27.md) | [Next day](day-29.md)

**Where:** Azure SQL compute with managed Iceberg support  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** UC managed storage, permission to create lab tables and supported Iceberg features. External-reader proof requires an eligible engine and authorized catalog access; do not add arbitrary JARs to bypass unsupported runtime features.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Parquet is a file encoding. Iceberg and Delta provide transactional table metadata across files. A directory containing Parquet is not automatically an Iceberg table. Readers must understand the actual metadata, table features and access path.

A native managed Iceberg table differs from a Delta table exposing Iceberg-compatible metadata. Supported writes, clustering, CDC and engine combinations depend on the current table/runtime feature set.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Iceberg on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/iceberg/)
- [CREATE TABLE and format constraints](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-create-table-using)

## 3. Open today's materials

- [docs/advanced-labs.md](../docs/advanced-labs.md)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Check the linked feature requirements against your workspace before creating a table.
2. On supported SQL compute, replace the namespace and run once:

```sql
CREATE TABLE main.de_pro_lab.day28_iceberg
  (order_id BIGINT, amount DOUBLE) USING ICEBERG;
INSERT INTO main.de_pro_lab.day28_iceberg VALUES (1,25), (2,40);
UPDATE main.de_pro_lab.day28_iceberg SET amount = 30 WHERE order_id = 1;
SELECT COUNT(*) AS n, SUM(amount) AS total FROM main.de_pro_lab.day28_iceberg;
DESCRIBE EXTENDED main.de_pro_lab.day28_iceberg;
```

3. Create a separate Delta equivalent and compare metadata, ownership, supported operations and maintenance requirements. Do not mutate the running core pipeline's format.
4. Through the current pipeline UI/docs configure a SEPARATE eligible minimal CDC pipeline with an Iceberg target where supported. Export its generated definition and document supported SCD/CDC features before assuming parity with the existing Delta pipeline.
5. If an external REST-catalog reader is available, authorize only the lab asset and verify its read. Otherwise record interoperability as a design matrix, not a successful external read.
6. Record restrictions for layout/partitioning and any feature compatibility changes. A missing feature should remain a documented prerequisite.

## 5. Verify the result

On supported compute the managed Iceberg table has two rows and sum 70. Metadata identifies its actual table type/format. External and Iceberg-target CDC evidence exists only after those independent runs succeed.

## 6. Break one thing and repair it

Choose one currently documented unsupported combination on an isolated table and predict/review the resulting failure. Avoid treating every data-source-not-found error as a missing Python library.

## 7. Explain without looking

Why are table and file formats different? Does every Delta feature work in every Iceberg reader? Can a source format and target format differ?

<details>
<summary>Answer notes - open after your attempt</summary>

Table metadata defines transactional interpretation over files. Feature compatibility must be checked per engine/table configuration. Ingestion can transform between supported source and target formats with an explicit schema/semantics contract.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-28/` if useful.

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

[All days](README.md) | [Previous day](day-27.md) | [Next day](day-29.md)
