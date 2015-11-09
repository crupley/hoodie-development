
import numpy as np
import pandas as pd

import scipy.interpolate


latmin = 37.70784
latmax = 37.8195
lonmin = -122.5185
lonmax = -122.35454

latbins = np.linspace(latmin, latmax, 100)
lonbins = np.linspace(lonmin, lonmax, 100)

def make_plotmesh(x, y, z):
    xi, yi = np.meshgrid(x, y)
    
    rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    zi = rbf(xi, yi)
    
    return xi, yi, zi

def cut_df(df, how='mean'):
	'''
	df with df.lat and df.lon
	Window df down to lat/lon range
	bin values; mean, sum, count
	'''

	df = df[df.lat > latmin]
	df = df[df.lat < latmax]
	df = df[df.lon > lonmin]
	df = df[df.lon < lonmax]

	df['lon_cut'] = pd.cut(df.lon, lonbins, labels=lonbins[1:])
	df['lat_cut'] = pd.cut(df.lat, latbins, labels=latbins[1:])

	return df