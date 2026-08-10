from jig.pytest_jig.utils import RunScope, resolve_run_name


def test_requested_name_wins():
    assert resolve_run_name("autofocus/fine", RunScope.PARTIAL) == "autofocus/fine"


def test_full_run_without_a_requested_name_is_named_after_its_scope():
    assert resolve_run_name(None, RunScope.FULL) == "full"


def test_partial_run_without_a_requested_name_is_named_after_its_scope():
    assert resolve_run_name(None, RunScope.PARTIAL) == "partial"


def test_empty_requested_name_falls_back_to_the_scope():
    assert resolve_run_name("", RunScope.FULL) == "full"
