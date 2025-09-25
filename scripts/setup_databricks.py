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
        # Create catalog
        try:
            w.catalogs.create(name=catalog, comment="ML Catalog")
            logger.info(f"Catalog {catalog} created.")
        except Exception:
            logger.info(f"Catalog {catalog} already exists.")

        # Create schema
        try:
            w.schemas.create(
                name=schema_name, catalog_name=catalog, comment="ML Schema"
            )
            logger.info(f"Schema {schema_name} created in {catalog}.")
        except Exception:
            logger.info(f"Schema {schema_name} already exists in {catalog}.")

        # Create volume
        try:
            w.volumes.create(
                name=volume_name,
                catalog_name=catalog,
                schema_name=schema_name,
                volume_type=VolumeType.MANAGED,
                comment="Data volume",
            )
            logger.info(f"Volume {volume_name} created in {catalog}.{schema_name}.")
        except Exception:
            logger.info(f"Volume {volume_name} already exists in {catalog}.{schema_name}.")

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
