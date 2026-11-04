# Day 23 - OpenSharing and Clean Rooms

[All days](README.md) | [Previous day](day-22.md) | [Next day](day-24.md)

**Where:** Azure Catalog Explorer and approved recipient/collaborator environment  
**Time:** about 90-120 minutes; external setup may take longer.  
**Prerequisites:** Provider share privileges, synthetic gold_sales, recipient setup and an eligible Clean Rooms test. Same-metastore Clean Rooms test collaboration is supported where the feature is enabled; a second external organization is not always required.

**Today's outcome:** build and verify the behavior below, explain one failure,
and write your own concept notes in this file. Read the answer notes only after
making your prediction. Starter cloud code still needs execution in your workspace.

## 1. Understand the concept

Sharing grants read access to selected assets across a provider/recipient boundary. Recipient type changes authentication and setup. Only sharing your gold table limits exposure more clearly than sharing an entire schema with future assets.

Clean Rooms support controlled collaborative execution with participant assets and analysis approvals. Review outputs as well as input access: an aggregate with a tiny group can still disclose information. Revocation restricts future access, not copies already exported.

## 2. Read with a purpose

Official Microsoft Learn links checked October 27, 2026. Read the sections
relevant to this lab: requirements, example, limitations and recovery. Record
your actual runtime/CLI/environment; feature availability can differ.

- [Create shares](https://learn.microsoft.com/en-us/azure/databricks/opensharing/create-share)
- [Create and test Clean Rooms](https://learn.microsoft.com/en-us/azure/databricks/clean-rooms/create-clean-room)

## 3. Open today's materials

- [docs/advanced-labs.md](../docs/advanced-labs.md)
- [notebooks/04_batch_silver_gold.py](../notebooks/04_batch_silver_gold.py)

Source links are workspace files. Import a `.py` notebook into Azure Databricks
when the lesson says Azure; local PowerShell does not provide `spark` or `dbutils`.
SQL snippets run in SQL cells/editor; Python snippets run in Python cells.
For SQL use your existing catalog and isolated `de_pro_lab` schema; update fully
qualified references too. Stop manually started compute when finished.

## 4. Predict, then build

Before each run write expected rows, values, failure boundary or plan behavior.
Use synthetic data and keep experiments isolated from the established streams.

1. Use the current sharing UI to create an approved disposable D2D recipient with its actual metastore sharing identifier, or an open-protocol recipient using the documented authentication setup. Keep activation credentials out of notes/Git.
2. As authorized provider, adapt:

```sql
CREATE SHARE lab_orders_share COMMENT 'Synthetic training data';
ALTER SHARE lab_orders_share ADD TABLE main.de_pro_lab.gold_sales;
GRANT SELECT ON SHARE lab_orders_share TO RECIPIENT YOUR_LAB_RECIPIENT;
```

3. As recipient create the shared catalog through its supported sharing workflow and query totals. Record the granted object and denied raw-source access.
4. Create an approval-based Clean Rooms test through Catalog Explorer. Use actual assigned participant catalog aliases, add synthetic assets and a notebook returning only grouped counts/revenue. Request approvals in the product, run, and inspect output access/logs.
5. Compare a D2D reader and open reader's credential lifecycle and permitted operations. If one is unavailable, record its design separately from the actual test.
6. Revoke the test share's recipient access and verify a fresh query fails. Inventory any prior output/export separately.

## 5. Verify the result

Recipient totals match the provider's synthetic gold, while unshared raw tables are inaccessible through the share. A clean-room run has an actual approval/run record and controlled output. Without those records the external exercise is pending.

## 6. Break one thing and repair it

Remove the recipient's SELECT-on-share grant, then attempt a new recipient read. Explain why it does not retroactively erase a previously downloaded result. Never send credentials through this chat or a committed journal.

## 7. Explain without looking

Why choose Clean Rooms instead of ordinary read sharing? What happens when a whole schema is shared? Does aggregate-only imply zero disclosure risk?

<details>
<summary>Answer notes - open after your attempt</summary>

Controlled computation/approval can meet different collaboration needs. Schema sharing can expose additional assets according to its semantics. Small groups and output combinations still require disclosure analysis.

</details>

## 8. My learning notes

Fill this in; the lesson is also your daily learning file. Keep credentials and
sensitive operational output out of these notes. Save small synthetic outputs or
redacted run references under `../evidence/day-23/` if useful.

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

[All days](README.md) | [Previous day](day-22.md) | [Next day](day-24.md)
