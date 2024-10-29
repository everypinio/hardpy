def test_schema_version():
    """Check last schema version.

    Actual schema from hardpy.pytest_hardpy.db must be equal
    to last schema (v1, v2, ...)

    Update the schema version in this test after creating a new version.
    """
    from hardpy.pytest_hardpy.db import ResultRunStore
    from hardpy.pytest_hardpy.db.schema.v1 import ResultRunStore as ResultRunStoreV1

    actual_schema = ResultRunStore
    last_schema = ResultRunStoreV1

    assert actual_schema == last_schema
