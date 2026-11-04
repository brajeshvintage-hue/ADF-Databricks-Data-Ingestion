# Databricks Professional: 30 days of building

For Azure Databricks. Prepared October 27, 2026. Plan assumes 90–120 minutes a day and basic Python/SQL. If those foundations are new, repeat days rather than treating day 30 as an exam deadline.

Build one **retail orders lakehouse**: files → bronze → validated silver → gold sales, with customer CDC, reproducible Python packaging, orchestration, security and operational evidence.

## Start here

1. Open **[your daily learning files](daily-learning/README.md)**.
2. Start **[Day 01](daily-learning/day-01.md)** and follow that file from top to bottom. No Azure compute is needed for Day 01.
3. Write your predictions and observations in the file's **My learning notes** section, then use **Next day** when you are ready.

Each of the 30 daily files contains its own explanation, official Azure documentation links, prerequisites, build steps, expected results, failure drill and completion checklist. Azure setup is introduced on Day 02. Keep the [setup guide](docs/setup.md), [original overview](docs/30-day-workbook.md) and [Topic 1 reference](docs/topic-01-python.md) as optional supporting material.

Use [the concept notes](docs/concepts.md) for explanations across the full project, and [official references](docs/sources.md) to check runtime-specific details.

Every day: predict the result, build, run, deliberately break one thing, explain the cause, then repair it. Read solutions only after making your prediction. A successful run alone does not complete a day.

## Files

| Location | Purpose |
|---|---|
| `daily-learning/day-01.md` through `day-30.md` | Individual lessons and personal learning notes; open one per day |
| `daily-learning/README.md` | Clickable daily index and usage instructions |
| `src/retail_de/` | Installable Python package; pure logic separated from Spark execution |
| `tests/` | Local contract tests with Python's standard library |
| `databricks.yml`, `resources/` | Dev/test bundle targets, wheel job and pipeline |
| `notebooks/` | Databricks source notebooks with runnable starter implementations |
| `pipelines/retail_pipeline.py` | Declarative Auto Loader, expectations, gold aggregation, SCD 1/2 |
| `docs/30-day-workbook.md` | Daily builds, failure drills and completion evidence |
| `docs/advanced-labs.md` | External-service and admin-dependent lab instructions |
| `.github/workflows/ci.yml` | Local test/build CI example; deployment commands are in setup |

## Local first run (PowerShell)

```powershell
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -v
python -m retail_de.cli --demo
```

Expected normalized names: `ALICE SMITH`, `BOB`, `None`, `None`. These commands require Python 3.10+ only. Spark notebooks run in Databricks, not in this local Python environment.

## Scope and readiness

The roadmap maps all nine domains in the [official exam guide effective October 9, 2026](https://www.databricks.com/sites/default/files/2026-09/databricks-certified-data-engineer-professional-exam-guide-oct-2026.pdf). The detailed first module expands the three Topic 1 bullets you supplied. New-guide SQL/Unity Catalog functions are included too. This is a learning project, not a set of recalled exam questions or a guarantee of readiness.

Cloud scripts are starter implementations for the exercises. They need your catalog, permissions and compute; they have **not** been executed in your Azure workspace. Features requiring another principal, a database, a sharing recipient, or an endpoint have explicit prerequisite gates. Record those as unverified until actually run.

Use the isolated schema `de_pro_lab` for disposable synthetic data only. No schedules are enabled. Stop compute after labs. Details, feature prerequisites and cleanup are in setup.
