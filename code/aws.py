import networkx as nx
from collections import Counter
from time import time


def graph_reduce(graph, max_size=1):
    '''
    INPUT: Graph G, int max_size
    OUTPUT: None

    Sequentially remove most highly connected nodes until largest cluster
    is max_size and output sequence to file.
    '''
    g = graph.copy()
    fn = str(g.node['namenode']['name']) + '.csv'
    with open('results/' + fn, 'wb') as f:
        f.write('node1,node2,size,edges,biggroup,timestamp\n')

    biggroup = len(max(nx.connected_components(g), key=len))

    while biggroup >= max_size:
        most_connected = Counter(nx.edge_betweenness_centrality(g, weight='sim')).most_common(1)[0][0]
        node1 = most_connected[0]
        node2 = most_connected[1]
        size = nx.number_connected_components(g)
        edges = g.number_of_edges()
        biggroup = len(max(nx.connected_components(g), key=len))
        outitems = (node1, node2, size, edges, biggroup, time())
        outs = '%d,%d,%d,%d,%d,%f\n' % outitems
        # print outs
        with open('results/' + fn, 'a') as f:
            f.write(outs)
        g.remove_edge(*most_connected)