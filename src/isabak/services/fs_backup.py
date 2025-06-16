from src.isabak.helpers import replace_env_vars
from os.path import join as path_join, exists as path_exists
from os import makedirs
import subprocess
from src.isabak.logs import get_logger

logger = get_logger(__name__)


def fs_backup(service_name: str, service_options: dict, destination: str):
    logger.debug(f"fs backup for service '{service_name}' started")

    folder = service_options.get("folder")

    if not check_options(service_name, folder):
        return

    destination = path_join(destination, "fs", "")
    makedirs(destination, exist_ok=True)

    try:
        folder = replace_env_vars(folder)
    except KeyError as e:
        logger.error(f"{e}, {service_name}.fs.folder")
        return

    folder = path_join(folder, "")

    if not path_exists(folder):
        logger.error(
            f"{service_name}.fs.folder '{folder}' does not exist in filesystem"
        )
        return

    try:
        subprocess.run(["rsync", "-a", folder, destination], check=True)
    except Exception as e:
        logger.exception(e, stack_info=True)
        return

    logger.debug(f"copied {folder} to {destination}")

    logger.debug("fs backup completed successfully")


def check_options(service_name: str, folder: str | None):
    if folder is None:
        logger.error(f"{service_name}.fs.folder is required")
        return False
    return True
