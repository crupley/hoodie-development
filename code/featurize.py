
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

import scipy.interpolate
from scipy.interpolate import Rbf
from sklearn.preprocessing import StandardScaler

from code.makedbs import get_db

def bin_interpolate(datax, datay, dataz, interpx, interpy, smooth=0):
	rbf = scipy.interpolate.Rbf(datax, datay, dataz,
								function='linear', smooth=smooth)
	interpz = rbf(interpx, interpy)
	return interpz


def window(df, latmin, latmax, lonmin, lonmax):
    df = df[df.lat > latmin]
    df = df[df.lat < latmax]
    df = df[df.lon > lonmin]
    df = df[df.lon < lonmax]
    return df

def dist(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return np.sqrt(dlat**2 + dlon**2)

def dist_by_node(node1, node2, df):
	lat1, lon1 = df.ix[node1][['lat', 'lon']]
	lat2, lon2 = df.ix[node2][['lat', 'lon']]
	return dist(lat1, lon1, lat2, lon2)

def fdist(f1, f2):
	'''

	feature distance
	'''
	return np.linalg.norm(f1-f2)**2

def fdist_by_node(n1, n2, df):
	f1 = df.ix[n1]
	f2 = df.ix[n2]
	return fdist(f1, f2)

	

def angle(testnode, neib1, neib2):
    v1 = testnode[['lat', 'lon']] - neib1[['lat', 'lon']]
    v2 = testnode[['lat', 'lon']] - neib2[['lat', 'lon']]
    return np.arccos(v1.dot(v2) / np.linalg.norm(v1) / np.linalg.norm(v2)) * 180 / np.pi


def find_closest(testnode, df, nneibs = 4, anglelim = 45):
	neibs = window(df, testnode.lat - 0.005,
                   	   testnode.lat + 0.005,
                   	   testnode.lon - 0.003,
                   	   testnode.lon + 0.003)

	neibs = neibs[['lat', 'lon']]
	neibs.drop(testnode.name, axis=0, inplace=True)

	if neibs.shape[0] == 0: return []

	neibs['dist'] = neibs.apply(lambda x: dist(x.lat, x.lon,
											   testnode.lat, testnode.lon),
								axis=1)
	neibs = neibs.sort_values('dist')

	closeix = [neibs.index[0]]
	i = 0
	while len(closeix) < nneibs:
	    i += 1
	    if len(neibs.index) < (i + 1):
	    	break
	    idx = neibs.index[i]
	    angles = [angle(testnode, neibs.ix[idx], neibs.ix[j]) for j in closeix]
	    if np.all(np.array(angles) > anglelim):
	        closeix.append(idx)
	return closeix



class featurizer():

	def __init__(self):
		self.features = pd.DataFrame()
		self.fsmooth = pd.DataFrame()

		self.latmin = 37.70784
		self.latmax = 37.8195
		self.lonmin = -122.5185
		self.lonmax = -122.35454

		self.latbins = np.linspace(self.latmin, self.latmax, 101)
		self.lonbins = np.linspace(self.lonmin, self.lonmax, 101)

		self.shapefile = self.window(get_db('usc_shapefile'))

		self.nodelat = self.shapefile.lat
		self.nodelon = self.shapefile.lon

		self.edges = None

		self.allfeatures = ['taxable_value', 'grocery', 'restaurant', 
							'retail', 'ncrimes', 'sgnf',
							'avg_hh_size', 'population', 'walkscore']

		self.alltables = ['assessment', 'business', 'sfpd', 
						  'usc_age_gender', 'usc_household',
						  'usc_pop', 'walkscore']

		self.featurenames = {'taxable_value': 'Property Value',
							 'grocery': 'Grocery',
							 'restaurant': 'Restaurants',
							 'retail': 'Retail',
							 'ncrimes': 'Crime',
							 'sgnf': 'Female:Male ratio',
							 'avg_hh_size': 'Household Size',
							 'population': 'Population',
							 'walkscore': 'Walkscore'}

		self.smoothing = {'taxable_value': 0.01,
						  'grocery': 0.1,
						  'restaurant': 0.01,
						  'retail': 0.3,
						  'ncrimes': 0.1,
						  'sgnf': 0.01,
						  'avg_hh_size': 0.1,
						  'population': 1,
						  'walkscore': 0}

	def window(self, df):
		df = df[df.lat > self.latmin]
		df = df[df.lat < self.latmax]
		df = df[df.lon > self.lonmin]
		df = df[df.lon < self.lonmax]
		df = df.reset_index()
		return df

	def binlatlon(self, df):
		df['lat_cut'] = pd.cut(df.lat, self.latbins,
							   labels = self.latbins[1:])
		df['lon_cut'] = pd.cut(df.lon, self.lonbins,
							   labels = self.lonbins[1:])
		return df

	def set_limits(self, latmin, latmax, lonmin, lonmax):
		self.latmin = latmin
		self.latmax = latmax
		self.lonmin = lonmin
		self.lonmax = lonmax


	def set_bin_resolution(self, npoints):
		self.latbins = np.linspace(latmin, latmax, npoints)
		self.lonbins = np.linspace(lonmin, lonmax, npoints)

	def plot(self, featurelist):
		nplots = len(featurelist)
		plt.figure(figsize = (16, 16*nplots))
		for i in xrange(1, nplots + 1):
			plt.subplot(nplots,1,i)
			plt.scatter(self.fsmooth.lon, self.fsmooth.lat,
					c=self.fsmooth[featurelist[i-1]], linewidths = 0)
			plt.colorbar()
			plt.axis('equal')
			plt.margins(0)
			ax = plt.gca()
			ax.set_axis_bgcolor('black')
			ax.get_xaxis().get_major_formatter().set_useOffset(False)
			plt.title(featurelist[i-1])
			plt.xlabel('Longitude')
			plt.ylabel('Latitude')


	def add_features(self, flist, how='usc', verbose=False):

		for f in flist:
			if verbose: print 'loading ', f; sys.stdout.flush()

			# load database table
			df1 = get_db(f)
			
			# merge in lat/lon for census data from shapefile
			if f in ['usc_age_gender', 'usc_household', 'usc_pop']:
				df1 = df1.merge(self.shapefile, left_on = 'id2',
								right_on = 'geoid')

			df1 = self.window(df1)

			# handling each table type
			if f == 'assessment':
				df1 = self.binlatlon(df1)
				df1 = df1[['lat_cut', 'lon_cut', 'taxable_value']]
				df1 = df1.groupby(['lat_cut', 'lon_cut']).mean()
				df1 = df1.reset_index().dropna()
				df1.columns = ['lat', 'lon', 'taxable_value']

			elif f == 'business':
				df1 = self.binlatlon(df1)
				df1 = df1[['lat_cut', 'lon_cut', 'category']]
				df1['count'] = 1
				df1 = df1.groupby(['lat_cut', 'lon_cut', 'category']).count()
				df1 = df1.reset_index().dropna()
				df2 = df1.pivot(columns = 'category',
								values = 'count').fillna(0)
				df1 = df1.merge(df2, left_index=True, right_index=True)
				df1.drop('category', axis = 1, inplace = True)
				df1 = df1.groupby(['lat_cut', 'lon_cut']).sum().reset_index()
				df1 = df1[['lat_cut', 'lon_cut', 'grocery',
						   'restaurant', 'retail']]
				df1.columns = ['lat', 'lon', 'grocery',
							   'restaurant', 'retail']

			elif f == 'sfpd':
				df1 = self.binlatlon(df1)
				df1['ncrimes'] = 1
				df1 = df1.groupby(['lat_cut', 'lon_cut']).count()
				df1 = df1.dropna().reset_index()
				df1 = df1[['lat_cut', 'lon_cut', 'ncrimes']]
				df1.columns = ['lat', 'lon', 'ncrimes']

			elif f == 'usc_age_gender':
				df1['sgnf'] = (2 * df1.f / df1.total).fillna(0) - 1
				df1 = df1[['lat', 'lon', 'sgnf']]

			elif f == 'usc_household':

				# calc average household size
				total_p = 0
				p_range = range(1,8)
				for i in p_range:
					col = 'p' + str(i)
					total_p += df1[col] * i
				av_p = total_p / df1.total
				df1['avg_hh_size'] = av_p
				df1.fillna(0, inplace = True)

				df1 = df1[['lat', 'lon', 'avg_hh_size']]

			elif f == 'usc_pop':
				df1 = df1[['lat', 'lon', 'total']]
				df1.columns = ['lat', 'lon', 'population']

			elif f == 'walkscore':
				df1 = df1[['lat', 'lon', 'walkscore']]

			# append results to final data frame
			for col in df1.columns[2:]:
				finterp = bin_interpolate(df1.lon, df1.lat, df1[col],
									  self.nodelon, self.nodelat)
				finterp = pd.Series(finterp, name = col)

				if self.features.shape == (0, 0):
					self.features = pd.concat((self.nodelat, self.nodelon,
											   finterp), axis = 1)
				else:
					self.features = pd.concat((self.features, finterp),
											  axis = 1)
	def smooth_features(self):
		self.fsmooth = self.features.copy()
		cols = self.features.drop(['lat', 'lon'], axis=1).columns

		if 'sgnf' in cols:
			# scale gender ratio by population
			if 'population' not in cols:
				self.add_features(['usc_pop'])

		if 'taxable_value' in cols:
			# log transform taxable value
			self.fsmooth.taxable_value[self.fsmooth.taxable_value < 0] = 0
			self.fsmooth.taxable_value = np.log(self.fsmooth.taxable_value+1)

		for col in cols:
			rbf = Rbf(self.features.lon, self.features.lat, 
					  self.fsmooth[col], function='linear',
					  smooth = self.smoothing[col])
			self.fsmooth[col] = rbf(self.features.lon, self.features.lat)

		# scale to zero mean, unit standard deviation
		ssc = StandardScaler()
		self.fsmooth.iloc[:,2:] = ssc.fit_transform(self.fsmooth.iloc[:,2:])



		
	def make_edges(self):
		edgelambda = lambda x: find_closest(x, df)
		self.edges = self.features.apply(edgelambda, axis = 1)



if __name__ == '__main__':
	
	f = featurizer()
	### if file not exists
	print 'Making features'
	f.add_features(f.alltables, verbose=True)

	### if file not exists
	print 'Making edges'
	f.make_edges()










