"""Wheel entry point usable locally (--demo) or as a Databricks wheel task."""
import argparse
import re
from retail_de.cleaning import normalize_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--catalog")
    parser.add_argument("--schema", default="de_pro_lab")
    args = parser.parse_args()
    if args.demo:
        print([normalize_name(v) for v in ["  Alice  Smith ", "bob", None, "   "]])
        return
    if not args.catalog:
        parser.error("--catalog is required unless --demo is set")
    for name in (args.catalog, args.schema):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            parser.error("Use simple catalog/schema identifiers for this lab")
    from pyspark.sql import SparkSession
    from retail_de.transforms import add_normalized_name

    spark = SparkSession.builder.getOrCreate()
    source = spark.createDataFrame(
        [(1, "  Alice  Smith "), (2, "bob"), (3, None), (4, "   ")],
        "customer_id long, customer_name string",
    )
    result = source.transform(add_normalized_name)
    # Schema must already exist: notebook 00 creates it.
    table = f"{args.catalog}.{args.schema}.customer_names"
    result.write.format("delta").mode("overwrite").saveAsTable(table)
    assert spark.table(table).count() == 4
    print(f"Wrote 4 synthetic rows to {table}")


if __name__ == "__main__":
    main()
