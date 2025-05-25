# import tkinter as tk
# from tkinter import filedialog, ttk
# import os
# import pandas as pd
#
#
# from lib.vaiables import day_list, serviceAccountKeyPath, file_path, clean_firebase_data, upload_excel_to_firebase
#
#
# def startApplicationUI():
#     # Create main window and start the Tkinter event loop
#     root = tk.Tk()
#     app = ApplicationUI(root)
#     root.mainloop()
#
# class ApplicationUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("Discipline-plus Excel Manager")
#         master.geometry("800x600")  # Set window size
#
#         # Set application icon (handle exceptions if file missing)
#         root_path = os.path.dirname(os.path.abspath(__file__))
#         icon_path = os.path.join(root_path, "assets", "images", "firebase_icon.ico")
#         try:
#             master.iconbitmap(icon_path)
#         except Exception as e:
#             print(f"Failed to load icon: {e}")
#
#         # Create frame to hold top buttons
#         button_frame = tk.Frame(master)
#         button_frame.pack(fill=tk.X, padx=5, pady=5)
#
#         # Add buttons for cleaning, uploading, and downloading
#
#         tk.Button(button_frame, text="View Excel Table", command=self.view_excel_table).pack(side=tk.LEFT, expand=True, fill=tk.X)
#         tk.Button(button_frame, text="Clean Excel Table", command=self.clean_excel_table).pack(side=tk.LEFT, expand=True, fill=tk.X)
#         tk.Button(button_frame, text="Upload To Firebase", command=self.upload_to_firebase).pack(side=tk.LEFT, expand=True, fill=tk.X)
#         tk.Button(button_frame, text="Load From Firebase", command=self.load_from_firebase).pack(side=tk.LEFT, expand=True, fill=tk.X)
#
#         # Frame for table and scrollbars
#         table_frame = tk.Frame(master)
#         table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
#
#         # Horizontal scrollbar only (vertical scrollbar removed)
#         self.x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
#         # self.y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)  # Removed vertical scrollbar
#
#         # Treeview widget for showing the table data
#         self.table = ttk.Treeview(
#             table_frame,
#             columns=[],
#             show='headings',  # Hide default first column
#             xscrollcommand=self.x_scroll.set,
#             # yscrollcommand=self.y_scroll.set   # Removed vertical scrollbar command
#         )
#         self.table.grid(row=0, column=0, sticky="nsew")
#
#         # Configure scrollbar commands
#         self.x_scroll.config(command=self.table.xview)
#         # self.y_scroll.config(command=self.table.yview)  # Removed vertical scrollbar config
#
#         # Place horizontal scrollbar
#         self.x_scroll.grid(row=1, column=0, sticky='ew')
#         # self.y_scroll.grid(row=0, column=1, sticky='ns')  # Removed vertical scrollbar grid
#
#         # Make the table expand to fill the space
#         table_frame.rowconfigure(0, weight=1)
#         table_frame.columnconfigure(0, weight=1)
#
#         # Bottom console: multiline text widget for logs/messages
#         self.console = tk.Text(master, height=5)
#         self.console.pack(fill=tk.X, padx=5, pady=(0, 5))
#
#
#     def clean_firebase(self):
#         clean_firebase_data(day_list=day_list, serviceAccountKeyPath=serviceAccountKeyPath)
#
#
#     def clean_excel_table(self):
#         # Remove all rows from the table
#         for i in self.table.get_children():
#             self.table.delete(i)
#         # Clear all columns
#         self.table["columns"] = []
#         # Log action to console
#         self.console.insert(tk.END, "Console cleared.\n")
#
#     def view_excel_table(self):
#         # Open file dialog and get Excel file path
#         file_path = self.select_excel_file()
#         if not file_path:
#             return
#
#         try:
#             # Read Excel and clean data
#             df = self.read_and_clean_excel(file_path)
#
#             # Clear existing table content
#             self.clean_excel_table()
#
#             # Prepare column names and widths with spacers
#             columns, widths = self.prepare_columns(df)
#
#             # Setup table headers and column widths
#             self.setup_table(columns, widths)
#
#             # Insert cleaned data rows into the table
#             self.insert_rows(df)
#
#             # Log success
#             self.console.insert(tk.END, f"Loaded Excel: {os.path.basename(file_path)}\n")
#         except Exception as e:
#             # Log any errors during loading
#             self.console.insert(tk.END, f"Error loading Excel: {e}\n")
#
#
#     def upload_to_firebase(self):
#         upload_excel_to_firebase(day_list=day_list, serviceAccountKeyPath=serviceAccountKeyPath, file_path=file_path)
#
#
#
#
#
#     def select_excel_file(self):
#         # Open file dialog to select Excel file
#         return filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#
#     def read_and_clean_excel(self, file_path):
#         # Read Excel into DataFrame
#         df = pd.read_excel(file_path)
#
#         # Remove rows where the first column is NaN
#         df = df.dropna(subset=[df.columns[0]])
#
#         return df
#
#     def prepare_columns(self, df):
#         # Clean header names (remove "Unnamed" headers)
#         original = ["" if str(col).startswith("Unnamed") else str(col) for col in df.columns]
#
#         clean_cols = []
#         widths = []
#
#         for idx, col in enumerate(original):
#             clean_cols.append(col)
#
#             # Set wider width for every third column
#             widths.append(150 if idx % 3 == 0 else 50)
#
#             # Insert spacer column after every 3rd column (except the last group)
#             if (idx + 1) % 3 == 0 and (idx + 1) != len(original):
#                 clean_cols.append(f"spacer_{idx}")
#                 widths.append(10)
#
#         return clean_cols, widths
#
#     def setup_table(self, columns, widths):
#         # Apply column names to Treeview table
#         self.table["columns"] = columns
#
#         for col, width in zip(columns, widths):
#             # Use blank header for spacer columns
#             heading = "" if col.startswith("spacer_") else col
#
#             # Configure table column heading and size
#             self.table.heading(col, text=heading)
#             self.table.column(col, width=width, stretch=False, anchor="w")
#
#     def insert_rows(self, df):
#         # Insert rows into table, handling spacers and missing values
#         for _, row in df.iterrows():
#             row_values = []
#             for idx, val in enumerate(row):
#                 # Replace NaN with empty string
#                 row_values.append("" if pd.isna(val) else val)
#
#                 # Add empty spacer value after every 3rd column (except last group)
#                 if (idx + 1) % 3 == 0 and (idx + 1) != len(row):
#                     row_values.append("")
#
#             # Add row to Treeview
#             self.table.insert("", tk.END, values=row_values)
#
#     def load_from_firebase(self):
#         # Placeholder for Firebase download functionality
#         self.console.insert(tk.END, "Download clicked (Not implemented).\n")
#