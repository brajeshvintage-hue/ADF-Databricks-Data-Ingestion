# Day 11 - Watermarks, event time and stateful aggregation

[All days](README.md) | [Previous day](day-10.md) | [Next day](day-12.md)

**Where:** Azure Python notebook with supported Structured Streaming compute  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 6 bronze for the starter dedup. The independent aggregation exercise below creates its own source/table/checkpoint. Use a unique suffix if rerunning from scratch.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

State remembers keys or window aggregates across micro-batches. An event-time watermark uses observed event progress and a delay to manage state. It is not a timer that advances merely because you wait.

Append output for a windowed aggregation waits until results can be finalized; update output exposes changed results for a suitable sink. Dedup within a watermark bounds guarantees and state; it is not global lifetime uniqueness.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Watermarks and deduplication](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/watermarks)
- [Structured Streaming production considerations](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/production)

## 3. Open today's materials

- [notebooks/05_streaming.py](../notebooks/05_streaming.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

For added Python cells that use `ns` or `root`, run this configuration cell first.
Replace `main` if your training catalog has a different name; the schema must
already exist from notebook 00. This cell only selects names; it creates nothing.

```python
catalog = 'main'
lab_schema = 'de_pro_lab'
ns = f'{catalog}.{lab_schema}'
root = f'/Volumes/{catalog}/{lab_schema}/lab_files'
```

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Run notebook 05's first section; inspect progress/state metrics supported by your compute.
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
4. Explain how update mode differs; use a documented compatible sink if testing it. Do not assume Delta append is a valid sink for every update-mode query.

## 5. Verify the result

The first five-minute window's input sum is 30. It can be emitted once watermark progress finalizes it. The latest window may remain unfinalized. Record observed watermark, window output and state rather than assuming one output row for every source row.

## 6. Break one thing and repair it

Wait without new event-time progress and observe that wall-clock time alone does not finalize old state. Compare with appending a later timestamp. Keep working checkpoints intact.

## 7. Explain without looking

What does the watermark bound? Why can the latest append-mode window be absent? Is dedup permanent after state eviction?

<details>
<summary>Answer notes - open after your attempt</summary>

It bounds event-time state for supported operators. A recent window is not yet finalized. Eviction limits the horizon of remembered duplicate keys; it does not create eternal uniqueness.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-11/` if useful.

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

[All days](README.md) | [Previous day](day-10.md) | [Next day](day-12.md)
