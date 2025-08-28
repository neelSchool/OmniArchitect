from parser.transformer_parser import ConstraintParser
from planner.networkx_planner import generate_plan
from renderer.renderer import render_plan_3d

def demo():
    parser = ConstraintParser()
    test_input = "We want good public transport with option every 15 min. The city should have 35% Green space with gardens, open play area, water bodies."
    constraints = parser.parse(test_input)

    if "error" in constraints:
        print("Parsing error:", constraints["error"])
        return

    print("\n--- Parsed Constraints ---")
    for k, v in constraints.items():
        print(f"{k}: {v}")

    plan_graph = generate_plan(constraints)
    render_plan_3d(plan_graph)

if __name__ == "__main__":
    demo()
