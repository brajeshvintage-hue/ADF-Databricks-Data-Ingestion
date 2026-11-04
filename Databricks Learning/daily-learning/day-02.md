# Day 02 - Build a wheel and deploy a bundle

[All days](README.md) | [Previous day](day-01.md) | [Next day](day-03.md)

**Where:** Local PowerShell, then Azure Databricks Jobs  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 1 complete; workspace URL; current Databricks CLI; permission to create an isolated schema, volume and job. If Azure access is missing, finish the local wheel section and record the deployment gap.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A wheel contains Python code and install metadata. A source archive contains material to build a distribution. A bundle describes workspace resources and artifacts; a job runs tasks. These are different boundaries, so a successful build cannot prove permissions or runtime behavior.

The wheel entry point `retail-demo` maps to `retail_de.cli:main`. The job uses that entry point and passes catalog/schema parameters. Targets select environment configuration while reusing the same application code.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Build and deploy a wheel](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/python-wheel)
- [Install the Databricks CLI](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/install)
- [Serverless bundle examples](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/examples)

## 3. Open today's materials

- [pyproject.toml](../pyproject.toml)
- [databricks.yml](../databricks.yml)
- [resources/retail_job.yml](../resources/retail_job.yml)
- [notebooks/00_setup.py](../notebooks/00_setup.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

Before local commands, open PowerShell in the project root (not inside this
daily-learning folder):

```powershell
cd 'C:\Users\braje\OneDrive\Desktop\Documents\ChatGPT\Databricks Learning'
```

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Build using an isolated local environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install build==1.2.2.post1
.\.venv\Scripts\python.exe -m build
.\.venv\Scripts\python.exe -m pip install --no-deps .\dist\retail_de-0.1.0-py3-none-any.whl
.\.venv\Scripts\retail-demo.exe --demo
```

2. Inspect the wheel with Python's `zipfile` or an archive viewer. Find package files and entry-point metadata. `--no-deps` is appropriate here only because this lab package declares no runtime dependencies.
3. Import `notebooks/00_setup.py` as a Python notebook. Set its catalog widget to an existing catalog you can use, keep schema `de_pro_lab`, and run it. This seeds immutable synthetic data; do not overwrite files later.
4. Install/configure the current CLI using the linked official instructions. Replace the two uppercase values:

```powershell
databricks auth login --host https://YOUR_WORKSPACE.azuredatabricks.net --profile AZURE_LAB
$env:DATABRICKS_CONFIG_PROFILE = 'AZURE_LAB'
$env:BUNDLE_VAR_catalog = 'YOUR_EXISTING_CATALOG'
$env:PATH = "$PWD/.venv/Scripts;$env:PATH"
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev retail_names
```

5. Inspect the successful job's output and the `customer_names` table in your catalog's `de_pro_lab` schema. Deploy creates pipeline definitions too; it does not run the pipeline.

## 5. Verify the result

dist contains a wheel and tar.gz. The installed console command produces Day 1's four-name list. The remote names job writes four synthetic rows. Record the actual artifact version and run ID; YAML validation alone is insufficient.

## 6. Break one thing and repair it

Change the job entry point to `missing_entry` in a development copy. Validate, deploy and run; identify the boundary that detects the error. Restore `retail-demo` and redeploy. Do not change the business function to fix a dispatch error.

## 7. Explain without looking

What does deploy do that build does not? How is entry_point different from a Python module path? Which identity needs table-write privileges?

<details>
<summary>Answer notes - open after your attempt</summary>

Build creates a distribution; deployment creates/updates resources and uploads artifacts; run executes them. The entry-point name resolves through installed distribution metadata. The workload's run-as identity needs data privileges, which may differ from the deployer's permissions.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-02/` if useful.

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

[All days](README.md) | [Previous day](day-01.md) | [Next day](day-03.md)
