# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from json import dumps
from logging import getLogger
from typing import Any

from glom import assign, glom
from pycouchdb import Server as DbServer
from pycouchdb.client import Database
from pycouchdb.exceptions import Conflict, GenericError, NotFound
from pydantic._internal._model_construction import ModelMetaclass
from requests.exceptions import ConnectionError  # noqa: A004

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817


class BaseStore:
    """HardPy base storage interface for CouchDB."""

    def __init__(self, db_name: str) -> None:
        config_manager = ConfigManager()
        config = config_manager.config
        self._db_srv = DbServer(config.database.url)
        self._db_name = db_name
        self._db = self._init_db()
        self._doc_id = config.database.doc_id
        self._log = getLogger(__name__)
        self._doc: dict = self._init_doc()
        self._schema: ModelMetaclass

    def compact(self) -> None:
        """Compact database."""
        self._db.compact()

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return glom(self._doc, key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value.

        HardPy collecting uses a simple key without dots.
        Assign is used to update a document.
        Assign is a longer function.

        Args:
            key (str): document key
            value: document value
        """
        try:
            dumps(value)
        except Exception:  # noqa: BLE001
            # serialize non-serializable objects as string
            value = dumps(value, default=str)
        if "." in key:
            assign(self._doc, key, value)
        else:
            self._doc[key] = value

    def update_db(self) -> None:
        """Update database by current document."""
        try:
            self._doc = self._db.save(self._doc)
        except Conflict:
            self._doc["_rev"] = self._db.get(self._doc_id)["_rev"]
            self._doc = self._db.save(self._doc)

    def update_doc(self) -> None:
        """Update current document by database."""
        self._doc["_rev"] = self._db.get(self._doc_id)["_rev"]
        self._doc = self._db.get(self._doc_id)

    def get_document(self) -> ModelMetaclass:
        """Get document by schema.

        Returns:
            ModelMetaclass: document by schema
        """
        self._doc = self._db.get(self._doc_id)
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear database."""
        try:
            # Clear statestore and runstore databases before each launch
            self._db.delete(self._doc_id)
        except (Conflict, NotFound):
            self._log.debug("Database will be created for the first time")
        self._doc: dict = self._init_doc()

    def _init_db(self) -> Database:
        try:
            return self._db_srv.create(self._db_name)  # type: ignore
        except Conflict:
            # database is already created
            return self._db_srv.database(self._db_name)
        except GenericError as exc:
            msg = f"Error initializing database {exc}"
            raise RuntimeError(msg) from exc
        except ConnectionError as exc:
            msg = f"Error initializing database: {exc}"
            raise RuntimeError(msg) from exc

    def _init_doc(self) -> dict:
        try:
            doc = self._db.get(self._doc_id)
        except NotFound:
            return {
                "_id": self._doc_id,
                DF.MODULES: {},
                DF.DUT: {
                    DF.TYPE: None,
                    DF.NAME: None,
                    DF.REVISION: None,
                    DF.SERIAL_NUMBER: None,
                    DF.PART_NUMBER: None,
                    DF.SUB_UNITS: [],
                    DF.INFO: {},
                },
                DF.TEST_STAND: {
                    DF.HW_ID: None,
                    DF.NAME: None,
                    DF.REVISION: None,
                    DF.TIMEZONE: None,
                    DF.LOCATION: None,
                    DF.NUMBER: None,
                    DF.INSTRUMENTS: [],
                    DF.DRIVERS: {},
                    DF.INFO: {},
                },
                DF.PROCESS: {
                    DF.NAME: None,
                    DF.NUMBER: None,
                    DF.INFO: {},
                },
            }

        # init document
        if DF.MODULES not in doc:
            doc[DF.MODULES] = {}

        doc[DF.DUT] = {
            DF.TYPE: None,
            DF.NAME: None,
            DF.REVISION: None,
            DF.SERIAL_NUMBER: None,
            DF.PART_NUMBER: None,
            DF.SUB_UNITS: [],
            DF.INFO: {},
        }

        doc[DF.TEST_STAND] = {
            DF.HW_ID: None,
            DF.NAME: None,
            DF.REVISION: None,
            DF.TIMEZONE: None,
            DF.LOCATION: None,
            DF.NUMBER: None,
            DF.INSTRUMENTS: [],
            DF.DRIVERS: {},
            DF.INFO: {},
        }

        doc[DF.PROCESS] = {
            DF.NAME: None,
            DF.NUMBER: None,
            DF.INFO: {},
        }

        return doc
