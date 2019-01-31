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

Times = pd.date_range(start='2017-12-01', end='2017-12-02', freq='1min', tz=tus.tz) # DatetimeIndex(start='2017-07-01', end='2017-07-02', freq='1min', tz=tus.tz)
# print(Times)

cs = tus.get_clearsky(Times)  # ineichen with climatology table by default

# print(type(cs["ghi"].at['2017-12-01 00:09:00+03:00']))



cs['ghi'].plot()
plt.contour
plt.ylabel('Irradiance $W/m^2$')
plt.title('Ineichen, climatological turbidity')

# plt.show(block = True)

# print(dict(cs['ghi']))

file_csv = open("day-clear.csv" , 'w')

min = 0
for i in cs['ghi']:
    min += 1
    hours = min/60
#    print(type(i))
    file_csv.write(str(hours))
    file_csv.write(";")
    file_csv.write(str(i))
    file_csv.write("\n")
file_csv.close()

file_read = open("day-clear.csv" , 'r')
text = file_read.readline(823)
print(len(text))
print(text)

