import os
import re
import json

def natural_sort_key(s):
    # Extracts chapter and slide numbers for natural sorting
    # Handles formats like chapter1_1.html, chapter14_15_2.html
    match = re.match(r"slides/python_automation_chapter(\d+(?:_\d+)*)_(\d+)\.html", s)
    if match:
        chapter_part = match.group(1)
        slide_num = int(match.group(2))
        
        chapter_nums = [int(n) for n in chapter_part.split('_')]
        
        # Return a tuple for consistent sorting comparison
        # Pad with zeros to ensure correct lexicographical comparison if needed, 
        # although Python's tuple comparison handles different lengths correctly.
        # Example: (1, 10) vs (1, 2) -> sorts correctly as numbers
        # Example: (14, 15, 2) vs (16, 0) -> sorts correctly
        return tuple(chapter_nums + [slide_num])
    else:
        # Fallback for unexpected formats: return a tuple that sorts them last
        # Using infinity equivalent for numbers and the string itself
        print(f"Warning: Unexpected file format, sorting last: {s}")
        return (float('inf'), s)

slide_dir = 'slides'
navigator_file = 'slide_navigator.html'
json_file = 'slide_files.json'

# 1. Get and sort file list from slides directory
slide_files = []
try:
    files = os.listdir(slide_dir)
    for f in files:
        if f.startswith('python_automation_chapter') and f.endswith('.html'):
            # Always use forward slashes for consistency
            slide_files.append(os.path.join(slide_dir, f).replace("\\", "/"))
except FileNotFoundError:
    print(f"Error: Directory '{slide_dir}' not found.")
    exit(1)

# Sort using the refined key
slide_files.sort(key=natural_sort_key)

print(f"Found and sorted {len(slide_files)} slide files.")

# 2. Update slide_navigator.html
# Create the JS array string, ensuring proper quoting
js_array_string = ", ".join([f"'{f}'" for f in slide_files])

try:
    with open(navigator_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File '{navigator_file}' not found.")
    exit(1)

# Regex to find the return statement's array brackets more reliably
# Looks for `return [` possibly followed by whitespace/newlines, then captures content until `];`
pattern = re.compile(
    r"(function\s+findPythonAutomationFiles\(\)\s*\{\s*.*?return\s*\[)"
    r"(.*?)(\s*\];\s*\})",
    re.DOTALL | re.MULTILINE
)

# Construct the replacement string with proper indentation
replacement = f"\1\n                {js_array_string}\n            \3"

new_content, num_subs = pattern.subn(replacement, content)

if num_subs == 0:
    print(f"Warning: Could not find the return array pattern in {navigator_file}. Manual check needed.")
else:
    try:
        with open(navigator_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {navigator_file}")
    except IOError as e:
        print(f"Error writing to {navigator_file}: {e}")
        exit(1)

# 3. Update slide_files.json
try:
    with open(json_file, 'w', encoding='utf-8') as f:
        # Dump the sorted list into the JSON file
        json.dump(slide_files, f, indent=2) # Use indent=2 for readability
    print(f"Successfully updated {json_file}")
except IOError as e:
    print(f"Error writing to {json_file}: {e}")
    exit(1)

print("Update process completed.") 