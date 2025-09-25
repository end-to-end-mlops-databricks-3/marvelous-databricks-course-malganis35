import json
import os
import kagglehub
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import VolumeType
from dotenv import load_dotenv
from loguru import logger


def load_files_from_source(config):
    """
    Return a list of local file paths defined in the config,
    whether they come from Kaggle or a local directory.
    """
    files = config["files"]
    source_type = config["source_type"]

    if source_type == "kaggle":
        dataset = config["kaggle_dataset"]
        logger.info(f"Downloading dataset {dataset} from Kaggle...")
        path = kagglehub.dataset_download(dataset)
        logger.info(f"Dataset downloaded to: {path}")

        # Debug: list files in the downloaded dataset
        logger.debug("Files available in the dataset:")
        for root, _, filenames in os.walk(path):
            for fname in filenames:
                logger.debug(f" - {os.path.join(root, fname)}")

        file_paths = [os.path.join(path, f) for f in files]
        for f in file_paths:
            if not os.path.exists(f):
                raise FileNotFoundError(
                    f"File {os.path.basename(f)} not found in {path}"
                )
        return file_paths

    elif source_type == "local":
        base_path = config["local_path"]
        file_paths = [os.path.join(base_path, f) for f in files]
        for f in file_paths:
            if not os.path.exists(f):
                raise FileNotFoundError(
                    f"File {os.path.basename(f)} not found in {base_path}"
                )
        return file_paths

    else:
        raise ValueError("source_type must be either 'kaggle' or 'local'")


# --- Helper functions for UC objects ---
def check_catalog_exists(w: WorkspaceClient, catalog_name: str):
    try:
        w.catalogs.get(catalog_name)
        logger.info(f"Catalog {catalog_name} exists.")
    except Exception as e:
        logger.error(f"Catalog {catalog_name} does not exist or cannot be accessed: {e}")
        raise SystemExit(1)


def ensure_schema(w: WorkspaceClient, catalog_name: str, schema_name: str):
    try:
        w.schemas.get(schema_name, catalog_name=catalog_name)
        logger.info(f"Schema {schema_name} already exists in {catalog_name}.")
    except Exception:
        logger.info(f"Creating schema {schema_name} in {catalog_name}...")
        try:
            w.schemas.create(
                name=schema_name, catalog_name=catalog_name, comment="ML Schema"
            )
            logger.info(f"Schema {schema_name} created in {catalog_name}.")
        except Exception as e:
            logger.error(f"Could not create schema {schema_name} in {catalog_name}: {e}")


def ensure_volume(w: WorkspaceClient, catalog_name: str, schema_name: str, volume_name: str):
    try:
        w.volumes.get(volume_name, catalog_name=catalog_name, schema_name=schema_name)
        logger.info(f"Volume {volume_name} already exists in {catalog_name}.{schema_name}.")
    except Exception:
        logger.info(f"Creating volume {volume_name} in {catalog_name}.{schema_name}...")
        try:
            w.volumes.create(
                name=volume_name,
                catalog_name=catalog_name,
                schema_name=schema_name,
                volume_type=VolumeType.MANAGED,
                comment="Data volume",
            )
            logger.info(f"Volume {volume_name} created in {catalog_name}.{schema_name}.")
        except Exception as e:
            logger.error(f"Could not create volume {volume_name} in {catalog_name}.{schema_name}: {e}")


def main():
    # --- Load host & token from .env ---
    load_dotenv()
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")

    if not host or not token:
        raise EnvironmentError(
            "DATABRICKS_HOST and DATABRICKS_TOKEN must be set in the .env file"
        )

    # --- Load config ---
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    catalogs = config["catalogs"]
    schema_name = config["schema_name"]
    volume_name = config["volume_name"]

    # --- Retrieve files to upload ---
    file_paths = load_files_from_source(config)

    # --- Initialize Databricks client ---
    w = WorkspaceClient(host=host, token=token)

    # Upload summary
    summary = {}

    for catalog in catalogs:
        # Check that catalog exists, otherwise exit
        check_catalog_exists(w, catalog)

        # Ensure schema and volume exist
        ensure_schema(w, catalog, schema_name)
        ensure_volume(w, catalog, schema_name, volume_name)

        # Upload files
        uploaded_files = []
        for local_file in file_paths:
            filename = os.path.basename(local_file)
            target_path = f"dbfs:/Volumes/{catalog}/{schema_name}/{volume_name}/{filename}"

            logger.debug("Attempting upload:")
            logger.debug(f"   Local :  {local_file}")
            logger.debug(f"   Remote: {target_path}")

            try:
                with open(local_file, "rb") as f:
                    w.dbfs.upload(target_path, f, overwrite=True)

                logger.info(f"{filename} uploaded to {target_path}")
                uploaded_files.append(target_path)

            except Exception as e:
                logger.error(
                    f"Error while uploading {filename} to {catalog}.{schema_name}.{volume_name}: {e}"
                )

        summary[catalog] = uploaded_files

    # --- Final summary ---
    logger.info("===== FINAL SUMMARY =====")
    total = 0
    for catalog, files in summary.items():
        logger.info(f"Catalog: {catalog}")
        if files:
            for f in files:
                logger.info(f" - {f}")
            total += len(files)
        else:
            logger.info(" (no files uploaded)")

    logger.info(f"Total uploaded files: {total}")
    logger.info("Process completed.")


if __name__ == "__main__":
    main()
