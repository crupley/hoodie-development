# dealing with shapefiles

import numpy as np
import pandas as pd
import code.pyshp.shapefile as shapefile

def sf_to_df(filename):
	'''
	converts shapefile records to dataframe
	'''
	sf = shapefile.Reader(filename)
	records = np.array(sf.records())
	rdf = pd.DataFrame(records)

	colnames = ['state',
				'county',
				'tract',
				'block',
				'geoid',
				'name',
				'mtfcc',
				'ur',
				'uace',
				'funcstat',
				'land_area',
				'water_area',
				'lat',
				'lon']
	rdf.columns = colnames

	rdf.geoid = rdf.geoid.astype('int')
	rdf.land_area = rdf.land_area.astype('int')
	rdf.water_area = rdf.water_area.astype('int')
	rdf.lat = rdf.lat.astype('float')
	rdf.lon = rdf.lon.astype('float')

	# drop empty columns
	rdf.drop(['ur', 'uace', 'funcstat'], axis=1, inplace=True)
	return rdf


