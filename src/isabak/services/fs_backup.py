import os
import logging
import subprocess

logger = logging.getLogger(__name__)


def fs_backup(service_name: str, config: dict, destination: str):
    logger.debug(f'{service_name} starting')

    if 'folder' not in config:
        logger.error(f'source folder config was not set')
        return

    source = os.path.join(config['folder'], '')

    if not os.path.exists(source):
        logger.error(f'source folder {source} does not exist')
        return

    os.makedirs(destination, exist_ok=True)

    try:
        subprocess.run(["rsync", "-a", source, destination], check=True)
    except Exception as e:
        logger.exception(e, stack_info=True)
        logger.error(f'{service_name} finished with errors')
        return

    logger.debug(f'{service_name} finished')
