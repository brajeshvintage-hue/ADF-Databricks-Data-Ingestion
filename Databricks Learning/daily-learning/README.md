# Your daily Databricks learning files

Start with **[Day 01](day-01.md)**. Open one file each day and follow it from top
to bottom. You do not need to navigate the larger workbook to find the daily steps.
Each file includes concept explanations, official Azure references, prerequisites,
commands or a guided UI lab, expected results, a failure drill, answer notes and
space for your own writing. Previous/next links take you through the sequence.

Allow 90-120 minutes daily, with extra time for external setup. A lesson may span
more than one calendar day. The objective is observable understanding and repair,
not checking off thirty dates. First five days develop the Python/tooling foundation;
later days grow the same retail lakehouse.

## Before the first Azure lab

Day 01 runs locally. Day 02 explains wheel/build tooling and Azure setup. You need
an existing Unity Catalog catalog, an isolated lab schema and appropriate compute
and permissions. The lessons use `main.de_pro_lab` as an example: replace the catalog
everywhere, including volume paths, SQL/YAML and job parameters, when yours differs.
Source notebooks live in [notebooks](../notebooks/00_setup.py); actual import/run
instructions appear in the relevant day's file.

Initial synthetic fixture: 4 orders, 3 valid, 1 quarantine, valid revenue 75.
Day 07's optional coupon order changes this to 5/4/1 and revenue 87. Additional
experiments need their own expected totals. Declarative `lp_silver` does not include
business-key deduplication; compare this explicitly with the batch silver behavior.

## Choose today's file

| Day | Learning file | Execution environment |
|---|---|---|
| 01 | [Python project structure and pure functions](day-01.md) | Local PowerShell; no Azure compute needed |
| 02 | [Build a wheel and deploy a bundle](day-02.md) | Local PowerShell, then Azure Databricks Jobs |
| 03 | [Third-party libraries and dependency diagnosis](day-03.md) | Local disposable venvs and Azure Python notebooks/Jobs |
| 04 | [Native expressions, Python UDFs and pandas UDFs](day-04.md) | Azure Databricks Python notebook |
| 05 | [Testing, DataFrame contracts and CI](day-05.md) | Local PowerShell and Azure Python notebook |
| 06 | [Batch formats, binary files and bronze ingestion](day-06.md) | Azure Python notebook |
| 07 | [Auto Loader schema changes and rescued data](day-07.md) | Azure Python notebook |
| 08 | [Declarative pipelines and materialized results](day-08.md) | Azure Lakeflow Pipeline; launch from local CLI or the pipeline UI |
| 09 | [Quality rules, quarantine, windows and joins](day-09.md) | Azure Python notebook and pipeline UI |
| 10 | [AUTO CDC, out-of-order changes and SCD history](day-10.md) | Azure pipeline and SQL notebook |
| 11 | [Watermarks, event time and stateful aggregation](day-11.md) | Azure Python notebook with supported Structured Streaming compute |
| 12 | [Checkpoint recovery and idempotent foreachBatch](day-12.md) | Azure Python notebook; use compute supporting foreachBatch |
| 13 | [Jobs, conditions, loops, retries and compute](day-13.md) | Azure Jobs UI, notebook tasks and authenticated CLI |
| 14 | [Lakeflow Connect versus governed federation](day-14.md) | Disposable source database, Azure ingestion UI and SQL |
| 15 | [VARIANT and bounded AI enrichment](day-15.md) | Supported Azure SQL warehouse/notebook; optional approved model endpoint |
| 16 | [Delta transactions, time travel and change data feed](day-16.md) | Azure SQL notebook/warehouse |
| 17 | [Liquid clustering, file layout and pruning](day-17.md) | Azure SQL compute with supported liquid clustering |
| 18 | [Deletion vectors and managed maintenance](day-18.md) | Azure SQL compute and Catalog Explorer |
| 19 | [Caches and fair performance experiments](day-19.md) | Azure SQL warehouse; optional supported classic Spark compute |
| 20 | [Join strategy, skew and shuffle diagnosis](day-20.md) | Azure SQL query profile or classic Spark UI |
| 21 | [Unity Catalog privileges, inheritance and functions](day-21.md) | Azure SQL plus two test identities where available |
| 22 | [PII detection, masks, row filters and ABAC](day-22.md) | Azure Python/SQL plus governed-tag/policy administration |
| 23 | [OpenSharing and Clean Rooms](day-23.md) | Azure Catalog Explorer and approved recipient/collaborator environment |
| 24 | [Deletion, retention and replay prevention](day-24.md) | Azure SQL; synthetic data only |
| 25 | [System tables, cost attribution and alerts](day-25.md) | Azure SQL plus Jobs/alert UI |
| 26 | [Diagnose failures and repair job runs](day-26.md) | Azure Jobs/pipeline UI, SQL and authenticated local CLI |
| 27 | [Promote the same revision through CI/CD](day-27.md) | Local shell, your CI provider and Azure dev/test targets |
| 28 | [Iceberg, table formats and interoperability](day-28.md) | Azure SQL compute with managed Iceberg support |
| 29 | [Dimensional grain, historical joins and metric views](day-29.md) | Azure SQL and the declarative pipeline |
| 30 | [Rebuild the lakehouse and resolve an incident](day-30.md) | Local environment, Azure isolated test target and your journal |

## Keep evidence honest

Cloud snippets and new daily exercises are authored starter material; they have not
been run in your Azure workspace. Local package contract tests have passed. External
databases, brokers, sharing, policy administration, inference endpoints and some
table features need additional access. Their lessons include a design path to keep
learning, but design work does not count as executed integration evidence.

The scope follows the [exam alignment audit](../docs/exam-alignment.md), while runtime
details use [Microsoft's Azure Databricks documentation](https://learn.microsoft.com/en-us/azure/databricks/). Check current
feature requirements before a lab. The [original overview](../docs/30-day-workbook.md)
and [setup reference](../docs/setup.md) remain available as supporting material.

Write directly in each file's My learning notes section, or copy that section into
your private notebook. The authoring generator should not be rerun over personal notes.
