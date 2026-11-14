import json
import httpx
from pathlib import Path
import pytest
from app.pipeline.fetcher import fetch_data


@pytest.mark.anyio
async def test_fetch_data_parses_catalog():

    fixture = Path(__file__).parent / "fixtures" / "example_data.json"
    records = json.loads(fixture.read_text())

    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(200)
    
        if request.method == "GET" and request.url.path.startswith("/basicspacedata/query"):
            return httpx.Response(200, json=records)
    
        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        response = await fetch_data(client, {"identity": "fake-user", "password": "fake-password"})

    assert response
    assert response[0].NORAD_CAT_ID == 634
