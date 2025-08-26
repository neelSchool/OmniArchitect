# renderer/renderer.py

def render_plan(plan: dict):
    print("\n--- City Plan Render ---")
    for key, val in plan.items():
        print(f"{key}: {val}")
    print("--- End of Render ---\n")
