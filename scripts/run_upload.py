# run the script
# On one environment: uv run scripts/run_upload.py --env dev --env-file .env --config project_config.ym
# On all environment: uv run scripts/run_upload.py --env all --env-file .env --config project_config.ym

import argparse
from mlops_course.data.config_loader import load_env, load_project_config
from mlops_course.data.uploader import load_files_from_source, upload_files


def main():
    parser = argparse.ArgumentParser(
        description="Upload files (local or Kaggle) to Databricks Volumes"
    )
    parser.add_argument(
        "--env", default="dev", choices=["dev", "acc", "prd", "all"],
        help="Target environment (dev, acc, prd, or all)"
    )
    parser.add_argument(
        "--env-file", default=".env",
        help="Path to .env file containing DATABRICKS_HOST and DATABRICKS_TOKEN"
    )
    parser.add_argument(
        "--config", default="project_config.yml",
        help="YAML configuration file"
    )
    args = parser.parse_args()

    # 1. Load environment variables
    host, token = load_env(args.env_file)

    # 2. Select environments to process
    envs = ["dev", "acc", "prd"] if args.env == "all" else [args.env]

    # 3. Upload summary
    summary = {}
    total = 0

    for env in envs:
        print(f"\n=== Uploading to {env} ===")

        # Load environment-specific config
        env_config, global_config = load_project_config(args.config, env)

        # Build source config
        data_source = global_config["data_source"]
        config_dict = {
            "source_type": data_source["source_type"],
            "files": [env_config["raw_data_file"]],
            "local_path": data_source.get("local_path", "./data/raw"),
            "kaggle_dataset": data_source.get("kaggle_dataset"),
        }

        # Load files
        files = load_files_from_source(config_dict)

        # Upload to Databricks
        uploaded = upload_files(host, token, env_config, files)

        summary[env] = uploaded
        total += len(uploaded)

    # 4. Final summary
    print("\n===== FINAL SUMMARY =====")
    for env, files in summary.items():
        print(f"Environment: {env}")
        if files:
            for f in files:
                print(f" - {f}")
        else:
            print(" (no files uploaded)")
    print(f"Total uploaded files: {total}")
    print("✅ Process completed.")


if __name__ == "__main__":
    main()
