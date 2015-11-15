
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


def graph_info(graph):
	print nx.info(graph)
	print 'Number of clusters:', nx.number_connected_components(graph)
	print 'Largest cluster:', len(max(nx.connected_components(graph),
									  key=len))

def make_graph(edgesdf, name=None):
	g = nx.from_pandas_dataframe(edgesdf, source='node1',
								 target='node2', edge_attr='fdist')
	if name:
		g.add_node('namenode', name=name)

	return g

