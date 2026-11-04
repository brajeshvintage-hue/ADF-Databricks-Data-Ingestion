# Databricks notebook source
# Capture metadata without printing secrets or the complete process environment.
import sys
import importlib.metadata as metadata
print(sys.version)
for package in ("retail_de", "humanize", "pandas", "pyarrow", "pyspark"):
    try:
        print(package, metadata.version(package))
    except metadata.PackageNotFoundError:
        print(package, "not installed as a distribution")

# COMMAND ----------
# MAGIC %md
# MAGIC Run the following in separate cells during Day 3:
# MAGIC
# MAGIC `%pip install humanize==4.11.0`
# MAGIC
# MAGIC `dbutils.library.restartPython()`
# MAGIC
# MAGIC `import humanize; print(humanize.intcomma(1234567))`
# MAGIC
# MAGIC Then install your own wheel from a real Workspace or Volume path, for example:
# MAGIC `%pip install /Volumes/main/de_pro_lab/lab_files/packages/retail_de-0.1.0-py3-none-any.whl`
# MAGIC
# MAGIC Build an sdist locally with `python -m build --sdist`, upload the resulting `.tar.gz`,
# MAGIC then install its real path with `%pip install <path>`. An sdist may need build
# MAGIC tools/network access; a wheel is already built. Use Environment dependencies
# MAGIC for reproducible serverless tasks; don't assume a notebook install configures a job.

# COMMAND ----------
# After the install/restart, execute code on workers, not just an import on driver.
from pyspark.sql import functions as F
@F.udf("string")
def worker_dependency_probe(value):
    import humanize
    return humanize.intcomma(value)
display(spark.range(3).select(worker_dependency_probe("id").alias("formatted")))
