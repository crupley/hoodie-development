import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cPickle as pickle
import networkx as nx

import code.featurize as fe
import code.graph as gr

def calc_dist(row):
    return fe.sim(groupavg.ix[row.group][2:], dfsm.ix[row.node][2:-1])


knum = 2
dfsm['group'] = -1

# initialize nodes
nodes = np.random.choice(dfsm.index, size=knum, replace=False)
for gr, node in enumerate(nodes):
    dfsm.group.loc[node] = gr

for i in xrange(10):
	groupavg = dfsm.groupby('group').mean()

	# build distance sets
	dist = pd.DataFrame(columns=['group', 'node'])

	for k in xrange(knum):
	    groupnodes = set(dfsm[dfsm.group == k].index)
	    neibnodes = set()
	    for node in groupnodes:
	        neibnodes = neibnodes.union(set(nx.all_neighbors(g, node)))
	    # remove group nodes from list
	    neibnodes = neibnodes.difference(groupnodes)
	    newrows = pd.DataFrame({'group': k * np.ones(len(neibnodes)),
	                            'node': list(neibnodes)})
	    dist = dist.append(newrows, ignore_index=True).astype('int')

	dist['dist'] = dist.apply(calc_dist, axis=1)

	# assign nearest node to group
	bestmatch = dist.sort_values('dist').iloc[0]
	dfsm.group.loc[dfsm.index == bestmatch.node] = bestmatch.group
	dfsm.group[dfsm.group != -1]