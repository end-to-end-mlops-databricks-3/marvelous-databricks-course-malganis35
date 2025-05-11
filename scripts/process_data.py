# %% Databricks notebook source


import yaml
from loguru import logger
from marvelous.timer import Timer
from pyspark.sql import SparkSession

from mlops_course.feature.data_processor import DataProcessor
from mlops_course.utils.config import ProjectConfig

# COMMAND ----------

config_path = "../project_config.yml"

config = ProjectConfig.from_yaml(config_path=config_path, env="dev")

# TO DO: Issue with permissions
# setup_logging(log_file=f"/Volumes/{config.catalog_name}/{config.schema_name}/logs/caotrido-1.log")

logger.info("Configuration loaded:")
logger.info(yaml.dump(config, default_flow_style=False))

# COMMAND ----------

# Load the hotel reservations dataset
spark = SparkSession.builder.getOrCreate()

df = spark.read.csv(
    f"/Volumes/{config.catalog_name}/{config.schema_name}/data/{config.raw_data_file}", header=True, inferSchema=True
).toPandas()

df.head(5)

# COMMAND ----------

# Preprocess the data
with Timer() as preprocess_timer:
    data_processor = DataProcessor(df, config, spark)
    data_processor.preprocess()

logger.info(f"Data preprocessing: {preprocess_timer}")

# Split the data
X_train, X_test = data_processor.split_data()
logger.info("Training set shape: %s", X_train.shape)
logger.info("Test set shape: %s", X_test.shape)

# Save to catalog
logger.info("Saving data to catalog")
data_processor.save_to_catalog(X_train, X_test)

# COMMAND ----------
