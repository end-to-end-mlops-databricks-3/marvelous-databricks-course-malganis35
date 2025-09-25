"""Unit tests for the BasicModel class using logistic regression."""

from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from mlops_course.model.basic_model import BasicModel
from mlops_course.utils.config import ProjectConfig, Tags


@pytest.fixture
def sample_config() -> ProjectConfig:
    """Fixture providing a complete ProjectConfig for initializing BasicModel."""
    return ProjectConfig(
        catalog_name="catalog",
        schema_name="schema",
        train_table="train",
        test_table="test",
        raw_data_file="data.csv",
        target="target",
        num_features=["num1", "num2"],
        cat_features=["cat1"],
        parameters={"C": 1.0},
        experiment_name_basic="/exp/basic",
        experiment_name_custom="/exp/custom",
        model_name="model",
        model_type="logistic-regression",
    )


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture providing a simple dataset with numeric and categorical features."""
    return pd.DataFrame({"num1": [1.0, 2.0], "num2": [2.0, 3.0], "cat1": ["A", "B"], "target": [0, 1]})


@pytest.fixture
def basic_model(sample_config: ProjectConfig) -> BasicModel:
    """Fixture initializing a BasicModel with required Tags and mocked SparkSession."""
    spark: MagicMock = MagicMock()
    tags = Tags(git_sha="abc123", branch="main", job_run_id="run-001")
    return BasicModel(sample_config, tags, spark)


def test_prepare_features_creates_pipeline(basic_model: BasicModel, sample_data: pd.DataFrame) -> None:
    """Test that prepare_features creates a valid scikit-learn pipeline."""
    basic_model.X_train = sample_data.drop(columns=["target"])
    basic_model.y_train = sample_data["target"]
    basic_model.prepare_features()

    assert isinstance(basic_model.pipeline, Pipeline)
    assert isinstance(basic_model.pipeline.named_steps["classifier"], LogisticRegression)


def test_train_fits_model(basic_model: BasicModel, sample_data: pd.DataFrame) -> None:
    """Test that the train method fits the model pipeline without error."""
    basic_model.X_train = sample_data.drop(columns=["target"])
    basic_model.y_train = sample_data["target"]
    basic_model.prepare_features()
    basic_model.train()

    assert hasattr(basic_model.pipeline, "predict")


@patch("mlops_course.model.basic_model.mlflow")
def test_log_model_logs_metrics(mock_mlflow: MagicMock, basic_model: BasicModel, sample_data: pd.DataFrame) -> None:
    """Test that MLflow logging includes model metrics and parameters."""
    mock_run = MagicMock()
    mock_run.info.run_id = "1234"
    mock_mlflow.start_run.return_value.__enter__.return_value = mock_run

    basic_model.X_train = sample_data.drop(columns=["target"])
    basic_model.y_train = sample_data["target"]
    basic_model.X_test = sample_data.drop(columns=["target"])
    basic_model.y_test = sample_data["target"]
    basic_model.train_set_spark = MagicMock()
    basic_model.data_version = "0"

    basic_model.prepare_features()
    basic_model.train()
    basic_model.log_model()

    mock_mlflow.log_metric.assert_any_call("accuracy", pytest.approx(1.0, rel=1e-2))
    mock_mlflow.log_param.assert_any_call("model_type", "Logistic Regression with preprocessing")


@patch("mlops_course.model.basic_model.mlflow")
def test_load_latest_model_and_predict(
    mock_mlflow: MagicMock, basic_model: BasicModel, sample_data: pd.DataFrame
) -> None:
    """Test that load_latest_model_and_predict loads model and makes predictions."""
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([0, 1])
    mock_mlflow.sklearn.load_model.return_value = mock_model

    result = basic_model.load_latest_model_and_predict(sample_data.drop(columns=["target"]))
    assert isinstance(result, np.ndarray)
    assert result.tolist() == [0, 1]


def test_load_data_loads_splits_correctly(basic_model: BasicModel, sample_data: pd.DataFrame) -> None:
    """Test that load_data correctly sets training and test sets from Spark tables."""
    basic_model.spark.table.return_value.toPandas.return_value = sample_data

    basic_model.load_data()

    assert list(basic_model.X_train.columns) == ["num1", "num2", "cat1"]
    assert basic_model.y_train.tolist() == [0, 1]


@patch("mlops_course.model.basic_model.MlflowClient")
@patch("mlops_course.model.basic_model.mlflow")
def test_register_model_registers_with_alias(
    mock_mlflow: MagicMock, mock_client: MagicMock, basic_model: BasicModel
) -> None:
    """Test that register_model calls MLflow and sets alias."""
    basic_model.run_id = "test-run"
    mock_mlflow.register_model.return_value.version = 42

    client_instance = MagicMock()
    mock_client.return_value = client_instance

    basic_model.register_model()

    mock_mlflow.register_model.assert_called_once()
    client_instance.set_registered_model_alias.assert_called_with(
        name=basic_model.model_name, alias="latest-model", version=42
    )


@patch("mlops_course.model.basic_model.mlflow")
def test_retrieve_current_run_dataset_returns_dataset(mock_mlflow: MagicMock, basic_model: BasicModel) -> None:
    """Test that retrieve_current_run_dataset loads dataset source."""
    mock_source = MagicMock()
    mock_source.load.return_value = "mocked-dataset"
    mock_mlflow.get_run.return_value.inputs.dataset_inputs[0].dataset = "mocked-info"
    mock_mlflow.data.get_source.return_value = mock_source

    basic_model.run_id = "123"
    result = basic_model.retrieve_current_run_dataset()

    assert result == "mocked-dataset"


@patch("mlops_course.model.basic_model.mlflow")
def test_retrieve_current_run_metadata_returns_dicts(mock_mlflow: MagicMock, basic_model: BasicModel) -> None:
    """Test that retrieve_current_run_metadata extracts metrics and params."""
    mock_data = {"metrics": {"acc": 0.9}, "params": {"C": 1.0}}
    mock_mlflow.get_run.return_value.data.to_dictionary.return_value = mock_data

    basic_model.run_id = "123"
    metrics, params = basic_model.retrieve_current_run_metadata()

    assert metrics == {"acc": 0.9}
    assert params == {"C": 1.0}
