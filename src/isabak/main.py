from src.isabak.config import load_config
from src.isabak.services.fs_backup import fs_backup
from src.isabak.services.mysql_backup import mysql_backup
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    logger.debug('loading configuration')
    config = load_config('config.yaml')

    if config is None:
        return

    logger.debug('configuration loaded')

    config_global = config.get('global')

    logger.debug('starting backups')

    for service_name, service_options in config.get('services').items():
        logger.info(f'{service_name} starting')

        destination = os.path.join(config_global.get('destination'), service_name, '')

        if service_options is None:
            logger.error(f'service {service_name} has no options')
            continue

        if "folder" in service_options:
            fs_backup(service_name, service_options, destination)

        if service_options.get('mysql') is not None:
            mysql_backup(service_name, service_options.get('mysql'), config_global.get('mysql'), destination)

        logger.info(f'{service_name} finished')

    logger.debug('backups finished')

if __name__ == '__main__':
    main()
