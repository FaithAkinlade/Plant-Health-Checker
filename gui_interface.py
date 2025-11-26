# Project: Plant Health Checker
# Students: Faith Akinlade, Smit Desai, Pratham Waghela
# Description: Provides a graphical user interface (GUI) using Tkinter to allow users to upload plant images and check
# their health. Integrates with the trained CNN model to make predictions.

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import ImageTk, Image
import os
import shutil
import platform
import subprocess
from datetime import datetime

# Try to import the prediction function.
try:
    from model_predict import predict_image
except ImportError:
    print("Warning: model_predict.py not found. Analysis will use dummy data.")
    predict_image = None


class PlantHealthApp:
    """
    The main application class for the Plant Health Checker.
    It manages the GUI window, handles user input (buttons/files),
    and coordinates the analysis and file saving processes.
    """
    def __init__(self, root):
       """
        Initializes the main application window and sets up the layout.
        :param root: The main window object from Tkinter.
        :type root: tk.Tk
        """
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

        #  RIGHT SIDE (Image Preview) 
        self.right_frame = tk.Frame(root, bg="white", highlightthickness=2, bd=2, relief="groove")
        self.right_frame.place(x=450, y=50, width=400, height=400)

        self.image_label = tk.Label(self.right_frame, bg="white", text="Preview Area")
        self.image_label.pack(expand=True, fill="both")

        self.selected_image_path = None
        self.displayed_image = None
        self.history_file = "history_log.txt"
        self.save_folder = "saved_images"

        

    def select_image(self):
        """
        Opens a file dialog so the user can choose an image file.
        :return: None
        """
        file_path = filedialog.askopenfilename(
            title="Select a Plant Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.show_image_on_right(file_path)

    def show_image_on_right(self, file_path):
        """
        Resizes and displays the chosen image in the preview box.
        :param file_path: The location of the image file.
        :type file_path: str
        :return: None
        """
        try:
            img = Image.open(file_path)
            img = img.resize((380, 380))
            self.displayed_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.displayed_image, text="")
        except Exception as e:
            messagebox.showerror("Error", "Could not open image.")

    # SAVE IMAGE FILE 
    def save_current_image(self):
        """
        Saves the currently selected image into the 'saved_images' folder.
        :return: None
        """
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

    # SAVE TEXT LOG ENTRY 
    def save_to_history(self, plant_class, confidence):
        """
        Writes the result of an analysis to the history log file.
        :param plant_class: The health status or disease name.
        :type plant_class: str
        :param confidence: The confidence percentage from the model.
        :type confidence: float
        :return: None
        """
        try:
            # FIXED: Added seconds back and corrected the order: File first, then Result
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = os.path.basename(self.selected_image_path)

            # This matches your first 3 lines format:
            log_entry = f"[{timestamp}] File: {filename} | Result: {plant_class} ({confidence:.2f}%)\n"

            with open(self.history_file, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error saving history: {e}")

    def get_plant_message(self, plant_class):
        messages = {
            "Healthy": "Your plant looks healthy! Keep watering at recommended intervals and provide sunlight.",
            "Rust": "Possible rust fungal infection detected. Consider removing infected leaves, and using antifungal spray.",
            "Powdery": "Possible powdery mildew detected. Consider removing leaves, improving air flow and treating with a baking sode solution."
        }

        return messages.get(plant_class, "More analysis is required.")

    def open_results_window(self):
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        if predict_image is None:
            plant_class = "Demo: Apple Rot"
            confidence = 88.5
        else:
            try:
                plant_class, confidence = predict_image(self.selected_image_path)
            except Exception as e:
                messagebox.showerror("Prediction Error", str(e))
                return

        self.save_to_history(plant_class, confidence)

        results_window = tk.Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("400x350")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 175
        results_window.geometry(f"+{x}+{y}")

        tk.Label(results_window, text="Analysis Complete", font=("Arial", 16, "bold")).pack(pady=20)

        details_frame = tk.Frame(results_window, relief="groove", borderwidth=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        color = "green" if "healthy" in plant_class.lower() else "red"
        tk.Label(details_frame, text=f"Condition: {plant_class}", font=("Arial", 12, "bold"), fg=color).pack(pady=5)
        tk.Label(details_frame, text=f"Confidence: {confidence:.2f}%", font=("Arial", 12)).pack(pady=5)

        tk.Label(details_frame, text="Recommendation:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Label(details_frame, text=self.get_plant_message(plant_class), wraplength=300, justify="center").pack(pady=5)

        tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

    # VIEW HISTORY POPUP 
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

    # OPEN SAVED FOLDER 
    def open_saved_images_folder(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        folder_path = os.path.abspath(self.save_folder)
        self.open_file_in_os(folder_path)

    # Helper function to open files/folders 
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
