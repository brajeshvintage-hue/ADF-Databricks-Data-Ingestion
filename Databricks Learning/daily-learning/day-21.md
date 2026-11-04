# Day 21 - Unity Catalog privileges, inheritance and functions

[All days](README.md) | [Previous day](day-20.md) | [Next day](day-22.md)

**Where:** Azure SQL plus two test identities where available  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** An authorized grantor, a lab account-level group and an independent consumer identity. Python UC functions need supported compute. Without a second identity, authorization enforcement remains unverified.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A UC object lives in catalog.schema.object. Namespace-use privileges and the object's own access privileges have different roles. Inherited grants can cover future objects, so a broad grant can affect more than today's table list.

A session-registered Python UDF disappears with session scope. A UC SQL/Python function is a governed persistent object with execution privileges and compute constraints. Discoverability is not proof that every principal can execute it.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Manage UC privileges](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/)
- [Governed SQL and Python UDFs](https://learn.microsoft.com/en-us/azure/databricks/udf/unity-catalog)

## 3. Open today's materials

- [notebooks/07_governance.sql](../notebooks/07_governance.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Set notebook 07's catalog/schema and run its first SQL-function cell. Compare its output to Day 4's name contract.
2. Create a small independent governed Python function on supported compute:

```sql
CREATE OR REPLACE FUNCTION main.de_pro_lab.twice_nullable(n BIGINT)
RETURNS BIGINT LANGUAGE PYTHON AS $$
return None if n is None else n * 2
$$;
SELECT main.de_pro_lab.twice_nullable(3), main.de_pro_lab.twice_nullable(NULL);
```

Replace main/de_pro_lab consistently. Record required CREATE FUNCTION and EXECUTE/namespace privileges and current runtime restrictions.
3. Have an authorized grantor create a lab group and grant USE CATALOG, USE SCHEMA and SELECT on a new synthetic table. Query as the consumer identity. Do not infer this result by querying only as owner.
4. On a separate training schema, demonstrate inherited SELECT: grant the group scoped SELECT, create a new table afterward, and verify access plus namespace-use requirements. Revoke training grants after evidence collection.
5. Add comments and an ordinary training-purpose tag to your synthetic table; inspect them in Catalog Explorer. Compare UC data grants with workspace job/notebook ACLs.

## 5. Verify the result

Governed Python function returns 6 and null; normalized SQL output matches the contract. Consumer access succeeds only with the required effective privileges. Save the grant matrix and actual second-identity result.

## 6. Break one thing and repair it

Remove the test consumer's namespace-use privilege or EXECUTE grant in an isolated exercise; observe which operation fails and restore it. Inspect inherited grants before concluding a revoke removed all effective access.

## 7. Explain without looking

Can SELECT alone always resolve an object? What does catalog-level SELECT imply for future tables? Is a session UDF a UC object?

<details>
<summary>Answer notes - open after your attempt</summary>

Namespace use also matters. Supported inherited privileges can apply to future descendants without conferring ownership. Session registration and governed UC functions have different scope/lifecycle.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-21/` if useful.

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

[All days](README.md) | [Previous day](day-20.md) | [Next day](day-22.md)
