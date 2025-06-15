import logging
from os.path import join as path_join
import subprocess

logger = logging.getLogger(__name__)


def mariadb_backup(
    service_name: str, service_options: dict, db_options: dict | None, destination: str
):
    logger.debug(f"{service_name} starting")

    if service_options.get("db_name") is None:
        logger.error(f"db_name is not set")
        return

    if not check_credentials(db_options):
        return

    try:
        create_credentials(db_options)
        create_backup(service_options, db_options, destination)
        delete_credentials(db_options)
    except Exception as e:
        logging.exception(e, stack_info=True)
        logger.error(f"{service_name} finished with errors")
        return

    logger.debug(f"{service_name} finished")


def create_credentials(db_options: dict):
    mariadb_container = db_options.get("container")
    mariadb_username = db_options.get("username")
    mariadb_password = db_options.get("password")
    cmd = f"""echo -e "[client]\\nuser={mariadb_username}\\npassword={mariadb_password}\\nhost=localhost\\n" > /backup.cnf"""
    subprocess.run(["docker", "exec", mariadb_container, "bash", "-c", cmd], check=True)


def create_backup(service_options: dict, db_options: dict, destination: str):
    db_name = service_options.get("db_name")
    mariadb_container = db_options.get("container")

    dump_cmd = [
        "docker",
        "exec",
        mariadb_container,
        "/usr/bin/mariadb-dump",
        "--defaults-extra-file=/backup.cnf",
        "--single-transaction",
        db_name,
    ]

    out_path = path_join(destination, "mariadb.sql.gz")
    with open(out_path, "wb") as f:
        gzip_proc = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE)
        gzip = subprocess.Popen(["gzip"], stdin=gzip_proc.stdout, stdout=f)
        gzip_proc.stdout.close()
        gzip.wait()


def check_credentials(db_options: dict | None) -> bool:
    if db_options is None:
        logger.error(f"mariadb global configs are not set")
        return False

    if "container" not in db_options:
        logger.error(f"mariadb container is not set")
        return False

    if "username" not in db_options:
        logger.error(f"mariadb username is not set")
        return False

    if "password" not in db_options:
        logger.error(f"mariadb password is not set")
        return False

    return True


def delete_credentials(db_options: dict):
    mariadb_container = db_options.get("container")
    subprocess.run(
        ["docker", "exec", mariadb_container, "rm", "/backup.cnf"], check=True
    )
