from src.isabak.config import *
from src.isabak.services.fs_backup import fs_backup
from src.isabak.services.mysql_backup import mysql_backup
from src.isabak.services.mariadb_backup import mariadb_backup
from src.isabak.services.postgres_backup import postgres_backup
from src.isabak.services.arr_backup import arr_backup
from os import makedirs
from os.path import join as path_join
import logging
from shutil import rmtree

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    logger.info("isabak started")

    config_file_path = "config.yaml"
    env_file_path = ".env"

    load_env(env_file_path)
    config = load_config(config_file_path)

    if config is None:
        return

    config = merge_config(config)

    if not verify_config(config):
        return

    logger.debug("configuration loaded")

    config_global = config.get("global")

    base_destination = path_join(config_global.get("destination"), "isabak")
    rmtree(base_destination)
    makedirs(base_destination)

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
                config_global.get("mysql", {}),
                destination,
            )

        if service_options.get("mariadb") is not None:
            mariadb_backup(
                service_name,
                service_options.get("mariadb"),
                config_global.get("mariadb", {}),
                destination,
            )

        if service_options.get("postgres") is not None:
            postgres_backup(service_name, service_options.get("postgres"), destination)

        if service_options.get("arr") is not None:
            arr_backup(
                service_name,
                service_options.get("arr"),
                config_global.get("domain"),
                destination,
            )

        logger.info(f"{service_name} finished")

    logger.info("isabak finished")


if __name__ == "__main__":
    main()
