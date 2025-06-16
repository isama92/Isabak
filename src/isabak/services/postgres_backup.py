from os import makedirs, getuid, getgid
from os.path import join as path_join, exists as path_exists, realpath as path_realpath
from shutil import move as shutil_move
from shutil import rmtree as shutil_rmtree
import subprocess
from src.isabak.logs import get_logger

logger = get_logger(__name__)


def postgres_backup(service_name: str, service_options: dict, destination: str):
    logger.debug(f"postgres backup for service '{service_name}' started")

    db_name = service_options.get("db_name")
    db_container = service_options.get("container")
    db_network = service_options.get("network")
    db_username = service_options.get("username")
    db_password = service_options.get("password")

    if not check_options(
        service_name, db_name, db_container, db_network, db_username, db_password
    ):
        return

    tmp_folder = path_join(destination, "tmp")
    makedirs(tmp_folder, exist_ok=True)
    logger.debug("tmp folder created")

    if not create_backup(
        db_name, db_container, db_network, db_username, db_password, tmp_folder
    ):
        return

    backup_path = path_join(tmp_folder, "last", f"{db_name}-latest.sql.gz")
    backup_path = path_realpath(backup_path)

    if not path_exists(backup_path):
        logger.error(f"backup file {backup_path} does not exist")
        return

    backup_path_dest = path_join(destination, f"db_{db_name}.sql.gz")

    shutil_move(backup_path, backup_path_dest)
    logger.debug("backup moved to backup folder")

    shutil_rmtree(tmp_folder)
    logger.debug("tmp folder removed")

    logger.debug("postgres backup completed successfully")


def create_backup(
    db_name: str,
    db_container: str,
    db_network: str,
    db_username: str,
    db_password: str,
    tmp_folder: str,
) -> bool:
    # fmt: off
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{tmp_folder}:/backups",
        "-u", f"{getuid()}:{getgid()}",
        "--network", db_network,
        "-e", f"POSTGRES_HOST={db_container}",
        "-e", f"POSTGRES_DB={db_name}",
        "-e", f"POSTGRES_USER={db_username}",
        "-e", f"POSTGRES_PASSWORD={db_password}",
        "prodrigestivill/postgres-backup-local", "/backup.sh"
    ]
    # fmt: on

    try:
        subprocess.run(
            docker_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
    except subprocess.CalledProcessError as e:
        logger.exception(e, stack_info=True)
        shutil_rmtree(tmp_folder)
        return False

    logger.debug("backup created")
    return True


def check_options(
    service_name: str,
    db_name: str | None,
    db_container: str | None,
    db_network: str | None,
    db_username: str | None,
    db_password: str | None,
) -> bool:
    if db_name is None:
        logger.error(f"{service_name}.postgres.db_name is required")
        return False
    if db_container is None:
        logger.error(f"{service_name}.postgres.container is required")
        return False
    if db_network is None:
        logger.error(f"{service_name}.postgres.network is required")
        return False
    if db_username is None:
        logger.error(f"{service_name}.postgres.username is required")
        return False
    if db_password is None:
        logger.error(f"{service_name}.postgres.password is required")
        return False
    return True
