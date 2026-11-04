# Day 22 - PII detection, masks, row filters and ABAC

[All days](README.md) | [Previous day](day-21.md) | [Next day](day-23.md)

**Where:** Azure Python/SQL plus governed-tag/policy administration  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Two lab identities/groups, policy-capable compute and permissions. Keep direct table-mask and ABAC examples on separate synthetic tables. Never add a training policy to a business catalog.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Detection identifies candidate sensitive content; policy decides who can see it. A regular expression is a limited detector, not proof all PII has been found. Column masks and row filters enforce query-time visibility; downstream transformed copies need their own access design.

ABAC selects controls using governed tags and policies so one scoped policy can cover many tagged assets. Tag assignment rights and policy scope are part of that enforcement boundary. Hashing/tokenization can preserve linkability and are not automatically anonymization.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Row filters and masks](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/)
- [Governed-tag ABAC](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/core-concepts)

## 3. Open today's materials

- [notebooks/07_governance.sql](../notebooks/07_governance.sql)
- [docs/advanced-labs.md](../docs/advanced-labs.md)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run notebook 07's synthetic people_demo mask/filter cells and test two identities with different lab group memberships.
2. Create candidate-PII input separately from the orders source:

```python
from pyspark.sql import functions as F
texts = spark.createDataFrame([(1, 'alice@example.test'), (2, 'ordinary text'), (3, None)],
                             'id long, text string')
flagged = texts.withColumn('candidate_email', F.coalesce(
    F.col('text').rlike(r'[^\s@]+@[^\s@]+\.[^\s@]+'), F.lit(False)))
display(flagged)
```

3. Write the synthetic texts to an isolated append-only Delta source and apply the same column expression to spark.readStream.table. Use a new checkpoint and published target. Verify an unauthorized identity sees the governed mask rather than the original candidate value. Keep raw input access restricted.
4. In Catalog Explorer create governed tag lab_pii, tag email columns in two NEW synthetic tables, and attach a schema-scoped column-mask ABAC policy using the linked guide. The policy recipe is also in advanced-labs if needed.
5. Tag the second table after policy creation and test automatic coverage. Compare synthetic hashing, protected lookup-token mapping, suppression and generalized values; document what information each retains.

## 5. Verify the result

Candidate flags are true, false, false for the three examples. Two identities should see the designed row/mask differences. New tagged assets should receive the scoped policy where eligible; save actual enforcement evidence.

## 6. Break one thing and repair it

Remove a tag from a disposable test column and inspect policy selection, then restore it. Test detector false positives/negatives. Do not claim regex coverage or a visual mask alone proves complete privacy protection.

## 7. Explain without looking

Why separate detection from access enforcement? Who may assign governed tags? Why can hashed email still be identifiable?

<details>
<summary>Answer notes - open after your attempt</summary>

Detection is uncertain classification; enforcement restricts visibility. Assignment privileges control a policy selection boundary. Predictable input spaces and linkage can permit reidentification of hashes.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-22/` if useful.

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

[All days](README.md) | [Previous day](day-21.md) | [Next day](day-23.md)
