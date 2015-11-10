
import numpy as np
import pandas as pd

import scipy.interpolate

from code.makedbs import get_db


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

	df['lat_cut'] = pd.cut(df.lat, latbins, labels=latbins[1:])
	df['lon_cut'] = pd.cut(df.lon, lonbins, labels=lonbins[1:])

	return df

def make_feature_df(dblist):

	df = pd.DataFrame()

	for db in dblist:
		print 'loading ', db
		df1 = get_db(db)
		df1 = cut_df(df1)
		if db == 'assessment':
			#df1 = get_db(db)
			#df1 = cut_df(df1)
			df1 = df1[['lat_cut', 'lon_cut', 'taxable_value']]
			df1 = df1.groupby(['lat_cut', 'lon_cut']).mean()
			df1 = df1.reset_index().dropna()

		elif db == 'business':
			#df1 = get_db(db)
			#df1 = cut_df(df1)
			df1 = df1[['lat_cut', 'lon_cut', 'category']]
			df1['count'] = 1
			df1 = df1.groupby(['lat_cut', 'lon_cut', 'category']).count()
			df1 = df1.reset_index().dropna()
			df2 = df1.pivot(columns = 'category', values = 'count').fillna(0)
			df1 = df1.merge(df2, left_index=True, right_index=True)
			df1.drop('category', axis = 1, inplace = True)
			df1 = df1.groupby(['lat_cut', 'lon_cut']).sum().reset_index()
			df1 = df1[['lat_cut', 'lon_cut', 'grocery',
					   'restaurant', 'retail']]

		elif db == 'sfpd':
			df1['count'] = 1
			df1 = df1.groupby(['lat_cut', 'lon_cut']).count()
			df1 = df1.dropna().reset_index()
			df1 = df1[['lat_cut', 'lon_cut', 'count']]



		if df.shape == (0, 0):
			df = df1.copy()
		else:
			df = df.merge(df1, on=['lat_cut', 'lon_cut'],
						  how='outer').fillna(0)

	return df





















