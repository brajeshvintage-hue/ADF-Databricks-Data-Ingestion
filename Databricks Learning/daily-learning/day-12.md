# Day 12 - Checkpoint recovery and idempotent foreachBatch

[All days](README.md) | [Previous day](day-11.md) | [Next day](day-13.md)

**Where:** Azure Python notebook; use compute supporting foreachBatch  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Day 6 bronze, root/ns configuration from setup, and permission to create scratch Delta tables. Keep transaction IDs paired with their stream/checkpoint identity.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Recovery can replay a micro-batch. foreachBatch supplies batch_id, but its sink effects must be designed to tolerate repetition. Transaction application/version IDs let a supported Delta append recognize repeated writes for the same transaction.

A checkpoint restores progress and state. It cannot make an external API call exactly-once or make writes to two independent systems atomic. Deleting checkpoints without redesigning sink identity can cause duplicates or skipped writes.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [foreachBatch semantics and replay](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/foreach)
- [Delta streaming writes](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/delta-lake)

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

1. Run notebook 05's foreachBatch section. Inspect the callback, target table and dedicated checkpoint.
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
5. Write a recovery matrix for: same checkpoint/same application ID; new checkpoint/new ID; new checkpoint/reused ID. Include the consequence of batch IDs starting again.

## 5. Verify the result

Transaction-protected replay produces two rows; plain double append produces four. The guarantee applies to the defined Delta sink transaction contract and retained transaction metadata, not arbitrary external effects or indefinite retention.

## 6. Break one thing and repair it

Use a new scratch table for each independent transaction test. Predict how reusing application/version 0 with different intended data can cause that transaction to be treated as already committed. Do not test by deleting production or working checkpoints.

## 7. Explain without looking

What is at-least-once? Where is idempotency implemented? Why not swallow all exceptions inside foreachBatch?

<details>
<summary>Answer notes - open after your attempt</summary>

A batch effect may be attempted more than once. The destination's transaction/key design must make replay safe. Swallowing failures can report success while losing data or leaving partial output.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-12/` if useful.

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

[All days](README.md) | [Previous day](day-11.md) | [Next day](day-13.md)
