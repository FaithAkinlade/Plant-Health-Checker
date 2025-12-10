# Plant Health Checker
# Authors: Faith Akinlade, Smit Desai, Pratham Waghela (Group 7)
# Description: Provides a graphical user interface (GUI) using Tkinter to allow users to upload plant images and check
# their health. Integrates with the trained CNN model to make predictions.

# gui_interface.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import ImageTk, Image
import os
import shutil
import platform
import subprocess
from datetime import datetime

# Import both prediction functions
try:
    from model_predict import predict_image, check_if_plant
except ImportError:
    print("Warning: model_predict.py not found. Analysis will use dummy data.")
    predict_image = None
    check_if_plant = None


class PlantHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 7: Plant Health Checker")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # BACKGROUND CANVAS
        self.canvas = tk.Canvas(root, width=900, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load Background Image
        try:
            self.bg_image = Image.open("background_fixed.jpg")
            self.bg_image = self.bg_image.resize((900, 650))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except FileNotFoundError:
            self.canvas.config(bg="#d9d9d9")
            print("Warning: background_fixed.jpg not found.")

        # LEFT SIDE 
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

        # BUTTONS 
        button_width = 24

        # 1. Select Image
        self.btn_select = tk.Button(root, text="Select Plant Image", command=self.select_image, width=button_width)
        self.canvas.create_window(center_x, 120, window=self.btn_select)

        # 2. Analyze
        self.btn_analyze = tk.Button(
            root, text="Analyze Plant Health", command=self.open_results_window,
            font=("Arial", 11, "bold"), width=button_width, bg="#e1e1e1"
        )
        self.canvas.create_window(center_x, 170, window=self.btn_analyze)

        # 3. Save Current Photo
        self.btn_save = tk.Button(
            root, text="Save Current Photo", command=self.save_current_image, width=button_width
        )
        self.canvas.create_window(center_x, 220, window=self.btn_save)

        # 4. View History List
        self.btn_view_list = tk.Button(
            root, text="View History List", command=self.view_history_popup, width=button_width
        )
        self.canvas.create_window(center_x, 270, window=self.btn_view_list)

        # 5. Open Saved Images Folder
        self.btn_open_folder = tk.Button(
            root, text="Open Saved Images Folder", command=self.open_saved_images_folder, width=button_width,
            bg="#d0f0c0"
        )
        self.canvas.create_window(center_x, 320, window=self.btn_open_folder)

        # 6. Reset
        self.btn_reset = tk.Button(root, text="Reset Selection", command=self.reset_selection, width=button_width)
        self.canvas.create_window(center_x, 380, window=self.btn_reset)

        # 7. Exit
        self.btn_exit = tk.Button(root, text="Exit", command=root.quit, width=button_width)
        self.canvas.create_window(center_x, 430, window=self.btn_exit)

        # RIGHT SIDE (Image Preview) 
        self.right_frame = tk.Frame(root, bg="white", highlightthickness=2, bd=2, relief="groove")
        self.right_frame.place(x=450, y=50, width=400, height=400)

        self.image_label = tk.Label(self.right_frame, bg="white", text="Preview Area")
        self.image_label.pack(expand=True, fill="both")

        self.selected_image_path = None
        self.displayed_image = None
        self.history_file = "history_log.txt"
        self.save_folder = "saved_images"

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select a Plant Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.show_image_on_right(file_path)

    def show_image_on_right(self, file_path):
        try:
            img = Image.open(file_path)
            img = img.resize((380, 380))
            self.displayed_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.displayed_image, text="")
        except Exception as e:
            messagebox.showerror("Error", "Could not open image.")

    def save_current_image(self):
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "No image selected to save.")
            return

        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_ext = os.path.splitext(self.selected_image_path)[1]
        new_filename = f"plant_{timestamp}{original_ext}"
        destination_path = os.path.join(self.save_folder, new_filename)

        try:
            shutil.copy(self.selected_image_path, destination_path)
            messagebox.showinfo("Success", f"Image saved successfully to '{self.save_folder}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    def save_to_history(self, plant_class, confidence):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = os.path.basename(self.selected_image_path)
            log_entry = f"[{timestamp}] File: {filename} | Result: {plant_class} ({confidence:.2f}%)\n"

            with open(self.history_file, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error saving history: {e}")

    def get_plant_type(self, full_class_name):
        if "___" in full_class_name:
            return full_class_name.split("___")[0]
        return full_class_name.split(" ")[0]

    def get_plant_condition(self, full_class_name):
        if "___" in full_class_name:
            condition_part = full_class_name.split("___")[1]
            return condition_part.replace("_", " ")
        return full_class_name

    def get_plant_message(self, plant_class):
        name = plant_class
        # Universal healthy message
        if "healthy" in name:
            return "Your plant looks healthy! Keep up the great care—continue proper watering, sunlight, and avoid over-fertilization."

        # Apple Diseases
        elif "Apple___Apple_scab" in name:
            return "Apple Scab detected. Remove infected leaves and apply a fungicide containing captan or mancozeb. Improve air circulation by pruning."
        elif "Apple___Black_rot" in name:
            return "Black Rot found on Apple. Remove infected fruits and branches immediately, and apply a copper-based fungicide."
        elif "Apple___Cedar_apple_rust" in name:
            return "Cedar Apple Rust detected. Remove nearby cedar hosts if possible and apply sulfur or copper fungicide at bud break."

        # Blueberry
        elif "Blueberry" in name:
            return "Potential blueberry issue. Check for mildew or discoloration and prune crowded branches to improve airflow."

        # Cherry Diseases
        elif "Cherry_(including_sour)___Powdery_mildew" in name:
            return "Powdery Mildew found on Cherry. Increase air flow by pruning and use neem oil or potassium bicarbonate spray."

        # Corn (Maize) Diseases
        elif "Cercospora_leaf_spot" in name:
            return "Cercospora Leaf Spot detected on Corn. Use crop rotation, avoid overhead watering, and apply a strobilurin fungicide."
        elif "Corn_(maize)___Common_rust_" in name:
            return "Common Rust in Corn. Improve ventilation and consider rust-resistant varieties next season."
        elif "Corn_(maize)___Northern_Leaf_Blight" in name:
            return "Northern Leaf Blight detected. Remove infected debris and apply fungicide early in the season."

        # Grape Diseases
        elif "Grape___Black_rot" in name:
            return "Black Rot on Grapes. Remove all infected fruit immediately and spray a fungicide like myclobutanil."
        elif "Grape___Esca_(Black_Measles)" in name:
            return "Esca/Black Measles in Grapes. Remove infected wood and avoid drought stress. Fungicide options are limited."
        elif "Grape___Leaf_blight" in name:
            return "Leaf Blight detected in Grapes. Remove infected leaves and apply copper fungicide."

        # Citrus/Orange
        elif "Orange___Haunglongbing_(Citrus_greening)" in name:
            return "Citrus Greening detected. Unfortunately, there is no cure. Remove severely infected trees and control psyllid insects."

        # Peach & Pepper Bacterial Spot
        elif "Bacterial_spot" in name:
            return "Bacterial Spot detected. Use copper spray, avoid overhead watering, and remove infected leaves."

        # Potato Diseases
        elif "Potato___Early_blight" in name:
            return "Early Blight in Potatoes. Remove affected foliage and apply chlorothalonil or copper fungicide."
        elif "Potato___Late_blight" in name:
            return "Late Blight detected. Quickly remove infected plants and use a fungicide such as fluazinam."

        # Squash Powdery Mildew
        elif "Squash___Powdery_mildew" in name:
            return "Powdery Mildew on Squash. Increase airflow and apply sulfur or neem oil."

        # Strawberry Leaf Scorch
        elif "Strawberry___Leaf_scorch" in name:
            return "Leaf Scorch on Strawberry. Remove infected leaves, ensure good drainage, and avoid watering from above."

        # Tomato Diseases
        elif "Tomato___Bacterial_spot" in name:
            return "Bacterial Spot on Tomato. Apply copper sprays and avoid touching wet leaves."
        elif "Tomato___Early_blight" in name:
            return "Early Blight in Tomato. Remove infected leaves and use fungicides containing chlorothalonil."
        elif "Tomato___Late_blight" in name:
            return "Late Blight detected. Remove plants immediately to prevent spreading and use resistant varieties."
        elif "Tomato___Leaf_Mold" in name:
            return "Leaf Mold on Tomato. Reduce humidity and use copper fungicide."
        elif "Tomato___Septoria_leaf_spot" in name:
            return "Septoria Leaf Spot found. Remove lower leaves and apply fungicide."
        elif "Tomato___Spider_mites" in name:
            return "Spider Mites detected. Spray with water to knock them off and use neem oil or insecticidal soap."
        elif "Tomato___Target_Spot" in name:
            return "Target Spot detected. Remove infected leaves and apply a broad-spectrum fungicide."
        elif "Tomato___Tomato_Yellow_Leaf_Curl_Virus" in name:
            return "Yellow Leaf Curl Virus detected. Remove infected plants and control whiteflies."
        elif "Tomato___Tomato_mosaic_virus" in name:
            return "Tomato Mosaic Virus. Remove plant and sanitize tools thoroughly."

        # Generic feedback
        else:
            return "We detected a potential plant issue. Monitor your plant closely and consider pruning affected leaves or using a fungicide."

    def open_results_window(self):
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        # Plant Photo Checker
        if check_if_plant:
            # Note: Now expecting TWO return values (is_plant, label)
            is_plant, detected_label = check_if_plant(self.selected_image_path)

            if not is_plant:
                # Ask the user if they want to proceed anyway
                response = messagebox.askyesno(
                    "Unusual Image Detected",
                    f"The system thinks this looks like: '{detected_label}'\n"
                    "It might not be a plant.\n\n"
                    "Do you want to analyze it anyway?"
                )
                if not response:  # If user clicks 'No', stop.
                    return

        # PERFORM ANALYSIS
        if predict_image is None:
            plant_class = "Demo: Apple___Black_rot"
            confidence = 88.5
        else:
            try:
                plant_class, confidence = predict_image(self.selected_image_path)
            except Exception as e:
                messagebox.showerror("Prediction Error", str(e))
                return

        self.save_to_history(plant_class, confidence)

        # 1. Get Clean Data
        plant_name = self.get_plant_type(plant_class)
        condition_name = self.get_plant_condition(plant_class)

        results_window = tk.Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("400x420")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 175
        results_window.geometry(f"+{x}+{y}")

        tk.Label(results_window, text="Analysis Complete", font=("Arial", 16, "bold")).pack(pady=15)

        details_frame = tk.Frame(results_window, relief="groove", borderwidth=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Plant Name
        tk.Label(details_frame, text="Plant Name:", font=("Arial", 10, "bold"), fg="gray").pack(pady=(10, 0))
        tk.Label(details_frame, text=plant_name, font=("Arial", 14, "bold"), fg="#2c3e50").pack(pady=(0, 5))

        # Condition
        tk.Label(details_frame, text="Plant Condition:", font=("Arial", 10, "bold"), fg="gray").pack(pady=(5, 0))
        cond_color = "green" if "healthy" in condition_name.lower() else "red"
        tk.Label(details_frame, text=condition_name, font=("Arial", 12, "bold"), fg=cond_color).pack(pady=(0, 5))

        # Confidence
        tk.Label(details_frame, text=f"Confidence: {confidence:.2f}%", font=("Arial", 10)).pack(pady=5)

        # Recommendation
        tk.Label(details_frame, text="Recommendation:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Label(details_frame, text=self.get_plant_message(plant_class), wraplength=300, justify="center").pack(pady=5)

        tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

    def view_history_popup(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("Analysis History")
        history_win.geometry("700x400")

        tk.Label(history_win, text="History Log", font=("Arial", 14, "bold")).pack(pady=10)

        text_area = scrolledtext.ScrolledText(history_win, width=80, height=15, font=("Consolas", 9))
        text_area.pack(padx=10, pady=10)

        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                content = f.read()
                text_area.insert(tk.END, content)
        else:
            text_area.insert(tk.END, "No history found yet.")

        text_area.config(state=tk.DISABLED)
        tk.Button(history_win, text="Close", command=history_win.destroy).pack(pady=5)

    def open_saved_images_folder(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        folder_path = os.path.abspath(self.save_folder)
        self.open_file_in_os(folder_path)

    def open_file_in_os(self, path):
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', path])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(path)
            else:  # linux
                subprocess.call(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open path: {e}")

    def reset_selection(self):
        self.selected_image_path = None
        self.image_label.config(image="", text="Preview Area")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlantHealthApp(root)
    root.mainloop()
