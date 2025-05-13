# %% Databricks notebook source

import yaml
from loguru import logger
from pyspark.sql import SparkSession

from mlops_course.feature.data_processor import DataProcessor
from mlops_course.utils.config import ProjectConfig

# COMMAND ----------

logger.info("Load configuration from YAML file")
config_path = "../project_config.yml"

config = ProjectConfig.from_yaml(config_path=config_path, env="dev")

logger.info("Configuration loaded:")
logger.info(yaml.dump(config, default_flow_style=False))

# COMMAND ----------

logger.info("Intialize Spark session")
spark = SparkSession.builder.getOrCreate()

logger.info("Load the hotel reservations dataset from the catalog")
df = spark.read.csv(
    f"/Volumes/{config.catalog_name}/{config.schema_name}/data/{config.raw_data_file}", header=True, inferSchema=True
).toPandas()
logger.info(f"Dataset shape: {df.shape}")

# COMMAND ----------

logger.info("Preprocess the data")
data_processor = DataProcessor(df, config, spark)
data_processor.preprocess()

logger.info("Split the data into train and test sets")
X_train, X_test = data_processor.split_data()

logger.info("Saving data to catalog")
data_processor.save_to_catalog(X_train, X_test)

# COMMAND ----------
