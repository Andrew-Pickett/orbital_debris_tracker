import json
from pathlib import Path

import httpx
import pydantic
import pytest

from app.pipeline.fetcher import fetch_data

fake_credentials = {"identity": "fake-user", "password": "fake-password"}


@pytest.mark.anyio
async def test_fetch_data_parses_catalog():

    fixture = Path(__file__).parent / "fixtures" / "example_data.json"
    records = json.loads(fixture.read_text())

    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(200)

        if request.method == "GET" and request.url.path.startswith(
            "/basicspacedata/query"
        ):
            return httpx.Response(200, json=records)

        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        response = await fetch_data(client, fake_credentials)

    assert response
    assert response[0].NORAD_CAT_ID == 634


@pytest.mark.anyio
async def test_fetch_data_handles_login_failure():
    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(401, text="Unauthorized")  # Unauthorized

        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError) as error:
            await fetch_data(client, fake_credentials)

        assert error.value.response.status_code == 401


@pytest.mark.anyio
async def test_fetch_data_handles_data_failure():
    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(200)

        if request.method == "GET" and request.url.path.startswith(
            "/basicspacedata/query"
        ):
            return httpx.Response(
                500, text="Internal Server Error"
            )  # Simulate server error

        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError) as error:
            await fetch_data(client, fake_credentials)

        assert error.value.response.status_code == 500


@pytest.mark.anyio
async def test_fetch_data_rejects_invalid_data():
    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(200)

        if request.method == "GET" and request.url.path.startswith(
            "/basicspacedata/query"
        ):
            return httpx.Response(
                200, json=[{}]
            )  # Returns a record missing required fields

        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(pydantic.ValidationError):
            await fetch_data(client, fake_credentials)


@pytest.mark.anyio
async def test_fetch_data_query():
    async def fake_handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/ajaxauth/login":
            return httpx.Response(200)

        if request.method == "GET" and request.url.path.startswith(
            "/basicspacedata/query"
        ):
            # Check that the query parameters are as expected
            assert "format/json" in str(request.url)
            return httpx.Response(200, json=[])

        return httpx.Response(404)

    transport = httpx.MockTransport(fake_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        await fetch_data(client, fake_credentials)
