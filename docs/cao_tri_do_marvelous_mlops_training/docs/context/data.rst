=================
Data Dictionary
=================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-04

.. admonition:: Objectives
    :class: important

    This article is intended to provide a comprehensive overview of the data used in the project.

source:

Data Dictionary
---------------

The file contains the different attributes of customers' reservation details. The detailed data dictionary is given below.

.. list-table:: Description des colonnes du dataset
   :widths: 25 75
   :header-rows: 1

   * - Colonne
     - Description
   * - **Booking_ID**
     - Unique identifier of each booking
   * - **no_of_adults**
     - Number of adults
   * - **no_of_children**
     - Number of Children
   * - **no_of_weekend_nights**
     - Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel
   * - **no_of_week_nights**
     - Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel
   * - **type_of_meal_plan**
     - Type of meal plan booked by the customer
   * - **required_car_parking_space**
     - Does the customer require a car parking space? (0 - No, 1 - Yes)
   * - **room_type_reserved**
     - Type of room reserved by the customer. The values are ciphered (encoded) by INN Hotels.
   * - **lead_time**
     - Number of days between the date of booking and the arrival date
   * - **arrival_year**
     - Year of arrival date
   * - **arrival_month**
     - Month of arrival date
   * - **arrival_date**
     - Date of the month
   * - **market_segment_type**
     - Market segment designation
   * - **repeated_guest**
     - Is the customer a repeated guest? (0 - No, 1 - Yes)
   * - **no_of_previous_cancellations**
     - Number of previous bookings that were canceled by the customer prior to the current booking
   * - **no_of_previous_bookings_not_canceled**
     - Number of previous bookings not canceled by the customer prior to the current booking
   * - **avg_price_per_room**
     - Average price per day of the reservation; prices of the rooms are dynamic. (in euros)
   * - **no_of_special_requests**
     - Total number of special requests made by the customer (e.g. high floor, view from the room, etc)
   * - **booking_status**
     - Flag indicating if the booking was canceled or not

Accessing the Data
------------------

The dataset is available on Kaggle. You can download it from the following link: https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset/data

We also provide the dataset within the Unity Catalog of our databricks (https://dbc-c2e8445d-159d.cloud.databricks.com/).
This is a managed data lake that allows us to store and manage our data in a secure and scalable way.
The raw dataset is stored in the following location:

.. code-block::

   /Volumes/{config.catalog_name}/{config.schema_name}/data/{config.raw_data_file}

The training and testing datasets are stored in the following locations:

.. code-block::

   /Volumes/{config.catalog_name}.{config.schema_name}.{config.train_table}
   /Volumes/{config.catalog_name}/{config.schema_name}.{config.test_table}

where:

- **catalog_name** : mlops_dev
- **schema_name** : caotrido
- **raw_data_file** : hotel_reservations.csv
- **train_table** : hotel_reservations_train_set
- **test_table** : hotel_reservations_test_set
