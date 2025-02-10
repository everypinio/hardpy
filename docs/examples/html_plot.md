# HTML with Bokeh

This is an example of using **Bokeh** with **pytest** for creating and testing a dialog box with HTML content.

### How to Start

1. Launch `hardpy init html_plot`.
2. Ensure you have the necessary packages installed, including `matplotlib`, and `bokeh`.
3. Create your `conftest.py` file with the provided fixture.
4. Create your `test_plot.py` file with the test case.
5. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
6. Launch `hardpy run html_plot`.

### conftest.py

This file contains a fixture that generates a Bokeh plot and exports it as HTML.

```python
import matplotlib.pyplot as plt
import pytest
from bokeh.io import export
from bokeh.plotting import figure

@pytest.fixture
def generate_bokeh_html():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Simple Plot")

    p = figure(width=400, height=400)
    p.line([1, 2, 3, 4], [10, 20, 25, 30], line_width=2)

    return export.get_layout_html(p)
```

### test_plot.py

This file contains a test case for the dialog box that utilizes the generated HTML from the fixture.

```python
import pytest
from hardpy import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Dialog box with HTML")

@pytest.mark.case_name("Base dialog box with HTML code")
def test_dialog_box_with_html_code(generate_bokeh_html):
    test_html = generate_bokeh_html

    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(html=test_html, is_raw_html=True),
    )
    response = run_dialog_box(dbx)
    assert response
```

This example demonstrates how to create a simple plot using Matplotlib and Bokeh, and how to use that plot in a dialog box for testing purposes.