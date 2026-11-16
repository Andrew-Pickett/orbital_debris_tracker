import configparser
from pathlib import Path

import httpx
from pydantic import TypeAdapter

from app.database.models import DataModel

record_adapter = TypeAdapter(list[DataModel])


def _load_credentials() -> dict[str, str]:
    config = configparser.ConfigParser()
    config_path = Path(__file__).with_name("SLTrack.ini")
    if not config.read(config_path):
        raise FileNotFoundError(f"Space-Track configuration not found: {config_path}")

    return {
        "identity": config.get("configuration", "username"),
        "password": config.get("configuration", "password"),
    }


async def fetch_data(
    client: httpx.AsyncClient, credentials: dict[str, str]
) -> list[DataModel]:
    base_url = "https://www.space-track.org"
    request_login = "/ajaxauth/login"
    request_query = "/basicspacedata/query"
    geo_query = (
        "/class/gp/DECAY_DATE/null-val/MEAN_MOTION/<1.01/"
        "ECCENTRICITY/<0.25/OBJECT_TYPE/payload/format/json"
    )

    #    async with httpx.AsyncClient(transport=transport) as client:

    login_response = await client.post(
        base_url + request_login,
        data=credentials,
    )
    login_response.raise_for_status()

    data_response = await client.get(base_url + request_query + geo_query)
    data_response.raise_for_status()
    return record_adapter.validate_python(data_response.json())


async def fetch_catalog() -> list[DataModel]:
    credentials = _load_credentials()

    async with httpx.AsyncClient(timeout=30.0) as client:
        return await fetch_data(client, credentials)
