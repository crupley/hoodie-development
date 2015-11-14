import networkx as nx
from collections import Counter
import sys
from time import time


def girvan_newman_step(graph):
    '''
    INPUT: Graph G
    OUTPUT: None

    Run one step of the Girvan-Newman community detection algorithm.
    Afterwards, the graph will have one more connected component.
    '''
    size = nx.number_connected_components(graph)
    edges = graph.number_of_edges()
    biggroup = len(max(nx.connected_components(graph), key=len))
    cur = 0
    while cur <= size:
        most_connected = Counter(nx.edge_betweenness_centrality(graph, weight='sim')).most_common(1)[0][0]
        node1 = most_connected[0]
        node2 = most_connected[1]
        outitems = (node1, node2, size, edges, biggroup, time())
        outs = '%d, %d, %d, %d, %d, %f\n' % outitems
        print outs; sys.stdout.flush()
        #print most_connected; sys.stdout.flush()
        graph.remove_edge(*most_connected)
        cur = nx.number_connected_components(graph)