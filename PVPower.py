import os

import itertools

import matplotlib.pyplot as plt

import pandas as pd

import pvlib
from pandas import DatetimeIndex

from pvlib import clearsky, atmosphere, solarposition

from pvlib.location import Location

# from pvlib.iotools import read_tmy3

tus = Location(30.5, 50, 'Etc/GMT-3', 300, 'Kiev')

Times = pd.date_range(start='2017-07-01', end='2017-07-02', freq='1min', tz=tus.tz) # DatetimeIndex(start='2017-07-01', end='2017-07-02', freq='1min', tz=tus.tz)
# print(Times)

cs = tus.get_clearsky(Times)  # ineichen with climatology table by default

# print(cs)

cs.plot()
plt.ylabel('Irradiance $W/m^2$')
plt.title('Ineichen, climatological turbidity')

plt.show(block = True)
