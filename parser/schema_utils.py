# parser/schema_utils.py

import numpy as np

SCHEMA = ["green_area_ratio", "transit_connectivity", "max_building_height"]

def to_matrix(constraints: dict) -> np.ndarray:
    # Simple numerical mapping — you can make this smarter later
    def encode(value):
        if isinstance(value, str):
            return hash(value) % 100 / 100.0  # crude text->float
        try:
            return float(value)
        except:
            return 0.0

    return np.array([encode(constraints.get(key, 0.0)) for key in SCHEMA])
