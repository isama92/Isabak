from src.isabak.config import *
from src.isabak.services.fs_backup import fs_backup
from src.isabak.services.mysql_backup import mysql_backup
from src.isabak.services.mariadb_backup import mariadb_backup
from src.isabak.services.postgres_backup import postgres_backup
from src.isabak.services.arr_backup import arr_backup
from src.isabak.borg import borg
from os import makedirs
from os.path import join as path_join
import logging
from shutil import rmtree

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app_name = "isabak"
config_file_path = "config.yaml"
env_file_path = ".env"


def main():
    logger.info(f"{app_name} started")

    load_env(env_file_path)
    config = load_config(config_file_path)

    if config is None:
        return

    config = merge_config(config)

    if not verify_config(config):
        return

    logger.debug("configuration loaded")

    base_destination = get_base_destination(config.get("destination"))

    if base_destination is None:
        return

    logger.debug("starting backups")

    for service_name, service_options in config.get("services").items():
        logger.info(f"{service_name} starting")

        if not isinstance(service_options, dict):
            logger.error(f"service '{service_name}' options are not valid")
            continue

        destination = str(path_join(base_destination, service_name, ""))

        makedirs(destination, exist_ok=True)

        if service_options.get("fs") is not None:
            fs_backup(service_name, service_options.get("fs"), destination)

        if service_options.get("mysql") is not None:
            mysql_backup(
                service_name,
                service_options.get("mysql"),
                config.get("mysql", {}),
                destination,
            )

        if service_options.get("mariadb") is not None:
            mariadb_backup(
                service_name,
                service_options.get("mariadb"),
                config.get("mariadb", {}),
                destination,
            )

        if service_options.get("postgres") is not None:
            postgres_backup(service_name, service_options.get("postgres"), destination)

        if service_options.get("arr") is not None:
            arr_backup(
                service_name,
                service_options.get("arr"),
                config.get("domain"),
                destination,
            )

        logger.info(f"{service_name} finished")

    if config.get("borg") is not None:
        borg(config.get("borg"))

    logger.info(f"{app_name} finished")


def get_base_destination(destination: str) -> str | None:
    base_destination = path_join(destination, app_name)

    try:
        rmtree(base_destination)
        pass
    except Exception as e:
        logger.debug(f"could not remove existing backup destination folder ({e})")

    try:
        makedirs(base_destination)
    except Exception as e:
        logger.error(f"could not create backup destination folder ({e})")
        return None

    return base_destination


if __name__ == "__main__":
    main()
