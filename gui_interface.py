# gui_interface.py (Update imports and __init__)
import tkinter as tk
from tkinter import filedialog, messagebox
from data_manager import PlantDataManager # <--- Added this

class PlantHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("500x400")

        # We load data immediately so the user doesn't have to click a button
        self.data_manager = PlantDataManager('data/plants_dataset.csv') # <--- Added
        self.data_manager.load_dataset() # <--- Added
        self.selected_image_path = None # <--- Added

        # Title
        self.label_title = tk.Label(root, text="Plant Health Checker", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=20)

        # Instructions
        tk.Label(root, text="Step 1: Upload Image", font=("Arial", 12)).pack(pady=(10, 5))

    # ... inside __init__ ...
        # INTERACTIVE ELEMENT 1: Select Image Button
        self.btn_select = tk.Button(root, text="Select Plant Image", command=self.select_image, height=2, width=20)
        self.btn_select.pack(pady=5)

        # Label to show file path
        self.label_file_path = tk.Label(root, text="No file selected", fg="gray", wraplength=400)
        self.label_file_path.pack(pady=5)

    # ... at the bottom of the class ...
    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select a Plant Image",
                                               filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            self.label_file_path.config(text=f"File: {file_path}", fg="black")
