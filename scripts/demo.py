"""Demo script to showcase hotel_resa package functionality."""

# %% Databricks notebook source
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.read.table("samples.nyctaxi.trips")
df.show(5)

# COMMAND ----------

print(list(df.columns))

# COMMAND ----------
