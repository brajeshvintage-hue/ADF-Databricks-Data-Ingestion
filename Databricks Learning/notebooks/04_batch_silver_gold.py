# Databricks notebook source
# MAGIC %run ./00_setup

# COMMAND ----------
from pyspark.sql import functions as F, Window
bronze = spark.table(f"{ns}.bronze_orders")
# Coalesce the entire rule: SQL NULL must not escape both valid/invalid branches.
rule = F.coalesce(
    F.col("order_id").isNotNull() & F.col("customer_id").isNotNull()
    & F.col("event_time").isNotNull() & (F.col("amount") >= 0)
    & F.col("_rescued_data").isNull(), F.lit(False))
tagged = bronze.withColumn("is_valid", rule)
tagged.filter(~F.col("is_valid")).write.format("delta").mode("overwrite").saveAsTable(f"{ns}.quarantine_orders")
valid = tagged.filter("is_valid")
# Deterministic tie breaker is source_file for this exercise. A real source should
# supply a sequence/version; identical same-file duplicates have identical payloads here.
w = Window.partitionBy("order_id").orderBy(F.col("event_time").desc(), F.col("source_file").desc())
silver = valid.withColumn("rn", F.row_number().over(w)).filter("rn = 1").drop("rn", "is_valid")
silver.write.format("delta").mode("overwrite").saveAsTable(f"{ns}.silver_orders")
gold = silver.groupBy(F.to_date("event_time").alias("order_date"), "region").agg(
    F.sum("amount").alias("revenue"), F.count("*").alias("orders"))
gold.write.format("delta").mode("overwrite").saveAsTable(f"{ns}.gold_sales")
display(gold)
# With ONLY batch_001: 3 silver rows; quarantine 1; CA revenue 35, US revenue 40.
# With batch_002: 4 silver rows; UK revenue 12 is added.
assert tagged.count() == valid.count() + spark.table(f"{ns}.quarantine_orders").count()
