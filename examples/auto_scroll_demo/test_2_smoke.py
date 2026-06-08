"""Smoke module — fast burst (~0.15s/case). 8 cases in ~1.2s.

Stresses scroll debounce and the user-scroll suppression window:
runningIndex changes about six times a second.
"""

import time
import pytest

pytestmark = pytest.mark.module_name("Smoke")

QUICK = 0.15


@pytest.mark.case_name("GPIO readout 1")
def test_smoke_1():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 2")
def test_smoke_2():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 3")
def test_smoke_3():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 4")
def test_smoke_4():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 5")
def test_smoke_5():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 6")
def test_smoke_6():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 7")
def test_smoke_7():
    time.sleep(QUICK)


@pytest.mark.case_name("GPIO readout 8")
def test_smoke_8():
    time.sleep(QUICK)
