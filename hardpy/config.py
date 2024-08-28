# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pathlib import Path

import rtoml


class ConfigManager:

    obj = {
        "title": "HardPy TOML config",
        "tests_dir": "tests",
        "database": {
            "user": "dev",
            "password": "dev",
            "host": "localhost",
            "port": 5984,
        },
        "frontend": {
            "host": "localhost",
            "port": 8000,
        },
        "socket": {
            "host": "localhost",
            "port": 6525,
        },
    }

    @classmethod
    def get_config(cls, toml_path: Path | None = None) -> dict:
        return rtoml.loads(toml_path)

    @classmethod
    def init_config(  # noqa: WPS211
        cls,
        tests_dir: str | None = None,
        database_user: str | None = None,
        database_password: str | None = None,
        database_host: str | None = None,
        database_port: int | None = None,
        frontend_host: str | None = None,
        frontend_port: int | None = None,
        socket_host: str | None = None,
        socket_port: int | None = None,
    ):
        if tests_dir:
            cls.obj["tests_dir"] = str(tests_dir)
        if database_user:
            cls.obj["database"]["user"] = database_user
        if database_password:
            cls.obj["database"]["password"] = database_password
        if database_host:
            cls.obj["database"]["host"] = database_host
        if database_port:
            cls.obj["database"]["port"] = database_port
        if frontend_host:
            cls.obj["frontend"]["host"] = frontend_host
        if frontend_port:
            cls.obj["frontend"]["port"] = frontend_port
        if socket_host:
            cls.obj["socket"]["host"] = socket_host
        if socket_port:
            cls.obj["socket"]["port"] = socket_port


    @classmethod
    def create_config(cls, parent_dir: Path):
        with open(parent_dir / "hardpy_config.toml", "w") as file:
            file.write(rtoml.dumps(cls.obj))

    @classmethod
    def dict_config(cls):
        return cls.obj
