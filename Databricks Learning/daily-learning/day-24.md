# Day 24 - Deletion, retention and replay prevention

[All days](README.md) | [Previous day](day-23.md) | [Next day](day-25.md)

**Where:** Azure SQL; synthetic data only  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Isolated purge_demo table and read access to the lab's lineage/source inventory. No shortened retention or disabled retention checks are needed.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

DELETE changes the table's current logical result. Historical versions and physical files have retention lifetimes; VACUUM removes eligible unreferenced files. Neither operation by itself proves erasure from every source, replica, backup and export.

If ingestion can replay an undeleted source record, a subject removed from silver can return. A complete design needs identity mapping, propagation, replay prevention and verification across relevant copies.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [VACUUM behavior and retention](https://learn.microsoft.com/en-us/azure/databricks/tables/operations/vacuum)
- [CDF retention limits](https://learn.microsoft.com/en-us/azure/databricks/tables/features/change-data-feed)

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

1. In notebook 07 execute only the purge_demo section, which creates one synthetic row, deletes it and inspects history/retention candidates.
2. Query the current state and an eligible prior version using the actual version from history. Use only the synthetic payload.
3. Inspect candidates without removing files:

```sql
VACUUM purge_demo DRY RUN;
```

4. Build an inventory for a synthetic subject: source files/database, bronze, quarantine, silver, gold, CDC/CDF, checkpoints, downstream shares/exports and backups. Record ownership, access, retention and deletion propagation separately.
5. Simulate replay in scratch tables: copy a synthetic subject to bronze/silver, delete only from silver, then rebuild silver from bronze. Observe reintroduction and design a maintained deletion/tombstone control appropriate to the pipeline.
6. Write an ordered runbook: identify scope, stop/prevent unwanted reintroduction, apply source/downstream deletion, honor retention obligations, verify current/historical exposure under the actual policy, and record exceptions requiring owners.

## 5. Verify the result

Current purge_demo count becomes zero while history can still describe prior operations. A dry run may return no eligible files on a new table; that is an expected observation. Scratch replay demonstrates why a single-layer DELETE is incomplete.

## 6. Break one thing and repair it

Present the claim 'DELETE succeeded, so all copies are gone' and refute it with the inventory. Do not force physical deletion with zero-hour retention. Keep compliance claims tied to the actual organizational policy and verified systems.

## 7. Explain without looking

Which operation changes current rows? What does VACUUM target? How can a pipeline reintroduce a deleted subject?

<details>
<summary>Answer notes - open after your attempt</summary>

DELETE updates logical state; VACUUM removes eligible unreferenced physical files under retention. Retained upstream input can recreate the row unless deletion state/source handling prevents replay.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-24/` if useful.

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

[All days](README.md) | [Previous day](day-23.md) | [Next day](day-25.md)
