
import numpy as np
import pandas as pd
import sys

import scipy.interpolate

from code.makedbs import get_db


# constants
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

def cut_df(df):
	'''
	INPUT
		df: dataframe with lat and lon columns, pandas DataFrame
	OUTPUT
		dataframe windowed to desired range with lat/lon bins added
	'''

	df = df[df.lat > latmin]
	df = df[df.lat < latmax]
	df = df[df.lon > lonmin]
	df = df[df.lon < lonmax]

	df['lat_cut'] = pd.cut(df.lat, latbins, labels=latbins[1:])
	df['lon_cut'] = pd.cut(df.lon, lonbins, labels=lonbins[1:])

	return df

def make_feature_df(dblist):
	'''
	INPUT
		dblist: names of database tables, list of strings
		must be in ['assessment', 'business', 'sfpd', 
					'usc_age_gender', 'usc_household',
					'usc_pop', 'walkscore']
	OUTPUT
		feature matrix, pandas DataFrame
	'''

	df = pd.DataFrame()

	for db in dblist:
		print 'loading ', db
		sys.stdout.flush()

		# load database table
		df1 = get_db(db)

		# merge in lat/lon for census data from shapefile
		if db in ['usc_age_gender', 'usc_household', 'usc_pop']:
			df2 = get_db('usc_shapefile')
			df1 = df1.merge(df2, left_on = 'id2', right_on = 'geoid')

		df1 = cut_df(df1)

		# handling each table type
		if db == 'assessment':
			df1 = df1[['lat_cut', 'lon_cut', 'taxable_value']]
			df1 = df1.groupby(['lat_cut', 'lon_cut']).mean()
			df1 = df1.reset_index().dropna()

		elif db == 'business':
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
			df1['ncrimes'] = 1
			df1 = df1.groupby(['lat_cut', 'lon_cut']).count()
			df1 = df1.dropna().reset_index()
			df1 = df1[['lat_cut', 'lon_cut', 'ncrimes']]

		elif db == 'usc_age_gender':
			df1 = df1.groupby(['lat_cut', 'lon_cut']).sum()
			df1 = df1.dropna().reset_index()
			df1['sgnf'] = (2 * df1.f / df1.total).fillna(0) - 1
			df1 = df1[['lat_cut', 'lon_cut', 'sgnf']]

		elif db == 'usc_household':
			df1 = df1.groupby(['lat_cut', 'lon_cut']).sum()
			df1 = df1.dropna().reset_index()

			# calc average household size
			total_p = 0
			p_range = range(1,8)
			for i in p_range:
				col = 'p' + str(i)
				total_p += df1[col] * i
			av_p = total_p / df1.total
			df1['avg_hh_size'] = av_p
			df1.fillna(0, inplace = True)

			df1 = df1[['lat_cut', 'lon_cut', 'avg_hh_size']]

		elif db == 'usc_pop':
			df1 = df1.groupby(['lat_cut', 'lon_cut']).sum()
			df1 = df1.dropna().reset_index()
			df1 = df1[['lat_cut', 'lon_cut', 'total']]
			df1.columns = ['lat_cut', 'lon_cut', 'pop']

		elif db == 'walkscore':
			df1 = df1.groupby(['lat_cut', 'lon_cut']).mean()
			df1 = df1.dropna().reset_index()
			df1 = df1[['lat_cut', 'lon_cut', 'walkscore']]

		# append results to final data frame
		if df.shape == (0, 0):
			df = df1.copy()
		else:
			df = df.merge(df1, on=['lat_cut', 'lon_cut'],
						  how='outer').fillna(0)
	return df





















