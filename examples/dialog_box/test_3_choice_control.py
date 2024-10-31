import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Choice control dialog boxes")


def test_radiobutton_long_line():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(
            fields=[
                "one",
                "two",
                "threethreethreethree threethreethree threethreethree threethreethree  threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethreethreethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree",  # noqa: E501
            ],
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


def test_checkbox_long_line():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(
            fields=[
                "one",
                "two",
                "threethreethreethree threethreethree threethreethree threethreethree  threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethreethreethreethree threethreethree threethreethree threethreethree threethreethree threethreethree threethreethree",  # noqa: E501
            ],
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"


def test_checkbox_big_list():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(
            fields=[
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine",
                "ten",
                "eleven",
                "twelve",
                "thirteen",
                "fourteen",
                "fifteen",
                "sixteen",
                "seventeen",
                "eighteen",
                "nineteen",
                "twenty",
                "twenty-one",
                "twenty-two",
                "twenty-three",
                "twenty-four",
                "twenty-five",
                "twenty-six",
                "twenty-seven",
                "twenty-eight",
                "twenty-nine",
                "thirty",
                "thirty-one",
                "thirty-two",
                "thirty-three",
                "thirty-four",
                "thirty-five",
                "thirty-six",
                "thirty-seven",
                "thirty-eight",
                "thirty-nine",
                "forty",
                "forty-one",
                "forty-two",
                "forty-three",
                "forty-four",
                "forty-five",
                "forty-six",
                "forty-seven",
                "forty-eight",
                "forty-nine",
                "fifty",
                "fifty-one",
                "fifty-two",
                "fifty-three",
                "fifty-four",
                "fifty-five",
                "fifty-six",
                "fifty-seven",
                "fifty-eight",
                "fifty-nine",
                "sixty",
            ],
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    correct_answer = {
        "one",
        "two",
    }
    assert set(response) == correct_answer, "The answer is not correct"
