from logging import getLogger

logger = getLogger(__name__)


def api_backup(
    service_name: str, service_options: dict, domain: str | None, destination: str
):
    logger.debug(f"api backup for service '{service_name}' started")

    subdomain = service_options.get("subdomain")
    endpoint = service_options.get("endpoint")
    api_key = service_options.get("api_key")
    folder = service_options.get("folder")

    if not check_options(service_name, domain, subdomain, endpoint, api_key, folder):
        return

    # TODO #

    logger.debug(f"api backup for service '{service_name}' finished successfully")


def check_options(
    service_name: str,
    domain: str | None,
    subdomain: str | None,
    endpoint: str | None,
    api_key: str | None,
    folder: str | None,
) -> bool:
    if domain is None:
        logger.error(f"global.domain is required")
        return False
    if subdomain is None:
        logger.error(f"{service_name}.api.subdomain is required")
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
