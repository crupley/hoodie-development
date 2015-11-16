import numpy as np
import pandas as pd
import networkx as nx

import code.featurize as fe


def crawl_cluster(knum, featuredf, graph):

	df = featuredf.copy()

	# randomly initialize nodes
	nodes = np.random.choice(df.index, size=knum, replace=False)

	# initialize group membership to -1 (no group)
	df['group'] = -1

	# assign initial nodes
	for gr, node in enumerate(nodes):
	    df.group.loc[node] = gr

	groupavg = df.groupby('group').mean()
	calc_dist = lambda row: fe.sim(groupavg.ix[row.group][2:],
								   df.ix[row.node][2:-1])

	groupednodes = set(nodes)
	while True:
	    groupavg = df.groupby('group').mean()

	    # build distance sets
	    dist = pd.DataFrame(columns=['group', 'node'])

	    # make list of neighbors to each cluster
	    for k in xrange(knum):
	        nodegroup = set(df[df.group == k].index)
	        neibnodes = set()
	        for node in nodegroup:
	            neibnodes = neibnodes.union(set(nx.all_neighbors(graph,node)))
	        # remove group nodes from list
	        neibnodes = neibnodes.difference(groupednodes)
	        newrows = pd.DataFrame({'group': k * np.ones(len(neibnodes)),
	                                'node': list(neibnodes)})
	        dist = dist.append(newrows, ignore_index=True).astype('int')

	    # no more neighbors = done!
	    if dist.shape[0] == 0: break

	    # calculate distance between neighbors and cluster mean
	    dist['dist'] = dist.apply(calc_dist, axis=1)

	    # assign nearest node to group
	    bestmatch = dist.sort_values('dist').iloc[0]
	    df.group.loc[df.index == bestmatch.node] = bestmatch.group
	    groupednodes = groupednodes.union({int(bestmatch.node)})

	return df