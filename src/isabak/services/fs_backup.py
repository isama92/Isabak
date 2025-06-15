from os.path import join as path_join, exists as path_exists
from os import getenv
from logging import getLogger
import subprocess
from re import compile as re_compile

logger = getLogger(__name__)


def fs_backup(service_name: str, source: str | None, destination: str):
    logger.debug(f"{service_name} starting")

    if source is None:
        logger.error(f"source folder config was not set")
        return

    try:
        source = replace_env_vars(service_name, source)
    except KeyError as e:
        logger.error(e)
        return

    source = path_join(source, "")

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


def replace_env_vars(service_name: str, source: str) -> str:
    pattern = re_compile(r"\$\{([a-zA-Z0-9_]+)\}")

    def replacer(match):
        env_var_name = match.group(1)
        env_var = getenv(env_var_name)
        if env_var is None:
            raise KeyError(
                f"environment variable '{env_var_name}' in service '{service_name}' is not set"
            )
        return env_var

    source = pattern.sub(replacer, source)
    return source
