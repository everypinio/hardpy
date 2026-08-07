# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pycouchdb import Server as DbServer
from pycouchdb.exceptions import Conflict


def update_db(doc: dict, doc_id: str, db: DbServer) -> None:
    """Persist in-memory document to storage backend."""
    try:
        saved = db.save(doc)
        doc["_rev"] = saved["_rev"]
    except Conflict:
        doc["_rev"] = db.get(doc_id)["_rev"]
        saved = db.save(doc)
        doc["_rev"] = saved["_rev"]

def update_doc(doc: dict, doc_id: str, db: DbServer) -> dict:
    """Reload document from storage backend to memory."""
    doc["_rev"] = db.get(doc_id)["_rev"]
    return db.get(doc_id)
