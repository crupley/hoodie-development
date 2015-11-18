import os
import cPickle as pickle
from graph_tool.all import *

files = os.listdir('results/graphs')

for f in files:
    with open('results/graphs/' + f, 'rb') as f:
        g = pickle.load(f)
    fn = f[:-4] + '.gt'
    g.save(fn)
