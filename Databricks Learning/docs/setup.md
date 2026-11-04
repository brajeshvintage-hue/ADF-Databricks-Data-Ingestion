# Setup and execution guide

## Local workstation

Python 3.10+, Git, a modern Databricks CLI with bundle support, and access to your Azure Databricks workspace. The local contract tests need no extra packages. The authoring environment currently has Python 3.11 but no Databricks CLI or Spark; cloud execution remains for your workspace.

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install build==1.2.2.post1
$env:PYTHONPATH = "$PWD/src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m build
```

`dist/` should contain one `.whl` and one `.tar.gz`. Commands above install build tooling only inside your venv. For CLI deployment, activate it (`.\.venv\Scripts\Activate.ps1`) or make sure the `python` on PATH has `build` installed. Do not weaken your machine's execution policy just for this lab; use the venv Python explicitly if activation is restricted.

If editing the package, install with `pip install -e .` for local development. For deployed jobs, build a versioned wheel. Editable source and an immutable artifact solve different problems. Commit dependency resolution or a lockfile for larger projects; the exact build-tool pins here are an instructional baseline, not proof of a fully locked transitive environment.

## Azure workspace prerequisites

- An existing Unity Catalog catalog, with `USE CATALOG` and permission to create a schema, tables, volumes and functions in your training area.
- Serverless Jobs and serverless Lakeflow pipelines enabled, or an admin-approved classic compute alternative. For manual Spark notebooks, use a recent supported runtime such as 16.4 LTS or newer; validate each feature against your actual runtime. Metric views, AI, ABAC and managed Iceberg have their own feature/runtime gates.
- Volume access, Jobs creation permission, and permission to run pipelines. Classic compute uses workspace-specific policies, node types and access modes; this project deliberately does not hard-code an Azure VM type.
- For SQL scripts: a supported SQL warehouse or suitable notebook compute. Change `USE CATALOG main`, `de_pro_lab` and fully qualified references to match your lab.
- All data is generated. No storage keys, real customer records, or existing business tables are required.

If you cannot create a schema/volume, ask the workspace owner to provision an isolated area and appropriate privileges. An authorization failure is not solved by changing Python code.

## Manual notebooks

Import `notebooks/*.py` as Databricks source notebooks (Git folders work too). SQL source files import as SQL notebooks. Run `00_setup` first and set its widgets to your catalog/schema. `%run ./00_setup` in later Python notebooks assumes they live in the same workspace folder.

Upload your built wheel under the lab Volume's `packages/` folder. Install its exact path through the serverless Environment pane or `%pip`; if Python restarts, rerun imports and configuration cells. Do not put PySpark, Databricks Connect, or an arbitrary pandas/Arrow upgrade in the remote wheel dependencies: use runtime-compatible versions and record them. The package itself needs no third-party library; Day 3 adds one intentionally as a separate exercise.

Minimum execution chain:

1. `00_setup.py`: creates synthetic files and append-only CDC events.
2. `03_ingest.py`: ingests files into `bronze_orders`.
3. `04_batch_silver_gold.py`: writes quarantine, deduplicated silver and gold.
4. `01_udfs.py`, `02_dependencies.py`: independent Topic 1 exercises once the wheel is installed.
5. `05_streaming.py`: separate streaming targets/checkpoints.
6. SQL notebooks: execute by cell on their assigned days.
7. `pipelines/retail_pipeline.py`: runs only in a pipeline, configured through the bundle or UI.

Never overwrite or delete files already consumed by these streams. The source fixture includes a deliberately invalid amount. The first batch has 4 orders: 3 valid, 1 quarantined, valid total revenue 75. The optional second file adds revenue 12. `lp_silver` deliberately does **not** deduplicate business keys: add a watermark/dedup extension and explain its limits on Day 11. The batch silver notebook does deduplicate order keys.

## Authenticate and deploy

Use your workspace URL from the Azure Databricks workspace, for example `https://adb-...azuredatabricks.net`. Run interactive OAuth locally; do not put tokens in files or Git.

```powershell
databricks version
databricks auth login --host https://YOUR-WORKSPACE.azuredatabricks.net --profile AZURE_LAB
$env:DATABRICKS_CONFIG_PROFILE = 'AZURE_LAB'
$env:BUNDLE_VAR_catalog = 'YOUR_EXISTING_CATALOG'
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev retail_names
```

This deploys the wheel job and pipeline definitions; deployment does not start pipeline processing. Run setup before the wheel job so the schema exists. Then:

```powershell
databricks bundle run -t dev retail_pipeline
```

Bundle environment version defaults to `2`; choose an available compatible Jobs environment with `BUNDLE_VAR_environment_version` if needed. Validate against the installed CLI schema; environment fields evolve. The included examples follow the current [Azure bundle examples](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/examples) using `environment_version`. Older examples may use `client` instead. Avoid mixing schemas by copying unrelated examples.

If serverless is unavailable, generate a supported job with `databricks bundle init default-python` in a separate comparison directory, choose classic compute, and adapt its compute block to the existing task. Classic tasks normally attach the wheel via `libraries: [{whl: ../dist/*.whl}]` instead of a serverless environment. Never guess your policy or node type.

For `test`, create `de_pro_lab_test` by rerunning notebook 00 with that schema. Then validate/deploy/run with `-t test`. Dev and test use the same code with different namespace/state. These are training targets, not production promotion controls.

## CI/CD lab

The supplied GitHub Actions workflow tests and builds. Run those same commands locally if you use Azure DevOps. Day 27 adds cloud validation/deployment in your own CI system using the organization's approved OAuth workload identity/service principal. Store host/profile/configuration in CI variables, use separate identities and grants per environment, and deploy the commit that passed tests. Do not copy an interactive user's OAuth cache to CI. There is no configured remote repository, CI identity or active deployment automation in this project.

## Cost and cleanup

All workloads are manually triggered. Start with the 4-row fixture; the benchmark is bounded to 100,000 rows. On classic compute configure auto-termination. Stop warehouses, streams and compute when finished.

`databricks bundle destroy -t dev` removes bundle-managed resources after you inspect its confirmation; it does not promise to delete every data object. Tables, volumes, source files and streaming checkpoints need a separate inventory. Do not drop the schema until you have saved learning evidence and confirmed it contains only this lab. No destructive cleanup is executed by this kit.
