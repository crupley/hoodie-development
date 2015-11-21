
import numpy as np
import pandas as pd
import networkx as nx
import os
import matplotlib

from sklearn.metrics.pairwise import pairwise_distances
from shapely.geometry import mapping

from code.featurize import fdist
from code.shapefiles import merge_shapefiles, make_shapefiles


FDICT = {0: 'taxable_value',
         1: 'grocery',
         2: 'restaurant',
         3: 'retail',
         4: 'ncrimes',
         5: 'sgnf',
         6: 'avg_hh_size',
         7: 'population',
         8: 'walkscore'}

FNAMES = {'taxable_value': 'Property Value',
		  'grocery': 'Grocery',
		  'restaurant': 'Restaurants',
		  'retail': 'Retail',
		  'ncrimes': 'Crime',
		  'sgnf': 'Female:Male ratio',
		  'avg_hh_size': 'Household Size',
		  'population': 'Population',
		  'walkscore': 'Walkscore'}

def mapno2list(s):
	return [int(s[i] + s[i+1]) for i in range(len(s)) if i%2 == 0]


def list2mapno(featurenumlist):
	f = tuple(featurenumlist)
	return '%02d' * len(f) % f


def mapno2fname(s):
	featurenumlist = mapno2list(s)
	return [FDICT[i] for i in featurenumlist]


def bigsize(row):
	'''
	calculate biggest cluster in graph after each cut
	'''
	g.remove_edge(row.source, row.target)
	return len(max(nx.connected_components(g), key=len))


def cutcon(row, graph):
	'''
	return number of connected components after each cut
	'''
	graph.remove_edge(row.source, row.target)
	return nx.number_connected_components(graph)


def cutrow(row, graph):
	'''
	reduce graph from list of cuts
	'''
	graph.remove_edge(row.source, row.target)
	return

def make_graph(cutdf):
	g = nx.from_pandas_dataframe(cutdf, 'source', 'target')
	return g


def assign_clusters(nodelist, graph):
    cc = list(nx.connected_components(graph))
    
    cnum = pd.Series(-1, index=nodelist)
    for node in nodelist:
        for i, cluster in enumerate(cc):
            if node in cluster: cnum.ix[node] = i
    return cnum


def row_errorsq(row, cluster_means):
    rowf = row.drop(['cnum'])
    return (fdist(rowf, cluster_means.ix[int(row.cnum)]))


def wcss(featuredf, cnum):
    df = featuredf.copy()
    df['cnum'] = cnum    # features = df.drop(['lat', 'lon'], axis = 1)
    cluster_means = df.groupby('cnum').mean()
    df['errors'] = df.apply(lambda x: row_errorsq(x, cluster_means),
    							axis = 1)

    return df.groupby('cnum').sum()['errors']


def elbow_plot(cutdf, featuredf, maxk=30):
	'''
	calculate wcss vs k

	cutdf: list of cuts containing columns 'source', 'target', and 'nclusters'

	'''

	ks = []
	wcsses = []

	graph = make_graph(cutdf)

	nclusterslast = nx.number_connected_components(graph)
	# ks.append(nclusterslast)
	# wcsses

	for i in cutdf.index:
		nclusters = cutcon(cutdf.ix[i], graph)
		if nclusters > nclusterslast:
			# print i, nclusters
			nclusterslast = nclusters
			ks.append(nclusters)
			cnum = assign_clusters(featuredf.index, graph)
			wcsses.append(wcss(featuredf, cnum).sum())
			if nclusters >= maxk: return ks, wcsses


	# for k in ks:
	#     # rebuild full graph
	#     #g = nx.from_pandas_dataframe(edges, 'source', 'target')
	#     g = graph.copy()

	#     # reduces graph to i clusters
	#     cutdf[cutdf.nclusters <= k].apply(lambda x: cutrow(x, g), axis=1)

	#     # assign cluster numbers
	#     featuredf['cnum'] = assign_clusters(featuredf.index, g)

	#     wcss = wcss(featuredf)
	#     wcsses.append(wcss.ix[wcss.index >= 0].sum())
	#     print 'k:', k, 'WCSSE:', wcss.ix[wcss.index >= 0].sum(),
	#     print g.number_of_edges()

	return ks, wcsses


def cut2cluster(featurelist, nclusters):
	'''
	returns Series with cluster number indexed by node number

	featurelist: '010507'
	nclusters: int
	'''

	fn = 'results/CL' + featurelist + '.csv'
	edges = pd.read_csv(fn)
	edges = edges[['source', 'target']]
	graph = make_graph(edges)

	# reduce graph according to cut list until nclusters are achieved
	for i in edges.index:
		ncc = cutcon(edges.ix[i], graph)
		if ncc >= nclusters: break


	# # add count of number of clusters after each cut
	# g = graph.copy()
	# edges['nclusters'] = edges.apply(lambda x: cutcon(x, g), axis=1)

	# # reduces graph to i clusters
	# g = graph.copy()
	# edges[edges.nclusters <= nclusters].apply(lambda x: cutrow(x, g), axis=1)

	nodelist = list(set(edges.source).union(set(edges.target)))

	# assign cluster numbers
	return assign_clusters(nodelist, graph)

def feature_bars(featuredf, cnum, plot=False, **kwargs):
	'''
	barplot of features grouped by cluster number
	'''
	df = featuredf.copy()
	df['cnum'] = cnum

	# scale values 0-1 then subtract average
	df = df.groupby('cnum').mean()
	df = df.sub(df.min(axis=0))
	df = df.div(df.max(axis=0))
	df = df.sub(df.mean(axis=0))
	
	if plot:
		df.T.plot(kind='bar', subplots=True, sharey=True, **kwargs)

	return df


def most_similar(featuredf, cluster_labels, cluster_number):
	'''
	returns feature distance from cluster_number to all others
	'''
	cluster_means = featuredf.groupby(cluster_labels).mean()
	df =  pd.DataFrame(pairwise_distances(cluster_means),
						metric='l2')
	return df[cluster_number]


def gencolors(n, cmap='jet'):
	c = matplotlib.cm.get_cmap('Set1')
	clist = [matplotlib.colors.rgb2hex(rgb) for rgb in c(np.linspace(0,1,n))]
	return clist


def list_(*args): return list(args)


def make_json(cnum, polys, clist, mapno, fbars):
	
	fnames = map(lambda x: [FDICT[n] for n in mapno2list(x)], mapno)


	featurelist = []
	for i in xrange(len(cnum)):
	    featurelist.append({"type": "Feature",
	                        "properties": {
	                        "color": clist.iloc[i],
	                        "mapno": mapno.iloc[i],
	                        "neibno": cnum.iloc[i],
	                        "bars" : map(list_, fnames[i],
	                        			 fbars.iloc[i]),
	                        "visible": False
	                        },
	                        "geometry": mapping(polys.iloc[i])
	                        })
	    
	geojson = {"type": "FeatureCollection",
	           "features": featurelist}

	return geojson


def merge_map_data(path, featuredf):
	files = os.listdir(path)
	files = [f[2:-4] for f in files if f[:2] == 'CL']
	files.remove('xx')
	files.remove('000406')

	files = [f for f in files if len(f) <= 6]

	fnames = [mapno2list(f) for f in files]



	nclusters = 25

	# make null map
	clist = gencolors(nclusters)
	cnum = cut2cluster('xx', nclusters)
	fbars = feature_bars(featuredf[FDICT.values()], cnum)


	featuredf = featuredf.ix[cnum.index]
	fn = 'data/uscensus/tl_2010_06075_tabblock10/tl_2010_06075_tabblock10.dbf'
	mergedf = merge_shapefiles(featuredf[['lat', 'lon']], fn)
	polys = make_shapefiles(featuredf[['lat', 'lon']], mergedf.polys, cnum)

	alldf = pd.DataFrame({'cnum': cnum.unique(),
                      'polygon': polys})
	alldf['color'] = clist
	alldf['mapno'] = ''
	alldf['fbars'] = map(list, fbars.round(2).values)

	# store results
	alldf.to_csv('results/alldf.csv')

	# make all other maps
	for i, f in enumerate(files):
		print f
		cnum = cut2cluster(f, nclusters)
		fbars = feature_bars(featuredf[fnames[i]], cnum)
		polys = make_shapefiles(featuredf[['lat', 'lon']],
								mergedf.polys, cnum)

		onedf = pd.DataFrame({'cnum': cnum.unique(),
                      'polygon': polys})

		onedf['color'] = clist
		onedf['mapno'] = f
		onedf['fbars'] = map(list, fbars.round(2).values)

		with open('results/alldf.csv', 'a') as storefile:
		    onedf.to_csv(storefile, header=False)

		alldf = pd.concat((alldf, onedf), axis=0)




	return alldf




