from logging import getLogger
import requests

logger = getLogger(__name__)


def arr_backup(
    service_name: str, service_options: dict, domain: str | None, destination: str
):
    logger.debug(f"arr backup for service '{service_name}' started")

    subdomain = service_options.get("subdomain")
    endpoint = service_options.get("endpoint")
    api_key = service_options.get("api_key")
    folder = service_options.get("folder")
    secure = service_options.get("secure", True)

    if not check_options(service_name, domain, endpoint, api_key, folder):
        return

    base_url = build_base_url(domain, subdomain, endpoint, secure)

    if not delete_existing_backups(base_url, api_key):
        return

    create_backup(service_name, base_url, api_key)
    wait_backup_creation(folder)
    copy_backup(service_name, folder, destination)

    logger.debug(f"arr backup completed successfully")


def build_base_url(
    domain: str, subdomain: str | None, endpoint: str, secure: bool
) -> str:
    scheme = "https" if secure else "http"
    host = f"{subdomain}.{domain}" if subdomain else domain

    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    return f"{scheme}://{host}{endpoint}"


def delete_existing_backups(base_url: str, api_key: str) -> bool:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }

    response = requests.get(f"{base_url}/system/backup", headers=headers)

    if response.status_code != 200:
        logger.error(f"backups list request failed with code {response.status_code}")
        return False

    backups = response.json()

    logger.debug(f"{len(backups)} backups found'")

    for backup in backups:
        backup_id = backup.get("id")
        if backup_id is None:
            logger.error(f"backup did not contain the backup id")
            return False
        response = requests.delete(
            f"{base_url}/system/backup/{backup_id}", headers=headers
        )
        if response.status_code != 200:
            logger.error(
                f"deletion of backup '{backup_id}' failed with code {response.status_code}"
            )
            return False

    logger.debug(f"{len(backups)} backups deleted")
    return True


def create_backup(service_name: str, base_url: str, api_key: str):
    # TODO: create backup
    pass


def wait_backup_creation(folder: str):
    # TODO: wait backup is created in folder
    # every 0.3s check if backup as been created until it is
    pass


def copy_backup(service_name: str, folder: str, destination: str):
    # TODO: copy the backup to destination
    pass


def check_options(
    service_name: str,
    domain: str | None,
    endpoint: str | None,
    api_key: str | None,
    folder: str | None,
) -> bool:
    if domain is None:
        logger.error(f"global.domain is required")
        return False
    if endpoint is None:
        logger.error(f"{service_name}.api.endpoint is required")
        return False
    if api_key is None:
        logger.error(f"{service_name}.api.api_key is required")
        return False
    if folder is None:
        logger.error(f"{service_name}.api.folder is required")
        return False
    return True
