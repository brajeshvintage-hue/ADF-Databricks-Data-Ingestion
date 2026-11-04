# Databricks notebook source
# Run manually in Azure Databricks. Change the catalog widget before running.
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "de_pro_lab")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
import re
for value in (catalog, schema):
    assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value), "Use simple identifiers"
ns = f"{catalog}.{schema}"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {ns}")
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {ns}.lab_files")
root = f"/Volumes/{catalog}/{schema}/lab_files"
dbutils.fs.mkdirs(f"{root}/orders")
print({"namespace": ns, "root": root, "spark": spark.version})

# COMMAND ----------
# Only append immutable source files. Rerunning is safe: never overwrite a seen file.
import json
rows = [
    dict(order_id=1, customer_id=10, customer_name=" Alice ", amount=25.0,
         event_time="2026-10-01T10:00:00Z", region="CA"),
    dict(order_id=2, customer_id=20, customer_name="bob", amount=40.0,
         event_time="2026-10-01T10:01:00Z", region="US"),
    dict(order_id=3, customer_id=10, customer_name=None, amount=-5.0,
         event_time="2026-10-01T10:02:00Z", region="CA"),
    dict(order_id=4, customer_id=30, customer_name="Cara", amount=10.0,
         event_time="2026-10-01T10:03:00Z", region="CA"),
]
path = f"{root}/orders/batch_001.json"
if not any(f.name == "batch_001.json" for f in dbutils.fs.ls(f"{root}/orders")):
    dbutils.fs.put(path, "\n".join(json.dumps(r) for r in rows), overwrite=False)

# COMMAND ----------
# The CDC source is separate from the order stream. Do not overwrite after consumers start.
if not spark.catalog.tableExists(f"{ns}.customer_cdc"):
    spark.createDataFrame(
        [(10, "Alice", "CA", 1, "INSERT"), (20, "Bob", "US", 1, "INSERT"),
         (10, "Alice", "US", 3, "UPDATE"), (10, "Alice", "CA", 2, "UPDATE"),
         (20, "Bob", "US", 4, "DELETE")],
        "customer_id long, name string, region string, sequence long, operation string",
    ).write.format("delta").mode("errorifexists").saveAsTable(f"{ns}.customer_cdc")
print("Expected SCD1: customer 10 region US; customer 20 absent.")
