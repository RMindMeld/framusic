import os
from collections import defaultdict
import re

def clean_filename(filename):
    # Remove content within parentheses and the parentheses themselves
    cleaned = re.sub(r'\([^)]*\)', '', filename)
    # Remove hashtags
    cleaned = cleaned.replace('#', '')
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    # Remove any potential double underscores
    cleaned = re.sub('_+', '_', cleaned)
    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')
    return cleaned

def rename_mp3_files(root_directory):
    # Dictionary to keep track of filename occurrences
    filename_count = defaultdict(int)
    
    # First pass: Count all filenames to prepare for numbering
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                base_name = os.path.splitext(file)[0]
                cleaned_name = clean_filename(base_name)
                filename_count[cleaned_name] += 1
    
    # Dictionary to keep track of current number for each filename
    current_number = defaultdict(int)
    
    # Second pass: Rename files
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                # Split filename and extension
                base_name, extension = os.path.splitext(file)
                
                # Clean the filename
                cleaned_name = clean_filename(base_name)
                
                # Construct new filename
                if filename_count[cleaned_name] > 1:
                    # Increment counter for this filename
                    current_number[cleaned_name] += 1
                    new_filename = f"{cleaned_name}_{current_number[cleaned_name]}{extension}"
                else:
                    new_filename = f"{cleaned_name}{extension}"
                
                # Get full paths
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)
                
                try:
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f"Renamed: {file} -> {new_filename}")
                except Exception as e:
                    print(f"Error renaming {file}: {str(e)}")

if __name__ == "__main__":
    # Get the directory path from user input
    directory = input("Enter the root directory path to search for MP3 files: ")
    
    # Verify the directory exists
    if os.path.exists(directory):
        print(f"Starting to rename MP3 files in {directory} and its subdirectories...")
        rename_mp3_files(directory)
        print("Finished renaming files.")
    else:
        print("Error: Directory does not exist!")
        