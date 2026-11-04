# Day 04 - Native expressions, Python UDFs and pandas UDFs

[All days](README.md) | [Previous day](day-03.md) | [Next day](day-05.md)

**Where:** Azure Databricks Python notebook  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Install the Day 2 wheel in the notebook's environment; use runtime-compatible pandas and Arrow. No bronze/silver tables needed.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A native Spark expression describes column operations for the engine. A scalar Python UDF enables a custom per-value rule. A pandas UDF moves batches through Arrow and operates on pandas objects. Batch transfer and vectorized business logic are related but different ideas.

The correct comparison starts with an identical contract: null/blank handling, output type and row cardinality. A Series-to-Series pandas UDF must return the same number of results as inputs. Timing an unused UDF with count can mislead because Spark can prune unneeded expressions.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Python scalar UDFs](https://learn.microsoft.com/en-us/azure/databricks/udf/python)
- [pandas UDF contracts](https://learn.microsoft.com/en-us/azure/databricks/udf/pandas)

## 3. Open today's materials

- [notebooks/01_udfs.py](../notebooks/01_udfs.py)
- [src/retail_de/transforms.py](../src/retail_de/transforms.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Predict normalized output for null, blank, tabs and repeated ASCII spaces.
2. Import and run `notebooks/01_udfs.py` in Azure. Its three implementations must agree with the explicit expected DataFrame.
3. Inspect each formatted plan. Identify where Python or Arrow evaluation occurs; labels can vary with runtime.
4. Run the bounded benchmark, which sums output string lengths. Save every trial and compute configuration. Do not report a universal speed ranking from this small fixture.
5. Write a second scalar function using `@udf('long')` to double a nullable integer. Then implement it as a native expression and a pandas UDF. State the null and output-type contract before running.

```python
from pyspark.sql import functions as F
@F.udf('long')
def double_or_null(value):
    return None if value is None else value * 2
display(spark.createDataFrame([(2,), (None,)], 'n long')
        .select(double_or_null('n').alias('twice')))
```

6. Compare a session registration in the starter notebook with the persistent governed functions you will build on Day 21.

## 5. Verify the result

All name implementations return ALICE SMITH, BOB, null, null. Each benchmark produces checksum 1,100,000 for 100,000 rows. Doubling returns 4 and null. Runtime timings can vary; correctness must agree.

## 6. Break one thing and repair it

In disposable definitions, remove null handling and return a shortened pandas Series. Observe and repair both errors. Do not rely on WHERE filtering to guarantee unsafe UDF inputs never arrive.

## 7. Explain without looking

When is a native expression preferable? Does Series.apply automatically vectorize a Python function? Why must a benchmark consume the transformed value?

<details>
<summary>Answer notes - open after your attempt</summary>

Prefer a built-in expression when it represents the rule clearly. Series.apply may still run Python element by element. Consuming transformed output prevents measuring a plan that discarded the work under investigation.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-04/` if useful.

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

[All days](README.md) | [Previous day](day-03.md) | [Next day](day-05.md)
