import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import re
import time
from utility import scan_directory_for_info

class DuplicatesTab(ttk.Frame):
   def __init__(self, master=None, entry_directory=None, **kw):
      super().__init__(master, **kw)

      self.instructions_label = ttk.Label(self, text="Below are the duplicate IDs found during scanning:")
      self.instructions_label.pack(pady=10)

      # Create a text widget to display the duplicate IDs
      self.duplicates_text = tk.Text(self, wrap='word', height=10, width=50)

      # Create a vertical scrollbar and attach it to the text widget
      self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.duplicates_text.yview)
      self.duplicates_text.config(yscrollcommand=self.scrollbar.set)

      # Pack the scrollbar and the text widget side by side
      self.scrollbar.pack(side="right", fill="y")
      self.duplicates_text.pack(side="left", fill="both", expand=True)

   def display_duplicate_ids(self, duplicate_ids):
        # Clear any existing text
        self.duplicates_text.delete('1.0', tk.END)

        # Display the duplicate IDs
        if duplicate_ids:
            for id in duplicate_ids:
                self.duplicates_text.insert(tk.END, f"{id}\n")
        else:
            self.duplicates_text.insert(tk.END, "No duplicate IDs found.\n")
