import tkinter as tk
from tkinter import ttk

class LogTab(ttk.Frame):
   def __init__(self, master=None, **kw):
      super().__init__(master, **kw)
      # Create a text widget for logs
      self.log_text = tk.Text(self, wrap="word", height=10, width=50)
      self.log_text.pack(fill="both", expand=True)
      
   def add_log(self, log_message):
      self.log_text.insert(tk.END, log_message + "\n")
      self.log_text.see(tk.END)  # Scroll to the end of the log