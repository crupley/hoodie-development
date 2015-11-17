import numpy as np
import networkx as nx
from collections import Counter
from time import time
import cPickle as pickle

from graph_tool.all import *


def graph_reduce(graph, max_size=1):
    '''
    INPUT: Graph G, int max_size
    OUTPUT: None

    Sequentially remove most highly connected nodes until largest cluster
    is max_size and output sequence to file.
    '''
    g = graph.copy()
    fn = str(g.node['namenode']['name']) + '.csv'

    # pick up where we left off
    if os.path.exists('results/' + fn):
        # remove identified nodes from graph
        with open('results/' + fn, 'wb') as f:
            line = f.readline()
            for line in f.readlines():
                lsp = line.split(',')
                print lsp[0], lsp[1]
                graph.remove_edge(float(lsp[0]), float(lsp[1]))
    else:
        # create results file
        with open('results/' + fn, 'wb') as f:
            f.write('node1,node2,size,edges,biggroup,timestamp\n')

    biggroup = len(max(nx.connected_components(g), key=len))

    while biggroup >= max_size:
        btw = nx.edge_betweenness_centrality(g, weight='sim')
        most_connected = Counter(btw).most_common(1)[0][0]
        node1 = most_connected[0]
        node2 = most_connected[1]
        size = nx.number_connected_components(g)
        edges = g.number_of_edges()
        biggroup = len(max(nx.connected_components(g), key=len))
        outitems = (node1, node2, size, edges, biggroup, time())
        outs = '%d,%d,%d,%d,%d,%f\n' % outitems
        with open('results/' + fn, 'a') as f:
            f.write(outs)
        g.remove_edge(*most_connected)
        if g.number_of_edges() == 0: return

def graph_reduce_gt(graph, filename):
    '''
    graph with dist and btw attributes
    filename to store the cutlist
    '''
    g = Graph(graph)
    cuts = []
    with open(filename, 'wb') as f:
        f.write('source,target,num_edges,timestamp\n')
    while g.num_edges() > 0:
        betweenness(g, eprop = g.ep.btw, weight = g.ep.dist)

        meidx = np.argmax(g.ep.btw.fa)
        maxedge = list(g.edges())[meidx]
        metup = eval(str(maxedge))
        cuts.append(metup)
        
        wstr = '%d,%d,%d,%f\n' % (metup[0], metup[1], g.num_edges(), time())
        with open(filename, 'a') as f:
            f.write(wstr)
        
        g.remove_edge(maxedge)
    return cuts


def build_graph(edges, distances, graph_name=None):
    '''
    edges: df with node1, node2, and dist
    '''

    g = Graph()

    # create graph properties
    gp = g.new_graph_property('string')
    g.graph_properties['Name'] = gp
    g.graph_properties['Name'] = graph_name
    eprop = g.new_edge_property("float")
    g.edge_properties['dist'] = eprop #feature distance
    g.edge_properties['btw'] = eprop  #betweenness
    g.list_properties()

    # create edges and edge weights
    g.add_edge_list(zip(edges.node1, edges.node2))
    for i, edge in enumerate(g.edges()):
        g.ep.dist[edge] = distances.iloc[i]

    remove_parallel_edges(g)
    return g



if __name__ == '__main__':
    graph = pickle.load(open('g070605.pkl', 'rb'))

    # time cal
    # start_time = time()
    # nx.edge_betweenness_centrality(graph, weight='sim')
    # print 'First edge time:', time() - start_time

    graph_reduce(graph)