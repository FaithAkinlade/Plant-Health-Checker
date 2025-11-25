# gui_interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
# from data_manager import PlantDataManager # Ensure this file exists for the app to run fully
from PIL import ImageTk, Image


class PlantHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("900x500")

        # ---------------- BACKGROUND CANVAS ----------------
        # Use Canvas to handle the background image and allow transparent text/buttons
        self.canvas = tk.Canvas(root, width=900, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load Background Image
        try:
            self.bg_image = Image.open("background_fixed.jpg")
            self.bg_image = self.bg_image.resize((900, 500))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            # Draw the image on the canvas
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except FileNotFoundError:
            # Fallback if the image is missing
            self.canvas.config(bg="#d9d9d9")
            print("Warning: background_fixed.jpg not found. Using default background color.")

        # ---------------- LEFT SIDE (Transparent Widgets on Canvas) ----------------
        # We use canvas.create_text and canvas.create_window for transparency

        # Title (Transparent text)
        self.canvas.create_text(
            150, 40,
            text="Plant Health Checker",
            font=("Arial", 18, "bold"),
            fill="black",
            anchor="center"
        )

        # Step label (Transparent text)
        self.canvas.create_text(
            150, 80,
            text="Step 1: Upload Image",
            font=("Arial", 12, "bold"),
            fill="black",
            anchor="center"
        )

        # Upload button
        self.btn_select = tk.Button(
            root,
            text="Select Plant Image",
            command=self.select_image,
            width=20,
            height=2
        )
        self.canvas.create_window(150, 130, window=self.btn_select)

        # File path label (Transparent text)
        self.text_file_path = self.canvas.create_text(
            150, 170,
            text="No file selected",
            fill="black",
            font=("Arial", 15, "bold"),  
            width=260,
            anchor="center"
        )

        # Analyze button
        self.btn_analyze = tk.Button(
            root,
            text="Analyze Plant Health",
            command=self.open_results_window,
            font=("Arial", 12, "bold"),
            width=20
        )
        self.canvas.create_window(150, 220, window=self.btn_analyze)

        # Reset button
        self.btn_reset = tk.Button(
            root,
            text="Reset Selection",
            command=self.reset_selection,
            width=20
        )
        self.canvas.create_window(150, 270, window=self.btn_reset)

        # Exit button
        self.btn_exit = tk.Button(
            root,
            text="Exit",
            command=root.quit,
            width=20
        )
        self.canvas.create_window(150, 320, window=self.btn_exit)

        # ---------------- RIGHT SIDE (Image Preview) ----------------
        # Frame size adjusted to 400x400 and placed at x=450
        self.right_frame = tk.Frame(root, bg="white", highlightthickness=2, bd=2, relief="groove")
        self.right_frame.place(x=450, y=50, width=400, height=400)  # <- RESIZED BLOCK

        self.image_label = tk.Label(self.right_frame, bg="white", text="Preview Area")
        self.image_label.pack(expand=True, fill="both")

        # Load dataset (Uncomment if data_manager is ready)
        # self.data_manager = PlantDataManager('data/plants_dataset.csv')
        # if not self.data_manager.load_dataset():
        #     messagebox.showerror("Error", "Dataset could not be loaded.")

        self.selected_image_path = None
        self.displayed_image = None

    # -----------------------------------------------------

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select a Plant Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            # Update canvas text item
            self.canvas.itemconfig(self.text_file_path, text=f"File: {file_path}", fill="black")
            self.show_image_on_right(file_path)

    def show_image_on_right(self, file_path):
        img = Image.open(file_path)

        # Resizing to fit the new 400x400 frame (380x380 keeps a small margin)
        img = img.resize((380, 380))

        self.displayed_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.displayed_image, text="")

    def open_results_window(self):
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        results_window = tk.Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("400x350")

        tk.Label(results_window, text="Analysis Complete",
                 font=("Arial", 16, "bold")).pack(pady=20)

        details_frame = tk.Frame(results_window, relief="groove", borderwidth=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Placeholder results
        tk.Label(details_frame, text="Condition: (Good/Bad)",
                 font=("Arial", 12)).pack(pady=5)
        tk.Label(details_frame, text="Confidence: (%)",
                 font=("Arial", 12)).pack(pady=5)
        tk.Label(details_frame, text="Details: (Plant details here)",
                 wraplength=300).pack(pady=10)

        tk.Button(results_window, text="Close",
                  command=results_window.destroy).pack(pady=10)

    def reset_selection(self):
        self.selected_image_path = None
        # Reset canvas text item
        self.canvas.itemconfig(self.text_file_path, text="No file selected", fill="gray")
        # Clear the preview area
        self.image_label.config(image="", text="Preview Area")


# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantHealthApp(root)
    root.mainloop()
