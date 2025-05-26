import tkinter as tk
import os
from lib.DisciplinePlusManager import DisciplinePlusManager
from lib import logger  # NEW import
from lib.managers.json.shared_preferences import SharedPreferences


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

        tk.Button(button_frame, text="Delete Firebase Data", command=self.delete_firebase_data).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Upload Excel Table", command=self.upload).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Load From Firebase", command=self.download).pack(side=tk.LEFT, expand=True, fill=tk.X)


        # === Excel File Picker with Label ===
        file_picker_label = tk.Label(master, text="Select Excel file:")
        file_picker_label.pack(anchor="w", padx=10, pady=(5, 0))

        file_picker_frame = tk.Frame(master)
        file_picker_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.file_entry = tk.Entry(file_picker_frame, state='disabled', width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        default_file = SharedPreferences.get("excel_file_path")

        self.file_entry.config(state='normal')
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, default_file)
        self.file_entry.config(state='disabled')

        browse_btn = tk.Button(file_picker_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        # ==========================================================================

        # Number of row  ===============================================================
        num_row_frame = tk.Frame(master)
        num_row_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        def only_numbers(char):
            return char.isdigit()

        vcmd = master.register(only_numbers)

        self.num_row_entry = tk.Entry(num_row_frame, validate="key", validatecommand=(vcmd, '%S'), width=5)
        self.num_row_entry.pack(side=tk.RIGHT, padx=(5, 0))  # Entry first (rightmost)

        def save_num_rows():
            value = self.num_row_entry.get()
            if value.isdigit():
                SharedPreferences.set('number_of_rows', value)
                logger.log(f"Saved number_of_rows = {value}")
            else:
                logger.log("Invalid number. Please enter digits only.")

        save_btn = tk.Button(num_row_frame, text="update", command=save_num_rows)
        save_btn.pack(side=tk.RIGHT, padx=(5, 5))

        num_row_label = tk.Label(num_row_frame, text="Number of rows:")
        num_row_label.pack(side=tk.RIGHT)

        # Load initial value
        self.num_row_entry.insert(0, SharedPreferences.get('number_of_rows'))

        # Console frame with vertical scrollbar =========================================================================
        console_frame = tk.Frame(master)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(console_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(console_frame, state='disabled', bg="#f0f0f0", yscrollcommand=scrollbar.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.text.yview)

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


    def browse_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select an Excel file",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.file_entry.config(state='disabled')

            # Store the file path for future refrence
            SharedPreferences.set("excel_file_path", file_path)

            logger.log(f"File selected: {file_path}")


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
