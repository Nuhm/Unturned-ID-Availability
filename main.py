import sv_ttk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scan_tab import ScanTab
from log_tab import LogTab
from duplicates_tab import DuplicatesTab
from utility import scan_directory_for_info


# Create the main window
root = tk.Tk()
root.title("ID Scanner")
root.resizable(False, False)

# Create a style object
sv_ttk.set_theme("dark")

# Create a notebook (tabs/pages)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=3, sticky="nsew")

# Create and add the 'Log' tab
log_tab = LogTab(notebook)
log_tab.pack(expand=True, fill="both")

# Create and add the 'Scan' tab, passing the log_tab instance
scan_tab = ScanTab(notebook)
scan_tab.pack(expand=True, fill="both")

# Create and add the 'Duplicates' tab
duplicates_tab = DuplicatesTab(notebook)
duplicates_tab.pack(expand=True, fill="both")

# Pass reference of duplicates_tab to scan_tab
scan_tab.set_duplicates_tab(duplicates_tab)

# Add tabs to the notebook
notebook.add(scan_tab, text='Scan')
notebook.add(log_tab, text='Log')
notebook.add(duplicates_tab, text="Duplicates")

# Pack notebook
notebook.pack(expand=1, fill="both")

# Run the main event loop
root.mainloop()
