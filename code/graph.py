
import numpy as np
import pandas as pd

import networkx as nx

from code.featurize import window, find_closest

def make_edges(latlondf):
	edgelambda = lambda x: find_closest(x, latlondf)
	n = latlondf.apply(edgelambda, axis = 1)

	edges = pd.DataFrame(columns=['node1', 'node2'])

	for node1 in n.index:
	    for node2 in n.ix[node1]:
	        newrow = {'node1':node1, 'node2':node2}
	        edges = edges.append(newrow, ignore_index=True)
	    edges.index.name = 'edge'
	return edges.astype('int')


