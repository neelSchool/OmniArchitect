# renderer/renderer.py

import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go


def render_plan_2d(graph):
    # Position nodes using spring layout for nice spacing
    pos = nx.spring_layout(graph, seed=42)

    # Separate nodes by type for coloring
    node_types = {'park': [], 'transit': [], 'building': []}
    for node, data in graph.nodes(data=True):
        node_types[data['type']].append(node)

    plt.figure(figsize=(10, 8))
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=node_types['park'], node_color='green', label='Parks', node_size=200)
    nx.draw_networkx_nodes(graph, pos, nodelist=node_types['transit'], node_color='blue', label='Transit', node_size=200)
    nx.draw_networkx_nodes(graph, pos, nodelist=node_types['building'], node_color='grey', label='Buildings', node_size=100)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    
    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=8)
    
    plt.legend()
    plt.title("City Plan 2D Visualization")
    plt.axis('off')
    plt.show()


def render_plan_3d(graph):
    # Create positions for nodes (3D)
    pos = nx.spring_layout(graph, dim=3, seed=42)  # 3D layout

    # Extract node coordinates and attributes
    node_x, node_y, node_z = [], [], []
    colors = []
    sizes = []
    for node, data in graph.nodes(data=True):
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        # Use height attribute for z (default 0)
        height = data.get('height')
        if height is None:
            height = 0
        node_z.append(height / 50)  # scale down height for visualization

        # Color nodes by type
        node_type = data.get('type', 'building')
        if node_type == 'park':
            colors.append('green')
            sizes.append(10)
        elif node_type == 'transit':
            colors.append('blue')
            sizes.append(10)
        else:  # building
            sizes.append(5 + (height / 10))
            colors.append('grey')

    # Create edge coordinates for lines
    edge_x, edge_y, edge_z = [], [], []
    for edge in graph.edges():
        h0 = graph.nodes[edge[0]].get('height')
        h1 = graph.nodes[edge[1]].get('height')
        h0 = h0 if h0 is not None else 0
        h1 = h1 if h1 is not None else 0

        x0, y0 = pos[edge[0]][0], pos[edge[0]][1]
        x1, y1 = pos[edge[1]][0], pos[edge[1]][1]

        z0 = h0 / 50
        z1 = h1 / 50

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(color=colors, size=sizes),
        text=list(graph.nodes()),
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title='City Plan 3D Visualization',
                      scene=dict(
                          xaxis=dict(showbackground=False),
                          yaxis=dict(showbackground=False),
                          zaxis=dict(title='Building Height'),
                      ),
                      showlegend=False)
    fig.write_html("city_plan_3d.html")
    print("3D visualization saved as city_plan_3d.html")


