import networkx as nx
import plotly.graph_objects as go


def render_plan_3d(graph):
    # Create 3D positions for nodes
    pos = nx.spring_layout(graph, dim=3, seed=42)

    # Define colors and sizes by type
    type_colors = {
        'park': 'green',
        'transit': 'blue',
        'building': 'grey',
        'commercial': 'orange',
        'industrial': 'red',
        'school': 'purple',
        'hospital': 'pink',
        'service': 'brown',
        'waste': 'black',
        'recreational': 'lightgreen',
        'water': 'aqua',
        'smart_hub': 'gold'
    }

    # Initialize coordinates
    node_x, node_y, node_z = [], [], []
    node_colors, node_sizes, node_labels = [], [], []

    for node, data in graph.nodes(data=True):
        x, y, z = pos[node]
        height = data.get('height', 0) or 0
        z = height / 50  # Scale height for 3D view

        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

        node_type = data.get('type', 'building')
        node_colors.append(type_colors.get(node_type, 'grey'))
        node_sizes.append(5 + (height / 10 if height else 10))
        node_labels.append(f"{node} ({node_type})")

    # Edge coordinates
    edge_x, edge_y, edge_z = [], [], []
    for edge in graph.edges():
        n0, n1 = edge
        x0, y0 = pos[n0][0], pos[n0][1]
        x1, y1 = pos[n1][0], pos[n1][1]

        h0 = graph.nodes[n0].get('height') or 0
        h1 = graph.nodes[n1].get('height') or 0

        z0 = h0 / 50
        z1 = h1 / 50

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    # Plotly traces
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='black', width=1),
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(color=node_colors, size=node_sizes),
        text=node_labels,
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='City Plan 3D Visualization',
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(title='Height (scaled)', showbackground=False),
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig.write_html("city_plan_3d.html")
    print("✅ 3D city plan saved as `city_plan_3d.html`")
