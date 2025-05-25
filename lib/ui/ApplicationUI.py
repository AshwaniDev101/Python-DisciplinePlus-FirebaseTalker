import tkinter as tk
import os
from lib.DisciplinePlusManager import DisciplinePlusManager
from lib import logger  # NEW import


def startApplicationUI():
    root = tk.Tk()
    app = ApplicationUI(root)
    logger.set_ui_logger(app)  # NEW: Set the global logger to this instance
    root.mainloop()


class ApplicationUI:
    def __init__(self, master):
        self.master = master

        # DisciplinePlus Manager
        self.discipline_plus_manager = DisciplinePlusManager()

        master.title("Discipline-plus Excel Manager")
        master.geometry("600x600")

        root_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(root_path, "assets", "images", "firebase_icon.ico")

        try:
            master.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")

        # Buttons frame (TOP)
        button_frame = tk.Frame(master)
        button_frame.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

        tk.Button(button_frame, text="Delete Firebase", command=self.delete_firebase_data).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Upload Excel Table", command=self.upload).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Load From Firebase", command=self.download).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Console (uneditable Text widget)
        self.text = tk.Text(master, state='disabled', bg="#f0f0f0")
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Floating Clear Console Button
        clear_btn = tk.Button(master, text="Clean", command=self._clear_console, bg="#f0f0f0")
        clear_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # bottom right corner

    def _clear_console(self):
        self.text.config(state='normal')
        self.text.delete("1.0", tk.END)
        self.text.config(state='disabled')

    def _append_to_console(self, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state='disabled')

    # ========================  Buttons  ======================================
    def delete_firebase_data(self):
        logger.log("Clean Firebase clicked")
        self.discipline_plus_manager.clean_firebase_data()

    def upload(self):
        logger.log("Upload clicked")
        self.discipline_plus_manager.upload_excel_to_firebase()

    def download(self):
        logger.log("Download clicked")
        # self.discipline_plus_manager.download_data_from_firebase()
