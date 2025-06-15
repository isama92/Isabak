from src.isabak.config import *
from src.isabak.services.fs_backup import fs_backup
from src.isabak.services.mysql_backup import mysql_backup
from src.isabak.services.mariadb_backup import mariadb_backup
import os
import logging

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

    logger.debug("starting backups")

    for service_name, service_options in config.get("services").items():
        logger.info(f"{service_name} starting")

        if not isinstance(service_options, dict):
            logger.error(f"service '{service_name}' options are not valid")
            continue

        destination = str(
            os.path.join(config_global.get("destination"), service_name, "")
        )

        if service_options is None:
            logger.error(f"service {service_name} has no options")
            continue

        if "folder" in service_options:
            fs_backup(service_name, service_options, destination)

        if service_options.get("mysql") is not None:
            mysql_backup(
                service_name,
                service_options.get("mysql"),
                config_global.get("mysql"),
                destination,
            )

        if service_options.get("mariadb") is not None:
            mariadb_backup(
                service_name,
                service_options.get("mariadb"),
                config_global.get("mariadb"),
                destination,
            )

        logger.info(f"{service_name} finished")

    logger.info("isabak finished")


if __name__ == "__main__":
    main()
