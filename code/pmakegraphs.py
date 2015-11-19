import itertools
import cPickle as pickle
from multiprocessing import Pool
import sys
import numpy as np
import pandas as pd

from graphreduce import build_graph
import featurize
from code.featurize import featurizer


# f = pickle.load(open('features.pkl', 'rb'))
# df = pickle.load(open('featuresdf.pkl', 'rb'))
df = pd.read_csv('featuresdf.csv')
# edges = pickle.load(open('edges.pkl', 'rb'))
edges = pd.read_csv('edges.csv')

fnums = {0: 'taxable_value',
         1: 'grocery',
         2: 'restaurant',
         3: 'retail',
         4: 'ncrimes',
         5: 'sgnf',
         6: 'avg_hh_size',
         7: 'population',
         8: 'walkscore'}
flist = fnums.keys()

def fdist(f1, f2):
	'''

	feature distance
	'''
	return np.linalg.norm(f1-f2)**2

def fdist_by_node(n1, n2, df):
	f1 = df.ix[n1]
	f2 = df.ix[n2]
	return fdist(f1, f2)

def make_graph(perm):
	sys.path.append('/home/ubuntu/repos/hoodie/code')
	# calculate feature distances for each edge
	labs = [fnums[c] for c in perm]
	fdlambda = lambda x: fdist_by_node(x.node1, x.node2, df[labs])
	fdist = edges.apply(fdlambda, axis = 1)

	# filename format
	fnbase = '%02d' * len(perm) % perm
	gn = 'CL' + fnbase
	fn = 'results/graphs/g' + fnbase + '.pkl'

	# make graph
	g = build_graph(edges, fdist, graph_name=gn)

	# save graph
	pickle.dump(g, open(fn, 'wb'))
	return

if __name__ == '__main__':

	# features dictionaries
	fnums = {0: 'taxable_value',
	         1: 'grocery',
	         2: 'restaurant',
	         3: 'retail',
	         4: 'ncrimes',
	         5: 'sgnf',
	         6: 'avg_hh_size',
	         7: 'population',
	         8: 'walkscore'}
	flist = fnums.keys()

	# make all permutations
	perms = []
	for i in range(1, len(flist)+1):
	    perm = list(itertools.combinations(flist, i))
	    perms.extend(perm)

	# make graphs in parallel
	p = Pool()
	outputs = p.map(make_graph, perms)
