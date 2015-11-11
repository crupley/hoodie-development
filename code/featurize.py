
import numpy as np
import pandas as pd
import sys
from itertools import combinations
from time import time

import scipy.interpolate

from code.makedbs import get_db


# constants
latmin = 37.70784
latmax = 37.8195
lonmin = -122.5185
lonmax = -122.35454

latbins = np.linspace(latmin, latmax, 101)
lonbins = np.linspace(lonmin, lonmax, 101)

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

def bin_interpolate(datax, datay, dataz, interpx, interpy):
	rbf = scipy.interpolate.Rbf(datax, datay, dataz, function='linear')
	interpz = rbf(interpx, interpy)
	return interpz


def make_feature_df(dblist, norm_to_pop=True, merge_type='inner',
					verbose=False):
	'''
	INPUT
		dblist: names of database tables, list of strings
			must be in ['assessment', 'business', 'sfpd', 
						'usc_age_gender', 'usc_household',
						'usc_pop', 'walkscore']
	OUTPUT
		feature matrix, pandas DataFrame
	'''
	dblist = dblist[:]
	if norm_to_pop:
		# population will be added if in list or not
		if 'usc_pop' in dblist:
			dblist.remove('usc_pop')
		dblist = ['usc_pop'] + dblist

	df = pd.DataFrame()

	for db in dblist:
		if verbose: print 'loading ', db; sys.stdout.flush()

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
						  how=merge_type).fillna(0)
	
	if norm_to_pop:
		# scale select columns by population
		scalecols = ['grocery', 'restaurant', 'retail', 'ncrimes']
		for col in scalecols:
			if col in df.columns:
				df[col] = (df[col]/df['pop']).replace(np.inf,np.nan).fillna(0)

	if verbose: print 'Complete'

	return df

def feature_permutations(levels):
	'''
	levels: list of length items to permute
	'''

	allfeatures = ['assessment', 'business', 'sfpd', 
               'usc_age_gender', 'usc_household',
               'usc_pop', 'walkscore']

	res = pd.DataFrame(columns = ('n', 'nodes', 'time', 'features'))
	for n in levels:
		print ''
		print n, 'length combinations'
		for db in combinations(allfeatures, n):
		    start_time = time()
		    dblist = list(db)
		    df = make_feature_df(dblist, norm_to_pop = False, verbose=False)
		    etime = time() - start_time
		    print n, df.shape[0], round(etime,1), dblist
		    d = {'n': n, 
		     'nodes': df.shape[0],
		     'features': dblist,
		     'time': etime}
		    res = res.append(d, ignore_index=True)
	return res
	# pickle.load(open('data/bin_overlap.pkl', 'rb'))


class featurizer():

	def __init__(self):
		self.features = pd.DataFrame()

		self.latmin = 37.70784
		self.latmax = 37.8195
		self.lonmin = -122.5185
		self.lonmax = -122.35454

		self.latbins = np.linspace(self.latmin, self.latmax, 101)
		self.lonbins = np.linspace(self.lonmin, self.lonmax, 101)

		df = get_db('usc_shapefile')
		df = df[df.lat > self.latmin]
		df = df[df.lat < self.latmax]
		df = df[df.lon > self.lonmin]
		df = df[df.lon < self.lonmax]
		self.shapefile = df



	def set_limits(self, latmin, latmax, lonmin, lonmax):
		self.latmin = latmin
		self.latmax = latmax
		self.lonmin = lonmin
		self.lonmax = lonmax


	def set_resolution(self, npoints):
		self.latbins = np.linspace(latmin, latmax, npoints)
		self.lonbins = np.linspace(lonmin, lonmax, npoints)

	def add_features(self, flist, how='usc', verbose=False):

		if how == 'usc':
			self.latbins = self.shapefile.lat
			self.lonbins = self.shapefile.lon

		for f in flist:
			if verbose: print 'loading ', db; sys.stdout.flush()

			# load database table
			df1 = get_db(f)

			# merge in lat/lon for census data from shapefile
			if f in ['usc_age_gender', 'usc_household', 'usc_pop']:
				df1 = df1.merge(self.shapefile, left_on = 'id2',
								right_on = 'geoid')

			# handling each table type
			if f == 'assessment':
				df1 = df1[['lat_cut', 'lon_cut', 'taxable_value']]
				df1 = df1.groupby(['lat_cut', 'lon_cut']).mean()
				df1 = df1.reset_index().dropna()

			# elif f == 'business':
			# 	df1 = df1[['lat_cut', 'lon_cut', 'category']]
			# 	df1['count'] = 1
			# 	df1 = df1.groupby(['lat_cut', 'lon_cut', 'category']).count()
			# 	df1 = df1.reset_index().dropna()
			# 	df2 = df1.pivot(columns = 'category', values = 'count').fillna(0)
			# 	df1 = df1.merge(df2, left_index=True, right_index=True)
			# 	df1.drop('category', axis = 1, inplace = True)
			# 	df1 = df1.groupby(['lat_cut', 'lon_cut']).sum().reset_index()
			# 	df1 = df1[['lat_cut', 'lon_cut', 'grocery',
			# 			   'restaurant', 'retail']]

			# elif f == 'sfpd':
			# 	df1['ncrimes'] = 1
			# 	df1 = df1.groupby(['lat_cut', 'lon_cut']).count()
			# 	df1 = df1.dropna().reset_index()
			# 	df1 = df1[['lat_cut', 'lon_cut', 'ncrimes']]

			elif f == 'usc_age_gender':
				df1['sgnf'] = (2 * df1.f / df1.total).fillna(0) - 1
				df1 = df1[['lat', 'lon', 'sgnf']]

			# elif f == 'usc_household':

			# 	# calc average household size
			# 	total_p = 0
			# 	p_range = range(1,8)
			# 	for i in p_range:
			# 		col = 'p' + str(i)
			# 		total_p += df1[col] * i
			# 	av_p = total_p / df1.total
			# 	df1['avg_hh_size'] = av_p
			# 	df1.fillna(0, inplace = True)

			# 	df1 = df1[['lat', 'lon', 'avg_hh_size']]

			# elif f == 'usc_pop':
			# 	df1 = df1.groupby(['lat_cut', 'lon_cut']).sum()
			# 	df1 = df1.dropna().reset_index()
			# 	df1 = df1[['lat_cut', 'lon_cut', 'total']]
			# 	df1.columns = ['lat', 'lon', 'pop']

			# elif f == 'walkscore':
			# 	df1 = df1[['lat', 'lon', 'walkscore']]

			finterp = bin_interpolate(df1.lon, df1.lat, df1.iloc[:,2],
									  self.lonbins, self.latbins)
			finterp = pd.Series(finterp)

			# append results to final data frame
			if self.features.shape == (0, 0):
				self.features = df2 = pd.concat((self.latbins, self.lonbins,
												 finterp), axis = 1)
				self.features.columns = df1.columns
			else:
				self.features = pd.concat((self.features, finterp), axis = 1)
				self.features.rename(columns = {0: df1.columns[-1]})





if __name__ == '__main__':
	res = feature_permutations()
	pickle.dump(res, open('data/bin_overlap.pkl', 'wb'))
	print 'Total elapsed time: ', res.time.sum()
	# pickle.load(open('data/bin_overlap.pkl', 'rb'))












