
import numpy as np
import pandas as pd
import networkx as nx

def assign_clusters(df, graph):
    cc = list(nx.connected_components(graph))
    
    cnum = pd.Series(-1, index=df.index)
    for row in df.index:
        for i, cluster in enumerate(cc):
            if row in cluster: cnum.ix[row] = i
    return cnum