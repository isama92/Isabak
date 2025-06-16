from src.isabak.config import (
    app_name,
    env_file_path,
    load_env,
    load_config,
    merge_config,
)
from src.isabak.logs import get_logger, set_basic_log_config
from src.isabak.service import services_backup
from src.isabak.borg import borg_transfer


def main():
    env_loaded = load_env()

    set_basic_log_config()
    logger = get_logger(__name__)

    logger.info(f"{app_name} started")

    logger.debug("{} {}".format(env_file_path, "loaded" if env_loaded else "not found"))

    config = load_config()

    if config is None:
        return

    config = merge_config(config)

    logger.debug("configuration loaded")

    if config.get("services"):
        services_backup(config)

    if config.get("borg"):
        borg_transfer(config.get("borg"))

    logger.info(f"{app_name} finished")


if __name__ == "__main__":
    main()
