import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import time

start_time = 0
num_dat_files = 0


def extract_info_from_file(file_path):
    info = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            id_match = re.match(r'^ID\s+(\d+)$', line)
            type_match = re.match(r'^Type\s+(.+)$', line)
            guid_match = re.match(r'^GUID\s+(.+)$', line)
            if id_match:
                info['ID'] = int(id_match.group(1))
            elif type_match:
                info['Type'] = type_match.group(1)
            elif guid_match:
                info['GUID'] = guid_match.group(1)
    return info

def scan_directory_for_info(directory):
    global start_time, num_dat_files
    start_time = time.time()
    num_dat_files = 0
    ignored_languages = ['english', 'spanish', 'arabic', 'hindi', 'bengali', 'portuguese', 'russian', 'japanese', 'punjabi', 'german']  # List of top 10 most common languages to be ignored
    all_info = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.dat'):
                lang_match = re.search(r'_(\w+)\.dat$', file.lower())  # Match common language patterns
                if lang_match:
                    lang = lang_match.group(1)
                    if lang not in ignored_languages:
                        num_dat_files += 1
                        file_path = os.path.join(root, file)
                        info = extract_info_from_file(file_path)
                        all_info.append(info)
    return all_info


def get_available_id_ranges(min_range, max_range, directory_to_scan):
    available_ids = set(range(min_range, max_range + 1))
    all_info = scan_directory_for_info(directory_to_scan)
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

def browse_directory():
    directory_to_scan = filedialog.askdirectory()
    if directory_to_scan:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory_to_scan)

def scan_directory():
    directory_to_scan = entry_directory.get()
    min_range = int(entry_min_range.get())
    max_range = int(entry_max_range.get())
    
    if not os.path.isdir(directory_to_scan):
        messagebox.showerror("Error", "Invalid directory!")
        return
    
    start_scan = time.time()
    available_id_ranges = get_available_id_ranges(min_range, max_range, directory_to_scan)
    end_scan = time.time()
    
    formatted_ranges = ', '.join(f"{start}-{end}" if start != end else f"{start}" for start, end in available_id_ranges)
    result_label.config(text="Available ID ranges: " + formatted_ranges)
    
    # Calculate time taken
    time_taken = end_scan - start_scan
    # Log time taken and number of .dat files read
    log_text = f"Time taken to scan: {time_taken:.2f} seconds\nNumber of .dat files read: {num_dat_files}"
    log_label.config(text=log_text)


# Create the main window
root = tk.Tk()
root.title("ID Scanner")

root.resizable(False, False)
root.configure(padx=25, pady=25)

# Create a style object
sv_ttk.set_theme("dark")

# Create and place widgets
label_directory = ttk.Label(root, text="Directory to scan:")
label_directory.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_directory = ttk.Entry(root, width=50)
entry_directory.grid(row=0, column=1, padx=5, pady=5)
button_browse = ttk.Button(root, text="Browse", command=browse_directory)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_min_range = ttk.Label(root, text="Minimum range:")
label_min_range.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_min_range = ttk.Entry(root, width=10)
entry_min_range.grid(row=1, column=1, padx=5, pady=5)
entry_min_range.insert(0, "2000")

label_max_range = ttk.Label(root, text="Maximum range:")
label_max_range.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_max_range = ttk.Entry(root, width=10)
entry_max_range.grid(row=2, column=1, padx=5, pady=5)
entry_max_range.insert(0, "65535")

button_scan = ttk.Button(root, text="Scan Directory", command=scan_directory)
button_scan.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

result_label = ttk.Label(root, text="", wraplength=400)
result_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

log_label = ttk.Label(root, text="", wraplength=400)
log_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


# Run the main event loop
root.mainloop()
