
from multiprocessing import Pool, Queue
import cPickle as pickle

from code.graphreduce import graph_reduce_gt

def f(g):
	fn = 'results/' + g.gp.Name
	c = graph_reduce_gt(g, fn)
	return c


if __name__ == '__main__':

	gs = pickle.load(open('g4.pkl', 'rb'))

	p = Pool(process=4)
	outputs = p.map(f, gs)