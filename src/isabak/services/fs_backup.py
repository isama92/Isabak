from os.path import join as path_join, exists as path_exists
from os import getenv
from logging import getLogger
import subprocess
from re import compile as re_compile

logger = getLogger(__name__)


def fs_backup(service_name: str, service_options: dict, destination: str):
    logger.debug(f"fs backup for service '{service_name}' started")

    folder = service_options.get("folder")

    if not check_options(service_name, folder):
        return

    try:
        folder = replace_env_vars(service_name, folder)
    except KeyError as e:
        logger.error(e)
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

    logger.debug("fs backup completed successfully")


def check_options(service_name: str, folder: str | None):
    if folder is None:
        logger.error(f"{service_name}.fs.folder is required")
        return False
    return True


def replace_env_vars(service_name: str, folder: str) -> str:
    pattern = re_compile(r"\$\{([a-zA-Z0-9_]+)\}")

    def replacer(match):
        env_var_name = match.group(1)
        env_var = getenv(env_var_name)
        if env_var is None:
            raise KeyError(
                f"environment variable '{env_var_name}' in {service_name}.fs.folder '{folder}' is required"
            )
        return env_var

    folder = pattern.sub(replacer, folder)
    return folder
