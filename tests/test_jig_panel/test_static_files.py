# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import asyncio
from pathlib import Path

import pytest
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from jig.jig_panel.static_files import SpaStaticFiles


def _write_panel_dist(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text("<html>panel</html>", encoding="utf-8")
    (directory / "asset.js").write_text("console.log('ok')", encoding="utf-8")


def _scope(path: str) -> dict:
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": f"/{path}" if not path.startswith("/") else path,
        "raw_path": f"/{path}".encode(),
        "query_string": b"",
        "headers": [],
        "client": ("test", 123),
        "server": ("test", 80),
    }


def _get_response(static: SpaStaticFiles, path: str) -> Response:
    return asyncio.run(static.get_response(path, _scope(path)))


def test_spa_static_files_falls_back_to_index_for_client_routes(
    tmp_path: Path,
) -> None:
    dist = tmp_path / "dist"
    _write_panel_dist(dist)
    static = SpaStaticFiles(directory=dist, html=True)

    response = _get_response(static, "results")

    assert response.status_code == 200
    assert Path(response.path).name == "index.html"


def test_spa_static_files_serves_existing_assets(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    _write_panel_dist(dist)
    static = SpaStaticFiles(directory=dist, html=True)

    response = _get_response(static, "asset.js")

    assert response.status_code == 200
    assert Path(response.path).name == "asset.js"


def test_spa_static_files_does_not_fallback_api_paths(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    _write_panel_dist(dist)
    static = SpaStaticFiles(directory=dist, html=True)

    with pytest.raises(StarletteHTTPException) as exc_info:
        _get_response(static, "api/missing")

    assert exc_info.value.status_code == 404
