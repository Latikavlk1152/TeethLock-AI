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
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Modern Theme Color Palette
BG_COLOR = "#121212"
CARD_BG = "#1E1E1E"
ACCENT_GREEN = "#00E676"
ACCENT_BLUE = "#29B6F6"
TEXT_COLOR = "#E0E0E0"
TEXT_MUTED = "#9E9E9E"

class CustomDialog(tk.Toplevel):
    """Custom themed dialog window matching the application color palette."""
    def __init__(self, parent, title, prompt, is_integer=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x220")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.is_integer = is_integer

        # Center dialog on parent window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 220) // 2
        self.geometry(f"+{x}+{y}")

        # Prompt Label
        tk.Label(self, text=prompt, font=("Helvetica", 11, "bold"), fg=TEXT_COLOR, bg=BG_COLOR, wraplength=360, justify="left").pack(pady=20, padx=20)

        # Entry Box
        self.entry = tk.Entry(self, font=("Helvetica", 12), bg="#2D2D2D", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat")
        self.entry.pack(pady=5, padx=20, ipadx=5, ipady=5)
        self.entry.focus()
        self.entry.bind("<Return>", lambda event: self.on_ok())

        # Buttons Container
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Cancel", font=("Helvetica", 10), bg="#333333", fg=TEXT_COLOR, relief="flat", width=12, command=self.on_cancel).pack(side="left", padx=10)
        tk.Button(btn_frame, text="OK", font=("Helvetica", 10, "bold"), bg=ACCENT_GREEN, fg="#121212", relief="flat", width=12, command=self.on_ok).pack(side="left", padx=10)

    def on_ok(self):
        val = self.entry.get().strip()
        if not val:
            return
        if self.is_integer:
            try:
                self.result = int(val)
            except ValueError:
                return
        else:
            self.result = val
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


class CustomMessageBox(tk.Toplevel):
    """Custom themed message box or confirmation dialog."""
    def __init__(self, parent, title, message, is_confirm=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x200")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = False

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 420) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
        self.geometry(f"+{x}+{y}")

        tk.Label(self, text=title, font=("Helvetica", 12, "bold"), fg=ACCENT_GREEN, bg=BG_COLOR).pack(anchor="w", padx=20, pady=(15, 5))
        tk.Label(self, text=message, font=("Helvetica", 10), fg=TEXT_COLOR, bg=BG_COLOR, wraplength=380, justify="left").pack(anchor="w", padx=20, pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        if is_confirm:
            tk.Button(btn_frame, text="Cancel", font=("Helvetica", 10), bg="#333333", fg=TEXT_COLOR, relief="flat", width=12, command=self.on_cancel).pack(side="left", padx=10)
            tk.Button(btn_frame, text="Proceed", font=("Helvetica", 10, "bold"), bg=ACCENT_GREEN, fg="#121212", relief="flat", width=12, command=self.on_ok).pack(side="left", padx=10)
        else:
            tk.Button(btn_frame, text="OK", font=("Helvetica", 10, "bold"), bg=ACCENT_BLUE, fg="#121212", relief="flat", width=14, command=self.on_ok).pack(side="left")

    def on_ok(self):
        self.result = True
        self.destroy()

    def on_cancel(self):
        self.result = False
        self.destroy()


class TeethLockApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family='Helvetica', size=12)
        self.button_font = tkfont.Font(family='Helvetica', size=11, weight="bold")
        
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

        self.configure(bg=BG_COLOR)

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, AddUserPage, TrainModelPage, TestModelPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "reset_status"):
            frame.reset_status()
        frame.tkraise()

    def on_closing(self):
        dialog = CustomMessageBox(self, "Quit Application", "Are you sure you want to exit TeethLock AI?", is_confirm=True)
        self.wait_window(dialog)
        if dialog.result:
            self.destroy()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(pady=40)

        label = tk.Label(header_frame, text="TEETHLOCK AI", font=controller.title_font, fg=ACCENT_GREEN, bg=BG_COLOR)
        label.pack(pady=5)
        
        sub_label = tk.Label(header_frame, text="Secure Biometric Authentication via Dental Pattern Recognition", font=controller.subtitle_font, fg=TEXT_MUTED, bg=BG_COLOR)
        sub_label.pack()

        cards_frame = tk.Frame(self, bg=BG_COLOR)
        cards_frame.pack(pady=20)

        # Block 1: Enrollment
        card1 = tk.Frame(cards_frame, bg=CARD_BG, bd=1, relief="solid", width=300, height=220)
        card1.pack_propagate(False)
        card1.grid(row=0, column=0, padx=15)
        
        tk.Label(card1, text="1. Enrollment", font=("Helvetica", 13, "bold"), fg=TEXT_COLOR, bg=CARD_BG).pack(pady=15)
        tk.Label(card1, text="Capture & register your\nteeth dataset securely.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="center").pack(pady=5)
        tk.Button(card1, text="Add New User", font=controller.button_font, fg="#121212", bg=ACCENT_GREEN, activebackground="#00C853", relief="flat", cursor="hand2", command=lambda: controller.show_frame("AddUserPage"), width=18, height=2).pack(pady=15)

        # Block 2: Model Control
        card2 = tk.Frame(cards_frame, bg=CARD_BG, bd=1, relief="solid", width=300, height=220)
        card2.pack_propagate(False)
        card2.grid(row=0, column=1, padx=15)
        
        tk.Label(card2, text="2. Model Control", font=("Helvetica", 13, "bold"), fg=TEXT_COLOR, bg=CARD_BG).pack(pady=15)
        tk.Label(card2, text="Train the CNN backbone\nwith captured image datasets.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="center").pack(pady=5)
        tk.Button(card2, text="Train Model", font=controller.button_font, fg="#121212", bg=ACCENT_BLUE, activebackground="#00B0FF", relief="flat", cursor="hand2", command=lambda: controller.show_frame("TrainModelPage"), width=18, height=2).pack(pady=15)

        # Block 3: Security Shield
        card3 = tk.Frame(cards_frame, bg=CARD_BG, bd=1, relief="solid", width=300, height=220)
        card3.pack_propagate(False)
        card3.grid(row=0, column=2, padx=15)
        
        tk.Label(card3, text="3. Security Shield", font=("Helvetica", 13, "bold"), fg=TEXT_COLOR, bg=CARD_BG).pack(pady=15)
        tk.Label(card3, text="Launch live verification\n& automated OS lockdown.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="center").pack(pady=5)
        tk.Button(card3, text="Test on Your Device", font=controller.button_font, fg="#121212", bg=ACCENT_GREEN, activebackground="#00C853", relief="flat", cursor="hand2", command=lambda: controller.show_frame("TestModelPage"), width=18, height=2).pack(pady=15)


class AddUserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        label = tk.Label(self, text="User Enrollment & Dataset Collection", font=controller.title_font, fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top", fill="x", pady=30)

        content_card = tk.Frame(self, bg=CARD_BG, padx=40, pady=30)
        content_card.pack(pady=10)

        tk.Label(content_card, text="Instructions:", font=("Helvetica", 12, "bold"), fg=ACCENT_GREEN, bg=CARD_BG).pack(anchor="w", pady=5)
        tk.Label(content_card, text="• Enter your name and numeric User ID.\n• Show your teeth clearly to the camera during capture.\n• 100 Region of Interest (ROI) frames will be saved automatically.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="left").pack(anchor="w", pady=5)

        self.status_label = tk.Label(content_card, text="Status: Ready to capture dataset", font=("Helvetica", 11, "italic"), fg=ACCENT_BLUE, bg=CARD_BG)
        self.status_label.pack(pady=20)

        tk.Button(content_card, text="Capture Teeth Dataset", font=controller.button_font, fg="#121212", bg=ACCENT_GREEN, relief="flat", cursor="hand2", command=self.capture_teeth, width=25, height=2).pack(pady=10)
        tk.Button(content_card, text="← Back to Dashboard", font=("Helvetica", 10), fg=TEXT_COLOR, bg="#333333", relief="flat", cursor="hand2", command=lambda: controller.show_frame("HomePage"), width=25, height=1).pack(pady=5)

    def reset_status(self):
        self.status_label.config(text="Status: Ready to capture dataset", fg=ACCENT_BLUE)

    def capture_teeth(self):
        try:
            name_dialog = CustomDialog(self, "User Name", "Enter your name:")
            self.wait_window(name_dialog)
            user_name = name_dialog.result
            if not user_name:
                return
            
            id_dialog = CustomDialog(self, "User ID", "Enter your numeric user ID (e.g., 1, 2, 11):", is_integer=True)
            self.wait_window(id_dialog)
            user_id = id_dialog.result
            if user_id is None:
                return

            conf_dialog = CustomMessageBox(self, "Confirmation", f"100 images will be captured of your teeth for {user_name.strip()}. Please show your teeth. Continue?", is_confirm=True)
            self.wait_window(conf_dialog)
            
            if conf_dialog.result:
                self.status_label.config(text=f"Status: Capturing dataset for {user_name.strip()}...", fg=ACCENT_GREEN)
                self.update_idletasks()

                dataset_script = os.path.join(BASE_DIR, "create_face_datasets.py")

                subprocess.run([
                    sys.executable,
                    dataset_script,
                    user_name.strip(),
                    str(user_id)
                ],
                check=True
                )

                self.status_label.config(text="Status: Dataset captured successfully!", fg=ACCENT_GREEN)
                success_box = CustomMessageBox(self, "Success", "Teeth captured successfully!")
                self.wait_window(success_box)
        except Exception as e:
            self.status_label.config(text="Status: Capture failed / cancelled", fg="#FF5252")
            err_box = CustomMessageBox(self, "Error", f"An error occurred: {str(e)}")
            self.wait_window(err_box)


class TrainModelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        label = tk.Label(self, text="Deep Learning Model Training", font=controller.title_font, fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top", fill="x", pady=30)

        content_card = tk.Frame(self, bg=CARD_BG, padx=40, pady=30)
        content_card.pack(pady=10)

        tk.Label(content_card, text="CNN Backbone Configuration:", font=("Helvetica", 12, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(anchor="w", pady=5)
        tk.Label(content_card, text="• Compiles Convolutional Layers & MaxPooling architecture.\n• Optimizes weights using Adam & categorical cross-entropy.\n• Ensure 'Add New User' dataset collection is completed first.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="left").pack(anchor="w", pady=5)

        self.status_label = tk.Label(content_card, text="Status: Ready to train model", font=("Helvetica", 11, "italic"), fg=ACCENT_BLUE, bg=CARD_BG)
        self.status_label.pack(pady=20)

        tk.Button(content_card, text="Start Training CNN", font=controller.button_font, fg="#121212", bg=ACCENT_BLUE, relief="flat", cursor="hand2", command=self.train_model, width=25, height=2).pack(pady=10)
        tk.Button(content_card, text="← Back to Dashboard", font=("Helvetica", 10), fg=TEXT_COLOR, bg="#333333", relief="flat", cursor="hand2", command=lambda: controller.show_frame("HomePage"), width=25, height=1).pack(pady=5)

    def reset_status(self):
        self.status_label.config(text="Status: Ready to train model", fg=ACCENT_BLUE)

    def train_model(self):
        try:
            conf_dialog = CustomMessageBox(self, "Confirmation", "Please complete the 'Add New User' step before training the model. This step is crucial for collecting necessary data. If already completed, Proceed. NOTE: Model training requires some time. Thank you for your patience! Continue?", is_confirm=True)
            self.wait_window(conf_dialog)

            if conf_dialog.result:
                self.status_label.config(text="Status: Training CNN model in progress...", fg=ACCENT_GREEN)
                self.update_idletasks()

                training_script = os.path.join(BASE_DIR, "training_model.py")

                subprocess.run([
                   sys.executable,
                   training_script
                ],
                check=True
                )

                self.status_label.config(text="Status: Model Training Complete!", fg=ACCENT_GREEN)
                success_box = CustomMessageBox(self, "Success", "Model Training Complete!")
                self.wait_window(success_box)
        except Exception as e:
            self.status_label.config(text="Status: Training failed", fg="#FF5252")
            err_box = CustomMessageBox(self, "Error", f"An error occurred: {str(e)}")
            self.wait_window(err_box)


class TestModelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        label = tk.Label(self, text="Real-Time Security Shield & Verification", font=controller.title_font, fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top", fill="x", pady=30)

        content_card = tk.Frame(self, bg=CARD_BG, padx=40, pady=30)
        content_card.pack(pady=10)

        tk.Label(content_card, text="Security Operation Guidelines:", font=("Helvetica", 12, "bold"), fg=ACCENT_GREEN, bg=CARD_BG).pack(anchor="w", pady=5)
        tk.Label(content_card, text="• Opens live webcam feed to verify trained dental patterns.\n• Grants access upon successful match confirmation.\n• Instantly triggers OS screen lock (Win + L) on impostor detection.", font=("Helvetica", 10), fg=TEXT_MUTED, bg=CARD_BG, justify="left").pack(anchor="w", pady=5)

        self.status_label = tk.Label(content_card, text="Status: Security Shield ready", font=("Helvetica", 11, "italic"), fg=ACCENT_BLUE, bg=CARD_BG)
        self.status_label.pack(pady=20)

        tk.Button(content_card, text="Launch Security Shield", font=controller.button_font, fg="#121212", bg=ACCENT_GREEN, relief="flat", cursor="hand2", command=self.test_model, width=25, height=2).pack(pady=10)
        tk.Button(content_card, text="← Back to Dashboard", font=("Helvetica", 10), fg=TEXT_COLOR, bg="#333333", relief="flat", cursor="hand2", command=lambda: controller.show_frame("HomePage"), width=25, height=1).pack(pady=5)

    def reset_status(self):
        self.status_label.config(text="Status: Security Shield ready", fg=ACCENT_BLUE)

    def test_model(self):
        try:
            self.status_label.config(text="Status: Running live camera verification...", fg=ACCENT_GREEN)
            self.update_idletasks()

            recognition_script = os.path.join(BASE_DIR, "lock_unlock_face_recognition.py")

            # Launches the camera verification script directly without blocking pop-ups
            subprocess.run([
               sys.executable,
               recognition_script
            ],
            check=True
            )
            
            self.status_label.config(text="Status: Security Shield session completed", fg=ACCENT_BLUE)
        except Exception as e:
            self.status_label.config(text="Status: Shield session ended / System locked", fg=TEXT_MUTED)


if __name__ == "__main__":
    app = TeethLockApp()
    app.mainloop()