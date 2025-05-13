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

    +--------------------+---------------------+-------------+-----------+----------+-----------+                                                  
    |tpep_pickup_datetime|tpep_dropoff_datetime|trip_distance|fare_amount|pickup_zip|dropoff_zip|
    +--------------------+---------------------+-------------+-----------+----------+-----------+
    | 2016-02-13 21:47:53|  2016-02-13 21:57:15|          1.4|        8.0|     10103|      10110|
    | 2016-02-13 18:29:09|  2016-02-13 18:37:23|         1.31|        7.5|     10023|      10023|
    | 2016-02-06 19:40:58|  2016-02-06 19:52:32|          1.8|        9.5|     10001|      10018|
    | 2016-02-12 19:06:43|  2016-02-12 19:20:54|          2.3|       11.5|     10044|      10111|
    | 2016-02-23 10:27:56|  2016-02-23 10:58:33|          2.6|       18.5|     10199|      10022|
    +--------------------+---------------------+-------------+-----------+----------+-----------+
    only showing top 5 rows

    ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance', 'fare_amount', 'pickup_zip', 'dropoff_zip']