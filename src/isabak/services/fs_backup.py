from os.path import join as path_join, exists as path_exists
from logging import getLogger
import subprocess

logger = getLogger(__name__)


def fs_backup(service_name: str, config: dict, destination: str):
    logger.debug(f"{service_name} starting")

    if "folder" not in config:
        logger.error(f"source folder config was not set")
        return

    source = path_join(config["folder"], "")

    if not path_exists(source):
        logger.error(f"source folder {source} does not exist")
        return

    try:
        subprocess.run(["rsync", "-a", source, destination], check=True)
    except Exception as e:
        logger.exception(e, stack_info=True)
        logger.error(f"{service_name} finished with errors")
        return

    logger.debug(f"{service_name} finished")
