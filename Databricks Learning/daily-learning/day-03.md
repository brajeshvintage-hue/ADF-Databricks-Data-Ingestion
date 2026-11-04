# Day 03 - Third-party libraries and dependency diagnosis

[All days](README.md) | [Previous day](day-02.md) | [Next day](day-04.md)

**Where:** Local disposable venvs and Azure Python notebooks/Jobs  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 2 distributions; a supported notebook environment; permission to upload files under the lab volume. Use a disposable venv for intentional resolver failures.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A dependency belongs to the environment executing the code. Laptop installation does not configure workers, and notebook installation does not configure a different job or pipeline. PyPI is a distribution source; wheel and source archive are package formats.

Source installs may require build tools and network access. Native wheels also depend on Python ABI, OS and CPU architecture. Exact direct-package pins do not fully lock transitive dependencies. Keep runtime-provided Spark/pandas/Arrow compatibility in mind.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Serverless dependency management](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)
- [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies)
- [Notebook-scoped Python libraries](https://learn.microsoft.com/en-us/azure/databricks/libraries/notebooks-python-libraries)

## 3. Open today's materials

- [notebooks/02_dependencies.py](../notebooks/02_dependencies.py)
- [resources/retail_job.yml](../resources/retail_job.yml)
- [docs/advanced-labs.md](../docs/advanced-labs.md)

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

1. Run notebook `02_dependencies.py`'s metadata cell. Record Python, pandas, Arrow and package versions.
2. On serverless use the Environment pane to add `humanize==4.11.0`; apply it. Where supported, notebook `%pip install humanize==4.11.0` is another notebook-scoped route. Restart Python when required and rerun imports.
3. Execute the notebook's worker UDF probe, not just `import humanize` on the driver.
4. Create `packages` inside the lab volume, upload your wheel and tar.gz, and install each by its actual Workspace/Volume path in separate clean environments. Record which build steps the source archive needs.
5. Repeat the dependency declaration in a disposable serverless job environment. For pipelines, inspect its own environment dependencies; prove one small compatible package is usable there independently.
6. Reproduce resolution failures locally:

```powershell
python -m venv .venv-dependency-drill
.\.venv-dependency-drill\Scripts\python.exe -m pip install humanize==0.0.0
.\.venv-dependency-drill\Scripts\python.exe -m pip install 'urllib3==1.26.20' 'urllib3>=2'
```

These last two commands are expected to fail. Do not apply them to shared compute.

## 5. Verify the result

Worker probe returns formatted strings for 0, 1 and 2; separately `humanize.intcomma(1234567)` returns `1,234,567`. Both deliberate local installs fail for explainable resolution reasons. A changed custom wheel should have a new version when redeployed to cached environments.

## 6. Break one thing and repair it

Remove the dependency from the disposable job and run it again. Diagnose whether the environment still contains it through another declared dependency/cache. Capture requested versus installed versions rather than assuming every import failure has the same cause.

## 7. Explain without looking

Why can driver and worker imports differ? What distinguishes wheel-tag failure from a resolver conflict? Why is --no-deps usually a poor conflict fix?

<details>
<summary>Answer notes - open after your attempt</summary>

Execution scopes can differ. Wheel tags constrain binary compatibility; resolution reconciles dependency constraints. Ignoring dependencies hides incompatibility rather than repairing the environment contract.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-03/` if useful.

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

[All days](README.md) | [Previous day](day-02.md) | [Next day](day-04.md)
