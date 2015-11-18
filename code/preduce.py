
from multiprocessing import Pool, Queue
import cPickle as pickle
import os

#from code.graphreduce import graph_reduce_gt
from graph_tool.all import *

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

def f(g):
	fn = 'results/' + g.gp.Name + '.csv'
	c = graph_reduce_gt(g, fn)
	return c


if __name__ == '__main__':

	gs = pickle.load(open('g8.pkl', 'rb'))

	p = Pool()
	outputs = p.map(f, gs)