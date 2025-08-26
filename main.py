# main.py

from parser.transformer_parser import ConstraintParser
from parser.schema_utils import to_matrix
from planner.city_planner import generate_plan
from renderer.renderer import render_plan

def demo():
    parser = ConstraintParser()
    test_input = "We want 25% green areas, full transit connectivity, and buildings under 45 meters."
    constraints = parser.parse(test_input)

    if "error" in constraints:
        print("Parsing error:", constraints["error"])
        return

    matrix = to_matrix(constraints)
    plan = generate_plan(matrix)
    render_plan(plan)

if __name__ == "__main__":
    demo()
