"""Data preprocessing module."""

import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, to_utc_timestamp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from datetime import datetime

from mlops_course.utils.config import ProjectConfig

class DataProcessor:
    """A class for preprocessing and managing DataFrame operations.

    This class handles data preprocessing, splitting, and saving to Databricks tables.
    """
    
    def __init__(self, pandas_df: pd.DataFrame, config: ProjectConfig, spark: SparkSession) -> None:
        self.df = pandas_df  # Store the DataFrame as self.df
        self.config = config  # Store the configuration
        self.spark = spark

    def preprocess(self) -> pd.DataFrame:
        """Apply full preprocessing pipeline to the dataset."""
        self._drop_unused_columns()
        self._create_features()
        self._encode_target_and_categories()
        self._log_and_scale_numeric()
        self._cleanup_columns()
        
        return self.df    
    
    def _drop_unused_columns(self):
        self.df.drop(columns=["Booking_ID"], errors='ignore', inplace=True)

    def _create_features(self):
        self.df["total_nights"] = self.df["no_of_weekend_nights"] + self.df["no_of_week_nights"]
        self.df["has_children"] = self.df["no_of_children"].apply(lambda x: 1 if x > 0 else 0)
        self.df["arrival_date_complete"] = pd.to_datetime(
            dict(year=self.df.arrival_year, month=self.df.arrival_month, day=self.df.arrival_date),
            errors='coerce'
        )

    def _encode_target_and_categories(self):
        if "booking_status" in self.df.columns:
            self.df["booking_status"] = self.df["booking_status"].map({"Canceled": 1, "Not_Canceled": 0})
        categorical_cols = ["type_of_meal_plan", "room_type_reserved", "market_segment_type"]
        self.df = pd.get_dummies(self.df, columns=[col for col in categorical_cols if col in self.df.columns], drop_first=True)

        # clean column names to remove spaces
        
        self.df.columns = (
        self.df.columns
        .str.replace(" ", "_")   # Remplacer les espaces par des underscores
        .str.replace(r"[;{}()\n\t=]", "", regex=True)  # Supprimer les caractères invalides restants
        )
        
    def _log_and_scale_numeric(self):
        for col in ["lead_time", "avg_price_per_room"]:
            if col in self.df.columns:
                self.df[col] = np.log1p(self.df[col])
        numerical_cols = [col for col in ["lead_time", "avg_price_per_room", "total_nights", "no_of_special_requests"] if col in self.df.columns]
        scaler = StandardScaler()
        self.df[numerical_cols] = scaler.fit_transform(self.df[numerical_cols])

    def _cleanup_columns(self):
        self.df.drop(columns=["arrival_year", "arrival_month", "arrival_date"], errors='ignore', inplace=True)

    # def preprocess(self) -> None:
    #     """Preprocess the DataFrame stored in self.df.

    #     This method handles missing values, converts data types, and performs feature engineering.
    #     """
    
    #     # Create a new column 'arrival_date_str' in the format YYYY-MM-DD
    #     self.df['arrival_date_str'] = (
    #     self.df['arrival_year'].astype(str) + '-' +
    #     self.df['arrival_month'].astype(str).str.zfill(2) + '-' +
    #     self.df['arrival_date'].astype(str).str.zfill(2)
    #     )

    #     # Function to correctly parse the date and handle exceptions
    #     def safe_parse_date(row):
    #         year = int(row['arrival_year'])
    #         month = int(row['arrival_month'])
    #         day = int(row['arrival_date'])
            
    #         try:
    #             return datetime(year, month, day)
    #         except ValueError as e:
    #             # Cas particulier : 29 février d'une année non bissextile
    #             if month == 2 and day == 29:
    #                 try:
    #                     return datetime(year, month, 28)
    #                 except:
    #                     return pd.NaT
    #             else:
    #                 return pd.NaT

    #     # Apply the function
    #     self.df['arrival_datetime'] = self.df.apply(safe_parse_date, axis=1)
    
    def split_data(self, test_size: float = 0.2, random_state: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Split the DataFrame (self.df) into training and test sets.

        :param test_size: The proportion of the dataset to include in the test split.
        :param random_state: Controls the shuffling applied to the data before applying the split.
        :return: A tuple containing the training and test DataFrames.
        """
        train_set, test_set = train_test_split(self.df, test_size=test_size, random_state=random_state)
        return train_set, test_set

    def save_to_catalog(self, train_set: pd.DataFrame, test_set: pd.DataFrame) -> None:
        """Save the train and test sets into Databricks tables.

        :param train_set: The training DataFrame to be saved.
        :param test_set: The test DataFrame to be saved.
        """
        train_set_with_timestamp = self.spark.createDataFrame(train_set).withColumn(
            "update_timestamp_utc", to_utc_timestamp(current_timestamp(), "UTC")
        )

        test_set_with_timestamp = self.spark.createDataFrame(test_set).withColumn(
            "update_timestamp_utc", to_utc_timestamp(current_timestamp(), "UTC")
        )

        train_set_with_timestamp.write.mode("overwrite").saveAsTable(
            f"{self.config.catalog_name}.{self.config.schema_name}.{self.config.train_table}"
        )

        test_set_with_timestamp.write.mode("overwrite").saveAsTable(
            f"{self.config.catalog_name}.{self.config.schema_name}.{self.config.test_table}"
        )
