# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from typing import Any

from glom import assign, glom
from pycouchdb.exceptions import Conflict, NotFound
from pydantic._internal._model_construction import ModelMetaclass

from hardpy.pytest_hardpy.db.base_connector import BaseConnector
from hardpy.pytest_hardpy.db.const import DatabaseField as DF


class BaseStore(BaseConnector):
    """HardPy base storage interface for CouchDB."""

    def __init__(self, db_name: str):
        super().__init__(db_name)
        self._log = getLogger(__name__)
        self._doc: dict = self._init_doc()
        self._schema: ModelMetaclass

    def compact(self):
        """Compact database."""
        self._db.compact()

    def get_field(self, key: str) -> Any:
        """Get field from the state store.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return glom(self._doc, key)

    def set_value(self, key: str, value):
        """Set a value in the state store."""
        assign(self._doc, key, value)
        try:
            self._doc = self._db.save(self._doc)
        except Conflict as exc:
            self._log.error(
                f"Error while saving runner document: {exc} "
                f"when trying to save key={key}, value={value}. "
                "Current document will be changed by "
                "document from database."
            )
            self._doc = self._db.get(self._doc_id)

    def get_document(self) -> ModelMetaclass:
        """Get document by schema.

        Returns:
            ModelMetaclass: document by schema
        """
        self._doc = self._db.get(self._doc_id)
        return self._schema(**self._doc)

    def _init_doc(self) -> dict:
        try:
            doc = self._db.get(self._doc_id)
        except NotFound:
            return {
                "_id": self._doc_id,
                DF.MODULES: {},
                DF.DUT: {
                    DF.SERIAL_NUMBER: None,
                    DF.INFO: {},
                },
                DF.TEST_STAND: {},
                DF.DRIVERS: {},
            }

        if DF.MODULES not in doc:
            doc[DF.MODULES] = {}

        for item in (DF.TEST_STAND, DF.DRIVERS):
            doc[item] = {}

        doc[DF.DUT] = {
            DF.SERIAL_NUMBER: None,
            DF.INFO: {},
        }

        return doc
