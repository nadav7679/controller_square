import asyncio
from .Buffer import Buffer
from datetime import datetime
import numpy as np
from random import random

class Sensor:
    """
    Base class for all sensors.
    """
    def __init__(self, name, buffer_size = 10000, sample_rate = 0.0005):
        self._name = name
        self._buffer_size = buffer_size
        self._sample_rate = sample_rate

        self.buffer = Buffer(
            buffer_size,
            [('value', np.float64), ('corr_value', np.float64), ('timestamp', np.float64)]
        )

        self._active = False

    def toggle(self, state: bool):
        """Toggles the sensor on or off.

        Args:
            state (bool): `True` to turn the sensor on, `False` to turn it off.
        """
        self._active = state

        loop = asyncio.get_running_loop()
        loop.create_task(self.loop())

    # === Physical ===
    async def read_sensor(self) -> float:
        """Reads sensor input from physical GPIO pins.

        Returns:
            float: Raw sensor input.
        """
        # TODO: Implement GPIO reading
        return np.sin(datetime.now().timestamp()) + 0.2 * random()

    # === Smoothing ===
    def filter_reading(self, raw: float) -> float:
        """Smoothes raw sensor input based on historical data.

        Args:
            raw (float): Raw sensor output.

        Returns:
            float: Smoothed sensor output.
        """
        # TODO: Implement smoothing algorithm

        # (13-11) some notes on smoothing algorithms (https://plotly.com/python/smoothing/) using scipy
        # 1. Savitzky-Golay Filter - interpolating polynomials
        # 2. Moving Averages (simple and triangular)
            # - triangular moving averages gives more weight to more recent datapoints, hence its probably more preferable than poly interp 
            #   and simple average 
        
        
        return raw + 1

    # === Main Loop ===
    async def loop(self):
        """
        Main loop for the sensor. Will execute until `self._active` is set to
        `False`, and repeats every `self._sample_rate` seconds.
        """
        while self._active:
            raw = await self.read_sensor()
            self.buffer += (
                raw,
                self.filter_reading(raw),
                datetime.now().timestamp()
            )
            await asyncio.sleep(self._sample_rate)
