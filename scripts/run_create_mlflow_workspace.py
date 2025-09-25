# Run the code : uv run scripts/run_create_mlflow_workspace.py --env-file ./.env --config-file ./project_config.yml
import os
import argparse
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import ResourceDoesNotExist
import mlflow
from mlops_course.utils.config import ProjectConfig


def main(env_file: str, config_file: str, environment: str, profile: str | None = None) -> None:
    """Main entry point to prepare and set an MLflow experiment on Databricks."""

    # Load environment variables from .env file
    load_dotenv(dotenv_path=env_file)

    # Retrieve the profile either from CLI or .env
    profile = profile or os.getenv("PROFILE")
    if not profile:
        raise ValueError("❌ PROFILE is not set in arguments or .env")

    # Load the project configuration
    config = ProjectConfig.from_yaml(config_path=config_file, env=environment)

    # Connect to Databricks
    w = WorkspaceClient(profile=profile)

    # Get the experiment path from config
    experiment_path = config.experiment_name_basic

    # Ensure parent directory exists (e.g. /Shared/experiments)
    exp_dir = "/".join(experiment_path.split("/")[:-1])  # => "/Shared/experiments"
    try:
        w.workspace.get_status(exp_dir)
    except ResourceDoesNotExist:
        w.workspace.mkdirs(exp_dir)
        print(f"✅ Directory {exp_dir} created")

    # Set MLflow experiment
    mlflow.set_experiment(experiment_path)
    print(f"✅ MLflow experiment ready: {experiment_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup and configure MLflow experiment on Databricks")
    parser.add_argument("--env-file", default="../.env", help="Path to .env file (default: ../.env)")
    parser.add_argument("--config-file", default="../project_config.yml", help="Path to project_config.yml")
    parser.add_argument("--environment", default="dev", choices=["dev", "acc", "prd"], help="Environment to use")
    parser.add_argument("--profile", default=None, help="Databricks profile (overrides PROFILE in .env)")

    args = parser.parse_args()

    main(
        env_file=args.env_file,
        config_file=args.config_file,
        environment=args.environment,
        profile=args.profile,
    )
