# Official references and what to verify

Checked October 27, 2026. Examples use current terminology while retaining older names you may encounter: Declarative Automation Bundles / Asset Bundles, AUTO CDC / APPLY CHANGES, Lakeflow Jobs / Workflows. Runtime and region support still need checking in your own Azure workspace.

The plan was also checked against [your uploaded October 9 guide](C:/Users/braje/Downloads/Databricks-Certified-Data-Engineer-Professional-Exam-Guide-9-Oct-2026.pdf), which contains the single current outline. See [the coverage audit](exam-alignment.md) for objective-level mapping and outstanding execution prerequisites.

| Area | Primary reference |
|---|---|
| Exam scope | [Professional exam guide; use the new outline from Oct 9, 2026](https://www.databricks.com/sites/default/files/2026-09/databricks-certified-data-engineer-professional-exam-guide-oct-2026.pdf) |
| Bundle structure and wheel | [Build a Python wheel bundle](https://docs.databricks.com/aws/en/dev-tools/bundles/python-wheel) |
| Serverless task YAML | [Azure bundle examples](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/examples) |
| Task control flow | [Bundle job task types](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/job-task-types) |
| Dependencies | [Bundle libraries](https://docs.databricks.com/aws/en/dev-tools/bundles/library-dependencies), [Azure serverless environments](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) |
| Notebook installs | [Notebook-scoped libraries](https://docs.databricks.com/aws/en/libraries/notebooks-python-libraries) |
| UDFs | [Scalar Python](https://docs.databricks.com/aws/en/udf/python), [pandas](https://docs.databricks.com/aws/en/udf/pandas) |
| Schema changes | [Azure schema evolution](https://learn.microsoft.com/en-us/azure/databricks/data-engineering/schema-evolution) |
| CDC | [AUTO CDC APIs and examples](https://learn.microsoft.com/azure/databricks/delta-live-tables/cdc) |
| Streaming correctness | [Watermarks](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/watermarks), [foreachBatch](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/foreach), [production behavior](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/production) |
| Change feed | [table_changes](https://learn.microsoft.com/azure/databricks/sql/language-manual/functions/table_changes), [CDF retention](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed) |
| Federation | [SQL Server federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/sql-server) |
| Managed CDC ingestion | [SQL Server integrated Connect pipeline](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sql-server-integrated-pipeline) |
| Sharing | [Shares](https://learn.microsoft.com/azure/databricks/delta-sharing/create-share), [recipient grants](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/security-grant-share) |
| Clean Rooms | [Create](https://learn.microsoft.com/en-us/azure/databricks/clean-rooms/create-clean-room), [monitor/manage](https://learn.microsoft.com/en-us/azure/databricks/clean-rooms/manage-clean-room) |
| ABAC | [Core concepts and policy examples](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/core-concepts) |
| AI enrichment | [ai_query](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_query) |
| Managed formats/layout | [Managed tables](https://learn.microsoft.com/en-us/azure/databricks/tables/managed), [CREATE TABLE](https://learn.microsoft.com/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-create-table-using) |
| Metric semantics | [Metric view YAML](https://learn.microsoft.com/azure/databricks/uc-semantics/metric-views/yaml-reference) |

The cross-cloud documentation above is used for shared Python/API concepts; Azure-specific setup and configuration use Microsoft Learn. In a runtime/API mismatch, use the documentation matching your installed CLI, runtime and workspace features, and capture that version in your journal.
