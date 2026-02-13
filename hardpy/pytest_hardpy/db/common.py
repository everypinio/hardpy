# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817


def create_default_doc_structure(doc_id: str, doc_id_for_rev: str) -> dict:
    """Create default document structure with standard fields.

    Args:
        doc_id (str): Document ID to use
        doc_id_for_rev (str): Document ID for _rev field (for JSON compatibility)

    Returns:
        dict: Default document structure
    """
    return {
        "_id": doc_id,
        "_rev": doc_id_for_rev,
        DF.MODULES: {},
        DF.DUT: {},
        DF.TEST_STAND: {},
        DF.PROCESS: {},
    }
