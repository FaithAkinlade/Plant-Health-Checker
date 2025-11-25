# gui_interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

# Try to import the prediction function.
# If it fails, the app will still run using dummy data.
try:
    from model_predict import predict_image
except ImportError:
    print("Warning: model_predict.py not found. Analysis will use dummy data.")
    predict_image = None


class PlantHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("900x500")
        self.root.resizable(False, False)  # Lock window size

        # BACKGROUND CANVAS 
        self.canvas = tk.Canvas(root, width=900, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load Background Image
        try:
            self.bg_image = Image.open("background_fixed.jpg")
            self.bg_image = self.bg_image.resize((900, 500))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except FileNotFoundError:
            self.canvas.config(bg="#d9d9d9")
            print("Warning: background_fixed.jpg not found.")

        # LEFT SIDE 
        # Center X coordinate for buttons
        center_x = 150

        # Title
        self.canvas.create_text(
            center_x, 40,
            text="Plant Health Checker",
            font=("Arial", 18, "bold"),
            fill="black",
            anchor="center"
        )

        # Step label
        self.canvas.create_text(
            center_x, 80,
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
        self.canvas.create_window(center_x, 130, window=self.btn_select)

        # Analyze button (Moved up since we removed the file path text)
        self.btn_analyze = tk.Button(
            root,
            text="Analyze Plant Health",
            command=self.open_results_window,
            font=("Arial", 12, "bold"),
            width=20
        )
        self.canvas.create_window(center_x, 200, window=self.btn_analyze)

        # Reset button
        self.btn_reset = tk.Button(
            root,
            text="Reset Selection",
            command=self.reset_selection,
            width=20
        )
        self.canvas.create_window(center_x, 250, window=self.btn_reset)

        # Exit button
        self.btn_exit = tk.Button(
            root,
            text="Exit",
            command=root.quit,
            width=20
        )
        self.canvas.create_window(center_x, 300, window=self.btn_exit)

        # RIGHT SIDE (Image Preview) 
        self.right_frame = tk.Frame(root, bg="white", highlightthickness=2, bd=2, relief="groove")
        self.right_frame.place(x=450, y=50, width=400, height=400)

        self.image_label = tk.Label(self.right_frame, bg="white", text="Preview Area")
        self.image_label.pack(expand=True, fill="both")

        self.selected_image_path = None
        self.displayed_image = None


    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select a Plant Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            # We no longer display the text path here
            self.show_image_on_right(file_path)

    def show_image_on_right(self, file_path):
        try:
            img = Image.open(file_path)
            # Resize to fit the 400x400 frame
            img = img.resize((380, 380))
            self.displayed_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.displayed_image, text="")
        except Exception as e:
            messagebox.showerror("Error", "Could not open image.")

    def get_plant_message(self, plant_class):
        name = plant_class.lower()
        if "healthy" in name:
            return "Your plant looks healthy! Keep up the good work."
        elif "rot" in name or "fung" in name:
            return "Possible fungal issue. Avoid overwatering."
        elif "bacteri" in name:
            return "Bacterial symptoms detected. Isolate the plant."
        elif "vir" in name:
            return "Possible viral infection. Check for pests."
        else:
            return "Disease detected. Consult a specialist."

    def open_results_window(self):
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        # Check if model is loaded
        if predict_image is None:
            # Fallback for testing UI without model
            plant_class = "Demo: Apple Rot"
            confidence = 88.5
        else:
            try:
                # Run ML prediction
                plant_class, confidence = predict_image(self.selected_image_path)
            except Exception as e:
                messagebox.showerror("Prediction Error", str(e))
                return

        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("400x350")

        # Center the window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 175
        results_window.geometry(f"+{x}+{y}")

        tk.Label(results_window, text="Analysis Complete",
                 font=("Arial", 16, "bold")).pack(pady=20)

        details_frame = tk.Frame(results_window, relief="groove", borderwidth=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        color = "green" if "healthy" in plant_class.lower() else "red"

        tk.Label(details_frame, text=f"Condition: {plant_class}",
                 font=("Arial", 12, "bold"), fg=color).pack(pady=5)

        tk.Label(details_frame, text=f"Confidence: {confidence:.2f}%",
                 font=("Arial", 12)).pack(pady=5)

        tk.Label(details_frame, text="Recommendation:",
                 font=("Arial", 10, "bold")).pack(pady=(10, 0))

        advice = self.get_plant_message(plant_class)
        tk.Label(details_frame, text=advice,
                 wraplength=300, justify="center").pack(pady=5)

        tk.Button(results_window, text="Close",
                  command=results_window.destroy).pack(pady=10)

    def reset_selection(self):
        self.selected_image_path = None
        self.image_label.config(image="", text="Preview Area")


# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantHealthApp(root)
    root.mainloop()
