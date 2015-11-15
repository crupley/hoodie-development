import networkx as nx
from collections import Counter
from time import time
import cPickle as pickle


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

if __name__ == '__main__':
    graph = pickle.load(open('g070605.pkl', 'rb'))

    # time cal
    # start_time = time()
    # nx.edge_betweenness_centrality(graph, weight='sim')
    # print 'First edge time:', time() - start_time

    graph_reduce(graph)