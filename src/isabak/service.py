from src.isabak.services.fs_backup import fs_backup
from src.isabak.services.mysql_backup import mysql_backup
from src.isabak.services.mariadb_backup import mariadb_backup
from src.isabak.services.postgres_backup import postgres_backup
from src.isabak.services.arr_backup import arr_backup
from src.isabak.logs import get_logger
from src.isabak.config import get_base_destination
from os import makedirs
from os.path import join as path_join

logger = get_logger(__name__)


def services_backup(config: dict):
    logger.debug("starting services backup")

    base_destination = config.get("destination")
    services = config.get("services")

    if not check_options(base_destination, services):
        return

    base_destination = get_base_destination(base_destination)

    if base_destination is None:
        return

    for service_name, service_options in services.items():
        logger.debug(f"{service_name} starting")

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

        logger.debug(f"{service_name} finished")

    logger.debug("services backup completed")


def check_options(destination, services) -> bool:
    if not isinstance(destination, str):
        logger.error("destination is required")
        return False
    if not isinstance(services, dict):
        logger.error("services is required")
        return False
    for service_name, service_options in services.items():
        if not isinstance(service_options, dict):
            logger.error(f"service '{service_name}' options are invalid")
            return False
    return True
