import tkinter as tk
from tkinter import ttk

class RangesTab(ttk.Frame):
    def __init__(self, master=None, entry_directory=None, **kw):
        super().__init__(master, **kw)

        self.instructions_label = ttk.Label(self, text="Below are the ID ranges found during scanning:")
        self.instructions_label.pack(pady=10)

        # Create a text widget to display the ID ranges
        self.ranges_text = tk.Text(self, wrap='word', height=10, width=50)

        # Create a vertical scrollbar and attach it to the text widget
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.ranges_text.yview)
        self.ranges_text.config(yscrollcommand=self.scrollbar.set)

        # Pack the scrollbar and the text widget side by side
        self.ranges_text.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def display_range_ids(self, range_ids):
        # Clear any existing text
        self.ranges_text.delete('1.0', tk.END)

        # Display the ID ranges
        if range_ids:
            self.ranges_text.insert(tk.END, range_ids)
        else:
            self.ranges_text.insert(tk.END, "No available ID ranges found.\n")
