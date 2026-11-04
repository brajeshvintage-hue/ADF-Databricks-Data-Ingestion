# Day 15 - VARIANT and bounded AI enrichment

[All days](README.md) | [Previous day](day-14.md) | [Next day](day-16.md)

**Where:** Supported Azure SQL warehouse/notebook; optional approved model endpoint  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** VARIANT-capable compute. AI extension needs an existing approved endpoint, invocation permissions and a small inference budget; use synthetic text only.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

VARIANT stores flexible nested values while allowing typed field extraction. Missing path, SQL null, JSON null, malformed JSON and an invalid cast are distinct cases. Flexible structure still needs an analytical contract.

AI enrichment is model-dependent interpretation. Store source identifiers, prompt/model provenance and errors. Repeated dashboard queries or retried UDF tasks should not accidentally trigger uncontrolled inference.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Query and flatten VARIANT](https://learn.microsoft.com/en-us/azure/databricks/semi-structured/variant)
- [ai_query contract and options](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_query)

## 3. Open today's materials

- [notebooks/09_variant_modeling.sql](../notebooks/09_variant_modeling.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run only the VARIANT section of notebook 09; its modeling sections belong to Day 29. Replace the catalog/schema header first.
2. Test nested extraction and null semantics independently:

```sql
SELECT variant_get(parse_json('{"order":{"id":7}}'), '$.order.id', 'bigint') AS id,
       variant_get(parse_json('{"order":{}}'), '$.order.id', 'bigint') AS missing;
SELECT try_parse_json('{invalid') AS malformed,
       is_variant_null(parse_json('null')) AS is_json_null;
```

3. Flatten the fixture's items with the current documented variant generator. Compare storing raw JSON STRING, a declared STRUCT and VARIANT for a newly added field. Test case-sensitive field names.
4. If endpoint access exists, run a bounded query on five synthetic reviews. Inspect the endpoint's request/response contract before adapting:

```sql
SELECT ai_query('YOUR_APPROVED_ENDPOINT',
  'Classify as positive, neutral or negative. Return one label: Delivery was fast') AS label;
```

5. Persist review key, input, endpoint/model provenance, prompt version, result, timestamp and error state in a lab table. Validate labels and separately test failure handling using supported ai_query options. If the endpoint is missing, record the blocked prerequisite rather than inventing an output.

## 5. Verify the result

Nested id is 7; missing field and try_parse_json malformed result are SQL null; is_json_null is true. AI output is not a fixed expected string: it must satisfy the chosen response contract and retain traceability.

## 6. Break one thing and repair it

Use a wrong extraction type and compare strict versus supported try conversion behavior. Simulate a missing endpoint or test response in an isolated exercise; retain the source review even when enrichment fails.

## 7. Explain without looking

Is flexible schema the same as no contract? Why preserve raw source/provenance? Should AI output automatically determine a financial fact?

<details>
<summary>Answer notes - open after your attempt</summary>

Consumers still need typed fields and quality rules. Source/provenance enables repair and audit. Model judgments need validation and a defined role, especially when deterministic source facts exist.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-15/` if useful.

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

[All days](README.md) | [Previous day](day-14.md) | [Next day](day-16.md)
