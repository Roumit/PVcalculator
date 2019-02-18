import os

import itertools

import matplotlib.pyplot as plt

import pandas as pd

import pvlib
from pandas import DatetimeIndex

from pvlib import clearsky, atmosphere, solarposition

from pvlib.location import Location

# from pvlib.iotools import read_tmy3

# PV pframeters
# pv_tilt = 30
# pv_azimuth = 180
# pv_power = 280
# pv_num = 90
# from_date = "2017-06-21"
# to_date = "2017-06-22"


# pv_w = pv_num * pv_power

def PVpower(pv_tilt, pv_azimuth, pv_power, pv_num, from_date, to_date, latitude, longitude, temp_cell):
    tus = Location(longitude=longitude, latitude=latitude, tz='Etc/GMT-3', altitude=300, name='Kiev')
    Times = pd.date_range(start=from_date, end=to_date, freq='6min', tz=tus.tz)
    cs = tus.get_clearsky(Times)
    module_parameters = {'pdc0': pv_power * pv_num, 'gamma_pdc': -0.004}
    system = pvlib.pvsystem.PVSystem(surface_tilt=pv_tilt, surface_azimuth=pv_azimuth,
                                 albedo=None, surface_type=None, module=None,
                                 module_parameters=module_parameters, modules_per_string=1,
                                 strings_per_inverter=1, inverter=None,
                                 inverter_parameters=None, racking_model='open_rack_cell_glassback',
                                 losses_parameters=None, name=None)
    solar = pvlib.solarposition.get_solarposition(time=Times, latitude=latitude, longitude=longitude)
    zenith = []
    for i in solar['zenith']:
        zenith.append(i)
    azimuth = []
    for i in solar['azimuth']:
        azimuth.append(i)
    dni = []
    for i in cs['dni']:
        dni.append(i)
    dhi = []
    for i in cs['dhi']:
        dhi.append(i)
    ghi = []
    for i in cs['ghi']:
        ghi.append(i)

    plot_day_tyme = []
    for i in range (0, 241, 1):
        plot_day_tyme.append(i/10)

    day_irr= []
    for i in cs['ghi']:
        day_irr.append(i)

    zenith_series = pd.Series(zenith, plot_day_tyme)
    azimuth_series = pd.Series(azimuth, plot_day_tyme)
    dni_series = pd.Series(dni, plot_day_tyme)
    dhi_series = pd.Series(dhi, plot_day_tyme)
    ghi_series = pd.Series(ghi, plot_day_tyme)
    ir = pvlib.pvsystem.PVSystem.get_irradiance(system, solar_zenith=zenith_series, solar_azimuth=azimuth_series, dni=dni_series, dhi=dhi_series, ghi=ghi_series)
    # plt.plot(ir)
    pv_watt = system.pvwatts_dc(g_poa_effective=ir["poa_global"], temp_cell=temp_cell)
    return pv_watt


Test = PVpower(pv_tilt=30, pv_azimuth=180, pv_power=280, pv_num=100, from_date='2017-06-21', to_date='2017-06-22',
               latitude=30.5, longitude=50, temp_cell=30)
Test_1 = PVpower(pv_tilt=30, pv_azimuth=90, pv_power=280, pv_num=100, from_date='2017-06-21', to_date='2017-06-22',
               latitude=30.5, longitude=50, temp_cell=30)
print(type(Test))
# Test.plot()

plot_day_tyme = []
for i in range (0, 241, 1):
    plot_day_tyme.append(i/10)

first = []
for i in Test:
    first.append(i)

second = []
for i in Test_1:
    second.append(i)

plt.plot(plot_day_tyme, first, plot_day_tyme, second)

plt.axis(xmin=0, xmax=24)
plt.show(block = True)






tus = Location(30.5, 50, 'Etc/GMT-3', 300, 'Kiev')

Times = pd.date_range(start='2017-06-21', end='2017-06-22', freq='6min', tz=tus.tz) # DatetimeIndex(start='2017-07-01', end='2017-07-02', freq='1min', tz=tus.tz)
Times_2 = pd.date_range(start='2017-01-21', end='2017-01-22', freq='6min', tz=tus.tz) # DatetimeIndex(start='2017-07-01', end='2017-07-02', freq='1min', tz=tus.tz)

# print(Times)

cs = tus.get_clearsky(Times)  # ineichen with climatology table by default
cs_2 = tus.get_clearsky(Times_2)  # ineichen with climatology table by default


module_parameters = {'pdc0': 315, 'gamma_pdc': -0.004}
system = pvlib.pvsystem.PVSystem(surface_tilt=15, surface_azimuth=90,
                                 albedo=None, surface_type=None, module=None,
                                 module_parameters=module_parameters, modules_per_string=1,
                                 strings_per_inverter=1, inverter=None,
                                 inverter_parameters=None, racking_model='open_rack_cell_glassback',
                                 losses_parameters=None, name=None)

# print(system.pvwatts_dc(800, 30))

solar_2106 = pvlib.solarposition.get_solarposition(time=Times, latitude=50, longitude=30.5)
solar_2101 = pvlib.solarposition.get_solarposition(time=Times_2, latitude=50, longitude=30.5)

# print(pvlib.solarposition.get_sun_rise_set_transit(Times, 30.5, 50))

zenith_2106 = []
for i in solar_2106['zenith']:
    zenith_2106.append(i)
azimuth_2106 = []
for i in solar_2106['azimuth']:
    azimuth_2106.append(i)
dni_2106 = []
for i in cs['dni']:
    dni_2106.append(i)
dhi_2106 = []
for i in cs['dhi']:
    dhi_2106.append(i)
ghi_2106 = []
for i in cs['ghi']:
    ghi_2106.append(i)

print(type(solar_2106))

plot_day_tyme = []
day_irr_2106= []
day_irr_2101= []

for i in cs['ghi']:
    day_irr_2106.append(i)

for i in cs_2['ghi']:
    day_irr_2101.append(i)

for i in range (0, 241, 1):
    plot_day_tyme.append(i/10)

zenith_2106_series = pd.Series(zenith_2106, plot_day_tyme)
azimuth_2106_series = pd.Series(azimuth_2106, plot_day_tyme)
dni_2106_series = pd.Series(dni_2106, plot_day_tyme)
dhi_2106_series = pd.Series(dhi_2106, plot_day_tyme)
ghi_2106_series = pd.Series(ghi_2106, plot_day_tyme)
# print(zenith_2106_series)

ir = pvlib.pvsystem.PVSystem.get_irradiance(system, solar_zenith=zenith_2106_series, solar_azimuth=azimuth_2106_series, dni=dni_2106_series, dhi=dhi_2106_series, ghi=ghi_2106_series)

# print(ir)
# plt.plot(ir)

pv_watt = system.pvwatts_dc(g_poa_effective=ir["poa_global"], temp_cell=30)

# print(pv_watt)
# pv_watt.plot()

# for i in range (0,241):
#     ir = pvlib.pvsystem.PVSystem.get_irradiance(system, solar_zenith=zenith_2106_series, solar_azimuth=azimuth_2106_series, dni=dni_2106[i], dhi=dhi_2106[i], ghi=ghi_2106[i])

#    pv_watt.append(system.pvwatts_dc(ir, 30))


# power_time = system.get_aoi(solar_2106['zenith'], solar_2106['azimuth'])

# system.get_irradiance(system, solar_2106['zenith'], solar_2106['azimuth'], dni=cs['dni'], dhi=cs['dhi'], ghi=cs['ghi'])

# print(power_time)


# cs.plot()

# power_time.plot()

# solar.plot()



# print(day_irr_2107)



# cs_param.append(plot_day_tyme)
# cs_param.append(plot_day_tyme)

# print(cs_param)

# plt.plot(cs_param)

# plt.plot(plot_day_tyme, day_irr_2101, plot_day_tyme, pv_watt)

# plt.ylabel('Irradiance $W/m^2$')
# plt.title('GHI 21 июня и 21 декабря')
# plt.axis(xmin=0, xmax=24)
# plt.show(block = True)

"""

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
"""
