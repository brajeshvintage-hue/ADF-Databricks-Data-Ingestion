"""Run in a Lakeflow Declarative Pipeline, not with python or as a notebook.

Run notebook 00 first. This graph owns tables named lp_* so it cannot collide
with the batch and Structured Streaming labs. Full refresh reconstructs targets
from retained source history; it is not interchangeable with a normal update.
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F

source = spark.conf.get("lab.source")
cdc_source = spark.conf.get("lab.cdc_source")


@dp.table(name="lp_bronze")
def bronze():
    return (spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaHints", "order_id LONG, customer_id LONG, amount DOUBLE, event_time TIMESTAMP")
        .option("rescuedDataColumn", "_rescued_data")
        .load(source))


valid_sql = "order_id IS NOT NULL AND customer_id IS NOT NULL AND event_time IS NOT NULL AND amount >= 0 AND _rescued_data IS NULL"


@dp.table(name="lp_checked")
@dp.expect("valid_order", valid_sql)
def checked():
    return spark.readStream.table("lp_bronze").withColumn(
        "is_valid", F.coalesce(F.expr(valid_sql), F.lit(False)))


@dp.table(name="lp_silver")
@dp.expect_or_drop("valid_order", valid_sql)
def silver():
    return spark.readStream.table("lp_checked")


@dp.table(name="lp_quarantine")
def quarantine():
    return spark.readStream.table("lp_checked").filter("NOT is_valid")


@dp.materialized_view(name="lp_gold")
def gold():
    return spark.read.table("lp_silver").groupBy(
        F.to_date("event_time").alias("order_date"), "region"
    ).agg(F.sum("amount").alias("revenue"))


@dp.temporary_view(name="customer_events")
def customer_events():
    return spark.readStream.table(cdc_source)


for target, scd_type in [("lp_customer_current", 1), ("lp_customer_history", 2)]:
    dp.create_streaming_table(target)
    dp.create_auto_cdc_flow(
        name=f"{target}_flow", target=target, source="customer_events",
        keys=["customer_id"], sequence_by=F.col("sequence"),
        apply_as_deletes=F.expr("operation = 'DELETE'"),
        except_column_list=["operation", "sequence"], stored_as_scd_type=scd_type,
    )
