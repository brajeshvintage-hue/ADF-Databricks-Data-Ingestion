# Day 30 - Rebuild the lakehouse and resolve an incident

[All days](README.md) | [Previous day](day-29.md)

**Where:** Local environment, Azure isolated test target and your journal  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Previous lessons' evidence; an isolated fresh namespace, schema-specific source/checkpoint configuration and available permissions. External-service gaps remain explicit rather than being assumed complete.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Integrated mastery means predicting outcomes, implementing contracts and diagnosing failures across boundaries. A green run proves an operation completed; reconciled business values and authorization tests establish more of the intended behavior.

Reproducibility requires source revision, distribution version, target configuration, environment and input inventory. Recovery must preserve the identity/progress assumptions established for each sink and stream.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Azure Databricks documentation hub](https://learn.microsoft.com/en-us/azure/databricks/)
- [CI/CD practices](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/)
- [Streaming production behavior](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/production)

## 3. Open today's materials

- [README.md](../README.md)
- [docs/exam-alignment.md](../docs/exam-alignment.md)
- [docs/verification.md](../docs/verification.md)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. From a fresh checkout or separate source copy create a new local venv, run contract tests and build/install the distribution. Do not reuse hidden notebook variables as proof of reproducibility.
2. Choose an isolated namespace and configure it consistently in setup, bundle variables, source paths and SQL. Run notebook 00 there, validate/deploy test, run retail_names and ingest the supplied first file.
3. Run batch silver/gold and the separate declarative pipeline. Reconcile 4 raw orders → 3 valid + 1 quarantine → valid amount 75. Validate customer 10 region US and customer 20 absent before new CDC extensions.
4. Add one new valid order, a business-key duplicate, a negative amount and a new field under immutable new filenames. PREDICT outcomes before updating. Explain why the current declarative lp_silver, which does not deduplicate business keys, differs from the batch silver rule.
5. Restart a stream with its existing checkpoint and verify sink behavior. Check actual second-identity access to protected published data.
6. Choose three incidents without looking up the fix first: missing dependency, wrong schema, changed field, duplicate join key, denied access or replayed batch. Diagnose from run/log/plan evidence, repair and reconcile.
7. Give a ten-minute explanation: source → contracts → tables → orchestration → security → monitoring → deployment. Finish your own runbook and list all unresolved prerequisites.

## 5. Verify the result

The initial isolated fixture reconciles to revenue 75; later values match your written predictions and actual dedup/quality rules. Save revision, artifact, namespace, run/update IDs and access tests. Unrun external integrations stay listed as gaps.

## 6. Break one thing and repair it

Use a new isolated namespace for a rebuild rather than deleting established working checkpoints. Trace each incident to its actual boundary before changing more than one thing. Record proof after repair.

## 7. Explain without looking

Could another person reproduce your result? Which tests establish correctness versus deployment? Which external objectives still lack evidence?

<details>
<summary>Answer notes - open after your attempt</summary>

A usable runbook includes setup, configuration, immutable input inventory, expected values and recovery. Different checks establish different boundaries. Readiness requires identifying gaps rather than counting calendar days completed.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-30/` if useful.

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

[All days](README.md) | [Previous day](day-29.md)
