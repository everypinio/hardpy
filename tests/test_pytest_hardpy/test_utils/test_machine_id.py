from hardpy.pytest_hardpy.utils import machine_id


def test_get_machine_id():
    _id = machine_id()
    assert _id
    assert len(_id) >= 17 # if machine id is MAC
