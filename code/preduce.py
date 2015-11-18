
from multiprocessing import Pool, Queue
import cPickle as pickle
import os

from code.graphreduce import graph_reduce_gt

def f(g):
	fn = 'results/' + g.gp.Name + '.csv'
	c = graph_reduce_gt(g, fn)
	return c


if __name__ == '__main__':

	gs = pickle.load(open('g8.pkl', 'rb'))

	p = Pool()
	outputs = p.map(f, gs)