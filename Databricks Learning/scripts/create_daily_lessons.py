"""Authoring helper for the daily Markdown lessons.

Run from the project root. This regenerates daily files, so preserve personal
notes before rerunning. Learners use daily-learning/README.md directly.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://learn.microsoft.com/en-us/azure/databricks/"
LESSONS = []


def lesson(title, where, need, understand, steps, expected, failure, questions, answer, references, files=()):
    LESSONS.append(dict(title=title, where=where, need=need, understand=understand,
        steps=steps, expected=expected, failure=failure, questions=questions,
        answer=answer, references=references, files=files))


lesson("Python project structure and pure functions", "Local PowerShell; no Azure compute needed",
"Python 3.10+ and this project folder. Start here even if you already know Python.",
"""A module is a Python file; a package groups importable modules. This project's `src/retail_de` package separates a business rule (`cleaning.py`) from Spark expressions (`transforms.py`) and execution (`cli.py`). This makes the rule testable without a workspace.

`normalize_name` has a contract: null or blank becomes `None`, repeated whitespace collapses, and text becomes uppercase. Idempotency means normalizing an already normalized result changes nothing. Folder structure improves maintainability; it does not itself distribute work across Spark executors.""",
r"""1. Open PowerShell and run from this exact project directory:

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
5. Draw how the CLI imports the cleaning module and how the tests import it. Save your diagram or five-sentence explanation below.""",
"Three existing test methods pass. The demo prints `['ALICE SMITH', 'BOB', None, None]`. The individual calls print `ALICE SMITH` and `None`. Your new validator needs cases for 0, -1, None, '5', True and non-finite numbers.",
"Temporarily replace whitespace collapse with only `strip().upper()`. Predict which test fails, rerun, and restore the implementation. If imports fail, check current directory and PYTHONPATH before changing application code.",
"What makes a function pure? Why is `src/` not automatically importable? Why should the amount policy be defined before implementing it?",
"Pure code has no external side effects and depends on explicit inputs. The explicit import path or installation exposes src to Python. Tests capture the chosen policy; code cannot resolve an unspecified contract for you.",
[("Bundle Python project anatomy", "dev-tools/bundles/python-wheel"), ("CI/CD tools and development lifecycle", "dev-tools/ci-cd/")],
["src/retail_de/cleaning.py", "tests/test_cleaning.py", "src/retail_de/cli.py"])

lesson("Build a wheel and deploy a bundle", "Local PowerShell, then Azure Databricks Jobs",
"Day 1 complete; workspace URL; current Databricks CLI; permission to create an isolated schema, volume and job. If Azure access is missing, finish the local wheel section and record the deployment gap.",
"""A wheel contains Python code and install metadata. A source archive contains material to build a distribution. A bundle describes workspace resources and artifacts; a job runs tasks. These are different boundaries, so a successful build cannot prove permissions or runtime behavior.

The wheel entry point `retail-demo` maps to `retail_de.cli:main`. The job uses that entry point and passes catalog/schema parameters. Targets select environment configuration while reusing the same application code.""",
r"""1. Build using an isolated local environment:

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

5. Inspect the successful job's output and the `customer_names` table in your catalog's `de_pro_lab` schema. Deploy creates pipeline definitions too; it does not run the pipeline.""",
"dist contains a wheel and tar.gz. The installed console command produces Day 1's four-name list. The remote names job writes four synthetic rows. Record the actual artifact version and run ID; YAML validation alone is insufficient.",
"Change the job entry point to `missing_entry` in a development copy. Validate, deploy and run; identify the boundary that detects the error. Restore `retail-demo` and redeploy. Do not change the business function to fix a dispatch error.",
"What does deploy do that build does not? How is entry_point different from a Python module path? Which identity needs table-write privileges?",
"Build creates a distribution; deployment creates/updates resources and uploads artifacts; run executes them. The entry-point name resolves through installed distribution metadata. The workload's run-as identity needs data privileges, which may differ from the deployer's permissions.",
[("Build and deploy a wheel", "dev-tools/bundles/python-wheel"), ("Install the Databricks CLI", "dev-tools/cli/install"), ("Serverless bundle examples", "dev-tools/bundles/examples")],
["pyproject.toml", "databricks.yml", "resources/retail_job.yml", "notebooks/00_setup.py"])

lesson("Third-party libraries and dependency diagnosis", "Local disposable venvs and Azure Python notebooks/Jobs",
"Day 2 distributions; a supported notebook environment; permission to upload files under the lab volume. Use a disposable venv for intentional resolver failures.",
"""A dependency belongs to the environment executing the code. Laptop installation does not configure workers, and notebook installation does not configure a different job or pipeline. PyPI is a distribution source; wheel and source archive are package formats.

Source installs may require build tools and network access. Native wheels also depend on Python ABI, OS and CPU architecture. Exact direct-package pins do not fully lock transitive dependencies. Keep runtime-provided Spark/pandas/Arrow compatibility in mind.""",
r"""1. Run notebook `02_dependencies.py`'s metadata cell. Record Python, pandas, Arrow and package versions.
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

These last two commands are expected to fail. Do not apply them to shared compute.""",
"Worker probe returns formatted strings for 0, 1 and 2; separately `humanize.intcomma(1234567)` returns `1,234,567`. Both deliberate local installs fail for explainable resolution reasons. A changed custom wheel should have a new version when redeployed to cached environments.",
"Remove the dependency from the disposable job and run it again. Diagnose whether the environment still contains it through another declared dependency/cache. Capture requested versus installed versions rather than assuming every import failure has the same cause.",
"Why can driver and worker imports differ? What distinguishes wheel-tag failure from a resolver conflict? Why is --no-deps usually a poor conflict fix?",
"Execution scopes can differ. Wheel tags constrain binary compatibility; resolution reconciles dependency constraints. Ignoring dependencies hides incompatibility rather than repairing the environment contract.",
[("Serverless dependency management", "compute/serverless/dependencies"), ("Bundle library dependencies", "dev-tools/bundles/library-dependencies"), ("Notebook-scoped Python libraries", "libraries/notebooks-python-libraries")],
["notebooks/02_dependencies.py", "resources/retail_job.yml", "docs/advanced-labs.md"])

lesson("Native expressions, Python UDFs and pandas UDFs", "Azure Databricks Python notebook",
"Install the Day 2 wheel in the notebook's environment; use runtime-compatible pandas and Arrow. No bronze/silver tables needed.",
"""A native Spark expression describes column operations for the engine. A scalar Python UDF enables a custom per-value rule. A pandas UDF moves batches through Arrow and operates on pandas objects. Batch transfer and vectorized business logic are related but different ideas.

The correct comparison starts with an identical contract: null/blank handling, output type and row cardinality. A Series-to-Series pandas UDF must return the same number of results as inputs. Timing an unused UDF with count can mislead because Spark can prune unneeded expressions.""",
r"""1. Predict normalized output for null, blank, tabs and repeated ASCII spaces.
2. Import and run `notebooks/01_udfs.py` in Azure. Its three implementations must agree with the explicit expected DataFrame.
3. Inspect each formatted plan. Identify where Python or Arrow evaluation occurs; labels can vary with runtime.
4. Run the bounded benchmark, which sums output string lengths. Save every trial and compute configuration. Do not report a universal speed ranking from this small fixture.
5. Write a second scalar function using `@udf('long')` to double a nullable integer. Then implement it as a native expression and a pandas UDF. State the null and output-type contract before running.

```python
from pyspark.sql import functions as F
@F.udf('long')
def double_or_null(value):
    return None if value is None else value * 2
display(spark.createDataFrame([(2,), (None,)], 'n long')
        .select(double_or_null('n').alias('twice')))
```

6. Compare a session registration in the starter notebook with the persistent governed functions you will build on Day 21.""",
"All name implementations return ALICE SMITH, BOB, null, null. Each benchmark produces checksum 1,100,000 for 100,000 rows. Doubling returns 4 and null. Runtime timings can vary; correctness must agree.",
"In disposable definitions, remove null handling and return a shortened pandas Series. Observe and repair both errors. Do not rely on WHERE filtering to guarantee unsafe UDF inputs never arrive.",
"When is a native expression preferable? Does Series.apply automatically vectorize a Python function? Why must a benchmark consume the transformed value?",
"Prefer a built-in expression when it represents the rule clearly. Series.apply may still run Python element by element. Consuming transformed output prevents measuring a plan that discarded the work under investigation.",
[("Python scalar UDFs", "udf/python"), ("pandas UDF contracts", "udf/pandas")],
["notebooks/01_udfs.py", "src/retail_de/transforms.py"])

lesson("Testing, DataFrame contracts and CI", "Local PowerShell and Azure Python notebook",
"Days 1–4 complete. Optional repository/CI access; local test/build commands work without a remote CI provider.",
"""Unit tests isolate a business rule. Integration tests exercise runtime boundaries such as Spark schema, worker dependencies and table writes. A test proving four rows exist cannot prove those four values are correct.

DataFrame.transform composes a DataFrame-to-DataFrame function; it is not a separate scheduler or an automatic performance optimization. CI repeats validation on a known revision so changes cannot rely solely on someone's notebook session.""",
r"""1. Run the existing local contract suite, then add your Day 1 amount-validator tests.
2. In Azure rerun notebook 01's `assertDataFrameEqual` and `assertSchemaEqual` checks. Where order matters, order by a key and explicitly check row order.
3. Write this small independent integration assertion:

```python
from pyspark.testing.utils import assertDataFrameEqual, assertSchemaEqual
from retail_de.transforms import add_normalized_name
source = spark.createDataFrame([(1, '  bob '), (2, None)], 'id long, customer_name string')
actual = source.transform(add_normalized_name).select('id', 'normalized_name')
expected = spark.createDataFrame([(1, 'BOB'), (2, None)], 'id long, normalized_name string')
assertDataFrameEqual(actual.orderBy('id'), expected.orderBy('id'), checkRowOrder=True)
assertSchemaEqual(actual.schema, expected.schema)
```

4. Inspect `.github/workflows/ci.yml`: identify checkout, Python setup, tests, build and artifact upload. Run the same commands locally. If using Azure DevOps, implement equivalent stages in your own training pipeline rather than uploading the GitHub workflow unchanged.
5. Reinstall the built wheel in a clean environment outside the source import path and repeat the demo. This catches accidental reliance on the source checkout.""",
"Local and Spark contract checks pass. CI/local build produces a versioned distribution. Record each check's scope: none of these alone proves a new workspace identity can write a UC table.",
"Change a test input to expose a missing rule, then fix the rule. Separately change the output type or column name and see the integration check fail. Restore the agreed contract.",
"What does a schema assertion catch that a count misses? Why test an installed wheel? What should run before cloud deployment in CI?",
"Schema checks detect structural/type mismatches; counts cannot. Installed-wheel testing checks packaging/import boundaries. Run relevant tests and artifact build before deployment, then a small workspace smoke test afterward.",
[("Testing through Databricks Connect", "dev-tools/databricks-connect/python/testing"), ("CI/CD on Azure Databricks", "dev-tools/ci-cd/")],
["tests/test_cleaning.py", "notebooks/01_udfs.py", ".github/workflows/ci.yml"])

lesson("Batch formats, binary files and bronze ingestion", "Azure Python notebook",
"Run notebook 00 first with your catalog/schema. It defines ns and root and seeds four orders. Import all Python notebooks into the same workspace folder so their relative %run paths resolve.",
"""File encoding and table semantics are different layers. JSON and CSV need parsing; Parquet carries a columnar schema. binaryFile returns file-level content and metadata, so it does not parse each JSON order into a row.

Bronze preserves an ingestion boundary. Auto Loader's cloudFiles source processes newly discovered files incrementally. Neither a successful file read nor append-only ingestion proves uniqueness of order_id.""",
r"""1. Run `00_setup.py` and inspect the source file. Use the values of `ns` and `root` it prints.
2. In the same notebook/session compare encodings:

```python
schema = 'order_id long, customer_id long, customer_name string, amount double, event_time timestamp, region string'
orders = spark.read.schema(schema).json(f'{root}/orders')
orders.write.mode('overwrite').option('header', True).csv(f'{root}/formats/csv')
orders.write.mode('overwrite').parquet(f'{root}/formats/parquet')
csv = spark.read.option('header', True).csv(f'{root}/formats/csv')
parquet = spark.read.parquet(f'{root}/formats/parquet')
csv.printSchema()
parquet.printSchema()
display(spark.read.format('binaryFile').load(f'{root}/orders')
        .select('path', 'length'))
```

3. Re-read CSV with the explicit schema and compare types/nulls.
4. Run `03_ingest.py` to create bronze. Run its ingestion cell again with the same checkpoint; verify count is unchanged.
5. If an approved broker exists, build a bounded Kafka/Event Hubs read using the source's documented authentication and offset options. Otherwise draw the design and mark broker execution pending. Compare connector-specific offset/credential concepts for Kafka, Kinesis and Pub/Sub; they are not interchangeable configurations.""",
"With only batch_001, parsed data has four rows; binaryFile has one file row. Header-only CSV reading produces string columns while Parquet retains declared types. Bronze stays at four rows when unchanged files are reprocessed with the same checkpoint.",
"In a scratch folder create malformed JSON and compare PERMISSIVE/FAILFAST parsing. Do not place this experiment in the working orders directory. Separate malformed syntax from a valid JSON value with the wrong business type.",
"Why isn't binaryFile equivalent to JSON reading? Where is source progress stored? Does count 4 prove unique business keys?",
"Binary ingestion preserves bytes per file, while JSON parsing produces records. Streaming checkpoints preserve progress. Row count alone cannot establish business uniqueness.",
[("Auto Loader source and behavior", "ingestion/cloud-object-storage/auto-loader/"), ("File formats and ingestion", "ingestion/")],
["notebooks/00_setup.py", "notebooks/03_ingest.py"])

lesson("Auto Loader schema changes and rescued data", "Azure Python notebook",
"Day 6 bronze/checkpoint exists. Keep the original source files immutable. New experiments use new filenames, not overwrites of consumed files.",
"""There are three separate persisted concerns: Auto Loader's schema, streaming progress/checkpoint state, and the target table schema. A new column can evolve the discovered schema and stop the stream so it can restart using that schema. The target must also accept the new column.

Rescued data records fields that do not conform to the parsing contract. It provides investigation context; it does not make those fields valid business values. A type mismatch is different from adding a new column.""",
r"""1. Run notebook 03's ingestion again and record the baseline count/schema.
2. In that notebook uncomment the optional `batch_002.json` creation lines and execute them once. Do not set overwrite=True.
3. Run ingestion. If it stops for a schema-evolution change, capture the message and rerun with the same schema/checkpoint locations. Verify coupon appears in the source and target schemas.
4. Inspect bronze:

```python
display(spark.table(f'{ns}.bronze_orders')
        .select('order_id', 'amount', 'coupon', '_rescued_data'))
```

5. Under a separate scratch input path create an amount='not-a-number' record. Create a separate cloudFiles stream with amount DOUBLE hints and rescue mode, its own schema path, checkpoint and target. Inspect the rescued JSON. Keep this experiment out of the core bronze stream.
6. Write a three-column inventory: source schema path, checkpoint path, destination table. Explain why none is a substitute for the others.""",
"With the two supplied files, bronze contains five rows and total valid order amount becomes 87. New-file creation should fail if blindly repeated; inspect existing files instead. A rescued type mismatch should remain visible for investigation.",
"Point a scratch stream at a new checkpoint and predict replay before executing into a new scratch target. Do not discard the working checkpoint. Compare counts and explain why downstream dedup may still be necessary.",
"Why can schema evolution require restart? Why might target mergeSchema be required too? What would a new checkpoint forget?",
"The running query was planned for an earlier schema. The sink has a separate schema contract. A new checkpoint lacks prior progress and state, so it cannot stand in for recovery of the old query.",
[("Schema inference, evolution and rescue", "ingestion/cloud-object-storage/auto-loader/schema")],
["notebooks/03_ingest.py"])

lesson("Declarative pipelines and materialized results", "Azure Lakeflow Pipeline; launch from local CLI or the pipeline UI",
"Notebook 00 has run; bundle deploy is complete; permission and compute for serverless pipelines. This file runs in a pipeline, not with local python.",
"""Declarative functions describe datasets and dependencies; the engine plans execution. A streaming read describes incremental input processing, whereas a batch read can describe a query whose materialized result must reflect the current source.

The project's lp_ tables are separately owned pipeline outputs. lp_gold is a materialized aggregate over lp_silver. The operational tradeoff includes refresh needs, late changes and cost, not just API syntax.""",
r"""1. Read the source file and identify every dataset name and read dependency before launching.
2. Check `resources/retail_pipeline.yml`: catalog, schema, source volume and CDC table must match notebook 00.
3. In the authenticated project shell:

```powershell
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev retail_pipeline
```

4. Open the pipeline graph. Trace lp_bronze → lp_checked → lp_silver/lp_quarantine → lp_gold. The customer CDC branch can be inspected today; Day 10 explains its semantics.
5. Query lp_gold and compare it with a batch GROUP BY over lp_silver. Inspect which functions return streaming DataFrames and which return batch DataFrames.
6. Add a small new immutable file, run another normal update, and observe incremental source progress. Compare this with notebook 03's explicit query/checkpoint management.""",
"For batch_001 only: four bronze, three valid silver, one quarantine, valid revenue 75. If Day 7 added batch_002: five bronze, four valid, one quarantine, revenue 87. Additional experimental files change the baseline; inventory them before asserting counts.",
"Introduce a missing-column reference in the development pipeline, inspect the reported graph/update error, restore the column and update again. Avoid collect(), arbitrary writes and external side effects inside dataset definitions.",
"Who schedules a declarative function? Which output needs a maintained full aggregate? When is Structured Streaming preferable?",
"The pipeline engine plans execution. A materialized result serves the aggregate query over changing source data. Explicit Structured Streaming is useful when you need supported custom sinks or operational control beyond the declarative graph.",
[("Pipeline Python development", "ldp/developer/python-dev"), ("Pipeline concepts", "ldp/")],
["pipelines/retail_pipeline.py", "resources/retail_pipeline.yml"])

lesson("Quality rules, quarantine, windows and joins", "Azure Python notebook and pipeline UI",
"Bronze from Day 6/7 and the pipeline from Day 8. Use the current source inventory when reconciling totals.",
"""A quality rule needs an explicit disposition: retain and measure, drop, fail, or route to quarantine. SQL null predicates can escape both WHERE valid and WHERE NOT valid unless you define null handling.

A row_number window chooses one version per key only when ordering is meaningful. Joining a fact to multiple matching dimension rows multiplies the fact. Validation must therefore include grain and cardinality, not just whether the job succeeded.""",
r"""1. Run `04_batch_silver_gold.py`. Inspect how the complete validity rule is coalesced to False.
2. Reconcile input = valid before dedup + quarantine, then count duplicates removed before silver. Distinguish rejected data from duplicate valid versions.
3. Write a SQL equivalent of the window:

```sql
-- Use your catalog and lab schema.
SELECT * EXCEPT(rn) FROM (
  SELECT *, row_number() OVER (
    PARTITION BY order_id ORDER BY event_time DESC, source_file DESC
  ) AS rn
  FROM bronze_orders
  WHERE order_id IS NOT NULL AND customer_id IS NOT NULL
    AND event_time IS NOT NULL AND amount >= 0 AND _rescued_data IS NULL
) WHERE rn = 1;
```

4. Inspect the warning/drop expectations in the pipeline. Change one to expect_or_fail in development, run, and record the failed update's outcome. Restore the original definition.
5. Create a two-row customer lookup, join to valid orders, aggregate revenue and then add a duplicate lookup key. Observe the change in cardinality and repair the lookup/join contract.""",
"Initial valid revenue is 75, or 87 after the optional coupon order. One supplied negative order is quarantined. A duplicated dimension key can inflate revenue even if all amounts are nonnegative and every task is green.",
"Create a small DataFrame containing amount null and use only amount >= 0 as a filter. Compare WHERE predicate and WHERE NOT predicate, then coalesce the rule. Explain which row was otherwise unaccounted for.",
"Does expect_or_drop automatically preserve rejected rows elsewhere? Why does dedup need a tie policy? Can a join pass all row-level quality tests and still be wrong?",
"Dropping needs a separate quarantine branch to preserve rejects. Ambiguous ties cannot reliably choose the intended version. Join multiplicity is a cross-row invariant that per-row rules may miss.",
[("Pipeline expectations", "ldp/expectations"), ("Query profile and row cardinality", "sql/user/queries/query-profile")],
["notebooks/04_batch_silver_gold.py", "pipelines/retail_pipeline.py"])

lesson("AUTO CDC, out-of-order changes and SCD history", "Azure pipeline and SQL notebook",
"Day 8 pipeline and notebook 00's append-only customer_cdc source. Use a pipeline configuration supporting AUTO CDC.",
"""CDC application turns a change stream into table state. The sequence is a source-order contract, not necessarily arrival order. SCD1 keeps current attributes; SCD2 preserves version intervals. AUTO CDC handles updates/deletes using keys, sequencing and the configured history policy.

The fixture deliberately contains customer 10's sequence 3 before sequence 2. The current state must still reflect sequence 3. Delta CDF exposes committed table changes; it is not the same operation as applying a database CDC feed.""",
r"""1. Read the five fixture CDC records in notebook 00 and predict both target states before querying.
2. Run a normal pipeline update and execute SQL using your catalog/schema:

```sql
SELECT * FROM lp_customer_current ORDER BY customer_id;
SELECT * FROM lp_customer_history ORDER BY customer_id, __START_AT;
```

3. Identify current SCD2 rows with __END_AT IS NULL and explain deleted keys.
4. Append one synthetic update using a NEW key/sequence pair:

```python
spark.createDataFrame([(10, 'Alice', 'UK', 5, 'UPDATE')],
    'customer_id long, name string, region string, sequence long, operation string'
).write.mode('append').saveAsTable(f'{ns}.customer_cdc')
```

Run that append only once, update the pipeline, and inspect the new history interval.
5. Design a same-key/same-sequence conflict. State a source ordering/tie rule before testing it with an isolated key. Do not use an arbitrary dropDuplicates to hide conflicting versions.""",
"Before the extension: customer 10 has region US; customer 20 is absent from current state after its delete. After sequence 5: customer 10 is UK and history reflects the transition. Sequence intervals are not automatically business timestamps.",
"Append a late lower-sequence event for a separate new synthetic customer after a higher sequence. Verify current state remains consistent with ordering. Explain any history changes rather than assuming the late row is always discarded.",
"Why is arrival-order last-write-wins unsafe? Can SCD sequence intervals be joined directly to order timestamps? How would full refresh affect source retention needs?",
"Arrival can reorder events. Only a defined mapping makes a sequence comparable with business time. Rebuilding history requires retaining the source changes needed to reconstruct it.",
[("AUTO CDC and SCD examples", "ldp/cdc")],
["pipelines/retail_pipeline.py", "notebooks/00_setup.py"])

lesson("Watermarks, event time and stateful aggregation", "Azure Python notebook with supported Structured Streaming compute",
"Day 6 bronze for the starter dedup. The independent aggregation exercise below creates its own source/table/checkpoint. Use a unique suffix if rerunning from scratch.",
"""State remembers keys or window aggregates across micro-batches. An event-time watermark uses observed event progress and a delay to manage state. It is not a timer that advances merely because you wait.

Append output for a windowed aggregation waits until results can be finalized; update output exposes changed results for a suitable sink. Dedup within a watermark bounds guarantees and state; it is not global lifetime uniqueness.""",
r"""1. Run notebook 05's first section; inspect progress/state metrics supported by your compute.
2. For an independent finite-source experiment run setup to obtain ns/root, then:

```python
from pyspark.sql import functions as F
spark.createDataFrame([
    ('2026-10-01 10:00:00', 10), ('2026-10-01 10:01:00', 20),
    ('2026-10-01 10:30:00', 5)
], 'ts string, amount long').selectExpr('CAST(ts AS TIMESTAMP) event_time', 'amount') \
 .write.mode('errorifexists').saveAsTable(f'{ns}.day11_events')
agg = (spark.readStream.table(f'{ns}.day11_events')
    .withWatermark('event_time', '10 minutes')
    .groupBy(F.window('event_time', '5 minutes')).sum('amount'))
q = (agg.writeStream.outputMode('append').format('delta')
    .option('checkpointLocation', f'{root}/checkpoints/day11_windows')
    .trigger(availableNow=True).toTable(f'{ns}.day11_windows'))
q.awaitTermination()
```

3. Inspect output and progress over triggers. Append a later event to advance progress, then an event for an old window. Rerun using the same checkpoint. A watermark becomes effective across processing progress; do not demand every window finalize in the first trigger.
4. Explain how update mode differs; use a documented compatible sink if testing it. Do not assume Delta append is a valid sink for every update-mode query.""",
"The first five-minute window's input sum is 30. It can be emitted once watermark progress finalizes it. The latest window may remain unfinalized. Record observed watermark, window output and state rather than assuming one output row for every source row.",
"Wait without new event-time progress and observe that wall-clock time alone does not finalize old state. Compare with appending a later timestamp. Keep working checkpoints intact.",
"What does the watermark bound? Why can the latest append-mode window be absent? Is dedup permanent after state eviction?",
"It bounds event-time state for supported operators. A recent window is not yet finalized. Eviction limits the horizon of remembered duplicate keys; it does not create eternal uniqueness.",
[("Watermarks and deduplication", "structured-streaming/watermarks"), ("Structured Streaming production considerations", "structured-streaming/production")],
["notebooks/05_streaming.py"])

lesson("Checkpoint recovery and idempotent foreachBatch", "Azure Python notebook; use compute supporting foreachBatch",
"Day 6 bronze, root/ns configuration from setup, and permission to create scratch Delta tables. Keep transaction IDs paired with their stream/checkpoint identity.",
"""Recovery can replay a micro-batch. foreachBatch supplies batch_id, but its sink effects must be designed to tolerate repetition. Transaction application/version IDs let a supported Delta append recognize repeated writes for the same transaction.

A checkpoint restores progress and state. It cannot make an external API call exactly-once or make writes to two independent systems atomic. Deleting checkpoints without redesigning sink identity can cause duplicates or skipped writes.""",
r"""1. Run notebook 05's foreachBatch section. Inspect the callback, target table and dedicated checkpoint.
2. Demonstrate replay independently of orchestration:

```python
batch = spark.createDataFrame([(1, 'A'), (2, 'B')], 'id long, value string')
def replay_safe_write():
    (batch.write.format('delta').mode('append')
      .option('txnAppId', 'day12-replay-demo-v1')
      .option('txnVersion', 0)
      .saveAsTable(f'{ns}.day12_replay_safe'))
replay_safe_write()
replay_safe_write()
assert spark.table(f'{ns}.day12_replay_safe').count() == 2
```

3. In another scratch table append the same two rows twice without transaction IDs. Compare its count.
4. Restart the actual notebook stream using its original checkpoint. Verify no unexpected appended duplicates.
5. Write a recovery matrix for: same checkpoint/same application ID; new checkpoint/new ID; new checkpoint/reused ID. Include the consequence of batch IDs starting again.""",
"Transaction-protected replay produces two rows; plain double append produces four. The guarantee applies to the defined Delta sink transaction contract and retained transaction metadata, not arbitrary external effects or indefinite retention.",
"Use a new scratch table for each independent transaction test. Predict how reusing application/version 0 with different intended data can cause that transaction to be treated as already committed. Do not test by deleting production or working checkpoints.",
"What is at-least-once? Where is idempotency implemented? Why not swallow all exceptions inside foreachBatch?",
"A batch effect may be attempted more than once. The destination's transaction/key design must make replay safe. Swallowing failures can report success while losing data or leaving partial output.",
[("foreachBatch semantics and replay", "structured-streaming/foreach"), ("Delta streaming writes", "structured-streaming/delta-lake")],
["notebooks/05_streaming.py"])

lesson("Jobs, conditions, loops, retries and compute", "Azure Jobs UI, notebook tasks and authenticated CLI",
"Day 2 deployment and bronze data. Permission to create training Jobs; supported serverless or policy-approved classic compute. Leave schedules disabled.",
"""Jobs coordinate task dependencies and run conditions. A task value is small orchestration metadata, not a substitute for a data table. Branches choose which outcomes run; For Each applies a task to a parameter set.

Compute configuration belongs to the execution environment. Standard serverless performance mode and performance-optimized mode trade usage against startup/execution latency. Retrying a transient failure can help; retrying an invalid data contract without a fix repeats the problem.""",
r"""1. In Jobs & Pipelines create a manual training job with ingestion → validation → gold. Use the imported source notebooks; configure the same catalog/schema widgets.
2. Create a validation notebook with:

```python
invalid = spark.table('YOUR_CATALOG.de_pro_lab.quarantine_orders').count()
dbutils.jobs.taskValues.set(key='invalid_orders', value=invalid)
```

3. Add an If/Else task comparing `{{tasks.validation.values.invalid_orders}}` with your threshold. Set gold's dependency to the chosen condition outcome.
4. Add For Each over `["CA", "US"]`. In its nested notebook read the region parameter and query only that region. Export/generate the job's bundle definition and inspect the resulting task graph.
5. Toggle Performance optimized for the same bounded serverless job where available. Run comparable trials and record startup, task execution and usage. Compare with the configuration needed for a high-memory classic notebook task; use real policy/node choices from your workspace.
6. Locate retry/automatic-optimization settings. For a disposable task choose an intentional failure and configure the retry behavior. Generate a second minimal job through the current API/SDK schema to compare with UI creation.""",
"The invalid-count branch is predictable from actual quarantine. CA/US loop tasks receive different parameters. A failed upstream task changes downstream eligibility. Record actual mode/usage, not an assumed universal cost reduction.",
"Fail the validation task once, inspect retries/skips and repair the failed section after fixing it. Distinguish a repair from a completely new run. Keep bundle-managed and API-created demonstration jobs separate.",
"Does depends_on mean a task always runs? What is max_retries protecting against? Why keep For Each parameters small?",
"Run-if/condition outcomes also control eligibility. Retries address supported transient/recoverable attempts, not arbitrary correctness flaws. Task parameters/values coordinate work; large datasets belong in durable data assets.",
[("Bundle task types and control flow", "dev-tools/bundles/job-task-types"), ("Serverless Jobs and performance modes", "jobs/run-serverless-jobs")],
["resources/retail_job.yml", "notebooks/04_batch_silver_gold.py"])

lesson("Lakeflow Connect versus governed federation", "Disposable source database, Azure ingestion UI and SQL",
"An eligible SQL Server/Azure SQL source, source-admin help for documented CDC prerequisites, network access, UC connection/catalog privileges. Without these, complete the design exercise and leave real ingestion marked pending.",
"""Managed ingestion creates and maintains a destination copy. Federation queries the external source through a governed connection and foreign catalog. The former has replication lag/storage; the latter depends on source query availability and load.

Source credentials and UC grants govern different boundaries. A user can have catalog access yet fail when the connection's database identity lacks source privileges. Connector prerequisites vary between SQL Server, MySQL and PostgreSQL.""",
r"""1. In a disposable SQL source create:

```sql
CREATE TABLE dbo.lab_customers (
  customer_id INT PRIMARY KEY, name VARCHAR(100), region VARCHAR(10)
);
INSERT INTO dbo.lab_customers VALUES (10, 'Alice', 'CA'), (20, 'Bob', 'US');
```

2. Follow the linked Connect tutorial and its source-specific setup. Select only this table, a lab destination, and manual/triggered updates. Save the generated pipeline definition.
3. After initial load, update 10 to US, insert customer 30, delete customer 20, and run another ingestion update. Verify all three change types.
4. Through Catalog Explorer create a separate SQL Server federation connection with approved credential handling. Do not write passwords in a notebook or Git.
5. After the connection exists, adapt:

```sql
CREATE FOREIGN CATALOG lab_foreign USING CONNECTION lab_sql_connection
OPTIONS (database 'YOUR_DISPOSABLE_DATABASE');
SELECT * FROM lab_foreign.dbo.lab_customers;
```

6. Compare the foreign query's freshness and execution plan with the replicated table. Write a source prerequisite/privilege/retention matrix for MySQL and PostgreSQL as well; do not claim execution for sources you have not run.""",
"The replicated and foreign-query results eventually reflect customers 10 and 30, with 20 deleted. Record lag and source/destination query evidence. If unavailable, a completed topology and access matrix is useful design evidence but not completed hands-on ingestion.",
"With the owner of your disposable source, remove the connection identity's read access, capture the failed boundary and restore it. Compare that with denying a UC consumer identity access to the foreign catalog.",
"Which solution persists a copy? Where can a query place load? Can UC grants repair missing source privileges?",
"Connect persists replicated data. Federated queries can execute work against the source. UC privileges do not manufacture permissions for the connection's underlying source credentials.",
[("Integrated SQL Server CDC pipeline", "ingestion/lakeflow-connect/sql-server-integrated-pipeline"), ("SQL Server federation", "query-federation/sql-server")],
["docs/advanced-labs.md"])

lesson("VARIANT and bounded AI enrichment", "Supported Azure SQL warehouse/notebook; optional approved model endpoint",
"VARIANT-capable compute. AI extension needs an existing approved endpoint, invocation permissions and a small inference budget; use synthetic text only.",
"""VARIANT stores flexible nested values while allowing typed field extraction. Missing path, SQL null, JSON null, malformed JSON and an invalid cast are distinct cases. Flexible structure still needs an analytical contract.

AI enrichment is model-dependent interpretation. Store source identifiers, prompt/model provenance and errors. Repeated dashboard queries or retried UDF tasks should not accidentally trigger uncontrolled inference.""",
r"""1. Run only the VARIANT section of notebook 09; its modeling sections belong to Day 29. Replace the catalog/schema header first.
2. Test nested extraction and null semantics independently:

```sql
SELECT variant_get(parse_json('{"order":{"id":7}}'), '$.order.id', 'bigint') AS id,
       variant_get(parse_json('{"order":{}}'), '$.order.id', 'bigint') AS missing;
SELECT try_parse_json('{invalid') AS malformed,
       is_variant_null(parse_json('null')) AS is_json_null;
```

3. Flatten the fixture's items with the current documented variant generator. Compare storing raw JSON STRING, a declared STRUCT and VARIANT for a newly added field. Test case-sensitive field names.
4. If endpoint access exists, run a bounded query on five synthetic reviews. Inspect the endpoint's request/response contract before adapting:

```sql
SELECT ai_query('YOUR_APPROVED_ENDPOINT',
  'Classify as positive, neutral or negative. Return one label: Delivery was fast') AS label;
```

5. Persist review key, input, endpoint/model provenance, prompt version, result, timestamp and error state in a lab table. Validate labels and separately test failure handling using supported ai_query options. If the endpoint is missing, record the blocked prerequisite rather than inventing an output.""",
"Nested id is 7; missing field and try_parse_json malformed result are SQL null; is_json_null is true. AI output is not a fixed expected string: it must satisfy the chosen response contract and retain traceability.",
"Use a wrong extraction type and compare strict versus supported try conversion behavior. Simulate a missing endpoint or test response in an isolated exercise; retain the source review even when enrichment fails.",
"Is flexible schema the same as no contract? Why preserve raw source/provenance? Should AI output automatically determine a financial fact?",
"Consumers still need typed fields and quality rules. Source/provenance enables repair and audit. Model judgments need validation and a defined role, especially when deterministic source facts exist.",
[("Query and flatten VARIANT", "semi-structured/variant"), ("ai_query contract and options", "sql/language-manual/functions/ai_query")],
["notebooks/09_variant_modeling.sql"])

lesson("Delta transactions, time travel and change data feed", "Azure SQL notebook/warehouse",
"An isolated de_pro_lab schema; permission to create/update/delete a disposable table. Do not use business tables for this exercise.",
"""Time travel reads a table snapshot at a version. Change data feed exposes change records across a range, including update preimages and postimages. Applying both as fresh inserts can double count business values.

CDF/history are subject to retention and supported table configuration. They are not an independent permanent archive. A delayed consumer needs a plan when its starting version is no longer available.""",
r"""1. Set the namespace header in notebook 06, then execute only its Day 16 section. It creates delta_changes, performs an update, insert and delete, and shows history.
2. Choose the actual CREATE/REPLACE version from DESCRIBE HISTORY; a rerun need not start at version 0. Substitute it below:

```sql
SELECT * FROM table_changes('YOUR_CATALOG.de_pro_lab.delta_changes', START_VERSION)
ORDER BY _commit_version, id, _change_type;
SELECT * FROM delta_changes VERSION AS OF START_VERSION;
```

3. Label insert, delete, update_preimage and update_postimage rows. Query the current table and reconcile its state to those changes.
4. In a scratch downstream target apply updates/deletes by key or demonstrate a signed delta calculation that removes preimages and adds postimages. State which interpretation your consumer expects.
5. Record source version progress in your consumer design, and explain how retries avoid applying the same source range twice. Read the current retention/feature constraints before changing any table settings.""",
"Current state is id 1 with value 'updated'; id 2 was inserted then deleted. Historical snapshot and CDF answer different questions. Record exact versions/change rows, since repeated table replacement retains a continuing history.",
"Treat every CDF row as an insert in a scratch calculation, show the incorrect result, then repair its change-type handling. Do not lower retention to manufacture an unavailable-version failure; explain the recovery design.",
"Why are there two records for an update? Does CDF automatically update your downstream table? What if the consumer falls behind retention?",
"Preimage and postimage describe before/after state. Your consumer must interpret them. It may need a new snapshot/backfill when required history is unavailable, with a carefully defined handoff to incremental processing.",
[("Change data feed and retention", "tables/features/change-data-feed"), ("table_changes function", "sql/language-manual/functions/table_changes")],
["notebooks/06_delta_and_performance.sql"])

# Keep registrations in day order to preserve the learning sequence.

lesson("Liquid clustering, file layout and pruning", "Azure SQL compute with supported liquid clustering",
"Isolated schema. Start at 100,000 rows; use larger data only with a chosen budget. Record query cache state and actual engine.",
"""Layout changes the physical work needed for a query. Liquid clustering organizes records around useful access keys without traditional fixed directory partitioning. Statistics and file skipping reduce scanned data when a predicate can exploit the layout.

Partitioning, ZORDER and liquid clustering are choices with compatibility constraints, not switches to stack blindly. A tiny table may show no measurable benefit even when a design is appropriate at larger scale.""",
r"""1. In notebook 06 run the bounded perf_orders creation and filtered query before the clustering commands.
2. Record query ID, files/bytes scanned, rows returned, plan and runtime. Then enable customer_id clustering, run OPTIMIZE and repeat.
3. Verify a business invariant:

```sql
SELECT COUNT(*) AS n, SUM(amount) AS total FROM perf_orders;
SELECT SUM(amount) AS filtered_total FROM perf_orders WHERE customer_id = 42;
DESCRIBE DETAIL perf_orders;
```

4. Where supported, compare fixed keys with CLUSTER BY AUTO and inspect how eligibility/optimization works. Do not assume automatic keys are chosen immediately on this small workload.
5. In a separate small disposable table compare a date-like partition key with a high-cardinality identifier. Inspect file counts. Write which query patterns justify each choice.
6. Use the Query History profile, not only wall-clock time. Keep a saved before/after record with cache conditions.""",
"The fixture has 100,000 rows and total amount 9,950,000. customer_id 42 has 100 rows and filtered total 4,200. Layout work must preserve values; performance improvement is not guaranteed at this size.",
"Propose partitioning by unique order_id and explain the small-file/directory consequence. Test only at a small bounded size. If a command rejects mixing clustering and partitioning, use the error to identify the supported layout contract.",
"Why can a faster query be misleading? When does clustering help skipping? Does changing keys rewrite every existing file immediately?",
"Caches and startup can dominate timings. Skipping needs an exploitable predicate and useful file organization/statistics. Metadata/key changes and physical maintenance are separate events; inspect actual operations.",
[("Liquid clustering and compatibility", "tables/clustering"), ("Query profile metrics", "sql/user/queries/query-profile")],
["notebooks/06_delta_and_performance.sql"])

lesson("Deletion vectors and managed maintenance", "Azure SQL compute and Catalog Explorer",
"Day 17 perf_orders. Use disposable copies and compute supporting the selected Delta table features; inspect protocol before changing features.",
"""Deletion vectors allow supported operations to record changed/deleted rows without immediately rewriting all original file content. Reads apply the relevant metadata to recover the current logical result. Logical deletion and physical removal occur at different stages.

UC managed tables let the platform own more maintenance responsibilities. Predictive optimization can schedule eligible maintenance, but enabled configuration is not proof a maintenance run already occurred.""",
r"""1. Create separate bounded Delta copies; if these names already exist, inspect them before rerunning:

```sql
CREATE TABLE day18_dv_on USING DELTA
TBLPROPERTIES ('delta.enableDeletionVectors' = 'true') AS SELECT * FROM perf_orders;
CREATE TABLE day18_dv_off USING DELTA
TBLPROPERTIES ('delta.enableDeletionVectors' = 'false') AS SELECT * FROM perf_orders;
DELETE FROM day18_dv_on WHERE order_id < 10;
DELETE FROM day18_dv_off WHERE order_id < 10;
DESCRIBE HISTORY day18_dv_on;
DESCRIBE HISTORY day18_dv_off;
```

2. Compare counts, operation metrics, feature/protocol metadata and physical-write observations. An enabled feature does not guarantee identical engines use an identical optimization for every operation.
3. Inspect managed/external table detail and ownership. In Catalog Explorer or documented SQL inspect predictive-optimization settings/inheritance for the lab's managed tables.
4. Record which operations are supported by your actual runtime/readers. Explain the cost/maintenance owner for an external table versus a UC managed table.
5. Distinguish OPTIMIZE, statistics maintenance and retention cleanup. Do not lower retention or change shared catalog settings to force activity.""",
"Both tables retain 99,990 rows. Logical contents should agree even if operation/file metrics differ. Capture table type, feature settings and any actual maintenance evidence separately.",
"Model an older reader that cannot understand an enabled feature. Test only if you have an isolated supported/older reader pair. Avoid casually upgrading business table protocols or interpreting absence of immediate physical deletion as a failed DELETE.",
"What is write amplification? Can current data be correct while old bytes remain? Who owns external-table cleanup?",
"Changing a few rows can cause disproportionately large rewrites. Transactional metadata can define correct current reads while old files remain under retention. External-table owners retain responsibilities that managed services may automate.",
[("Deletion vectors", "tables/features/deletion-vectors"), ("Predictive optimization", "optimizations/predictive-optimization"), ("Managed tables", "tables/managed")],
["notebooks/06_delta_and_performance.sql"])

lesson("Caches and fair performance experiments", "Azure SQL warehouse; optional supported classic Spark compute",
"Day 17 perf_orders and access to Query History/profile. Some Spark persistence APIs are unavailable on serverless; use supported classic compute for that optional comparison.",
"""Result caching can avoid executing a query. Disk/data caching can avoid fetching remote files again. Spark persistence stores an explicitly selected intermediate representation. Each caches a different thing and has different lifetime/availability.

A warm query being faster does not prove your code or clustering improved. Measure repeatable inputs, result consumption, engine/startup conditions, cache indicators and scanned work.""",
r"""1. Execute a filtered aggregate from Day 17 three times and record query IDs, wall time, bytes scanned and cache/profile availability.
2. Inspect whether a result-cache hit bypassed the execution you hoped to measure. If your supported SQL environment allows it, disable cached results for a controlled experiment using the current documented setting; otherwise compare queries with evidence that execution occurred.
3. Change the predicate, then the projected expression, and predict which type of cache may still help. A comment change alone is not reliable proof of cache bypass.
4. Optional supported classic Spark experiment:

```python
from pyspark.sql import functions as F
base = spark.table(f'{ns}.perf_orders').filter('customer_id < 100')
cached = base.persist()
print(cached.agg(F.sum('amount')).first()[0])
print(cached.agg(F.sum('amount')).first()[0])
cached.unpersist()
```

5. Inspect storage/cache evidence; compare before/after unpersist. Explain what happens when a worker is replaced or when underlying table data changes. Do not restart shared compute just to create a cold run.""",
"Repeated queries return identical values. Timing and cache hits vary by engine; record observations without inventing a universal speedup. Supported Spark persistence is explicitly released by unpersist.",
"Present a deliberately misleading result: a cached run after a code change. List what additional evidence is needed before attributing the speedup to that change, then collect that evidence where available.",
"What did each cache store? Does unpersist clear SQL result caching? Why might a cached query lack an execution profile?",
"Caches store query results, file data or selected DataFrame intermediates. Unpersist acts on the persisted Spark object, not every platform cache. A reused result may bypass normal execution and its operator profile.",
[("Disk caching behavior", "optimizations/disk-cache"), ("Query profile and cached-query limitations", "sql/user/queries/query-profile")],
["notebooks/06_delta_and_performance.sql"])

lesson("Join strategy, skew and shuffle diagnosis", "Azure SQL query profile or classic Spark UI",
"Day 17 perf_orders. Choose profile tools supported by your compute. Use bounded experiments rather than intentionally exhausting memory.",
"""A shuffle redistributes records for grouping or joins. Skew means some keys/partitions carry far more work. Broadcast can avoid a large-side shuffle when the other side is small enough, but an oversized broadcast can create memory pressure.

Cardinality bugs and resource problems are different: a duplicate dimension key can inflate revenue with perfect execution speed. Check business grain before tuning the plan.""",
r"""1. Run notebook 06's dimension-view and broadcast join section. Compare hinted/unhinted formatted plans and actual query profiles; adaptive planning can affect the final strategy.
2. Use this deterministic cardinality experiment:

```sql
WITH facts AS (SELECT * FROM VALUES (1,10),(2,20) AS f(customer_id,amount)),
dims AS (SELECT * FROM VALUES (1,'A'),(1,'B'),(2,'C') AS d(customer_id,name))
SELECT COUNT(*) AS joined_rows, SUM(amount) AS joined_amount
FROM facts JOIN dims USING(customer_id);
```

3. Repair by defining the intended unique dimension state before joining; do not just SELECT DISTINCT the final revenue.
4. Create a bounded skewed DataFrame using many rows with one customer_id, group/join it and inspect task distributions or profile operators. Compare with uniform Day 17 data.
5. Propose preaggregation, corrected key logic, supported adaptive handling or a different layout. For each proposal state the evidence that would make it appropriate.""",
"The tiny duplicate-dimension join returns 3 rows and sum 40, while original fact sum is 30. A valid unique-dimension repair preserves 30. Capture shuffle/scan/operator metrics from real runs rather than guessing from the source code alone.",
"Design a broadcast of a dimension larger than memory and explain the likely pressure boundary. Do not deliberately crash shared compute. Identify whether the actual bottleneck is scan, shuffle, join expansion or a straggling partition.",
"Why does more compute not fix a many-to-many mistake? What makes a broadcast safe? Which observation suggests skew?",
"Resources cannot repair wrong multiplicity. Broadcast must fit the actual execution memory/strategy constraints. Disproportionately slow or large partitions/tasks suggest skew and require investigation.",
[("Spark UI diagnosis", "optimizations/spark-ui-guide/"), ("SQL query profile", "sql/user/queries/query-profile")],
["notebooks/06_delta_and_performance.sql"])

lesson("Unity Catalog privileges, inheritance and functions", "Azure SQL plus two test identities where available",
"An authorized grantor, a lab account-level group and an independent consumer identity. Python UC functions need supported compute. Without a second identity, authorization enforcement remains unverified.",
"""A UC object lives in catalog.schema.object. Namespace-use privileges and the object's own access privileges have different roles. Inherited grants can cover future objects, so a broad grant can affect more than today's table list.

A session-registered Python UDF disappears with session scope. A UC SQL/Python function is a governed persistent object with execution privileges and compute constraints. Discoverability is not proof that every principal can execute it.""",
r"""1. Set notebook 07's catalog/schema and run its first SQL-function cell. Compare its output to Day 4's name contract.
2. Create a small independent governed Python function on supported compute:

```sql
CREATE OR REPLACE FUNCTION main.de_pro_lab.twice_nullable(n BIGINT)
RETURNS BIGINT LANGUAGE PYTHON AS $$
return None if n is None else n * 2
$$;
SELECT main.de_pro_lab.twice_nullable(3), main.de_pro_lab.twice_nullable(NULL);
```

Replace main/de_pro_lab consistently. Record required CREATE FUNCTION and EXECUTE/namespace privileges and current runtime restrictions.
3. Have an authorized grantor create a lab group and grant USE CATALOG, USE SCHEMA and SELECT on a new synthetic table. Query as the consumer identity. Do not infer this result by querying only as owner.
4. On a separate training schema, demonstrate inherited SELECT: grant the group scoped SELECT, create a new table afterward, and verify access plus namespace-use requirements. Revoke training grants after evidence collection.
5. Add comments and an ordinary training-purpose tag to your synthetic table; inspect them in Catalog Explorer. Compare UC data grants with workspace job/notebook ACLs.""",
"Governed Python function returns 6 and null; normalized SQL output matches the contract. Consumer access succeeds only with the required effective privileges. Save the grant matrix and actual second-identity result.",
"Remove the test consumer's namespace-use privilege or EXECUTE grant in an isolated exercise; observe which operation fails and restore it. Inspect inherited grants before concluding a revoke removed all effective access.",
"Can SELECT alone always resolve an object? What does catalog-level SELECT imply for future tables? Is a session UDF a UC object?",
"Namespace use also matters. Supported inherited privileges can apply to future descendants without conferring ownership. Session registration and governed UC functions have different scope/lifecycle.",
[("Manage UC privileges", "data-governance/unity-catalog/manage-privileges/"), ("Governed SQL and Python UDFs", "udf/unity-catalog")],
["notebooks/07_governance.sql"])

lesson("PII detection, masks, row filters and ABAC", "Azure Python/SQL plus governed-tag/policy administration",
"Two lab identities/groups, policy-capable compute and permissions. Keep direct table-mask and ABAC examples on separate synthetic tables. Never add a training policy to a business catalog.",
"""Detection identifies candidate sensitive content; policy decides who can see it. A regular expression is a limited detector, not proof all PII has been found. Column masks and row filters enforce query-time visibility; downstream transformed copies need their own access design.

ABAC selects controls using governed tags and policies so one scoped policy can cover many tagged assets. Tag assignment rights and policy scope are part of that enforcement boundary. Hashing/tokenization can preserve linkability and are not automatically anonymization.""",
r"""1. Run notebook 07's synthetic people_demo mask/filter cells and test two identities with different lab group memberships.
2. Create candidate-PII input separately from the orders source:

```python
from pyspark.sql import functions as F
texts = spark.createDataFrame([(1, 'alice@example.test'), (2, 'ordinary text'), (3, None)],
                             'id long, text string')
flagged = texts.withColumn('candidate_email', F.coalesce(
    F.col('text').rlike(r'[^\s@]+@[^\s@]+\.[^\s@]+'), F.lit(False)))
display(flagged)
```

3. Write the synthetic texts to an isolated append-only Delta source and apply the same column expression to spark.readStream.table. Use a new checkpoint and published target. Verify an unauthorized identity sees the governed mask rather than the original candidate value. Keep raw input access restricted.
4. In Catalog Explorer create governed tag lab_pii, tag email columns in two NEW synthetic tables, and attach a schema-scoped column-mask ABAC policy using the linked guide. The policy recipe is also in advanced-labs if needed.
5. Tag the second table after policy creation and test automatic coverage. Compare synthetic hashing, protected lookup-token mapping, suppression and generalized values; document what information each retains.""",
"Candidate flags are true, false, false for the three examples. Two identities should see the designed row/mask differences. New tagged assets should receive the scoped policy where eligible; save actual enforcement evidence.",
"Remove a tag from a disposable test column and inspect policy selection, then restore it. Test detector false positives/negatives. Do not claim regex coverage or a visual mask alone proves complete privacy protection.",
"Why separate detection from access enforcement? Who may assign governed tags? Why can hashed email still be identifiable?",
"Detection is uncertain classification; enforcement restricts visibility. Assignment privileges control a policy selection boundary. Predictable input spaces and linkage can permit reidentification of hashes.",
[("Row filters and masks", "data-governance/unity-catalog/filters-and-masks/"), ("Governed-tag ABAC", "data-governance/unity-catalog/abac/core-concepts")],
["notebooks/07_governance.sql", "docs/advanced-labs.md"])

lesson("OpenSharing and Clean Rooms", "Azure Catalog Explorer and approved recipient/collaborator environment",
"Provider share privileges, synthetic gold_sales, recipient setup and an eligible Clean Rooms test. Same-metastore Clean Rooms test collaboration is supported where the feature is enabled; a second external organization is not always required.",
"""Sharing grants read access to selected assets across a provider/recipient boundary. Recipient type changes authentication and setup. Only sharing your gold table limits exposure more clearly than sharing an entire schema with future assets.

Clean Rooms support controlled collaborative execution with participant assets and analysis approvals. Review outputs as well as input access: an aggregate with a tiny group can still disclose information. Revocation restricts future access, not copies already exported.""",
r"""1. Use the current sharing UI to create an approved disposable D2D recipient with its actual metastore sharing identifier, or an open-protocol recipient using the documented authentication setup. Keep activation credentials out of notes/Git.
2. As authorized provider, adapt:

```sql
CREATE SHARE lab_orders_share COMMENT 'Synthetic training data';
ALTER SHARE lab_orders_share ADD TABLE main.de_pro_lab.gold_sales;
GRANT SELECT ON SHARE lab_orders_share TO RECIPIENT YOUR_LAB_RECIPIENT;
```

3. As recipient create the shared catalog through its supported sharing workflow and query totals. Record the granted object and denied raw-source access.
4. Create an approval-based Clean Rooms test through Catalog Explorer. Use actual assigned participant catalog aliases, add synthetic assets and a notebook returning only grouped counts/revenue. Request approvals in the product, run, and inspect output access/logs.
5. Compare a D2D reader and open reader's credential lifecycle and permitted operations. If one is unavailable, record its design separately from the actual test.
6. Revoke the test share's recipient access and verify a fresh query fails. Inventory any prior output/export separately.""",
"Recipient totals match the provider's synthetic gold, while unshared raw tables are inaccessible through the share. A clean-room run has an actual approval/run record and controlled output. Without those records the external exercise is pending.",
"Remove the recipient's SELECT-on-share grant, then attempt a new recipient read. Explain why it does not retroactively erase a previously downloaded result. Never send credentials through this chat or a committed journal.",
"Why choose Clean Rooms instead of ordinary read sharing? What happens when a whole schema is shared? Does aggregate-only imply zero disclosure risk?",
"Controlled computation/approval can meet different collaboration needs. Schema sharing can expose additional assets according to its semantics. Small groups and output combinations still require disclosure analysis.",
[("Create shares", "opensharing/create-share"), ("Create and test Clean Rooms", "clean-rooms/create-clean-room")],
["docs/advanced-labs.md", "notebooks/04_batch_silver_gold.py"])

lesson("Deletion, retention and replay prevention", "Azure SQL; synthetic data only",
"Isolated purge_demo table and read access to the lab's lineage/source inventory. No shortened retention or disabled retention checks are needed.",
"""DELETE changes the table's current logical result. Historical versions and physical files have retention lifetimes; VACUUM removes eligible unreferenced files. Neither operation by itself proves erasure from every source, replica, backup and export.

If ingestion can replay an undeleted source record, a subject removed from silver can return. A complete design needs identity mapping, propagation, replay prevention and verification across relevant copies.""",
r"""1. In notebook 07 execute only the purge_demo section, which creates one synthetic row, deletes it and inspects history/retention candidates.
2. Query the current state and an eligible prior version using the actual version from history. Use only the synthetic payload.
3. Inspect candidates without removing files:

```sql
VACUUM purge_demo DRY RUN;
```

4. Build an inventory for a synthetic subject: source files/database, bronze, quarantine, silver, gold, CDC/CDF, checkpoints, downstream shares/exports and backups. Record ownership, access, retention and deletion propagation separately.
5. Simulate replay in scratch tables: copy a synthetic subject to bronze/silver, delete only from silver, then rebuild silver from bronze. Observe reintroduction and design a maintained deletion/tombstone control appropriate to the pipeline.
6. Write an ordered runbook: identify scope, stop/prevent unwanted reintroduction, apply source/downstream deletion, honor retention obligations, verify current/historical exposure under the actual policy, and record exceptions requiring owners.""",
"Current purge_demo count becomes zero while history can still describe prior operations. A dry run may return no eligible files on a new table; that is an expected observation. Scratch replay demonstrates why a single-layer DELETE is incomplete.",
"Present the claim 'DELETE succeeded, so all copies are gone' and refute it with the inventory. Do not force physical deletion with zero-hour retention. Keep compliance claims tied to the actual organizational policy and verified systems.",
"Which operation changes current rows? What does VACUUM target? How can a pipeline reintroduce a deleted subject?",
"DELETE updates logical state; VACUUM removes eligible unreferenced physical files under retention. Retained upstream input can recreate the row unless deletion state/source handling prevents replay.",
[("VACUUM behavior and retention", "tables/operations/vacuum"), ("CDF retention limits", "tables/features/change-data-feed")],
["notebooks/07_governance.sql"])

lesson("System tables, cost attribution and alerts", "Azure SQL plus Jobs/alert UI",
"System schema access granted by the administrator, available operational records and a test notification destination you control. Do not export sensitive audit/system data into public notes.",
"""System tables expose operational evidence with access and ingestion-latency constraints. Usage quantity has a unit; price attribution requires matching rates, effective dates, cloud/SKU and workload identifiers. List-price estimates are not automatically invoiced spend.

An alert evaluates a signal against a condition and should lead to a specific action. Missing data, delayed data and a healthy zero are different cases. Design firing, recovery, identity and evaluation latency before relying on the alert.""",
r"""1. Run notebook 08's billing, lakeflow and audit queries where permitted. Describe the schemas first if a field differs in your environment.
2. Link one known job/run to operational records using actual available identifiers. Inspect compute metadata and effective-dated pricing, separating units and estimated list cost from billed cost.
3. Create a deterministic test signal:

```sql
CREATE TABLE main.de_pro_lab.day25_alert_signal (invalid_orders BIGINT);
INSERT INTO main.de_pro_lab.day25_alert_signal VALUES (0);
SELECT invalid_orders FROM main.de_pro_lab.day25_alert_signal;
```

4. In the current SQL/Lakehouse alert UI save that query, set invalid_orders > 0, choose supported compute and a test destination you control. Evaluate the healthy state. Change the synthetic value to 1, evaluate the transition, restore 0 and inspect recovery history. Disable any test schedule when finished.
5. Design signal/query, threshold, latency and response for freshness, business metric, anomaly, cost, SQL health, audit/security and AI failure rate. Implement one additional signal if time permits, or connect the first result to a disposable Job condition.""",
"The signal transitions healthy → triggered → recovered according to actual alert evaluation semantics. Operational queries may lag the job; record observation time and data time. Permission denial is an access prerequisite to resolve, not an empty dataset.",
"Evaluate a no-row/null signal in a separate test and record how the alert treats it. Avoid interpreting missing data as proof of health. Compare an actionable failure alert with a noisy threshold that fires on expected invalid data.",
"Why can't DBUs be summed across units as money? What timestamp controls a price join? What should an alert recipient do next?",
"Quantity and currency are different measures. Rate validity must match the usage interval and relevant SKU/cloud. A useful alert includes a defined investigation/response and distinguishes stale/missing evidence.",
[("System tables and access", "admin/system-tables/"), ("SQL alerts and evaluation", "sql/user/alerts/")],
["notebooks/08_observability.sql"])

lesson("Diagnose failures and repair job runs", "Azure Jobs/pipeline UI, SQL and authenticated local CLI",
"A known training job/run and pipeline ID from previous days. Permission to monitor them; Spark UI availability depends on compute.",
"""Classify the failed boundary before changing code: parameter, missing object, dependency, privilege, bad input, memory/resource pressure or external system. Logs, plans and task state provide different evidence.

Job lifecycle success does not prove business correctness. Repairing selected tasks can save work, but their input assumptions must still hold. A pipeline full refresh has different reconstruction implications from an ordinary update.""",
r"""1. Select one completed run and record its job ID, run ID, task states and output counts. Fetch the same run from your authenticated local shell:

```powershell
databricks jobs get YOUR_JOB_ID
databricks jobs get-run YOUR_RUN_ID
```

Replace the IDs with numeric values from your own job. Inspect equivalent monitoring through the current REST API/SDK reference, using configured authentication rather than a pasted token.
2. Query your actual pipeline event log:

```sql
SELECT timestamp, event_type, message, details
FROM event_log('YOUR_PIPELINE_ID')
ORDER BY timestamp DESC LIMIT 50;
```

3. If the documented regional pipeline-events system table is enabled, compare it with per-pipeline events and its access/latency requirements. Do not assume a beta system table is present everywhere.
4. Introduce a wrong schema parameter in a disposable downstream task. Locate the failure in task output, classify the boundary, fix the parameter and repair the relevant failed tasks.
5. Inspect one relevant SQL profile or classic Spark stage/task/log. Reconcile the repaired output to expected keys and revenue, not only a green task indicator.""",
"UI and CLI identify the same run/task state. The wrong schema produces a diagnosable missing-object/access boundary rather than a new business rule. A repaired run has both successful task state and reconciled data.",
"Write a timeline: change → first failure → diagnostic evidence → root cause → correction → repair → output proof. Explain why rerunning everything or increasing memory would not repair a wrong schema parameter.",
"When is repair appropriate? Why preserve the source revision/run ID? When might a full refresh require retained raw history?",
"Repair is appropriate when corrected tasks can safely reuse the relevant upstream outputs. Revision/run IDs connect evidence to actual code. Reconstructing targets needs adequate retained source data and correct refresh semantics.",
[("Pipeline event log", "ldp/monitor-event-logs"), ("Spark UI troubleshooting", "optimizations/spark-ui-guide/"), ("Databricks CLI Jobs commands", "dev-tools/cli/reference/jobs-commands")],
["notebooks/08_observability.sql", "docs/advanced-labs.md"])

lesson("Promote the same revision through CI/CD", "Local shell, your CI provider and Azure dev/test targets",
"Successful Day 2 deployment; test schema initialized; approved CI identity if configuring remote deployment. The supplied workflow tests/builds only and does not deploy automatically.",
"""Promotion should identify the tested code revision, artifact and target configuration. Environment-specific namespaces and grants differ while application rules remain the same. CI build success and a deployed smoke test are complementary evidence.

Interactive developer OAuth credentials and noninteractive CI workload identity have different lifecycles. Bundle ownership also differs from ad hoc UI/API changes; redeployment can reconcile declared resource settings.""",
r"""1. In notebook 00 set schema to de_pro_lab_test and run setup with the same intended test catalog. Keep dev data/checkpoints separate.
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
5. Change a harmless label on the disposable bundle-managed job through the UI, redeploy the declared configuration and inspect reconciliation.""",
"Dev/test write to distinct declared namespaces with the same application behavior. There is a reproducible association between tested revision, built wheel and successful target smoke run. Without CI identity/repository access, mark remote CI execution pending.",
"In a development branch override a target to an unavailable catalog. Compare configuration validation with runtime privilege/object checks, then restore the target before deployment. Never use a production identity for this experiment.",
"What should be promoted: source guesses or an identified tested revision? Can bundle validate prove data privileges? Why version a changed wheel?",
"Promote a known revision/artifact with traceable target settings. Validation is not runtime authorization. Versioned artifacts expose changes and help avoid stale cached implementations.",
[("CI/CD development process", "dev-tools/ci-cd/"), ("Bundle configurations and targets", "dev-tools/bundles/examples")],
[".github/workflows/ci.yml", "databricks.yml", "docs/setup.md"])

lesson("Iceberg, table formats and interoperability", "Azure SQL compute with managed Iceberg support",
"UC managed storage, permission to create lab tables and supported Iceberg features. External-reader proof requires an eligible engine and authorized catalog access; do not add arbitrary JARs to bypass unsupported runtime features.",
"""Parquet is a file encoding. Iceberg and Delta provide transactional table metadata across files. A directory containing Parquet is not automatically an Iceberg table. Readers must understand the actual metadata, table features and access path.

A native managed Iceberg table differs from a Delta table exposing Iceberg-compatible metadata. Supported writes, clustering, CDC and engine combinations depend on the current table/runtime feature set.""",
r"""1. Check the linked feature requirements against your workspace before creating a table.
2. On supported SQL compute, replace the namespace and run once:

```sql
CREATE TABLE main.de_pro_lab.day28_iceberg
  (order_id BIGINT, amount DOUBLE) USING ICEBERG;
INSERT INTO main.de_pro_lab.day28_iceberg VALUES (1,25), (2,40);
UPDATE main.de_pro_lab.day28_iceberg SET amount = 30 WHERE order_id = 1;
SELECT COUNT(*) AS n, SUM(amount) AS total FROM main.de_pro_lab.day28_iceberg;
DESCRIBE EXTENDED main.de_pro_lab.day28_iceberg;
```

3. Create a separate Delta equivalent and compare metadata, ownership, supported operations and maintenance requirements. Do not mutate the running core pipeline's format.
4. Through the current pipeline UI/docs configure a SEPARATE eligible minimal CDC pipeline with an Iceberg target where supported. Export its generated definition and document supported SCD/CDC features before assuming parity with the existing Delta pipeline.
5. If an external REST-catalog reader is available, authorize only the lab asset and verify its read. Otherwise record interoperability as a design matrix, not a successful external read.
6. Record restrictions for layout/partitioning and any feature compatibility changes. A missing feature should remain a documented prerequisite.""",
"On supported compute the managed Iceberg table has two rows and sum 70. Metadata identifies its actual table type/format. External and Iceberg-target CDC evidence exists only after those independent runs succeed.",
"Choose one currently documented unsupported combination on an isolated table and predict/review the resulting failure. Avoid treating every data-source-not-found error as a missing Python library.",
"Why are table and file formats different? Does every Delta feature work in every Iceberg reader? Can a source format and target format differ?",
"Table metadata defines transactional interpretation over files. Feature compatibility must be checked per engine/table configuration. Ingestion can transform between supported source and target formats with an explicit schema/semantics contract.",
[("Iceberg on Azure Databricks", "iceberg/"), ("CREATE TABLE and format constraints", "sql/language-manual/sql-ref-syntax-ddl-create-table-using")],
["docs/advanced-labs.md"])

lesson("Dimensional grain, historical joins and metric views", "Azure SQL and the declarative pipeline",
"Day 9 silver data, Day 10 history, supported metric-view compute. Set namespace references in notebook 09, including the fully qualified source inside metric YAML.",
"""Grain states what one fact row represents. Customer/product/date dimensions add analytical context; a historical dimension must match the version valid for the fact's relevant time. Joining all historical versions inflates measures.

A metric view centralizes analytical definitions. A materialized aggregate persists a result for a refresh/performance need. Defining a reusable metric does not automatically make every expensive query precomputed.""",
r"""1. Run notebook 09's fact and metric-view sections after changing all main/de_pro_lab references, including YAML source. Check fact order_id uniqueness and reconcile revenue to silver.
2. Design a separate business-time SCD2 dimension; the core sequence column is an ordering number, not a timestamp. Test a point-in-time join:

```sql
WITH fact AS (
 SELECT 10 customer_id, TIMESTAMP '2026-10-01 10:00:00' order_time, 25 amount
), dim AS (
 SELECT * FROM VALUES
 (10, 'CA', TIMESTAMP '2026-01-01', TIMESTAMP '2026-10-01 12:00:00'),
 (10, 'US', TIMESTAMP '2026-10-01 12:00:00', CAST(NULL AS TIMESTAMP))
 AS d(customer_id,region,valid_from,valid_to)
)
SELECT f.amount, d.region FROM fact f JOIN dim d
 ON f.customer_id=d.customer_id AND f.order_time>=d.valid_from
 AND (f.order_time<d.valid_to OR d.valid_to IS NULL);
```

3. Remove the interval condition in a scratch query, compare row count/revenue, then restore it. Add boundary-time tests at exactly valid_to/valid_from.
4. Query sales_metrics with MEASURE(Revenue)/MEASURE(Orders) at multiple region groupings. Add a ratio from properly aggregated components.
5. Add a second materialized gold aggregate through the pipeline and compare its refresh/performance role with the metric definition.""",
"The historical join returns one CA row with amount 25. Without time filtering it returns two matches and can sum to 50. Core fact revenue remains 75 or 87 depending on the supplied files, plus any deliberate later valid additions.",
"Average regional ratios and compare with a global ratio computed from summed numerators/denominators. Explain the weighting difference. Do not repair join inflation by averaging away duplicate fact rows.",
"What is the fact grain? Why use a half-open history interval? Does a metric view always persist preaggregated rows?",
"State the real business entity per fact row. Half-open intervals avoid double matches at shared boundaries. Metric definitions and materialized query results have distinct roles; inspect actual materialization configuration.",
[("Metric-view YAML and semantics", "uc-semantics/metric-views/yaml-reference"), ("Pipeline materialized views", "ldp/developer/python-dev")],
["notebooks/09_variant_modeling.sql", "pipelines/retail_pipeline.py"])

lesson("Rebuild the lakehouse and resolve an incident", "Local environment, Azure isolated test target and your journal",
"Previous lessons' evidence; an isolated fresh namespace, schema-specific source/checkpoint configuration and available permissions. External-service gaps remain explicit rather than being assumed complete.",
"""Integrated mastery means predicting outcomes, implementing contracts and diagnosing failures across boundaries. A green run proves an operation completed; reconciled business values and authorization tests establish more of the intended behavior.

Reproducibility requires source revision, distribution version, target configuration, environment and input inventory. Recovery must preserve the identity/progress assumptions established for each sink and stream.""",
r"""1. From a fresh checkout or separate source copy create a new local venv, run contract tests and build/install the distribution. Do not reuse hidden notebook variables as proof of reproducibility.
2. Choose an isolated namespace and configure it consistently in setup, bundle variables, source paths and SQL. Run notebook 00 there, validate/deploy test, run retail_names and ingest the supplied first file.
3. Run batch silver/gold and the separate declarative pipeline. Reconcile 4 raw orders → 3 valid + 1 quarantine → valid amount 75. Validate customer 10 region US and customer 20 absent before new CDC extensions.
4. Add one new valid order, a business-key duplicate, a negative amount and a new field under immutable new filenames. PREDICT outcomes before updating. Explain why the current declarative lp_silver, which does not deduplicate business keys, differs from the batch silver rule.
5. Restart a stream with its existing checkpoint and verify sink behavior. Check actual second-identity access to protected published data.
6. Choose three incidents without looking up the fix first: missing dependency, wrong schema, changed field, duplicate join key, denied access or replayed batch. Diagnose from run/log/plan evidence, repair and reconcile.
7. Give a ten-minute explanation: source → contracts → tables → orchestration → security → monitoring → deployment. Finish your own runbook and list all unresolved prerequisites.""",
"The initial isolated fixture reconciles to revenue 75; later values match your written predictions and actual dedup/quality rules. Save revision, artifact, namespace, run/update IDs and access tests. Unrun external integrations stay listed as gaps.",
"Use a new isolated namespace for a rebuild rather than deleting established working checkpoints. Trace each incident to its actual boundary before changing more than one thing. Record proof after repair.",
"Could another person reproduce your result? Which tests establish correctness versus deployment? Which external objectives still lack evidence?",
"A usable runbook includes setup, configuration, immutable input inventory, expected values and recovery. Different checks establish different boundaries. Readiness requires identifying gaps rather than counting calendar days completed.",
[("Azure Databricks documentation hub", ""), ("CI/CD practices", "dev-tools/ci-cd/"), ("Streaming production behavior", "structured-streaming/production")],
["README.md", "docs/exam-alignment.md", "docs/verification.md"])


def render():
    assert len(LESSONS) == 30, len(LESSONS)
    # The order is intentional and matches the existing exam-aligned workbook.
    out = ROOT / "daily-learning"
    out.mkdir(exist_ok=True)
    targets = [out / f"day-{i:02d}.md" for i in range(1, 31)] + [out / "README.md"]
    if any(p.exists() for p in targets):
        raise FileExistsError("Daily files already exist; preserve learner notes before regenerating")
    for number, item in enumerate(LESSONS, 1):
        nav = ["[All days](README.md)"]
        if number > 1:
            nav.append(f"[Previous day](day-{number-1:02d}.md)")
        if number < 30:
            nav.append(f"[Next day](day-{number+1:02d}.md)")
        material = "\n".join(f"- [{path}](../{path})" for path in item["files"])
        refs = "\n".join(f"- [{label}]({BASE}{path})" for label, path in item["references"])
        bootstrap = ""
        local_start = ""
        if "```powershell" in item["steps"]:
            local_start = r"""
Before local commands, open PowerShell in the project root (not inside this
daily-learning folder):

```powershell
cd 'C:\Users\braje\OneDrive\Desktop\Documents\ChatGPT\Databricks Learning'
```
"""
        if "{ns}" in item["steps"] or "{root}" in item["steps"]:
            bootstrap = """
For added Python cells that use `ns` or `root`, run this configuration cell first.
Replace `main` if your training catalog has a different name; the schema must
already exist from notebook 00. This cell only selects names; it creates nothing.

```python
catalog = 'main'
lab_schema = 'de_pro_lab'
ns = f'{catalog}.{lab_schema}'
root = f'/Volumes/{catalog}/{lab_schema}/lab_files'
```
"""
        text = f"""# Day {number:02d} - {item['title']}

{' | '.join(nav)}

**Where:** {item['where']}  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** {item['need']}

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

{item['understand']}

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

{refs}

## 3. Open today's materials

{material}

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.
{local_start}
{bootstrap}
## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

{item['steps']}

## 5. Verify the result

{item['expected']}

## 6. Break one thing and repair it

{item['failure']}

## 7. Explain without looking

{item['questions']}

<details>
<summary>Answer notes - open after your attempt</summary>

{item['answer']}

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-{number:02d}/` if useful.

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

{' | '.join(nav)}
"""
        (out / f"day-{number:02d}.md").write_text(text, encoding="utf-8")
    rows = "\n".join(
        f"| {i:02d} | [{x['title']}](day-{i:02d}.md) | {x['where']} |"
        for i, x in enumerate(LESSONS, 1))
    index = f"""# Your daily Databricks learning files

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
{rows}

## Keep evidence honest

Cloud snippets and new daily exercises are authored starter material; they have not
been run in your Azure workspace. Local package contract tests have passed. External
databases, brokers, sharing, policy administration, inference endpoints and some
table features need additional access. Their lessons include a design path to keep
learning, but design work does not count as executed integration evidence.

The scope follows the [exam alignment audit](../docs/exam-alignment.md), while runtime
details use [Microsoft's Azure Databricks documentation]({BASE}). Check current
feature requirements before a lab. The [original overview](../docs/30-day-workbook.md)
and [setup reference](../docs/setup.md) remain available as supporting material.

Write directly in each file's My learning notes section, or copy that section into
your private notebook. The authoring generator should not be rerun over personal notes.
"""
    (out / "README.md").write_text(index, encoding="utf-8")
    print(f"Created {len(LESSONS)} daily lessons and their index in {out}")


if __name__ == "__main__":
    render()
