===========================
Data Preprocessing Pipeline
===========================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-04

.. admonition:: Objectives
    :class: important

    This document explains the different steps performed by the `DataProcessor` class to prepare hotel reservation data for machine learning. Each step contributes to cleaning, transforming, and organizing the data in a way that makes it suitable for training and evaluating models.

Overview
========

The preprocessing workflow starts with reading raw CSV data into a table and ends with storing clean, enriched datasets in a Databricks catalog. The main steps are:

1. Removing unused columns
2. Creating new features
3. Encoding categories and target variable
4. Transforming numerical values
5. Dropping redundant columns
6. Splitting the dataset into training and test subsets
7. Saving processed datasets to the catalog
8. Enabling Change Data Feed (optional)

Step-by-Step Breakdown
======================

1. Drop Unused Columns
----------------------

The first step removes irrelevant columns from the dataset. In this case, the column named ``Booking_ID`` is dropped since it uniquely identifies each row but does not help the model learn patterns.

2. Create New Features
----------------------

This step generates new, meaningful columns from existing ones:

- ``total_nights``: Adds up weeknights and weekend nights to get the total duration of the stay.
- ``has_children``: A binary column indicating whether children were included in the booking.
- ``arrival_date_complete``: Combines year, month, and day columns into a single, standard date format for easier time-based analysis.

3. Encode Target and Categorical Columns
----------------------------------------

- The target variable ``booking_status`` is converted into numerical values:
  - ``Canceled`` → 1
  - ``Not_Canceled`` → 0

- Other descriptive columns like ``type_of_meal_plan``, ``room_type_reserved``, and ``market_segment_type`` are converted using one-hot encoding, a method that replaces text labels with binary columns (1s and 0s).

- To avoid issues when storing data in Databricks tables, the column names are cleaned to remove spaces and special characters.

4. Transform and Normalize Numerical Columns
--------------------------------------------

Some numeric columns are adjusted to improve model performance:

- ``lead_time`` and ``avg_price_per_room`` are transformed using a logarithmic scale to reduce the impact of extreme values.
- All selected numerical columns are then standardized (scaled to have similar ranges) using a method called z-score normalization.

5. Drop Redundant Columns
-------------------------

Once new features are created, the original columns for ``arrival_year``, ``arrival_month``, and ``arrival_date`` are removed to avoid redundancy.

6. Split Into Training and Test Sets
------------------------------------

The processed dataset is divided into two parts:

- **Training Set (80%)**: Used to train the model.
- **Test Set (20%)**: Used to evaluate how well the model performs on unseen data.

This ensures the model does not "memorize" the training data but learns to generalize.

7. Save to Databricks Catalog
-----------------------------

The training and test sets are saved as managed Delta tables in Databricks. A timestamp column ``update_timestamp_utc`` is also added to each table, capturing the time of data insertion.

8. Enable Change Data Feed (Optional)
-------------------------------------

Finally, the pipeline can activate a feature in Delta Lake called **Change Data Feed**, which allows tracking changes to the data over time. This is useful for auditing or incremental model training.

Conclusion
==========

This structured preprocessing approach ensures that the raw data is cleaned, enriched, and well-formatted before machine learning is applied. Each step adds value and prepares the data for accurate, reliable predictions.
