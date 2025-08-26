# planner/city_planner.py

import numpy as np

def generate_plan(constraint_matrix: np.ndarray) -> dict:
    """
    Convert the constraint matrix into a mock city plan.
    This is a placeholder. Real logic would optimize city layout here.
    """
    # Extract values with fallback defaults
    green_area = constraint_matrix[0] if constraint_matrix.size > 0 else 0.1
    transit_connectivity = constraint_matrix[1] if constraint_matrix.size > 1 else 0.0
    max_building_height = constraint_matrix[2] if constraint_matrix.size > 2 else 50.0

    plan = {
        "green_area_ratio": green_area,
        "transit_connectivity": transit_connectivity,
        "max_building_height": max_building_height,
        "description": f"Plan with {green_area*100:.1f}% green area, "
                       f"connectivity score {transit_connectivity:.2f}, "
                       f"max building height {max_building_height}m."
    }
    return plan
