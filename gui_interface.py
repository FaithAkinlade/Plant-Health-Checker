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

    # ... inside __init__ ...
        # INTERACTIVE ELEMENT 1: Select Image Button
        self.btn_select = tk.Button(root, text="Select Plant Image", command=self.select_image, height=2, width=20)
        self.btn_select.pack(pady=5)

        # Label to show file path
        self.label_file_path = tk.Label(root, text="No file selected", fg="gray", wraplength=400)
        self.label_file_path.pack(pady=5)

    # INTERACTIVE ELEMENT 2: Analyze Button (Triggers Window 2)
        self.btn_analyze = tk.Button(root, text="Analyze Plant Health", command=self.open_results_window,
                                     bg="lightgreen", font=("Arial", 12, "bold"))
        self.btn_analyze.pack(pady=30)


    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select a Plant Image",
                                               filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            self.label_file_path.config(text=f"File: {file_path}", fg="black")

    def open_results_window(self):
        """Opens the Second Window with details."""
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        # Create the Second Window (Popup)
        results_window = tk.Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("400x350")

        # Content of Second Window
        tk.Label(results_window, text="Analysis Complete", font=("Arial", 16, "bold")).pack(pady=20)

        # Placeholder Details
        details_frame = tk.Frame(results_window, relief="groove", borderwidth=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(details_frame, text="Condition: (G)ood/bad)", font=("Arial", 12)).pack(pady=5)
        tk.Label(details_frame, text="Confidence: (Health Percentage)", font=("Arial", 12)).pack(pady=5)
        tk.Label(details_frame, text="Details: (The plant details that we will output.", wraplength=300).pack(pady=10)

        # Close Button
        tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)
