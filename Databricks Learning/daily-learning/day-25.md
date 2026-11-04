# Day 25 - System tables, cost attribution and alerts

[All days](README.md) | [Previous day](day-24.md) | [Next day](day-26.md)

**Where:** Azure SQL plus Jobs/alert UI  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** System schema access granted by the administrator, available operational records and a test notification destination you control. Do not export sensitive audit/system data into public notes.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

System tables expose operational evidence with access and ingestion-latency constraints. Usage quantity has a unit; price attribution requires matching rates, effective dates, cloud/SKU and workload identifiers. List-price estimates are not automatically invoiced spend.

An alert evaluates a signal against a condition and should lead to a specific action. Missing data, delayed data and a healthy zero are different cases. Design firing, recovery, identity and evaluation latency before relying on the alert.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [System tables and access](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/)
- [SQL alerts and evaluation](https://learn.microsoft.com/en-us/azure/databricks/sql/user/alerts/)

## 3. Open today's materials

- [notebooks/08_observability.sql](../notebooks/08_observability.sql)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run notebook 08's billing, lakeflow and audit queries where permitted. Describe the schemas first if a field differs in your environment.
2. Link one known job/run to operational records using actual available identifiers. Inspect compute metadata and effective-dated pricing, separating units and estimated list cost from billed cost.
3. Create a deterministic test signal:

```sql
CREATE TABLE main.de_pro_lab.day25_alert_signal (invalid_orders BIGINT);
INSERT INTO main.de_pro_lab.day25_alert_signal VALUES (0);
SELECT invalid_orders FROM main.de_pro_lab.day25_alert_signal;
```

4. In the current SQL/Lakehouse alert UI save that query, set invalid_orders > 0, choose supported compute and a test destination you control. Evaluate the healthy state. Change the synthetic value to 1, evaluate the transition, restore 0 and inspect recovery history. Disable any test schedule when finished.
5. Design signal/query, threshold, latency and response for freshness, business metric, anomaly, cost, SQL health, audit/security and AI failure rate. Implement one additional signal if time permits, or connect the first result to a disposable Job condition.

## 5. Verify the result

The signal transitions healthy → triggered → recovered according to actual alert evaluation semantics. Operational queries may lag the job; record observation time and data time. Permission denial is an access prerequisite to resolve, not an empty dataset.

## 6. Break one thing and repair it

Evaluate a no-row/null signal in a separate test and record how the alert treats it. Avoid interpreting missing data as proof of health. Compare an actionable failure alert with a noisy threshold that fires on expected invalid data.

## 7. Explain without looking

Why can't DBUs be summed across units as money? What timestamp controls a price join? What should an alert recipient do next?

<details>
<summary>Answer notes - open after your attempt</summary>

Quantity and currency are different measures. Rate validity must match the usage interval and relevant SKU/cloud. A useful alert includes a defined investigation/response and distinguishes stale/missing evidence.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-25/` if useful.

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

[All days](README.md) | [Previous day](day-24.md) | [Next day](day-26.md)
