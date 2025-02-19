from time import sleep

from hardpy import (
    HTMLComponent,
    set_message,
    set_operator_message,
)


def test_operator_message_with_html():
    test_html = """
    <!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>

    <p>My first paragraph.</p>

    </body>
    </html>
    """
    set_operator_message(
        msg="Test operator message with html",
        title="Operator message",
        html=HTMLComponent(html=test_html, is_raw_html=True),
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True

def test_operator_message_with_html_and_border():
    test_html = """
    <!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>

    <p>My first paragraph.</p>

    </body>
    </html>
    """
    set_operator_message(
        msg="Test operator message with html",
        title="Operator message",
        html=HTMLComponent(html=test_html, is_raw_html=True, border=10, width=20),
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True
