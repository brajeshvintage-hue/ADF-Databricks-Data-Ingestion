# Day 27 - Promote the same revision through CI/CD

[All days](README.md) | [Previous day](day-26.md) | [Next day](day-28.md)

**Where:** Local shell, your CI provider and Azure dev/test targets  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Successful Day 2 deployment; test schema initialized; approved CI identity if configuring remote deployment. The supplied workflow tests/builds only and does not deploy automatically.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Promotion should identify the tested code revision, artifact and target configuration. Environment-specific namespaces and grants differ while application rules remain the same. CI build success and a deployed smoke test are complementary evidence.

Interactive developer OAuth credentials and noninteractive CI workload identity have different lifecycles. Bundle ownership also differs from ad hoc UI/API changes; redeployment can reconcile declared resource settings.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [CI/CD development process](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/)
- [Bundle configurations and targets](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/examples)

## 3. Open today's materials

- [.github/workflows/ci.yml](../.github/workflows/ci.yml)
- [databricks.yml](../databricks.yml)
- [docs/setup.md](../docs/setup.md)

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

1. In notebook 00 set schema to de_pro_lab_test and run setup with the same intended test catalog. Keep dev data/checkpoints separate.
2. From the authenticated project shell, rerun tests/build and deploy the SAME checked revision:

```powershell
$env:PYTHONPATH = "$PWD/src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m build --wheel
databricks bundle validate -t dev
databricks bundle validate -t test
databricks bundle deploy -t test
databricks bundle run -t test retail_names
```

Ensure the shell's python used by the bundle artifact build has build tooling, as on Day 2. Inspect output schema and record the target identity/revision.
3. Review the supplied CI workflow; in your own GitHub/Azure DevOps training pipeline add bundle validation, then deployment using approved workload identity and a bounded smoke run. Do not copy local OAuth caches into CI.
4. Use a Databricks Git folder to inspect branch/revision provenance. Build a promotion checklist connecting source revision, tests, artifact version, target and run-as grants.
5. Change a harmless label on the disposable bundle-managed job through the UI, redeploy the declared configuration and inspect reconciliation.

## 5. Verify the result

Dev/test write to distinct declared namespaces with the same application behavior. There is a reproducible association between tested revision, built wheel and successful target smoke run. Without CI identity/repository access, mark remote CI execution pending.

## 6. Break one thing and repair it

In a development branch override a target to an unavailable catalog. Compare configuration validation with runtime privilege/object checks, then restore the target before deployment. Never use a production identity for this experiment.

## 7. Explain without looking

What should be promoted: source guesses or an identified tested revision? Can bundle validate prove data privileges? Why version a changed wheel?

<details>
<summary>Answer notes - open after your attempt</summary>

Promote a known revision/artifact with traceable target settings. Validation is not runtime authorization. Versioned artifacts expose changes and help avoid stale cached implementations.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-27/` if useful.

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

[All days](README.md) | [Previous day](day-26.md) | [Next day](day-28.md)
