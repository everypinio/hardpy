import pytest

from hardpy import Chart, ChartType, set_case_chart

pytestmark = pytest.mark.module_name("Production Test Charts")


@pytest.mark.case_name("Voltage vs Current Characteristics")
def test_voltage_current_characteristics():
    chart = Chart()
    chart.add_series(x_data=[1, 2, 3], y_data=[1, 2, 3], marker_name="Device A")
    chart.add_series(x_data=[1, 2, 4], y_data=[5, 4, 3], marker_name="Device B")
    set_case_chart(chart)


@pytest.mark.case_name("Frequency Response Analysis")
def test_frequency_response_analysis():
    chart = Chart(
        type=ChartType.LINE_LOG_X,
        title="Frequency Response",
        x_label="Frequency (Hz)",
        y_label="Gain (dB)",
    )
    x_data = [10**i for i in range(5)]
    y_data = [i**2 for i in range(5)]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Amplifier Response")
    set_case_chart(chart)
