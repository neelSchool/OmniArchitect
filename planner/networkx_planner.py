# planner/networkx_planner.py

import networkx as nx
import random

def generate_plan(constraints):
    G = nx.Graph()

    num_parks = int(constraints.get("green_area_ratio", 0.2) * 20)
    num_transit = int(constraints.get("transit_connectivity", 0.5) * 15)
    num_buildings = 30
    max_height = constraints.get("max_building_height", 30)

    # Add parks
    for i in range(num_parks):
        G.add_node(f"park_{i}", type='park', height=None)

    # Add transit nodes
    for i in range(num_transit):
        G.add_node(f"transit_{i}", type='transit', height=None)

    # Add buildings with random height up to max_height
    for i in range(num_buildings):
        height = random.uniform(5, max_height)
        G.add_node(f"building_{i}", type='building', height=height)

    # Connect transit nodes randomly based on connectivity (simplified)
    transit_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'transit']
    for i in range(len(transit_nodes)):
        for j in range(i + 1, len(transit_nodes)):
            if random.random() < constraints.get("transit_connectivity", 0.5):
                G.add_edge(transit_nodes[i], transit_nodes[j], type='transit_road')

    # Connect buildings to nearest transit node (simplified)
    for node, data in G.nodes(data=True):
        if data['type'] == 'building':
            if transit_nodes:
                nearest = random.choice(transit_nodes)
                G.add_edge(node, nearest, type='access_road')

    # Connect parks with some roads
    park_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'park']
    for park in park_nodes:
        # Connect each park to a random transit node for accessibility
        if transit_nodes:
            transit_node = random.choice(transit_nodes)
            G.add_edge(park, transit_node, type='park_access')

    return G
