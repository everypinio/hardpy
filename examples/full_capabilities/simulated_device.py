"""Stand-in for a real instrument driver.

Values are deterministic so the example always produces the same report.
"""

from __future__ import annotations

from math import exp, log10, sin

SUPPLY_VOLTAGE_V = 3.31
IDLE_CURRENT_MA = 12.4
FIRMWARE_VERSION = "1.4.2"
CUTOFF_FREQUENCY_HZ = 5000
AUTOFOCUS_COARSE_PEAK_UM = 120.0
AUTOFOCUS_FINE_PEAK_UM = 118.5
AUTOFOCUS_DITHER_AMPLITUDE_UM = 2.0
ALIGNMENT_OFFSET_UM = 0.4


class SimulatedDevice:
    """Device under test simulator."""

    def __init__(self, serial_number: str) -> None:
        self.serial_number = serial_number
        self._is_powered = False

    @property
    def is_powered(self) -> bool:
        """Whether the device is powered on."""
        return self._is_powered

    def power_on(self) -> None:
        """Power the device on."""
        self._is_powered = True

    def power_off(self) -> None:
        """Power the device off."""
        self._is_powered = False

    def read_firmware_version(self) -> str:
        """Read the firmware version.

        Returns:
            str: firmware version
        """
        return FIRMWARE_VERSION

    def measure_supply_voltage(self) -> float:
        """Measure the supply voltage.

        Returns:
            float: supply voltage in volts
        """
        return SUPPLY_VOLTAGE_V

    def measure_idle_current(self) -> float:
        """Measure the current drawn while idle.

        Returns:
            float: idle current in milliamperes
        """
        return IDLE_CURRENT_MA

    def sweep_frequency_response(self) -> tuple[list[float], list[float]]:
        """Sweep the frequency response of the device.

        Returns:
            tuple[list[float], list[float]]: frequencies in hertz and gains in decibels
        """
        frequencies = [10 * 1.5**step for step in range(20)]
        gains = [
            -10 * log10(1 + (frequency / CUTOFF_FREQUENCY_HZ) ** 2)
            for frequency in frequencies
        ]
        return frequencies, gains

    def record_startup_current(self) -> tuple[list[float], list[float]]:
        """Record the current drawn during startup.

        Returns:
            tuple[list[float], list[float]]: times in milliseconds and currents in
                milliamperes
        """
        times = [step * 5 for step in range(60)]
        currents = [
            IDLE_CURRENT_MA + 40 * exp(-time / 60) * abs(sin(time / 25))
            for time in times
        ]
        return times, currents

    def measure_autofocus_coarse_peak(self) -> float:
        """Measure the coarse autofocus peak position.

        Returns:
            float: peak position in micrometres
        """
        return AUTOFOCUS_COARSE_PEAK_UM

    def measure_autofocus_fine_peak(self) -> float:
        """Measure the fine autofocus peak position.

        Returns:
            float: peak position in micrometres
        """
        return AUTOFOCUS_FINE_PEAK_UM

    def measure_autofocus_dither(self) -> float:
        """Measure the autofocus dither amplitude.

        Returns:
            float: dither amplitude in micrometres
        """
        return AUTOFOCUS_DITHER_AMPLITUDE_UM

    def measure_alignment_offset(self) -> float:
        """Measure the optical alignment offset.

        Returns:
            float: offset in micrometres
        """
        return ALIGNMENT_OFFSET_UM
