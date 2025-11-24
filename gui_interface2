# gui_interface.py (Update imports and __init__)
import tkinter as tk
from tkinter import filedialog, messagebox
from data_manager import PlantDataManager

class PlantHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("500x400")

        # We load data immediately so the user doesn't have to click a button
        self.data_manager = PlantDataManager('data/plants_dataset.csv')
        self.data_manager.load_dataset()
        self.selected_image_path = None 

        # Title
        self.label_title = tk.Label(root, text="Plant Health Checker", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=20)

        # Instructions
        tk.Label(root, text="Step 1: Upload Image", font=("Arial", 12)).pack(pady=(10, 5))
