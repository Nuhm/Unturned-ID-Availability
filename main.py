import os
import re

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
    all_info = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.dat'):
                file_path = os.path.join(root, file)
                info = extract_info_from_file(file_path)
                all_info.append(info)
    return all_info

def get_available_id_ranges(min_range, max_range):
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

# Example usage:
directory_to_scan = r'F:\SteamLibrary\steamapps\workshop\content\304930'
min_range = 2000
max_range = 65535
available_id_ranges = get_available_id_ranges(min_range, max_range)
formatted_ranges = ', '.join(f"{start}-{end}" if start != end else f"{start}" for start, end in available_id_ranges)
print("Available ID ranges:", formatted_ranges)
