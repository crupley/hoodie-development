import itertools
import cPickle as pickle
from multiprocessing import Pool

from code.graphreduce import build_graph
from code.featurize import fdist_by_node


f = pickle.load(open('features.pkl', 'rb'))
df = f.fsmooth.copy()
edges = pickle.load(open('edges.pkl', 'rb'))

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

def make_graph(perm):
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
	outputs = p.map(make_graph, perms[:2])