# Databricks notebook source
# MAGIC %run ./00_setup

# COMMAND ----------
# Stateful dedup uses a different target/checkpoint from bronze ingestion.
from pyspark.sql import functions as F
events = (spark.readStream.table(f"{ns}.bronze_orders")
    .filter("order_id IS NOT NULL AND event_time IS NOT NULL AND amount >= 0")
    .withWatermark("event_time", "10 minutes")
    .dropDuplicatesWithinWatermark(["order_id"]))
q = (events.writeStream.format("delta")
    .option("checkpointLocation", f"{root}/checkpoints/dedup")
    .trigger(availableNow=True).toTable(f"{ns}.stream_orders"))
q.awaitTermination()
print(q.lastProgress)

# COMMAND ----------
# Day 12: foreachBatch is at-least-once; this Delta write uses transaction IDs
# to make replay of the same batch idempotent for this single sink.
# Requires compute that supports foreachBatch. If unavailable on your serverless
# environment, run this cell on supported classic compute and record that choice.
def write_batch(batch, batch_id):
    (batch.write.format("delta").mode("append")
        .option("txnAppId", "retail-orders-single-sink-v1")
        .option("txnVersion", batch_id)
        .saveAsTable(f"{ns}.foreach_orders"))

q2 = (spark.readStream.table(f"{ns}.bronze_orders").writeStream
    .foreachBatch(write_batch)
    .option("checkpointLocation", f"{root}/checkpoints/foreach")
    .trigger(availableNow=True).start())
q2.awaitTermination()
# Keep txnAppId stable with this checkpoint. A new checkpoint resets batch IDs:
# give that NEW stream a NEW txnAppId or legitimate writes could be skipped.
