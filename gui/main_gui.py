# gui/main_gui.py

import tkinter as tk
from tkinter import messagebox

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

    def on_submit(self):
        user_input = self.text_input.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a description.")
            return

        print("User Input Received:")
        print(user_input)

        # Placeholder for sending to parser
        # parsed = parse_input(user_input)
        # planner.generate_city(parsed)
        # renderer.render(parsed_city)

        messagebox.showinfo("Input Received", "Thank you! Input received and will be processed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniArchitectGUI(root)
    root.mainloop()
