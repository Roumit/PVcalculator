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
    tus = Location(longitude=longitude, latitude=latitude, tz='Etc/GMT-2', altitude=300, name='Kiev')
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

    # Calculate angle from sun to panel, decrese dni when angle in too small


#    for i in range(0,241,1):
#        if zenith[i] > 80:
#            dni[i] = dni[i]/10
    dhi = []
    for i in cs['dhi']:
        dhi.append(i)
    ghi = []
    for i in cs['ghi']:
        ghi.append(i)

    plot_day_tyme = []
    for i in range (0, 241, 1):
        plot_day_tyme.append(i/10)

#    solar.plot()
#    plt.axis(xmin=0, xmax=24)
#    plt.show(block = True)

    # Azimut of sunrise and sunset
    sunrize_az = 0
    sunset_az = 0
    for i in range(0,241,1):
        if sunrize_az == 0:
            if zenith[i] < 90:
                print(i)
                sunrize_az = azimuth[i]
        elif sunset_az ==0:
            if zenith[i] > 90:
                print(i)
                sunset_az = azimuth[i]

    # Azimut of sunrise and sunset +15grad elevation
    sunrize_az_15 = 0
    sunset_az_15 = 0
    for i in range(0,241,1):
        if sunrize_az_15 == 0:
            if zenith[i] < 75:
                print(i)
                sunrize_az_15 = azimuth[i]
        elif sunset_az_15 ==0:
            if zenith[i] > 75:
                print(i)
                sunset_az_15 = azimuth[i]

    print(f"sunrize azimuth = {sunrize_az}\nsunset azimuth = {sunset_az}\n+- from South = {(sunset_az - sunrize_az)/2}")
    print(f"sunrize+15 azimuth = {sunrize_az_15}\nsunset-15 azimuth = {sunset_az_15}\n+- from South = {(sunset_az_15 - sunrize_az_15)/2}")

    zenith_series = pd.Series(zenith, plot_day_tyme)
    azimuth_series = pd.Series(azimuth, plot_day_tyme)
    dni_series = pd.Series(dni, plot_day_tyme)
    dhi_series = pd.Series(dhi, plot_day_tyme)
    ghi_series = pd.Series(ghi, plot_day_tyme)
    ir = pvlib.pvsystem.PVSystem.get_irradiance(system, solar_zenith=zenith_series, solar_azimuth=azimuth_series, dni=dni_series, dhi=dhi_series, ghi=ghi_series)
#    print(ir)
#    ir.plot()
#    plt.show(block = True)

    pv_watt = system.pvwatts_dc(g_poa_effective=ir["poa_global"], temp_cell=temp_cell)
    return pv_watt


Test = PVpower(pv_tilt=35, pv_azimuth=270, pv_power=280, pv_num=100, from_date='2018-04-19', to_date='2018-04-20',
               latitude=50, longitude=30.5, temp_cell=30)
Test_1 = PVpower(pv_tilt=35, pv_azimuth=90, pv_power=280, pv_num=100, from_date='2018-04-19', to_date='2018-04-20',
                latitude=50, longitude=30.5, temp_cell=30)
Test_2 = PVpower(pv_tilt=35, pv_azimuth=180, pv_power=280, pv_num=200, from_date='2018-04-19', to_date='2018-04-20',
                latitude=50, longitude=30.5, temp_cell=30)
print(type(Test))
# Test.plot()

plot_day_tyme = []
for i in range (0, 241, 1):
    plot_day_tyme.append(i/10)

first = []
first_wh = 0
for i in Test:
    first.append(i)
    first_wh += i/10

second = []
secont_wh = 0
for i in Test_1:
    second.append(i)
    secont_wh += i/10

first_1 = []
first_1_wh = 0
for i in range(0,241,1):
    first_1.append(first[i] + second[i])
    first_1_wh += (first[i] + second[i])/10

third = []
third_wh = 0
for i in Test_2:
    third.append(i)
    third_wh += i

print(f"Wh south = {third_wh}\nWh E-W = {first_1_wh}")
plt.plot(plot_day_tyme, first_1, plot_day_tyme, third, plot_day_tyme, first, plot_day_tyme, second)

plt.axis(xmin=0, xmax=24)
plt.show(block = True)
