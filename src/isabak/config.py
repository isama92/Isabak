import yaml
import os
import logging

logger = logging.getLogger(__name__)


def load_config(path: str) -> dict|None:
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        logger.error(f'config file {path} not found')
        return None

    config = yaml.safe_load(f)

    if config.get('global') is None or config.get('global').get('destination') is None:
        logger.error('global.destination config was not set')
        return None

    if config.get('services') is None:
        logger.error('no services defined in config file')
        return None

    if config.get('global').get('base_domain') is None:
        base_domain = os.environ.get('SRV_DOMAIN')
        config["global"]["base_domain"] = base_domain

    return config
