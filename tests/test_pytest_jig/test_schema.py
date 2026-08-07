def test_schema_version():
    """Check last schema version.

    Actual schema from jig.pytest_jig.db must be equal
    to last schema (v1, v2, ...)

    Update the schema version in this test after creating a new version.
    """
    from jig.pytest_jig.db import ResultRunStore
    from jig.pytest_jig.db.schema.v1 import ResultRunStore as ResultRunStoreV1

    actual_schema = ResultRunStore
    last_schema = ResultRunStoreV1

    assert actual_schema == last_schema
