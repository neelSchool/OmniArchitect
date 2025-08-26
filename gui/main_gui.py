# gui/main_gui.py

import tkinter as tk
from tkinter import messagebox
from parser.transformer_parser import ConstraintParser
from parser.schema_utils import to_matrix
from planner.city_planner import generate_plan
from renderer.renderer import render_plan

class OmniArchitectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniArchitect")

        self.label = tk.Label(root, text="Enter your city design request:")
        self.label.pack(pady=10)

        self.text_input = tk.Text(root, height=10, width=50)
        self.text_input.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=5)

        self.parser = ConstraintParser()

    def on_submit(self):
        user_input = self.text_input.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a description.")
            return

        self.status_label.config(text="Parsing input...")
        constraints = self.parser.parse(user_input)

        if "error" in constraints:
            messagebox.showerror("Parser Error", "Failed to extract constraints.")
            return

        self.status_label.config(text="Building plan...")
        matrix = to_matrix(constraints)
        plan = generate_plan(matrix)

        self.status_label.config(text="Rendering...")
        render_plan(plan)

        messagebox.showinfo("Done", "City plan rendered successfully.")
        self.status_label.config(text="Done.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniArchitectGUI(root)
    root.mainloop()
