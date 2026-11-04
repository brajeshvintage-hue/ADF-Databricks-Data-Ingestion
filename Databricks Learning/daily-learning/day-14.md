# Day 14 - Lakeflow Connect versus governed federation

[All days](README.md) | [Previous day](day-13.md) | [Next day](day-15.md)

**Where:** Disposable source database, Azure ingestion UI and SQL  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** An eligible SQL Server/Azure SQL source, source-admin help for documented CDC prerequisites, network access, UC connection/catalog privileges. Without these, complete the design exercise and leave real ingestion marked pending.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Managed ingestion creates and maintains a destination copy. Federation queries the external source through a governed connection and foreign catalog. The former has replication lag/storage; the latter depends on source query availability and load.

Source credentials and UC grants govern different boundaries. A user can have catalog access yet fail when the connection's database identity lacks source privileges. Connector prerequisites vary between SQL Server, MySQL and PostgreSQL.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Integrated SQL Server CDC pipeline](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sql-server-integrated-pipeline)
- [SQL Server federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/sql-server)

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

1. In a disposable SQL source create:

```sql
CREATE TABLE dbo.lab_customers (
  customer_id INT PRIMARY KEY, name VARCHAR(100), region VARCHAR(10)
);
INSERT INTO dbo.lab_customers VALUES (10, 'Alice', 'CA'), (20, 'Bob', 'US');
```

2. Follow the linked Connect tutorial and its source-specific setup. Select only this table, a lab destination, and manual/triggered updates. Save the generated pipeline definition.
3. After initial load, update 10 to US, insert customer 30, delete customer 20, and run another ingestion update. Verify all three change types.
4. Through Catalog Explorer create a separate SQL Server federation connection with approved credential handling. Do not write passwords in a notebook or Git.
5. After the connection exists, adapt:

```sql
CREATE FOREIGN CATALOG lab_foreign USING CONNECTION lab_sql_connection
OPTIONS (database 'YOUR_DISPOSABLE_DATABASE');
SELECT * FROM lab_foreign.dbo.lab_customers;
```

6. Compare the foreign query's freshness and execution plan with the replicated table. Write a source prerequisite/privilege/retention matrix for MySQL and PostgreSQL as well; do not claim execution for sources you have not run.

## 5. Verify the result

The replicated and foreign-query results eventually reflect customers 10 and 30, with 20 deleted. Record lag and source/destination query evidence. If unavailable, a completed topology and access matrix is useful design evidence but not completed hands-on ingestion.

## 6. Break one thing and repair it

With the owner of your disposable source, remove the connection identity's read access, capture the failed boundary and restore it. Compare that with denying a UC consumer identity access to the foreign catalog.

## 7. Explain without looking

Which solution persists a copy? Where can a query place load? Can UC grants repair missing source privileges?

<details>
<summary>Answer notes - open after your attempt</summary>

Connect persists replicated data. Federated queries can execute work against the source. UC privileges do not manufacture permissions for the connection's underlying source credentials.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-14/` if useful.

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

[All days](README.md) | [Previous day](day-13.md) | [Next day](day-15.md)
