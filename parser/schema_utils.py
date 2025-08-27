import numpy as np

# Updated list of all 20 factors
SCHEMA = [
    "green_area_ratio",
    "transit_connectivity",
    "max_building_height",
    "education_access",
    "housing_affordability",
    "energy_access",
    "water_access",
    "water_bodies",
    "road_network_density",
    "population_density",
    "industrial_zone_ratio",
    "commercial_zone_ratio",
    "public_service_access",
    "waste_management",
    "healthcare_access",
    "recreational_zone_ratio",
    "noise_pollution_level",
    "air_quality_index",
    "smart_infrastructure",
    "disaster_resilience"
]

def to_matrix(constraints: dict) -> np.ndarray:
    def encode(value):
        if isinstance(value, str):
            return hash(value) % 100 / 100.0
        try:
            return float(value)
        except:
            return 0.0
    return np.array([encode(constraints.get(key, 0.0)) for key in SCHEMA])
