# gui_interface.py (Version 1)
import tkinter as tk

class PlantHealthApp:
    """
    The main GUI class for the Plant health checker app.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("500x400")

        # Title
        self.label_title = tk.Label(root, text="Plant Health Checker", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=20)
        
        # Instructions
        tk.Label(root, text="Step 1: Upload Image", font=("Arial", 12)).pack(pady=(10, 5))
