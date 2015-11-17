
import numpy as np
import pandas as pd
import networkx as nx

from code.featurize import fdist

def bigsize(row):
    g.remove_edge(row.node1, row.node2)
    return len(max(nx.connected_components(g), key=len))


def cutcon(row):
    g.remove_edge(row.node1, row.node2)
    return nx.number_connected_components(g)


def cutrow(row, graph):
    graph.remove_edge(row.node1, row.node2)
    return

def assign_clusters(df, graph):
    cc = list(nx.connected_components(graph))
    
    cnum = pd.Series(-1, index=df.index)
    for row in df.index:
        for i, cluster in enumerate(cc):
            if row in cluster: cnum.ix[row] = i
    return cnum


def row_errorsq(row, cluster_means):
    rowf = row.drop(['cnum'])
    return (fdist(rowf, cluster_means.ix[int(row.cnum)]))**2


def wcss(df):
    dfcp = df.copy()
    features = df.drop(['lat', 'lon'], axis = 1)
    cluster_means = features.groupby('cnum').mean()
    dfcp['errors'] = features.apply(lambda x: row_errorsq(x, cluster_means), axis = 1)

    return dfcp.groupby('cnum').sum()['errors']