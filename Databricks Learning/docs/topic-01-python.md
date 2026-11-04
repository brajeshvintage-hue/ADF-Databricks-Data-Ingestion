# Topic 1 — learn the development model, then implement it

Spend Days 1–5 here. You should be able to rebuild this module from an empty directory and explain every file's role.

## 1. What a scalable Python project means

It means changes remain understandable as the project gains modules, jobs and contributors. It does not mean that adding folders automatically makes Spark faster.

`cleaning.py` owns business rules and has no Spark dependency. `transforms.py` turns those rules into distributed column operations. `cli.py` handles parameters and runtime orchestration. Tests describe expected behavior. `pyproject.toml` tells a build tool how to create an installable distribution. Bundle YAML describes workspace resources and deployment configuration.

The `src/` layout helps prevent the working directory from accidentally making an uninstalled package importable. Run tests with an explicit `PYTHONPATH` for this first exercise; then repeat against an installed wheel from a directory outside the repository. A notebook can explore results and call package code; production logic should not depend on a hidden earlier cell.

**Experiment:** remove a whitespace-normalization step, predict which contract tests fail, run them, and restore it. Add a new rule only after writing an example that distinguishes old and new behavior.

**Explain:** Which code changes for a new catalog? Which code changes for a new business rule? Why is a hard-coded catalog inside a pure function a design problem?

## 2. Wheel, bundle and job are different artifacts

A **wheel** packages Python modules and distribution metadata. A **bundle** defines deployable resources and references code/artifacts. A **job** runs tasks on compute. Building a wheel does not deploy a job, deployment does not prove the code works, and configuration validation is not a data test.

The `retail-demo` entry point in `pyproject.toml` maps to `retail_de.cli:main`. The job's `entry_point` must match that installed entry point. `package_name` identifies the distribution. Neither is an arbitrary notebook path. The main function accepts `--catalog` and `--schema`; named job parameters become command-line flags.

**Experiment:** build both distributions with `python -m build`. Inspect the wheel as a zip archive; find modules and the entry-point metadata. Install the wheel in a fresh venv and invoke `retail-demo --demo`. Change the job entry point to a nonexistent value; distinguish successful YAML validation from failed runtime dispatch. Restore it and redeploy.

**Explain:** What gets built, uploaded, created, and executed in `bundle deploy` followed by `bundle run`? How do dev/test targets avoid writing to the same namespace?

## 3. Dependencies are part of the execution environment

An installed package is usable only where the code executes. A local laptop installation does not configure Databricks workers. Notebook-scoped installs, classic compute libraries, serverless task environments and pipeline dependencies have different lifecycles. Declare the dependency at the scope that owns the workload.

PyPI is a source of distributions; it is not a file format. A wheel is prebuilt; a source archive must be built during installation and can require compilers, build dependencies and index access. Pure-Python wheels such as this project's `py3-none-any` wheel are portable across compatible Python versions. Native wheels also have Python ABI, operating-system and CPU-architecture constraints.

An exact version for a direct dependency does not lock its transitive dependencies. A lockfile improves reproducibility, but you must also account for the Python/runtime environment. Avoid overriding Spark runtime libraries without a documented compatibility reason. On serverless, bump a custom package's version when publishing a changed build so cached environments can pick up the change.

Use `02_dependencies.py`. Install the example PyPI library, your local wheel and your source archive separately. Save version output and the actual installer error from each controlled failure.

| Symptom | Evidence to collect | Likely next action |
|---|---|---|
| Import works locally but fails remotely | Worker traceback, task environment, installed distribution metadata | Declare dependency for that task, not just the laptop |
| `No matching distribution found` | Requested version, Python version, index and wheel tags | Choose an available compatible distribution |
| `not a supported wheel` | Wheel filename/tags and compute OS/architecture | Build/select the correct wheel |
| Resolver conflict | Conflicting constraints and dependency tree | Reconcile constraints; do not hide it with `--no-deps` |
| Source build failure | Build backend/compiler logs | Supply supported tools or a compatible prebuilt wheel |
| Old behavior after redeploy | Installed version, artifact version, environment cache | Publish a new version and rebuild/redeploy |
| Package unavailable only in pipeline | Pipeline dependency settings | Add the dependency to the pipeline environment |

**Failure drill:** in a disposable venv request `humanize==0.0.0` and capture why resolution fails. In a separate disposable venv request `urllib3==1.26.20` and `urllib3>=2`; inspect the conflicting constraints. These are local drills, not modifications to a shared runtime. Rebuild the environment from declared requirements afterward.

## 4. Native expression, Python UDF, pandas UDF

Spark expressions operate on columns in Spark's execution engine. A scalar Python UDF executes your custom function for individual values across a Python boundary. A pandas UDF exchanges batches using Arrow and accepts/returns pandas objects. Batching lowers some overhead but does not automatically make arbitrary Python logic vectorized or faster.

Use the native expression when it expresses the rule cleanly. Use a Python UDF when required custom logic cannot reasonably be expressed with built-ins. Consider a pandas UDF when batch/vectorized computation fits the rule and compatible dependencies are available. Measure actual workloads and examine plans; no fixed speed multiplier applies to every UDF.

In this kit all three implementations normalize ASCII names to the same contract. Scalar nulls are `None`; pandas often represents missing values with `pd.NA` or NaN. Declare the Spark return type. A Series-to-Series pandas UDF returns one result per input element, with matching length. Iterator pandas UDFs can amortize initialization per iterator, but that state is not globally unique across tasks or retries.

**Experiment:** run `01_udfs.py` and compare values and schemas before timing. Use formatted plans to identify Python/Arrow evaluation stages. The benchmark sums string lengths; `count()` alone can let Spark prune an unused UDF and give a misleading timing. Repeat trials, record cold/warm runs and compute configuration.

**Failure drills:** remove null handling from a disposable scalar function; shorten a pandas output Series; declare a return type inconsistent with actual values. Explain each error rather than memorizing its message. Do not call `collect()`, create a Spark session, or perform a remote API request for every row inside a UDF. Task retries can repeat external effects.

**Evaluation order:** a `WHERE` clause is not a reliable guard that guarantees an unsafe UDF will never receive nulls. Make the function itself safe for its contract.

## 5. SQL and Unity Catalog functions

`spark.udf.register` in notebook 01 registers a session function. The SQL function in notebook 07 is a persistent Unity Catalog object with catalog/schema scope and permissions. Test the same inputs against it. Record who can create and execute it and which compute supports it. A governed Python UC function has its own execution/dependency constraints; it is not made persistent by simply adding a Python decorator.

## Day 5 completion gate

Without reading the files, draw the path from source → test → wheel → bundle → task environment → Spark executors. Rebuild the local demo in a fresh venv. Deploy and run the job in dev. Show matching native, scalar and pandas results, plus a failure and repair for each dependency/packaging category. Explain why a CI unit test pass cannot prove runtime installation or UC privileges.

Use [the journal template](journal-template.md) to write your own explanation. The notes above are the reference explanation; your journal must include your prediction and observed evidence.

## References

- [Python wheel bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/python-wheel)
- [Bundle dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies)
- [Serverless dependency environments](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)
- [Notebook-scoped libraries](https://learn.microsoft.com/en-us/azure/databricks/libraries/notebooks-python-libraries)
- [Scalar Python UDFs](https://learn.microsoft.com/en-us/azure/databricks/udf/python)
- [Pandas UDFs](https://learn.microsoft.com/en-us/azure/databricks/udf/pandas)
- [UC SQL/Python functions](https://learn.microsoft.com/en-us/azure/databricks/udf/unity-catalog)
