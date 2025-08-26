import os
import shutil
import subprocess
import sys
import webbrowser

def clean_pycache(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            full_path = os.path.join(dirpath, "__pycache__")
            print(f"Removing {full_path}...")
            shutil.rmtree(full_path)

def main():
    root = os.path.dirname(__file__)
    clean_pycache(root)
    html_path = os.path.join(root, "city_plan_3d.html")
    if os.path.exists(html_path):
        print(f"Deleting existing {html_path}...")
        os.remove(html_path)

    print("Running python -m main...")
    result = subprocess.run([sys.executable, "-m", "main"])
    if result.returncode != 0:
        print("main module failed!", file=sys.stderr)
        sys.exit(result.returncode)

    if os.path.exists(html_path):
        print(f"Opening {html_path} in browser...")
        webbrowser.open(f"file://{html_path}")
    else:
        print("Error: city_plan_3d.html not found!", file=sys.stderr)

if __name__ == "__main__":
    main()
