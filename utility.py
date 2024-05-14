import os
import re
import time

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
   start_time = time.time()
   num_dat_files = 0
   ignored_languages = ['english', 'spanish', 'arabic', 'hindi', 'bengali', 'portuguese', 'russian', 'japanese', 'punjabi', 'german']  
   all_info = []
   encountered_ids = set()  # Keep track of encountered IDs to detect duplicates
   duplicate_ids = set()    # Store duplicate IDs
   for root, dirs, files in os.walk(directory):
      for file in files:
            if file.endswith('.dat'):
               lang_match = re.search(r'_(\w+)\.dat$', file.lower())
               if lang_match:
                  lang = lang_match.group(1)
                  if lang not in ignored_languages:
                        num_dat_files += 1
                        file_path = os.path.join(root, file)
                        info = extract_info_from_file(file_path)
                        all_info.append(info)
                        # Check for duplicates
                        if 'ID' in info:
                           if info['ID'] in encountered_ids:
                              duplicate_ids.add(info['ID'])
                           else:
                              encountered_ids.add(info['ID'])
   end_time = time.time()
   time_taken = end_time - start_time
   return all_info, time_taken, num_dat_files, duplicate_ids
