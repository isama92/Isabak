import logging
from os.path import join as path_join
import subprocess

logger = logging.getLogger(__name__)


def mysql_backup(service_name: str, service_options: dict, mysql_options: dict | None, destination: str):
    logger.debug(f'{service_name} starting')

    if service_options.get('db_name') is None:
        logger.error(f'db_name is not set')
        return

    if not check_credentials(mysql_options):
        return

    try:
        create_credentials(mysql_options)
        create_backup(service_options, mysql_options, destination)
        delete_credentials(mysql_options)
    except Exception as e:
        logging.exception(e, stack_info=True)
        logger.error(f'{service_name} finished with errors')
        return

    logger.debug(f'{service_name} finished')


def create_credentials(mysql_options: dict):
    mysql_container = mysql_options.get('container')
    mysql_username = mysql_options.get('username')
    mysql_password = mysql_options.get('password')
    cmd = f"""echo -e "[client]\\nuser={mysql_username}\\npassword={mysql_password}\\nhost=localhost\\n" > /backup.cnf"""
    subprocess.run([
        "docker", "exec", mysql_container, "bash", "-c", cmd
    ], check=True)


def create_backup(service_options: dict, mysql_options: dict, destination: str):
    db_name = service_options.get('db_name')
    mysql_container = mysql_options.get('container')

    dump_cmd = [
        "docker", "exec", mysql_container,
        "/usr/bin/mysqldump",
        "--defaults-extra-file=/backup.cnf",
        "--single-transaction",
        db_name
    ]

    out_path = path_join(destination, "mysql.sql.gz")
    with open(out_path, "wb") as f:
        gzip_proc = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE)
        gzip = subprocess.Popen(["gzip"], stdin=gzip_proc.stdout, stdout=f)
        gzip_proc.stdout.close()
        gzip.wait()


def check_credentials(mysql_options: dict | None) -> bool:
    if mysql_options is None:
        logger.error(f'mysql global configs are not set')
        return False

    if 'container' not in mysql_options:
        logger.error(f'mysql container is not set')
        return False

    if 'username' not in mysql_options:
        logger.error(f'mysql username is not set')
        return False

    if 'password' not in mysql_options:
        logger.error(f'mysql password is not set')
        return False

    return True


def delete_credentials(mysql_options: dict):
    mysql_container = mysql_options.get('container')
    subprocess.run([
        "docker", "exec", mysql_container, "rm", "/backup.cnf"
    ], check=True)
