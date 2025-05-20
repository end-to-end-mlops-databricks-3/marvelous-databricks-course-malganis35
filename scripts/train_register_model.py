"""Main entry point for train a model and register to MLFlow on hotel reservation data."""

# Databricks notebook source

import os

import mlflow
from dotenv import load_dotenv
from loguru import logger
from marvelous.common import is_databricks
from pyspark.sql import SparkSession

from mlops_course.model.basic_model import BasicModel
from mlops_course.utils.config import ProjectConfig, Tags

# COMMAND ----------
if not is_databricks():
    load_dotenv()
    profile = os.environ["PROFILE"]
    mlflow.set_tracking_uri(f"databricks://{profile}")
    mlflow.set_registry_uri(f"databricks-uc://{profile}")

# COMMAND ----------
config = ProjectConfig.from_yaml(config_path="../project_config.yml", env="dev")
spark = SparkSession.builder.getOrCreate()
tags_dict = {"git_sha": "abcd12345", "branch": "week2", "job_run_id": ""}
tags = Tags(**tags_dict)

# COMMAND ----------
# Initialize model
# Initialize model with the config path
basic_model = BasicModel(config=config, tags=tags, spark=spark)
logger.info("Model initialized.")

# COMMAND ----------
# Load data and prepare features
basic_model.load_data()
basic_model.prepare_features()
logger.info("Loaded data, prepared features.")

# COMMAND ----------
# Train + log the model (runs everything including MLflow logging)
basic_model.train()
basic_model.log_model()
logger.info("Model training completed.")

# COMMAND ----------
basic_model.register_model()
logger.info("Registered model")

# COMMAND ----------
