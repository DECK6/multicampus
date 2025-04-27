#!/usr/bin/env python3
import os
import json
import re

def natural_sort_key(s):
    """
    Sort strings with numbers in a natural way (e.g., chapter1, chapter2, chapter10)
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def generate_slide_list():
    """
    Generate a JSON file containing all Python automation slides in natural order
    """
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__)) or '.'
    
    # Find all HTML files that start with python_automation_
    slide_files = []
    for file in os.listdir(current_dir):
        if file.startswith('python_automation_') and file.endswith('.html'):
            slide_files.append(file)
    
    # Sort files in natural order
    slide_files.sort(key=natural_sort_key)
    
    # Write the sorted list to a JSON file
    with open('slide_files.json', 'w', encoding='utf-8') as f:
        json.dump(slide_files, f, indent=2, ensure_ascii=False)
    
    print(f"Generated slide_files.json with {len(slide_files)} slides")
    return slide_files

if __name__ == "__main__":
    files = generate_slide_list()
    print(f"Found {len(files)} slide files")
    print("First 5 slides:", files[:5])
    print("Last 5 slides:", files[-5:]) 