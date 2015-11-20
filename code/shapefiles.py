# dealing with shapefiles

import numpy as np
import pandas as pd
import code.pyshp.shapefile as shapefile
import warnings

from shapely.geometry import Polygon, mapping
import shapely.ops

from code.shapes import make_polys

def sf_to_df(filename):
	'''
	INPUT
		filename: string
	OUTPUT
		shapefile records; pandas DataFrame

	Converts shapefile records from US Census 2010 to dataframe.
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


def get_shapefiles(filename):
	'''
	path to dbf file
	list of polygons
	'''
	sf = shapefile.Reader(filename)
	polys = map(lambda x: Polygon(x.points), sf.shapes())
	return polys

def merge_shapefiles(latlon, filename):
	'''
	latlon df, path to dbf
	df with polys column
	'''
	shapedf = sf_to_df(filename)
	shapedf = shapedf[['lat', 'lon']]
	shapedf['polys'] = get_shapefiles(filename)
	mergedf = latlon.merge(shapedf, left_on=['lat', 'lon'],
					   	   right_on=['lat', 'lon'])
	return mergedf

def make_shapefiles(latlon, polys, cnum):
	'''
	latlon df, shapefile polygons, cnum list of cluster numbers

	'''
	
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		parr = pd.Series(polys)
		validbool = map(lambda x: x.is_valid, parr)

	df = latlon.copy()
	df['cnum'] = cnum
	cxpolys = make_polys(df)

	neibs = []
	for i, c in enumerate(cnum.unique()):
	    sub = parr[(np.array(cnum) == c) & (np.array(validbool))]
	    group = shapely.ops.cascaded_union(list(sub))
	    neibs.append(group.union(cxpolys[i]))

	return neibs

def list_(*args): return list(args)


def make_json(polys, clist, mapnos, fnames, fbars):
	# all polygons
	featurelist = []
	for i, poly in enumerate(polys):
	    featurelist.append({"type": "Feature",
	                        "properties": {
	                        "color": clist[i],
	                        "mapno": mapnos[i],
	                        "neibno": i,
	                        "bars" : map(list_, fnames, fbars.ix[i].values.tolist())
	                        },
	                        "geometry": mapping(poly)
	                        })
	    
	geojson = {"type": "FeatureCollection",
	           "features": featurelist}

	return geojson

