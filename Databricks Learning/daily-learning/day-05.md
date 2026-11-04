# Day 05 - Testing, DataFrame contracts and CI

[All days](README.md) | [Previous day](day-04.md) | [Next day](day-06.md)

**Where:** Local PowerShell and Azure Python notebook  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Days 1–4 complete. Optional repository/CI access; local test/build commands work without a remote CI provider.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Unit tests isolate a business rule. Integration tests exercise runtime boundaries such as Spark schema, worker dependencies and table writes. A test proving four rows exist cannot prove those four values are correct.

DataFrame.transform composes a DataFrame-to-DataFrame function; it is not a separate scheduler or an automatic performance optimization. CI repeats validation on a known revision so changes cannot rely solely on someone's notebook session.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Testing through Databricks Connect](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect/python/testing)
- [CI/CD on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/)

## 3. Open today's materials

- [tests/test_cleaning.py](../tests/test_cleaning.py)
- [notebooks/01_udfs.py](../notebooks/01_udfs.py)
- [.github/workflows/ci.yml](../.github/workflows/ci.yml)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run the existing local contract suite, then add your Day 1 amount-validator tests.
2. In Azure rerun notebook 01's `assertDataFrameEqual` and `assertSchemaEqual` checks. Where order matters, order by a key and explicitly check row order.
3. Write this small independent integration assertion:

```python
from pyspark.testing.utils import assertDataFrameEqual, assertSchemaEqual
from retail_de.transforms import add_normalized_name
source = spark.createDataFrame([(1, '  bob '), (2, None)], 'id long, customer_name string')
actual = source.transform(add_normalized_name).select('id', 'normalized_name')
expected = spark.createDataFrame([(1, 'BOB'), (2, None)], 'id long, normalized_name string')
assertDataFrameEqual(actual.orderBy('id'), expected.orderBy('id'), checkRowOrder=True)
assertSchemaEqual(actual.schema, expected.schema)
```

4. Inspect `.github/workflows/ci.yml`: identify checkout, Python setup, tests, build and artifact upload. Run the same commands locally. If using Azure DevOps, implement equivalent stages in your own training pipeline rather than uploading the GitHub workflow unchanged.
5. Reinstall the built wheel in a clean environment outside the source import path and repeat the demo. This catches accidental reliance on the source checkout.

## 5. Verify the result

Local and Spark contract checks pass. CI/local build produces a versioned distribution. Record each check's scope: none of these alone proves a new workspace identity can write a UC table.

## 6. Break one thing and repair it

Change a test input to expose a missing rule, then fix the rule. Separately change the output type or column name and see the integration check fail. Restore the agreed contract.

## 7. Explain without looking

What does a schema assertion catch that a count misses? Why test an installed wheel? What should run before cloud deployment in CI?

<details>
<summary>Answer notes - open after your attempt</summary>

Schema checks detect structural/type mismatches; counts cannot. Installed-wheel testing checks packaging/import boundaries. Run relevant tests and artifact build before deployment, then a small workspace smoke test afterward.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-05/` if useful.

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

[All days](README.md) | [Previous day](day-04.md) | [Next day](day-06.md)
