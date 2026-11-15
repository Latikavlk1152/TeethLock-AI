"""
TeethLock AI Authentication System

GUI application for:
- User registration
- Dataset collection
- Model training
- Authentication testing

Developed as a Final Year B.E. Project.
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TeethLockApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("TeethLock - AI Authentication System")
        self.resizable(False, False)
        self.geometry("1200x600")
        window_width = 1200
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=10)
        container.grid_columnconfigure(0, weight=10)

        self.frames = {}
        for F in (HomePage, AddUserPage, TrainModelPage, TestModelPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Teeth Lock System", font=controller.title_font, fg="#263942")
        label.pack(side="top", fill="x", pady=10)
        button_add_user = tk.Button(self, text="Add New User", fg="#ffffff", bg="#263942", command=lambda: controller.show_frame("AddUserPage"))
        button_train_model = tk.Button(self, text="Train Model", fg="#ffffff", bg="#263942", command=lambda: controller.show_frame("TrainModelPage"))
        button_test_model = tk.Button(self, text="Test on Your Device", fg="#ffffff", bg="#263942", command=lambda: controller.show_frame("TestModelPage"))
        button_add_user.pack(pady=10)
        button_train_model.pack(pady=10)
        button_test_model.pack(pady=10)

    

class AddUserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Add New User", font=controller.title_font, fg="#263942")
        label.pack(side="top", fill="x", pady=10)
        button_capture_teeth = tk.Button(self, text="Capture Teeth", fg="#ffffff", bg="#263942", command=self.capture_teeth)
        button_back = tk.Button(self, text="Back", fg="#263942", bg="#ffffff", command=lambda: controller.show_frame("HomePage"))
        button_capture_teeth.pack(pady=10)
        button_back.pack(pady=10)

    def capture_teeth(self):
        try:
            user_info = simpledialog.askstring("Input", "Enter your name and user ID (comma-separated):")
            if user_info:
                user_name, user_id = map(str.strip, user_info.split(','))
                user_id = int(user_id)

                confirmed = messagebox.askokcancel("Confirmation", "100 images will be captured of your teeth. Please show your teeth. Continue?")
                if confirmed:
                    dataset_script = os.path.join(BASE_DIR, "create_face_datasets.py")

                    subprocess.run([
                       sys.executable,
                       dataset_script,
                       user_name,
                       str(user_id)
                    ],
                    check=True
                    )


                    messagebox.showinfo("Success", "Teeth captured successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


class TrainModelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Train Model", font=controller.title_font, fg="#263942")
        label.pack(side="top", fill="x", pady=10)
        button_train = tk.Button(self, text="Train Model", fg="#ffffff", bg="#263942", command=self.train_model)
        button_back = tk.Button(self, text="Back", fg="#263942", bg="#ffffff", command=lambda: controller.show_frame("HomePage"))
        button_train.pack(pady=10)
        button_back.pack(pady=10)

    def train_model(self):
        try:
            confirmed = messagebox.askokcancel("Confirmation", "Please complete the 'Add New User' step before training the model. This step is crucial for collecting necessary data. If already completed, Proceed. NOTE: Model training requires some time. Thank you for your patience! Continue?")
            if confirmed:
                    training_script = os.path.join(BASE_DIR, "training_model.py")

                    subprocess.run([
                       sys.executable,
                       training_script
                    ],
                    check=True
                    )


            messagebox.showinfo("Success", "User Registration Complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class TestModelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Test on Your Device", font=controller.title_font, fg="#263942")
        label.pack(side="top", fill="x", pady=10)
        button_test = tk.Button(self, text="Test Model", fg="#ffffff", bg="#263942", command=self.test_model)
        button_back = tk.Button(self, text="Back", fg="#263942", bg="#ffffff", command=lambda: controller.show_frame("HomePage"))
        button_test.pack(pady=10)
        button_back.pack(pady=10)

    def test_model(self):
        try:
            # Call the lock_unlock_face_recognition.py file using subprocess
            # Modify the paths accordingly
            recognition_script = os.path.join(BASE_DIR, "lock_unlock_face_recognition.py")

            subprocess.run([
               sys.executable,
               recognition_script
            ],
            check=True
            )

            # messagebox.showinfo("Success", "Testing successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = TeethLockApp()
    
    app.mainloop()