# Day 01 - Python project structure and pure functions

[All days](README.md) | [Next day](day-02.md)

**Where:** Local PowerShell; no Azure compute needed  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Python 3.10+ and this project folder. Start here even if you already know Python.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

A module is a Python file; a package groups importable modules. This project's `src/retail_de` package separates a business rule (`cleaning.py`) from Spark expressions (`transforms.py`) and execution (`cli.py`). This makes the rule testable without a workspace.

`normalize_name` has a contract: null or blank becomes `None`, repeated whitespace collapses, and text becomes uppercase. Idempotency means normalizing an already normalized result changes nothing. Folder structure improves maintainability; it does not itself distribute work across Spark executors.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Bundle Python project anatomy](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/python-wheel)
- [CI/CD tools and development lifecycle](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/)

## 3. Open today's materials

- [src/retail_de/cleaning.py](../src/retail_de/cleaning.py)
- [tests/test_cleaning.py](../tests/test_cleaning.py)
- [src/retail_de/cli.py](../src/retail_de/cli.py)

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

1. Open PowerShell and run from this exact project directory:

```powershell
cd 'C:\Users\braje\OneDrive\Desktop\Documents\ChatGPT\Databricks Learning'
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -v
python -m retail_de.cli --demo
```

2. Open `src/retail_de/cleaning.py` and `tests/test_cleaning.py`. Match each rule to a test case.
3. Before running this, write your prediction:

```powershell
python -c "from retail_de.cleaning import normalize_name; print(normalize_name('  Alice   Smith ')); print(normalize_name(None))"
```

4. In a new local file implement `is_valid_amount(value)`: accept finite numeric values >= 0; reject null, booleans, text, NaN and infinity. Decide whether invalid input returns `False` or raises; document your choice and test it. Keep this function independent of Spark.
5. Draw how the CLI imports the cleaning module and how the tests import it. Save your diagram or five-sentence explanation below.

## 5. Verify the result

Three existing test methods pass. The demo prints `['ALICE SMITH', 'BOB', None, None]`. The individual calls print `ALICE SMITH` and `None`. Your new validator needs cases for 0, -1, None, '5', True and non-finite numbers.

## 6. Break one thing and repair it

Temporarily replace whitespace collapse with only `strip().upper()`. Predict which test fails, rerun, and restore the implementation. If imports fail, check current directory and PYTHONPATH before changing application code.

## 7. Explain without looking

What makes a function pure? Why is `src/` not automatically importable? Why should the amount policy be defined before implementing it?

<details>
<summary>Answer notes - open after your attempt</summary>

Pure code has no external side effects and depends on explicit inputs. The explicit import path or installation exposes src to Python. Tests capture the chosen policy; code cannot resolve an unspecified contract for you.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-01/` if useful.

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

[All days](README.md) | [Next day](day-02.md)
