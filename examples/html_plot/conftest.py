import os
import tempfile

import matplotlib.pyplot as plt
import pytest
from bokeh.io import output_file, save
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

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp_file:
        output_file(tmp_file.name)
        save(p)

        with open(tmp_file.name, "r") as f:  # noqa: PTH123, UP015
            html_string = f.read()

    os.unlink(tmp_file.name)  # noqa: PTH108

    return html_string
