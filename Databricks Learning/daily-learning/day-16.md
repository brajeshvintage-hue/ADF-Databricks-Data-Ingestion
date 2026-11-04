# Day 16 - Delta transactions, time travel and change data feed

[All days](README.md) | [Previous day](day-15.md) | [Next day](day-17.md)

**Where:** Azure SQL notebook/warehouse  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** An isolated de_pro_lab schema; permission to create/update/delete a disposable table. Do not use business tables for this exercise.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Time travel reads a table snapshot at a version. Change data feed exposes change records across a range, including update preimages and postimages. Applying both as fresh inserts can double count business values.

CDF/history are subject to retention and supported table configuration. They are not an independent permanent archive. A delayed consumer needs a plan when its starting version is no longer available.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Change data feed and retention](https://learn.microsoft.com/en-us/azure/databricks/tables/features/change-data-feed)
- [table_changes function](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/table_changes)

## 3. Open today's materials

- [notebooks/06_delta_and_performance.sql](../notebooks/06_delta_and_performance.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Set the namespace header in notebook 06, then execute only its Day 16 section. It creates delta_changes, performs an update, insert and delete, and shows history.
2. Choose the actual CREATE/REPLACE version from DESCRIBE HISTORY; a rerun need not start at version 0. Substitute it below:

```sql
SELECT * FROM table_changes('YOUR_CATALOG.de_pro_lab.delta_changes', START_VERSION)
ORDER BY _commit_version, id, _change_type;
SELECT * FROM delta_changes VERSION AS OF START_VERSION;
```

3. Label insert, delete, update_preimage and update_postimage rows. Query the current table and reconcile its state to those changes.
4. In a scratch downstream target apply updates/deletes by key or demonstrate a signed delta calculation that removes preimages and adds postimages. State which interpretation your consumer expects.
5. Record source version progress in your consumer design, and explain how retries avoid applying the same source range twice. Read the current retention/feature constraints before changing any table settings.

## 5. Verify the result

Current state is id 1 with value 'updated'; id 2 was inserted then deleted. Historical snapshot and CDF answer different questions. Record exact versions/change rows, since repeated table replacement retains a continuing history.

## 6. Break one thing and repair it

Treat every CDF row as an insert in a scratch calculation, show the incorrect result, then repair its change-type handling. Do not lower retention to manufacture an unavailable-version failure; explain the recovery design.

## 7. Explain without looking

Why are there two records for an update? Does CDF automatically update your downstream table? What if the consumer falls behind retention?

<details>
<summary>Answer notes - open after your attempt</summary>

Preimage and postimage describe before/after state. Your consumer must interpret them. It may need a new snapshot/backfill when required history is unavailable, with a carefully defined handoff to incremental processing.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-16/` if useful.

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

[All days](README.md) | [Previous day](day-15.md) | [Next day](day-17.md)
