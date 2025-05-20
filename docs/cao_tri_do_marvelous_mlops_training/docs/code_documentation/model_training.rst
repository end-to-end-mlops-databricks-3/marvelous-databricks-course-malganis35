=============================
Model Training and Tracking
=============================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-05

.. admonition:: Objectives
    :class: important

    This document explains how the `BasicModel` class loads data, prepares features, trains a model, and logs it using MLflow. It provides a structured framework to manage end-to-end model lifecycle tracking and registration in Databricks.

Overview
========

The training workflow includes:

1. Loading datasets from Delta tables in the catalog
2. Defining a scikit-learn pipeline
3. Training a Logistic Regression model
4. Logging the model, parameters, and metrics with MLflow
5. Registering the trained model in Unity Catalog
6. Retrieving run metadata
7. Loading and using the latest registered model for prediction

Step-by-Step Breakdown
======================

1. Load Data from Delta Tables
------------------------------

The method ``load_data()`` retrieves training and test datasets from the Databricks catalog using Spark SQL. It separates features and target columns for both sets and stores them as instance attributes:

- ``X_train`` and ``y_train`` from the training table
- ``X_test`` and ``y_test`` from the test table

This prepares the data for preprocessing and model training.

2. Prepare Features with Pipeline
----------------------------------

The ``prepare_features()`` method builds a scikit-learn pipeline consisting of:

- ``ColumnTransformer`` to one-hot encode categorical variables and passthrough numerical ones
- ``LogisticRegression`` model using hyperparameters from the config

This preprocessing pipeline ensures the model receives clean, vectorized inputs.

3. Train the Model
-------------------

The ``train()`` method calls `.fit()` on the pipeline using training data. The full pipeline—including transformations and classifier—is stored as ``self.pipeline``.

4. Log Model and Metrics with MLflow
------------------------------------

The ``log_model()`` method performs the following:

- Starts an MLflow run under the specified experiment
- Logs classification metrics (accuracy, precision, recall, F1)
- Logs model hyperparameters
- Captures model input/output signature using ``infer_signature()``
- Logs the Spark training dataset as a reference
- Logs the trained model with ``mlflow.sklearn.log_model()``

This allows full reproducibility of the model training process.

5. Register Model in Unity Catalog
-----------------------------------

The ``register_model()`` method:

- Registers the model version using MLflow
- Assigns an alias (``latest-model``) for easier retrieval
- Tags the model version with metadata

This step is key for production deployment and governance in a Unity Catalog environment.

6. Retrieve Run Dataset
------------------------

The ``retrieve_current_run_dataset()`` method:

- Queries MLflow to fetch the dataset used for training in a specific run
- Returns the source as a loaded dataset object

Useful for audit, debugging, or retraining.

7. Retrieve Run Metadata
-------------------------

The ``retrieve_current_run_metadata()`` method:

- Returns dictionaries of logged metrics and parameters for the current run
- Useful for programmatic validation and reporting

8. Load Latest Model and Predict
---------------------------------

The ``load_latest_model_and_predict()`` method:

- Loads the latest registered model (via alias ``latest-model``)
- Runs predictions on a given DataFrame ``input_data``

This step is used for model inference in batch or real-time prediction contexts.

Conclusion
==========

The `BasicModel` class provides a structured and reproducible machine learning workflow integrated with Databricks and MLflow. It covers all critical phases from preprocessing and training to logging and deployment.

