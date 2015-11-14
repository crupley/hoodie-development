import networkx as nx
from collections import Counter


def girvan_newman_step(graph):
    '''
    INPUT: Graph G
    OUTPUT: None

    Run one step of the Girvan-Newman community detection algorithm.
    Afterwards, the graph will have one more connected component.
    '''
    size = nx.number_connected_components(graph)
    cur = 0
    while cur <= size:
        most_connected = Counter(nx.edge_betweenness_centrality(graph)).most_common(1)[0][0]
        graph.remove_edge(*most_connected)
        cur = nx.number_connected_components(graph)

def find_communities_n(G, n):
    '''
    INPUT: Graph G, int n
    OUTPUT: list of lists

    Run the Girvan-Newman algorithm on G for n steps. Return the resulting
    communities.
    '''
    G1 = G.copy()
    for i in xrange(n):
        girvan_newman_step(G1)
    return list(nx.connected_components(G1))


def find_communities_modularity(G, max_iter=None):
    '''
    INPUT:
        G: networkx Graph
        max_iter: (optional) if given, maximum number of iterations
    OUTPUT: list of lists of strings (node names)

    Run the Girvan-Newman algorithm on G and find the communities with the
    maximum modularity.
    '''
    degrees = G.degree()
    num_edges = G.number_of_edges()
    G1 = G.copy()
    best_modularity = -1.0
    best_comps = nx.connected_components(G1)
    i = 0
    while G1.number_of_edges() > 0:
        subgraphs = nx.connected_component_subgraphs(G1)
        modularity = get_modularity(subgraphs, degrees, num_edges)
        if modularity > best_modularity:
            best_modularity = modularity
            best_comps = list(nx.connected_components(G1))
        girvan_newman_step(G1)
        i += 1
        if max_iter and i >= max_iter:
            break
    return best_comps


def get_modularity(subgraphs, degrees, num_edges):
    '''
    INPUT:
        subgraphs: graph broken in subgraphs
        degrees: dictionary of degree values of original graph
        num_edges: float, number of edges in original graph
    OUTPUT: Float (modularity value, between -0.5 and 1)

    Return the value of the modularity for the graph G.
    '''
    output = 0
    for c in subgraphs:
        for i in c.nodes():
            for j in c.nodes():
                a = int(c.has_edge(i, j))
                output += a - ( degrees[i] * degrees[j] / float(2 * num_edges) )
    return output / float(2 * num_edges)