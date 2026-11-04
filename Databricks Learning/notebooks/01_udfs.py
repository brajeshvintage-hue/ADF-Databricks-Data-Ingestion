# Databricks notebook source
# Install the built retail_de wheel through the notebook Environment pane or %pip,
# then restart Python if needed. pandas/Arrow must be compatible with the runtime.
from retail_de.transforms import add_normalized_name, name_udfs
from pyspark.sql import functions as F
from pyspark.testing.utils import assertDataFrameEqual, assertSchemaEqual
df = spark.createDataFrame(
    [(1, "  Alice  Smith "), (2, "bob"), (3, None), (4, " \t ")],
    "id long, customer_name string",
)
python_name, pandas_name = name_udfs()
native = df.transform(add_normalized_name).select("id", "normalized_name")
scalar = df.select("id", python_name("customer_name").alias("normalized_name"))
vector = df.select("id", pandas_name("customer_name").alias("normalized_name"))
expected = spark.createDataFrame(
    [(1, "ALICE SMITH"), (2, "BOB"), (3, None), (4, None)],
    "id long, normalized_name string",
)
for actual in (native, scalar, vector):
    assertDataFrameEqual(actual.orderBy("id"), expected.orderBy("id"), checkRowOrder=True)
    assertSchemaEqual(actual.schema, expected.schema)
    actual.explain("formatted")
display(native)

# COMMAND ----------
# SQL registration is session-scoped; it does not create a governed UC function.
from retail_de.cleaning import normalize_name
spark.udf.register("normalize_name_session", normalize_name, "string")
df.createOrReplaceTempView("names_input")
display(spark.sql("SELECT id, normalize_name_session(customer_name) AS name FROM names_input"))

# COMMAND ----------
# Bounded benchmark: consume the UDF result so Spark cannot prune it as with count().
# Increase only after checking cost. Repeated trials are observations, not universal rankings.
from time import perf_counter
large = spark.range(100_000).selectExpr("id", "'  Alice  Smith ' AS customer_name")
implementations = {
    "native": large.transform(add_normalized_name).select("normalized_name"),
    "python": large.select(python_name("customer_name").alias("normalized_name")),
    "pandas": large.select(pandas_name("customer_name").alias("normalized_name")),
}
for trial in range(3):
    for label, frame in implementations.items():
        started = perf_counter()
        checksum = frame.select(F.sum(F.length("normalized_name"))).first()[0]
        assert checksum == 1_100_000
        print(trial, label, round(perf_counter() - started, 3), checksum)
