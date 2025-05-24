import tkinter as tk
from tkinter import filedialog, ttk
import os
import pandas as pd

def startApplicationUI():
    # Create main window and start the Tkinter event loop
    root = tk.Tk()
    app = ApplicationUI(root)
    root.mainloop()

class ApplicationUI:
    def __init__(self, master):
        self.master = master
        master.title("Discipline-plus Excel Manager")
        master.geometry("800x600")  # Set window size

        # Set application icon (handle exceptions if file missing)
        root_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(root_path, "assets", "images", "firebase_icon.ico")
        try:
            master.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")

        # Create frame to hold top buttons
        button_frame = tk.Frame(master)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Add buttons for cleaning, uploading, and downloading
        tk.Button(button_frame, text="Clean Firebase", command=self.clean_text).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Upload Excel Table", command=self.upload).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(button_frame, text="Load From Firebase", command=self.download).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Frame for table and scrollbars
        table_frame = tk.Frame(master)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # Horizontal scrollbar only (vertical scrollbar removed)
        self.x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        # self.y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)  # Removed vertical scrollbar

        # Treeview widget for showing the table data
        self.table = ttk.Treeview(
            table_frame,
            columns=[],
            show='headings',  # Hide default first column
            xscrollcommand=self.x_scroll.set,
            # yscrollcommand=self.y_scroll.set   # Removed vertical scrollbar command
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        # Configure scrollbar commands
        self.x_scroll.config(command=self.table.xview)
        # self.y_scroll.config(command=self.table.yview)  # Removed vertical scrollbar config

        # Place horizontal scrollbar
        self.x_scroll.grid(row=1, column=0, sticky='ew')
        # self.y_scroll.grid(row=0, column=1, sticky='ns')  # Removed vertical scrollbar grid

        # Make the table expand to fill the space
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Bottom console: multiline text widget for logs/messages
        self.console = tk.Text(master, height=5)
        self.console.pack(fill=tk.X, padx=5, pady=(0, 5))

    def clean_text(self):
        # Remove all rows from the table
        for i in self.table.get_children():
            self.table.delete(i)
        # Clear all columns
        self.table["columns"] = []
        # Log action to console
        self.console.insert(tk.END, "Console cleared.\n")

    def upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            # Drop rows where first column is NaN (you can change the column index or name)
            df = df.dropna(subset=[df.columns[0]])

            self.clean_text()

            # Replace 'Unnamed...' headers with empty string
            original_columns = ["" if str(col).startswith("Unnamed") else str(col) for col in df.columns]

            clean_columns = []
            column_widths = []

            for idx, col in enumerate(original_columns):
                clean_columns.append(col)
                column_widths.append(150 if idx % 3 == 0 else 50)

                if (idx + 1) % 3 == 0 and (idx + 1) != len(original_columns):
                    spacer_name = f"spacer_{idx}"
                    clean_columns.append(spacer_name)
                    column_widths.append(10)

            self.table["columns"] = clean_columns

            for col, width in zip(clean_columns, column_widths):
                if col.startswith("spacer_"):
                    self.table.heading(col, text="")
                    self.table.column(col, width=width, stretch=False)
                else:
                    self.table.heading(col, text=col)
                    self.table.column(col, width=width, stretch=False, anchor="w")

            # Insert rows after dropna; convert NaN to empty string when inserting
            for _, row in df.iterrows():
                row_values = []
                for idx, val in enumerate(row):
                    row_values.append("" if pd.isna(val) else val)
                    if (idx + 1) % 3 == 0 and (idx + 1) != len(row):
                        row_values.append("")
                self.table.insert("", tk.END, values=row_values)

            self.console.insert(tk.END, f"Loaded Excel: {os.path.basename(file_path)}\n")

        except Exception as e:
            self.console.insert(tk.END, f"Error loading Excel: {e}\n")

    def download(self):
        # Placeholder for Firebase download functionality
        self.console.insert(tk.END, "Download clicked (Not implemented).\n")





# import tkinter as tk
# import os
#
#
# def startApplicationUI():
#     root = tk.Tk()
#     app = ApplicationUI(root)
#     root.mainloop()
#
# class ApplicationUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("Discipline-plus Excel Manager")
#         master.geometry("600x600")
#
#         root_path = os.path.dirname(os.path.abspath(__file__))
#         icon_path = os.path.join(root_path, "assets", "images", "firebase_icon.ico")
#
#         try:
#             master.iconbitmap(icon_path)
#         except Exception as e:
#             print(f"Failed to load icon: {e}")
#
#
#         # Buttons frame (TOP)
#         button_frame = tk.Frame(master)
#         button_frame.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
#
#         tk.Button(button_frame, text="Clean Firebase", command=self.clean_text).pack(side=tk.LEFT, expand=True, fill=tk.X)
#         tk.Button(button_frame, text="Upload Excel Table", command=self.upload).pack(side=tk.LEFT, expand=True, fill=tk.X)
#         tk.Button(button_frame, text="Load From Firebase", command=self.download).pack(side=tk.LEFT, expand=True, fill=tk.X)
#
#         # Multiline text widget
#         self.text = tk.Text(master)
#         self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
#
#     def clean_text(self):
#         self.text.delete("1.0", tk.END)
#
#     def upload(self):
#         print("Upload clicked")
#
#     def download(self):
#         print("Download clicked")
#
#
