import networkx as nx
import random

# Clamp value within min/max if clamp is defined
def clamp_value(key, val):
    CLAMPS = {
        "population_density": (1000, 20000),
        "green_area_ratio": (0.0, 0.6),
        "road_network_density": (0.1, 1.0),
        "max_building_height": (10, 100),
        "water_bodies": (0, 5),
        "industrial_zone_ratio": (0.0, 0.5),
        "commercial_zone_ratio": (0.0, 0.5),
        "recreational_zone_ratio": (0.0, 0.5),
        "air_quality_index": (0, 150),
        "noise_pollution_level": (0.0, 1.0)
    }
    if key in CLAMPS:
        min_val, max_val = CLAMPS[key]
        return max(min(val, max_val), min_val)
    return val


def generate_plan(constraints):
    G = nx.Graph()

    # Apply clamping
    for key in constraints:
        constraints[key] = clamp_value(key, constraints[key])

    # Extract & interpret constraints
    parks = int(constraints["green_area_ratio"] * 20)
    transits = int(constraints["transit_connectivity"] * 15)
    max_height = constraints["max_building_height"]
    buildings = int(constraints["population_density"] / 1000)
    industrial = int(constraints["industrial_zone_ratio"] * 10)
    commercial = int(constraints["commercial_zone_ratio"] * 10)
    recreation = int(constraints["recreational_zone_ratio"] * 10)
    water_bodies = int(constraints["water_bodies"])
    schools = int(constraints["education_access"] * 10)
    hospitals = int(constraints["healthcare_access"] * 10)
    services = int(constraints["public_service_access"] * 10)
    waste_nodes = int(constraints["waste_management"] * 5)
    smart_nodes = int(constraints["smart_infrastructure"] * 5)
    roads_density = constraints["road_network_density"]

    # Add various node types
    def add_nodes(count, label, height=None):
        for i in range(count):
            h = random.uniform(5, max_height) if height == 'random' else height
            G.add_node(f"{label}_{i}", type=label, height=h)

    add_nodes(parks, "park")
    add_nodes(water_bodies, "water")
    add_nodes(transits, "transit")
    add_nodes(buildings, "building", height='random')
    add_nodes(commercial, "commercial", height='random')
    add_nodes(industrial, "industrial", height='random')
    add_nodes(recreation, "recreational")
    add_nodes(schools, "school")
    add_nodes(hospitals, "hospital")
    add_nodes(services, "service")
    add_nodes(waste_nodes, "waste")
    add_nodes(smart_nodes, "smart_hub")

    # Connect nodes based on road density
    nodes = list(G.nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < roads_density * 0.05:
                G.add_edge(nodes[i], nodes[j], type='road')

    return G
