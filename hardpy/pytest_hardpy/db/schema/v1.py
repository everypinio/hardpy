# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from hardpy.pytest_hardpy.utils import TestStatus as Status  # noqa: TC001


class IBaseResult(BaseModel):
    """Base class for all result models."""

    model_config = ConfigDict(extra="forbid")

    status: Status
    stop_time: int | None
    start_time: int | None
    name: str


class CaseStateStore(IBaseResult):
    """Test case description.

    Example:
    ```
    {
      "test_one": {
        "status": "passed",
        "name": "Test 2",
        "start_time": 1695817188,
        "stop_time": 1695817189,
        "assertion_msg": null,
        "msg": null,
        "attempt": 1,
        "dialog_box": {
          "title_bar": "Example of text input",
          "dialog_text": "Type some text and press the Confirm button",
          "widget": {
            "info": {
              "text": "some text"
            },
            "type": "textinput"
          },
          visible: true,
          id: "af6ac3e7-7ce8-4a6b-bb9d-88c3e10b5c7a",
          font_size: 14
        }
      }
    }
    ```
    """

    assertion_msg: str | None = None
    msg: dict | None = None
    dialog_box: dict = {}
    attempt: int = 0


class CaseRunStore(IBaseResult):
    """Test case description with artifact.

    Example:
    ```
    {
      "test_one": {
        "status": "passed",
        "name": "Test 2",
        "start_time": 1695817188,
        "stop_time": 1695817189,
        "assertion_msg": null,
        "msg": null,
        "artifact": {}
      }
    }
    ```
    """

    assertion_msg: str | None = None
    msg: dict | None = None
    artifact: dict = {}


class ModuleStateStore(IBaseResult):
    """Test module description.

    Example:
    ```
    {
      "test_2_b": {
        "status": "passed",
        "name": "Module 2",
        "start_time": 1695816886,
        "stop_time": 1695817016,
        "cases": {
          "test_one": {
            "status": "passed",
            "name": "Test 1",
            "start_time": 1695817015,
            "stop_time": 1695817016,
            "assertion_msg": null,
            "msg": null
          }
        }
      }
    }
    ```
    """

    cases: dict[str, CaseStateStore] = {}


class ModuleRunStore(IBaseResult):
    """Test module description.

    Example:
    ```
    {
      "test_2_b": {
        "status": "passed",
        "name": "Module 2",
        "start_time": 1695816886,
        "stop_time": 1695817016,
        "artifact": {},
        "cases": {
          "test_one": {
            "status": "passed",
            "name": "Test 1",
            "start_time": 1695817015,
            "stop_time": 1695817016,
            "assertion_msg": null,
            "msg": null,
            "artifact": {}
          }
        }
      }
    }
    ```
    """

    cases: dict[str, CaseRunStore] = {}
    artifact: dict = {}


class Dut(BaseModel):
    """Device under test description.

    Example:
    ```
    {
      "dut": {
        "serial_number": "a9ad8dca-2c64-4df8-a358-c21e832a32e4",
        "part_number": "part_number_1",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      }
    }
    ```
    """

    model_config = ConfigDict(extra="forbid")

    serial_number: str | None
    part_number: str | None
    info: dict = {}


class TestStand(BaseModel):
    """Test stand description.

    Example:
    ```
    {
      "test_stand": {
        "hw_id": "840982098ca2459a7b22cc608eff65d4",
        "name": "test_stand_1",
        "info": {
          "geo": "Belgrade"
        },
        "timezone": "Europe/Belgrade",
        "drivers": {
          "driver_1": "driver info",
          "driver_2": {
            "state": "active",
            "port": 8000
          }
        },
        "location": "Belgrade_1"
      }
    }
    ```
    """

    model_config = ConfigDict(extra="forbid")

    hw_id: str | None = None
    name: str | None = None
    timezone: str | None = None
    drivers: dict = {}
    info: dict = {}
    location: str | None = None


class ResultStateStore(IBaseResult):
    """Test run description.

    Example:
    ```
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "progress": 100,
      "stop_time": 1695817266,
      "start_time": 1695817263,
      "status": "failed",
      "name": "hardpy-stand",
      "alert": "",
      "dut": {
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "part_number": "part_1",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      },
      "test_stand": {
        "hw_id": "840982098ca2459a7b22cc608eff65d4",
        "name": "test_stand_1",
        "info": {
          "geo": "Belgrade"
        },
        "timezone": "Europe/Belgrade",
        "drivers": {
          "driver_1": "driver info",
          "driver_2": {
            "state": "active",
            "port": 8000
          }
        },
        "location": "Belgrade_1"
      },
      "operator_msg": {
        "msg": "Operator message",
        "title": "Message",
        "visible": true,
        "id": "f45ac1e7-2ce8-4a6b-bb9d-8863e30bcc78"
      },
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info ",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "attempt": 1,
              "dialog_box": {
                "title_bar": "Example of text input",
                "dialog_text": "Type some text and press the Confirm button",
                "widget": {
                  "info": {
                    "text": "some text"
                  },
                  "type": "textinput"
                },
                visible: true,
                id: "f45bc1e7-2c18-4a4b-2b9d-8863e30bcc78",
                font_size: 14
              }
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "attempt": 1,
              "msg": [
                "Current minute 21"
              ]
            }
          }
        }
      }
    }
    ```
    """

    model_config = ConfigDict(extra="forbid")

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")
    progress: int
    test_stand: TestStand
    dut: Dut
    modules: dict[str, ModuleStateStore] = {}
    operator_msg: dict = {}
    alert: str


class ResultRunStore(IBaseResult):
    """Test run description.

    Example:
    ```
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "stop_time": 1695817266,
      "start_time": 1695817263,
      "status": "failed",
      "name": "hardpy-stand",
      "dut": {
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "part_number": "part_1",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      },
      "test_stand": {
        "hw_id": "840982098ca2459a7b22cc608eff65d4",
        "name": "test_stand_1",
        "info": {
          "geo": "Belgrade"
        },
        "timezone": "Europe/Belgrade",
        "drivers": {
          "driver_1": "driver info",
          "driver_2": {
            "state": "active",
            "port": 8000
          }
        },
        "location": "Belgrade_1"
      },
      "artifact": {},
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "artifact": {},
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "artifact": {}
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "msg": [
                "Current minute 21"
              ],
              "artifact": {
                "data_str": "123DATA",
                "data_int": 12345,
                "data_dict": {
                  "test_key": "456DATA"
                }
              }
            }
          }
        }
      }
    }
    ```
    """

    model_config = ConfigDict(extra="forbid")
    # Create the new schema class with version update
    # when you change this class or fields in this class.
    __version__: ClassVar[int] = 1

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")

    test_stand: TestStand
    dut: Dut
    modules: dict[str, ModuleRunStore] = {}
    artifact: dict = {}
