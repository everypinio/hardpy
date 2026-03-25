# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from time import sleep

from pycouchdb import Server as DbServer
from pycouchdb.exceptions import Conflict


def update_db(doc: dict, doc_id: str, db: DbServer) -> None:
    """Persist in-memory document to storage backend."""
    try:
        doc = db.save(doc)
    except Conflict:
        doc["_rev"] = db.get(doc_id)["_rev"]
        doc = db.save(doc)


def update_doc(doc: dict, doc_id: str, db: DbServer) -> dict:
    """Reload document from storage backend to memory."""
    retries = 5
    latest_doc = db.get(doc_id)
    for attempt in range(retries):
        try:
            doc["_rev"] = latest_doc["_rev"]
            break
        except KeyError:
            sleep(0.1 * (attempt + 1))
            if attempt == retries - 1:
                raise
            latest_doc = db.get(doc_id)
    return latest_doc
