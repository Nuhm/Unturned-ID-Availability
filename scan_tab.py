import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import re
import time
from utility import scan_directory_for_info
from duplicates_tab import DuplicatesTab
from ranges_tab import RangesTab

class ScanTab(ttk.Frame):
   def __init__(self, master=None, **kw):
      super().__init__(master, **kw)

      # Initialize external tabs
      self.ranges_tab = None
      self.duplicates_tab = None

      # Widgets for the 'Scan' tab
      self.label_directory = ttk.Label(self, text="Directory to scan:")
      self.label_directory.grid(row=0, column=0, padx=5, pady=5, sticky="w")

      self.entry_directory = ttk.Entry(self, width=50)
      self.entry_directory.grid(row=0, column=1, padx=5, pady=5)

      self.button_browse = ttk.Button(self, text="Browse", command=self.browse_directory)
      self.button_browse.grid(row=0, column=2, padx=5, pady=5)

      self.label_min_range = ttk.Label(self, text="Minimum range:")
      self.label_min_range.grid(row=1, column=0, padx=5, pady=5, sticky="w")

      self.entry_min_range = ttk.Entry(self, width=10)
      self.entry_min_range.grid(row=1, column=1, padx=5, pady=5)
      self.entry_min_range.insert(0, "2000")

      self.label_max_range = ttk.Label(self, text="Maximum range:")
      self.label_max_range.grid(row=2, column=0, padx=5, pady=5, sticky="w")

      self.entry_max_range = ttk.Entry(self, width=10)
      self.entry_max_range.grid(row=2, column=1, padx=5, pady=5)
      self.entry_max_range.insert(0, "65535")

      self.button_scan = ttk.Button(self, text="Scan Directory", command=self.scan_directory)
      self.button_scan.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

   def set_duplicates_tab(self, duplicates_tab):
      self.duplicates_tab = duplicates_tab

   def set_ranges_tab(self, ranges_tab):
      self.ranges_tab = ranges_tab

   def browse_directory(self):
      directory_to_scan = filedialog.askdirectory()
      if directory_to_scan:
            self.entry_directory.delete(0, tk.END)
            self.entry_directory.insert(0, directory_to_scan)

   def get_available_id_ranges(self, min_range, max_range, directory_to_scan):
      available_ids = set(range(min_range, max_range + 1))
      # After scanning in the scan_tab.py:
      all_info, time_taken, num_dat_files, duplicate_ids = scan_directory_for_info(directory_to_scan)
      if self.duplicates_tab:  # Check if duplicates_tab is set
          self.duplicates_tab.display_duplicate_ids(duplicate_ids)
      used_ids = set()
      for info in all_info:
            if 'ID' in info:
               used_ids.add(info['ID'])
      available_ranges = []
      start = None
      for i in range(min_range, max_range + 1):
            if i not in used_ids:
               if start is None:
                  start = i
            elif start is not None:
               available_ranges.append((start, i - 1))
               start = None
      if start is not None:
            available_ranges.append((start, max_range))
      return available_ranges

   def scan_directory(self):
      directory_to_scan = self.entry_directory.get()
      min_range = int(self.entry_min_range.get())
      max_range = int(self.entry_max_range.get())

      if not os.path.isdir(directory_to_scan):
            messagebox.showerror("Error", "Invalid directory!")
            return

      # Code to perform scanning
      start_scan = time.time()
      available_id_ranges = self.get_available_id_ranges(min_range, max_range, directory_to_scan)
      end_scan = time.time()

      formatted_ranges = ', '.join(f"{start}-{end}" if start != end else f"{start}" for start, end in available_id_ranges)
      if self.ranges_tab:
         self.ranges_tab.display_range_ids(formatted_ranges)

      # Calculate time taken
      time_taken = end_scan - start_scan
      # Log time taken and number of .dat files read
      #self.logs_tab.add_log("Scan started at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
      #self.logs_tab.add_log(f"Time taken to scan: {time_taken:.2f} seconds\nNumber of .dat files read: {num_dat_files}")