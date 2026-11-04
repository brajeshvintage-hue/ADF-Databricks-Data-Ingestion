# Databricks notebook source
# MAGIC %run ./00_setup

# COMMAND ----------
from pyspark.sql import functions as F
stream = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{root}/schemas/orders")
    .option("cloudFiles.schemaHints", "order_id LONG, customer_id LONG, amount DOUBLE, event_time TIMESTAMP")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("rescuedDataColumn", "_rescued_data")
    .load(f"{root}/orders")
    .withColumn("source_file", F.col("_metadata.file_path"))
    .withColumn("ingested_at", F.current_timestamp()))
q = (stream.writeStream.format("delta")
    .option("checkpointLocation", f"{root}/checkpoints/bronze")
    .option("mergeSchema", "true")
    .trigger(availableNow=True).toTable(f"{ns}.bronze_orders"))
q.awaitTermination()
print(q.lastProgress)
display(spark.table(f"{ns}.bronze_orders"))

# COMMAND ----------
# Day 7: run once, then rerun the ingestion cell. A new column can cause a planned
# schema-evolution failure; retry with the same schema/checkpoint locations.
# Uncomment only on Day 7; avoid overwriting files already consumed.
# next_row = dict(order_id=5, customer_id=40, customer_name="Dan", amount=12.0,
#                 event_time="2026-10-01T10:04:00Z", region="UK", coupon="SAVE")
# dbutils.fs.put(f"{root}/orders/batch_002.json", json.dumps(next_row), overwrite=False)
