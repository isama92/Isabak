from yaml import safe_load as yaml_load
from os import getenv
from os.path import exists as path_exists
from logging import getLogger
from dotenv import load_dotenv

logger = getLogger(__name__)


def load_env(path: str) -> None:
    logger.debug(f"loading {path}")

    if not path_exists(path):
        logger.debug(f"{path} not found")
        return

    load_dotenv(path)

    logger.debug(f"{path} loaded")


def load_config(path: str) -> dict | None:
    logger.debug(f"loading {path}")

    try:
        f = open(path, "r")
    except FileNotFoundError:
        logger.error(f"{path} not found")
        return None

    config = yaml_load(f)

    if not isinstance(config, dict):
        logger.error(f"{path} is empty or not valid")
        return None

    if config.get("global") is None:
        config["global"] = {}

    logger.debug(f"{path} loaded")

    return config


def merge_config(config: dict) -> dict:
    logger.debug(f"merging env into config")

    env_destination = getenv("DESTINATION")
    if env_destination is not None:
        config["global"]["destination"] = env_destination

    env_domain = getenv("DOMAIN")
    if env_domain is not None:
        config["global"]["domain"] = env_domain.replace(
            "${SRV_DOMAIN}", getenv("SRV_DOMAIN", "")
        )

    return config


def verify_config(config: dict) -> bool:
    logger.debug(f"verifying configuration")

    if config.get("global").get("destination") is None:
        logger.error("global.destination config was not set")
        return False

    if config.get("global").get("domain") is None:
        logger.debug("global.domain config was not set")

    if not isinstance(config.get("services"), dict):
        logger.error("no services defined in config file")
        return False

    logger.info(f"configuration ok")

    return True
