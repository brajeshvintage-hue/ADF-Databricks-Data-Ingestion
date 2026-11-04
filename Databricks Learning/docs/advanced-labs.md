# Labs with external services or elevated permissions

These are executable lab recipes once their prerequisites exist. They are not automatically completed by deploying the core bundle. Use synthetic data and disposable resource names. Replace `main.de_pro_lab` consistently. Save exact feature/runtime availability in your journal.

## Day 14 — Lakeflow Connect and federation

**Need:** a disposable SQL Server/Azure SQL database supported by your chosen Connect mode, source-side CDC/change tracking prerequisites from the current connector guide, network connectivity, a least-privilege source identity, UC connection/catalog privileges and a supported pipeline configuration. Azure SQL and full SQL Server can have different prerequisites; follow the specific source guide rather than copying database-admin commands blindly.

1. In the disposable source, create `dbo.lab_customers(customer_id INT PRIMARY KEY, name VARCHAR(100), region VARCHAR(10))`; insert `(10,'Alice','CA')` and `(20,'Bob','US')`.
2. Follow the [integrated SQL Server Connect tutorial](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sql-server-integrated-pipeline) and its source setup prerequisites. In the ingestion wizard select only this table, your lab destination, and a manual/triggered schedule. Inspect and export its generated configuration.
3. Run initial load. In the source update 10 to US, insert 30 and delete 20. Run ingestion again; verify the destination reflects those changes. Record source sequence/checkpoint behavior and lag.
4. Independently create a SQL Server connection through Catalog Explorer using the source identity. Create a foreign catalog with the current [federation guide](https://learn.microsoft.com/en-us/azure/databricks/query-federation/sql-server). Supply credentials through the approved connection UI/secret mechanism, never commit passwords.

```sql
-- After lab_sql_connection exists; requires appropriate connection/catalog privileges.
CREATE FOREIGN CATALOG lab_foreign USING CONNECTION lab_sql_connection
OPTIONS (database 'YOUR_DISPOSABLE_DATABASE');
SELECT * FROM lab_foreign.dbo.lab_customers;
```

Compare query pushdown and the load imposed on the source with the replicated Delta copy. Use a second identity to prove that source credentials and UC grants enforce different boundaries. If you only have one identity, the permission test remains unverified.

## Day 15 — Bounded AI enrichment

**Need:** an approved model-serving endpoint, permission to invoke it, supported SQL compute and a small inference budget. Use your actual endpoint name; a made-up name cannot run.

```sql
CREATE OR REPLACE TEMP VIEW lab_reviews AS
SELECT * FROM VALUES
 (1, 'Delivery was fast'), (2, 'Item arrived broken'),
 (3, 'Works as described'), (4, 'Package was late'), (5, 'Excellent support')
AS t(review_id, review);

-- Substitute the endpoint. Inspect its request/response contract first.
SELECT review_id,
       ai_query('YOUR_APPROVED_ENDPOINT',
         concat('Classify as positive, neutral, or negative. Return one label: ', review)
       ) AS label
FROM lab_reviews;
```

Persist a bounded result table rather than re-invoking inference on every read. Keep source text/key, model/endpoint, prompt version, timestamp and errors. Validate output labels. Explore documented `failOnError`/response typing options supported by your endpoint before running a larger batch. Contrast deterministic quality rules with model judgment. [ai_query reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_query).

For VARIANT array exploration after notebook 09, use the SQL generator supported on your runtime, for example:

```sql
SELECT p.payload:order_id::BIGINT AS order_id, item.value:sku::STRING AS sku
FROM main.de_pro_lab.raw_payloads p,
LATERAL variant_explode(p.payload:items) item;
```

## Day 22 — Governed tags and ABAC

**Need:** ABAC-capable compute, permissions to create/manage a governed tag and assign it, schema policy privileges, and two test identities. Create a governed `lab_pii` tag using the account/workspace governed-tag UI. Keep it separate from the ordinary `purpose` tag in notebook 07.

1. Create two **new** synthetic tables with an `email STRING` column in your lab schema; do not reuse a table already carrying a manual column mask.
2. Assign governed tag `lab_pii` to the email column using Catalog Explorer with the appropriate assignment privileges.
3. Create the mask and policy in the lab schema. Adapt the policy syntax to the current [ABAC reference](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/core-concepts) if your workspace has different feature availability.

```sql
CREATE OR REPLACE FUNCTION main.de_pro_lab.mask_tagged_text(s STRING)
RETURNS STRING RETURN '***';

CREATE POLICY lab_mask_tagged_email
ON SCHEMA main.de_pro_lab
COLUMN MASK main.de_pro_lab.mask_tagged_text
TO `account users`
FOR TABLES
MATCH COLUMNS has_tag('lab_pii') AS pii_col
ON COLUMN pii_col;
```

4. Query as both identities, inspect policy selection, and then tag the second table. Verify the policy applies without attaching a new per-table mask.
5. Remove the tag on a disposable copy and observe the effect. Explain who controls tag assignment and why this is part of the enforcement boundary. Scope policies to the lab schema; never apply a training policy to the whole business catalog.

## Day 23 — Sharing and Clean Rooms

**Need:** provider share privileges, an eligible synthetic gold table, and an approved disposable recipient. For D2D use the recipient metastore sharing identifier; for an open recipient follow the current authentication/activation setup. Never put an activation credential in Git or a journal.

Create the recipient in Catalog Explorer according to the recipient type, then run as an authorized provider:

```sql
CREATE SHARE lab_orders_share COMMENT 'Synthetic training data only';
ALTER SHARE lab_orders_share ADD TABLE main.de_pro_lab.gold_sales;
GRANT SELECT ON SHARE lab_orders_share TO RECIPIENT YOUR_LAB_RECIPIENT;
```

As recipient, create the catalog from the share using its sharing UI and read gold totals. Revoke the training share's SELECT permission afterward and test a new recipient query. Compare a D2D reader with an open-protocol reader and inspect authentication lifetime. [Share setup](https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/create-share), [share grants](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/security-grant-share).

For Clean Rooms, follow [create a clean room](https://learn.microsoft.com/en-us/azure/databricks/clean-rooms/create-clean-room). A supported same-metastore test collaboration is possible using your own or another user's sharing identifier; two external organizations are not always necessary for a learning test. Use the approval-based model, add synthetic assets and a notebook returning only grouped counts/revenue, request the required approvals through the product, run, and inspect logs/output-table access. Use the catalog aliases assigned to participants inside the clean room. Approval-based execution is not itself a proof of statistical privacy: review small-group disclosure and output access.

## Day 25–26 — CLI, API and SDK observation

Obtain your actual job and run IDs from Jobs UI or bundle output.

```powershell
databricks jobs get YOUR_JOB_ID
databricks jobs get-run YOUR_RUN_ID
databricks api get /api/2.2/jobs/runs/get --json '{"run_id":123456}'
```

Replace `123456` too. On Windows, if your shell changes inline JSON quoting, put the JSON object in a UTF-8 file and pass `--json @request.json` according to your CLI help.

Optional SDK version, in an environment with a compatible `databricks-sdk` and configured unified authentication:

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient(profile="AZURE_LAB")  # local workstation profile
run = w.jobs.get_run(run_id=YOUR_NUMERIC_RUN_ID)
print(run.state)
```

Compare lifecycle state, result state, task state and error details. Do not infer data correctness from a successful lifecycle alone. Inspect job/pipeline permissions if monitoring is denied.

## Day 28 — Managed Iceberg

**Need:** Unity Catalog, managed storage and an engine/workspace configuration supporting managed Iceberg. Check the current [CREATE TABLE reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-create-table-using) and [managed tables guide](https://learn.microsoft.com/en-us/azure/databricks/tables/managed). Do not install arbitrary Iceberg JARs into a managed runtime to bypass unsupported features.

```sql
CREATE TABLE main.de_pro_lab.iceberg_orders
  (order_id BIGINT, amount DOUBLE) USING ICEBERG;
INSERT INTO main.de_pro_lab.iceberg_orders VALUES (1, 25), (2, 40);
UPDATE main.de_pro_lab.iceberg_orders SET amount = 30 WHERE order_id = 1;
SELECT * FROM main.de_pro_lab.iceberg_orders;
DESCRIBE EXTENDED main.de_pro_lab.iceberg_orders;
```

Verify sum 70. Record actual engine, metadata and supported operations. Compare a managed Delta table exposing Iceberg-readable metadata with a native managed Iceberg table: these are different table designs. For pipeline CDC to Iceberg, use a separate minimal eligible pipeline generated by the current UI and export its format-specific configuration; do not change the running core Delta pipeline in place. Record supported SCD/CDC/table-feature constraints. Test an external REST-catalog reader only if you have one and can configure least-privilege access.
