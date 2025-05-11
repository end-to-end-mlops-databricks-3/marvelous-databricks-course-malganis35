import numpy as np
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from mlops_course.feature.data_processor import DataProcessor
from mlops_course.utils.config import ProjectConfig
from unittest.mock import MagicMock

@pytest.fixture
def sample_config():
    return ProjectConfig(
        num_features=[],
        cat_features=[],
        target="booking_status",
        catalog_name="catalog",
        schema_name="schema",
        parameters={},
        raw_data_file="dummy.csv",
        train_table="train_table",
        test_table="test_table"
    )


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
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
        "no_of_special_requests": [1, 2]
    })


@pytest.fixture
def processor(sample_dataframe, sample_config):
    spark_mock = MagicMock()
    return DataProcessor(sample_dataframe.copy(), sample_config, spark_mock)


def test_preprocess_pipeline_runs(processor):
    df_processed = processor.preprocess()
    assert "total_nights" in df_processed.columns
    assert "has_children" in df_processed.columns
    assert "arrival_date_complete" in df_processed.columns
    assert "booking_status" in df_processed.columns
    assert "type_of_meal_plan_Meal_Plan_2" in df_processed.columns


def test_split_data_shapes(processor):
    processor.preprocess()
    train, test = processor.split_data(test_size=0.5, random_state=1)
    assert len(train) + len(test) == len(processor.df)
    assert not train.equals(test)


@patch("mlops_course.feature.data_processor.to_utc_timestamp")
@patch("mlops_course.feature.data_processor.current_timestamp")
def test_save_to_catalog_calls_spark_write(mock_current_ts, mock_to_utc_ts, processor):
    # Mock les fonctions Spark
    mock_current_ts.return_value = MagicMock(name="current_timestamp")
    mock_to_utc_ts.return_value = MagicMock(name="utc_timestamp")

    # Mock la méthode Spark saveAsTable
    processor.spark.createDataFrame.return_value.withColumn.return_value.write.mode.return_value.saveAsTable = MagicMock()

    df_train, df_test = processor.split_data()
    processor.save_to_catalog(df_train, df_test)

    # Vérifie les appels à saveAsTable
    calls = processor.spark.createDataFrame.return_value.withColumn.return_value.write.mode.return_value.saveAsTable.call_args_list
    assert len(calls) == 2

def test_preprocess_without_booking_status(processor):
    processor.df.drop(columns=["booking_status"], inplace=True)
    df_processed = processor.preprocess()
    assert "booking_status" not in df_processed.columns

def test_log_and_scale_with_missing_columns(processor):
    # Supprime volontairement certaines colonnes avant le traitement
    processor.df.drop(columns=["lead_time", "avg_price_per_room"], inplace=True)
    
    # Appelle uniquement la fonction concernée
    processor._log_and_scale_numeric()
    
    # Vérifie que les autres colonnes attendues ont bien été transformées (s'il en reste)
    for col in ["total_nights", "no_of_special_requests"]:
        if col in processor.df.columns:
            assert np.allclose(processor.df[col].mean(), 0, atol=1e-6)
