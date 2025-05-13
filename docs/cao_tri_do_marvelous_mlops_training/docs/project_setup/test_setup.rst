=====================
Test your local setup
=====================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-04

.. admonition:: Objectives
    :class: important

    This article is intended to test your local setup and make sure everything is working properly.

We provide a test script to check if your local setup is working properly. This script will run a simple test to check if the data is loaded correctly (demo.py).

.. code-block:: python
    
    # %% Databricks notebook source
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()

    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)

    # COMMAND ----------

    print(list(df.columns))

Run this script on the Databricks cluster using VS Code. Click on the "Run" button in the top right corner of the editor and select **"Upload and Run on Databricks"**. This will execute the code in the Databricks notebook and display the results in the output panel.

You should see the following output:

.. code-block:: bash

   