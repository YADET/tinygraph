""" 
Name:       TV_show_use_case.py
Author(s):  Gary Hutson & Matt Jackson on behalf of Packt publishing
Date:       09/12/2022
Usage:      python TV_show_use_case.py.py
"""
import matplotlib.pyplot as plt
import igraph
from collections import Counter

# Examining the graph structure
# Import custom functions
from graphtastic.utils import graph_from_attributes_and_edgelist
node_attr_path = './data/musae_facebook_target.csv'
edgelist_path = './data/musae_facebook_edges.csv'
attributes = ['page_name', 'page_type']

# Create a graph from our wrapper functions
g = graph_from_attributes_and_edgelist(node_attr_path, edgelist_path, attributes)
# Generate histogram
histogram = g.degree_distribution(bin_width=5)
print(histogram)

# Plot histogram
import matplotlib.pyplot as plt
bins = 30
plt.hist(g.degree(), bins)
plt.xlabel('Node degree centrality')
plt.ylabel('Frequency')
plt.show()

# Measuring connectedness
connected_components = g.clusters()
print(connected_components)

# Looking at the top degree nodes
degree = list(zip(g.vs['page_name'], g.degree()))
sorted_degree = sorted(degree, key=lambda x: x[1], reverse=True)   
print(sorted_degree[:10])

tv_nodes = g.vs.select(page_type_eq='tvshow')
tv_indices = [node.index for node in tv_nodes]
tv_degree = list(zip(g.vs[tv_indices]['page_name'], g.degree(tv_indices)))
sorted_tv_degree = sorted(tv_degree, key=lambda x: x[1], reverse=True)
print(sorted_tv_degree[:10])

# Using select() to interrogate the graph
gov_pol_nodes = g.vs.select(page_type_in=['government', 'politician'])
one_to_three_100_nodes = g.vs.select(_degree_ge=100, 
                                     _degree_le=140, 
                                     page_type_eq='tvshow')

print(one_to_three_100_nodes['page_name'])

# Get the node degree
g.vs['node_degree'] = g.degree()
one_to_three_100_nodes = g.vs.select(node_degree_ge=100,
                                     node_degree_le=140,
                                     page_type_eq='tvshow')
print(one_to_three_100_nodes['page_name'])

# Explore the properties of our nodes
today_show_id = g.vs.select(page_name_eq='Today Show')[0].index
print(today_show_id)
today_show_edges = g.es.select(_incident=[today_show_id])

sources = [edge.source for edge in today_show_edges]
targets = [edge.target for edge in today_show_edges]
print(sources)
print(targets)

neighbor_nodes = list(set(sources + targets))
neighbor_nodes.remove(909)
print(neighbor_nodes)
print(len(neighbor_nodes))

neighbor_page_types = g.vs[neighbor_nodes]['page_type']
print(neighbor_page_types)


page_type_dict = Counter(neighbor_page_types)
print(page_type_dict)

ids_and_page_types = zip(neighbor_nodes, neighbor_page_types)
politician_id = [id_tuple for id_tuple in list(ids_and_page_types) if id_tuple[1] == 'politician']
print(politician_id)


politician_name = g.vs[22243]['page_name']
print(politician_name)
