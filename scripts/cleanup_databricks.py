import json
import os
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
from loguru import logger


def delete_volume(w: WorkspaceClient, catalog_name: str, schema_name: str, volume_name: str):
    """Delete a volume if it exists."""
    full_name = f"{catalog_name}.{schema_name}.{volume_name}"
    try:
        w.volumes.delete(full_name, force=True)
        logger.info(f"Deleted volume {full_name}")
    except Exception as e:
        logger.warning(f"Could not delete volume {full_name}: {e}")


def delete_schema(w: WorkspaceClient, catalog_name: str, schema_name: str):
    """Delete a schema if it exists (must be empty or force=True)."""
    full_name = f"{catalog_name}.{schema_name}"
    try:
        w.schemas.delete(full_name, force=True)
        logger.info(f"Deleted schema {full_name}")
    except Exception as e:
        logger.warning(f"Could not delete schema {full_name}: {e}")


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

    # --- Initialize Databricks client ---
    w = WorkspaceClient(host=host, token=token)

    # --- Cleanup loop ---
    for catalog in catalogs:
        logger.info(f"Processing cleanup in catalog: {catalog}")

        # 1. Delete volume
        delete_volume(w, catalog, schema_name, volume_name)

        # 2. Delete schema
        delete_schema(w, catalog, schema_name)

    logger.info("Cleanup completed.")


if __name__ == "__main__":
    main()
