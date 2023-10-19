""" 
Name:       implement_python_model.py
Author(s):  Gary Hutson & Matt Jackson on behalf of Packt publishing
Date:       09/12/2022
Usage:      python implement_python_model.py
"""

# Load in data
import csv
with open('./data/musae_facebook_target.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    data = [line for line in reader]
    print(data[:10])
    print(len(data))

# Adding nodes and attributes
node_ids = [int(row[0]) for row in data[1:]]
page_names = [row[2] for row in data[1:]]
page_types = [row[3] for row in data[1:]]

# Check if the nodes ids are with the length of the node ids
assert node_ids == list(range(len(node_ids)))

# Create the graph
import igraph as ig
g = ig.Graph(directed=False)
g.add_vertices(len(node_ids))

print(len(g.vs))
assert len(node_ids) == len(g.vs)

# Print out the relevant vertex names
g.vs['page_name'] = page_names
g.vs['page_type'] = page_types
print(g.vs[0]['page_name'])
print(g.vs[0]['page_type'])

# Adding edges - relationships to the graph
with open('./data/musae_facebook_edges.csv', 'r') as csv_file_2:
	reader = csv.reader(csv_file_2)
	edge_data = [row for row in reader]
	print(edge_data[:10])
	print(len(edge_data))

edges = [[int(row[0]), int(row[1])] for row in edge_data[1:]]
print(edges[:10])
g.add_edges(edges)
print(len(g.es))

first_edge = g.es[0]
print(first_edge.source)
print(first_edge.target)
print(g.vs[0]['page_name'])
print(g.vs[18427]['page_name'])

# Write a generic import method
def read_csv(csv_path):
    ''''
    Import a csv file.
 
    :param csv_path: Path to the csv to import.
    :return: A list of lists read from the csv.
    '''
 
    import csv
    import os
 
    assert os.path.exists(csv_path), \
        f'File could not be found at {csv_path}.'
 
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        data = [row for row in reader]
 
    return data

# Create add nodes method
def add_nodes(g, nodes, attributes):
    '''
    Add nodes to the graph.
 
    :param g: An igraph Graph() object.
    :param nodes: A list of lists containing nodes and node attributes, with a header. The first
                  element of each list in nodes should be the node ID.
    :param attributes: A list of attributes corresponding to the header (index 0) of the nodes list.
                       The names of attributes in this list will be added to the graph.
    '''
 
    assert nodes[0][0] == 'id', \
        f'The first column in the imported csv should be the ID header, "id". Instead, it '\
        f'is {nodes[0][0]}.'
 
    node_ids = [int(row[0]) for row in nodes[1:]]
    assert node_ids == list(range(len(node_ids))), \
        f'Node IDs should increase sequentially in the imported csv, from 0 to the number of'\
        f' nodes-1, {len(node_ids)}.'
 
    assert isinstance(attributes, list), \
        f'Attributes to add to the graph should be a list. Instead attributes is of type'\
        f' {type(attributes)}.'
 
    g.add_vertices(len(node_ids))
 
    headers = nodes[0]
    for attribute in attributes:
        attr_index = headers.index(attribute)
        g.vs[attribute] = [row[attr_index] for row in nodes[1:]]
 
    return g

# Create add edges method
def add_edges(g, edges):
    '''
    Add edges to the graph, where nodes are already present.
 
    :param g: An igraph Graph() object.
    :param edges: A list of lists containing edges, with a header.
    '''
    
    assert len(edges[0]) == 2, \
        f'Each element in the imported edges csv should be of length 2, representing an edge'\
        f' between two linked nodes. Instead, the first element is of length {len(edges)[0]}.'
 
    edges_to_add = [[int(row[0]), int(row[1])] for row in edges[1:]]
    g.add_edges(edges_to_add)
 
    return g

# Create function to bring this all together
import igraph
def graph_from_attributes_and_edgelist(node_attr_csv, edgelist_csv, attributes):
    
    g = igraph.Graph(directed=False)
 
    nodes = read_csv(node_attr_csv)
    edges = read_csv(edgelist_csv)
 
    g = add_nodes(g, nodes, attributes)
    g = add_edges(g, edges)
 
    return g

# Test our new function methods we have created
node_attr_path = './data/musae_facebook_target.csv'
edgelist_path = './data/musae_facebook_edges.csv'
attributes = ['page_name', 'page_type']
# Create a graph from our wrapper functions
g = graph_from_attributes_and_edgelist(node_attr_path, edgelist_path, attributes)

# Compare new method to original graph
print(g.vs[0]['page_name'])
print(g.vs[0]['page_type'])
first_edge = g.es[0]
print(first_edge.source)
print(first_edge.target)
print(len(g.es))
print(g.vs[0]['page_name'])
print(g.vs[18427]['page_name'])
