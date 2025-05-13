from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from mlops_course.feature.data_processor import DataProcessor
from mlops_course.utils.config import ProjectConfig


@pytest.fixture
def sample_config():
    """Provide a minimal valid ProjectConfig instance for testing.

    :return: A ProjectConfig instance with required fields.
    """
    return ProjectConfig(
        num_features=[],
        cat_features=[],
        target="booking_status",
        catalog_name="catalog",
        schema_name="schema",
        parameters={},
        raw_data_file="dummy.csv",
        train_table="train_table",
        test_table="test_table",
    )


@pytest.fixture
def mock_config():
    """Provide a mock ProjectConfig with predefined values.

    :return: A mock ProjectConfig instance for SQL-related tests.
    """
    return ProjectConfig(
        env="dev",
        catalog_name="my_catalog",
        schema_name="my_schema",
        train_table="train_table",
        test_table="test_table",
        num_features=[],
        cat_features=[],
        target="booking_status",
        parameters={},
        raw_data_file="dummy.csv"
    )


@pytest.fixture
def sample_dataframe():
    """Provide a sample pandas DataFrame mimicking hotel reservation data.

    :return: A mock DataFrame used for preprocessing and testing.
    """
    return pd.DataFrame(
        {
            "Booking_ID": ["ID1", "ID2"],
            "no_of_weekend_nights": [1, 2],
            "no_of_week_nights": [2, 3],
            "no_of_children": [0, 1],
            "arrival_year": [2023, 2023],
            "arrival_month": [5, 5],
            "arrival_date": [10, 11],
            "booking_status": ["Canceled", "Not_Canceled"],
            "type_of_meal_plan": ["Meal Plan 1", "Meal Plan 2"],
            "room_type_reserved": ["Room A", "Room B"],
            "market_segment_type": ["Online", "Offline"],
            "lead_time": [10, 20],
            "avg_price_per_room": [100.0, 150.0],
            "no_of_special_requests": [1, 2],
        }
    )


@pytest.fixture
def processor(sample_dataframe, sample_config):
    """Create a DataProcessor instance with mocked Spark session.

    :param sample_dataframe: The sample DataFrame fixture.
    :param sample_config: The ProjectConfig fixture.
    :return: A DataProcessor instance.
    """
    spark_mock = MagicMock()
    return DataProcessor(sample_dataframe.copy(), sample_config, spark_mock)


def test_preprocess_pipeline_runs(processor):
    """Test that the preprocessing pipeline runs and creates expected columns.

    :param processor: A configured DataProcessor instance.
    :return: Asserts new features are correctly added to the DataFrame.
    """
    df_processed = processor.preprocess()
    assert "total_nights" in df_processed.columns
    assert "has_children" in df_processed.columns
    assert "arrival_date_complete" in df_processed.columns
    assert "booking_status" in df_processed.columns
    assert "type_of_meal_plan_Meal_Plan_2" in df_processed.columns


def test_split_data_shapes(processor):
    """Test that the split_data method produces disjoint, complete splits.

    :param processor: A configured DataProcessor instance.
    :return: Asserts train + test = full data, and train != test.
    """
    processor.preprocess()
    train, test = processor.split_data(test_size=0.5, random_state=1)
    assert len(train) + len(test) == len(processor.df)
    assert not train.equals(test)


@patch("mlops_course.feature.data_processor.to_utc_timestamp")
@patch("mlops_course.feature.data_processor.current_timestamp")
def test_save_to_catalog_calls_spark_write(mock_current_ts, mock_to_utc_ts, processor):
    """Test that save_to_catalog calls Spark's saveAsTable twice.

    :param mock_current_ts: Mocked current_timestamp function.
    :param mock_to_utc_ts: Mocked to_utc_timestamp function.
    :param processor: A DataProcessor instance with mock Spark.
    :return: Asserts saveAsTable is called for both train and test sets.
    """
    mock_current_ts.return_value = MagicMock(name="current_timestamp")
    mock_to_utc_ts.return_value = MagicMock(name="utc_timestamp")

    # Mock Spark's saveAsTable chain
    processor.spark.createDataFrame.return_value.withColumn.return_value.write.mode.return_value.saveAsTable = (
        MagicMock()
    )

    df_train, df_test = processor.split_data()
    processor.save_to_catalog(df_train, df_test)

    # Check that saveAsTable was called twice
    calls = processor.spark.createDataFrame.return_value.withColumn.return_value.write.mode.return_value.saveAsTable.call_args_list
    assert len(calls) == 2


def test_preprocess_without_booking_status(processor):
    """Test that preprocessing works even if the target column is missing.

    :param processor: A configured DataProcessor instance.
    :return: Asserts that missing target column does not raise error.
    """
    processor.df.drop(columns=["booking_status"], inplace=True)
    df_processed = processor.preprocess()
    assert "booking_status" not in df_processed.columns


def test_log_and_scale_with_missing_columns(processor):
    """Test _log_and_scale_numeric handles missing numeric columns gracefully.

    :param processor: A configured DataProcessor instance.
    :return: Asserts remaining numeric columns are scaled if present.
    """
    # Intentionally drop some numeric columns
    processor.df.drop(columns=["lead_time", "avg_price_per_room"], inplace=True)

    # Call the specific private method
    processor._log_and_scale_numeric()

    # Check that scaling was applied to remaining columns
    for col in ["total_nights", "no_of_special_requests"]:
        if col in processor.df.columns:
            assert np.allclose(processor.df[col].mean(), 0, atol=1e-6)


def test_enable_change_data_feed_calls_spark_sql(mock_config):
    """Test that enable_change_data_feed issues correct ALTER TABLE SQL.

    :param mock_config: A mock ProjectConfig with catalog/schema/table info.
    :return: Asserts Spark SQL is called twice with expected table statements.
    """
    mock_spark = MagicMock()
    processor = DataProcessor(pandas_df=None, config=mock_config, spark=mock_spark)

    processor.enable_change_data_feed()

    expected_train_sql = (
        f"ALTER TABLE {mock_config.catalog_name}.{mock_config.schema_name}.{mock_config.train_table} "
        "SET TBLPROPERTIES (delta.enableChangeDataFeed = true);"
    )
    expected_test_sql = (
        f"ALTER TABLE {mock_config.catalog_name}.{mock_config.schema_name}.{mock_config.test_table} "
        "SET TBLPROPERTIES (delta.enableChangeDataFeed = true);"
    )

    mock_spark.sql.assert_any_call(expected_train_sql)
    mock_spark.sql.assert_any_call(expected_test_sql)
    assert mock_spark.sql.call_count == 2
