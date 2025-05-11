import tempfile

import pytest
import yaml

from mlops_course.utils.config import ProjectConfig, Tags


@pytest.fixture
def config_yaml_content():
    return {
        "num_features": ["f1", "f2"],
        "cat_features": ["c1", "c2"],
        "target": "target_col",
        "parameters": {"param1": 0.1, "param2": 100},
        "prd": {
            "catalog_name": "catalog_prd",
            "schema_name": "schema_prd",
            "raw_data_file": "file_prd.csv",
            "train_table": "train_prd",
            "test_table": "test_prd",
        },
        "acc": {
            "catalog_name": "catalog_acc",
            "schema_name": "schema_acc",
            "raw_data_file": "file_acc.csv",
            "train_table": "train_acc",
            "test_table": "test_acc",
        },
        "dev": {
            "catalog_name": "catalog_dev",
            "schema_name": "schema_dev",
            "raw_data_file": "file_dev.csv",
            "train_table": "train_dev",
            "test_table": "test_dev",
        },
    }


def test_from_yaml_loads_dev_env_correctly(config_yaml_content):
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(config_yaml_content, tmp)
        tmp.seek(0)
        config = ProjectConfig.from_yaml(tmp.name, env="dev")
        assert config.catalog_name == "catalog_dev"
        assert config.schema_name == "schema_dev"
        assert config.parameters == {"param1": 0.1, "param2": 100}


def test_from_yaml_invalid_env_raises_error(config_yaml_content):
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(config_yaml_content, tmp)
        tmp.seek(0)
        with pytest.raises(ValueError, match="Invalid environment: test_env"):
            ProjectConfig.from_yaml(tmp.name, env="test_env")


def test_tags_model_instantiation():
    tags = Tags(git_sha="abc123", branch="main", job_run_id="42")
    assert tags.git_sha == "abc123"
    assert tags.branch == "main"
    assert tags.job_run_id == "42"
