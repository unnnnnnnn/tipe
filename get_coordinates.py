import datetime as dt
import numpy as np
import ephem
import pandas as pd
import time
import os
import pytz
from tzwhere import tzwhere

os.chdir(os.path.dirname(__file__))

def setup(latitude, longitude, altitude):
    import ephem

    obs = ephem.Observer()
    obs.lat = str(latitude)
    obs.lon = str(longitude)
    obs.elevation = altitude

    sun = ephem.Sun()
    return obs, sun

def get_coordinates(time, latitude, longitude, altitude=0):

    try:
        time_utc = time.tz_convert('UTC')
    except TypeError:
        time_utc = time

    sun_coords = pd.DataFrame(index=time)

    obs, sun = setup(latitude, longitude, altitude)

    alts = []
    azis = []
    for thetime in time_utc:
        obs.date = ephem.Date(thetime)
        sun.compute(obs)
        alts.append(np.rad2deg(sun.alt))
        azis.append(np.rad2deg(sun.az))

    sun_coords['elevation'] = alts
    sun_coords['azimuth'] = azis

    return sun_coords

lat = 48.866667
lon = 2.333333

tzwhere = tzwhere.tzwhere()
tz = tzwhere.tzNameAt(lat, lon)
print(tz)

day = dt.datetime.today()
midnight = day.replace(hour=0, minute=0, second=0, microsecond=0)
times = pd.date_range(start=midnight, freq="30min", periods=48)

df = get_coordinates(times, lat, lon)

file_name = "data/position_th/{}.csv".format(str(day)[:11])
df.to_csv(file_name)