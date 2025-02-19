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
