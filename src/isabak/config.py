import yaml
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_env(path: str) -> None:
    logger.debug(f"loading {path}")

    load_dotenv(path)

    logger.debug(f"{path} loaded")


def load_config(path: str) -> dict:
    logger.debug(f"loading {path}")

    try:
        f = open(path, "r")
    except FileNotFoundError:
        logger.error(f"config file {path} not found")
        return {}

    config = yaml.safe_load(f)

    if config.get("global") is None:
        config["global"] = {}

    logger.debug(f"{path} loaded")

    return config


def merge_config(config: dict) -> dict:
    logger.debug(f"merging .env and config.yaml files")

    env_destination = os.environ.get("DESTINATION")
    if env_destination is not None:
        config["global"]["destination"] = env_destination

    env_domain = os.environ.get("DOMAIN")
    if env_domain is not None:
        config["global"]["domain"] = env_domain.replace(
            "${SRV_DOMAIN}", os.getenv("SRV_DOMAIN", "")
        )

    return config


def verify_config(config: dict) -> bool:
    logger.debug(f"verifying configuration")

    if config.get("global").get("destination") is None:
        logger.error("global.destination config was not set")
        return False

    if config.get("global").get("domain") is None:
        logger.debug("global.domain config was not set")

    if config.get("services") is None:
        logger.error("no services defined in config file")
        return False

    logger.info(f"configuration ok")

    return True
