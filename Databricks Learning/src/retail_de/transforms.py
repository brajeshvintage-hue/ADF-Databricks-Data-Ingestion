"""Spark imports stay here, away from pure Python functions."""


def add_normalized_name(df):
    from pyspark.sql import functions as F

    value = F.trim(F.regexp_replace(F.col("customer_name"), r"\s+", " "))
    return df.withColumn(
        "normalized_name", F.when(F.length(value) > 0, F.upper(value))
    )


def name_udfs():
    import pandas as pd
    from pyspark.sql import functions as F
    from retail_de.cleaning import normalize_name

    scalar = F.udf(normalize_name, "string", useArrow=False)

    @F.pandas_udf("string")
    def vectorized(names: pd.Series) -> pd.Series:
        # Vectorized pandas string operations, not Series.apply(Python function).
        out = names.astype("string").str.replace(r"\s+", " ", regex=True).str.strip().str.upper()
        return out.mask(out.eq(""))

    return scalar, vectorized
