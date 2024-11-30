# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.route("/oauth2/callback")
async def index(request: Request) -> None:
    """OAuth2 callback page."""
    print(json.dumps(dict(request.query_params)))  # noqa: T201
    success_template = """
    <html><body>
        <h1>😎 Success</h1>
        <p>You have been redirected from the Authentication Portal<p>
        <p>Your received response data:</p>
        <ul>
        <li><b>Authorization Code</b>: <i>{{code}}</i></li>
        <li><b>Issuer</b>: <i>{{iss}}</i></li>
        <li><b>Scope of the access request</b>: <i>{{scope}}</i></li>
        <li><b>State data</b>: <i>{{state}}</i></li>
        </ul>
        <p>It is the technical data needed by the application that requests access token.</p>
        <p>Probably, the application already received this information.</p>
        <p><b>ℹ️ You can close the window</b></p>
        </body></html>
    """  # noqa: E501, RUF001

    error_template = """
    <html><body>
        <h1>😞 Error: '{{error}}'</h1>
        <p>You have been redirected from the Authentication Portal<p>
        <p>Your received response data:</p>
        <ul>
        <li><b>Error description</b>: <i>{{error_description}}</i></li>
        <li><b>Issuer</b>: <i>{{iss}}</i></li>
        <li><b>State data</b>: <i>{{state}}</i></li>
        </ul>
        <p>It is the technical data needed by the application that requests access token.</p>
        <p>Probably, the application already received this information.</p>
        <p><b>ℹ️ You can close the window</b></p>
        </body></html>
    """  # noqa: E501, RUF001

    if request.query_params.get("code") is not None:
        return HTMLResponse(
            content=success_template.replace(
                "{{code}}",
                request.query_params.get("code"),  # type: ignore
            )
            .replace("{{iss}}", request.query_params.get("iss"))
            .replace("{{scope}}", request.query_params.get("scope"))
            .replace("{{state}}", request.query_params.get("state")),
            status_code=HTTPStatus.OK,
        )

    if request.query_params.get("error") is not None:
        return HTMLResponse(
            content=error_template.replace(
                "{{error}}",
                request.query_params.get("error"),  # type: ignore
            )
            .replace(
                "{{error_description}}",
                request.query_params.get("error_description"),
            )
            .replace("{{iss}}", request.query_params.get("iss"))
            .replace("{{state}}", request.query_params.get("state")),
            status_code=HTTPStatus.OK,
        )

    server_error = """
    <html><body>
        <h1>Internal Server Error'</h1>
        </body></html>
    """

    return HTMLResponse(
        content=server_error,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    ) # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8088)
