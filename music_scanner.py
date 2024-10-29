import os
import json
from pathlib import Path
import mutagen

def scan_music_directory(base_path):
    """
    Scans the music directory and creates a JSON file with playlist and song information.
    
    Args:
        base_path (str): Path to the directory containing music playlists
    """
    music_data = {}
    
    # Walk through all directories in the base path
    for root, dirs, files in os.walk(base_path):
        # Get playlist name (directory name)
        playlist_name = os.path.basename(root)
        
        # Skip the base directory itself
        if root == base_path:
            continue
            
        # Initialize playlist array
        music_data[playlist_name] = []
        
        # Process all music files in the directory
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a', '.wav')):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_path)
                
                # Try to get metadata
                try:
                    audio = mutagen.File(file_path)
                    if audio is not None:
                        title = file
                        if hasattr(audio, 'tags') and audio.tags:
                            title = audio.tags.get('title', [file])[0]
                    else:
                        title = file
                except:
                    title = file
                
                # Add song information
                song_info = {
                    "title": title,
                    "path": relative_path.replace("\\", "/")  # Ensure proper path format for web
                }
                
                music_data[playlist_name].append(song_info)
    
    # Write the data to a JSON file
    output_path = os.path.join(base_path, 'music_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(music_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created music_data.json with {len(music_data)} playlists")
    
    # Create HTML file if it doesn't exist
    html_template_path = os.path.join(base_path, 'index.html')
    if not os.path.exists(html_template_path):
        source_html = None  # Replace with the content of the HTML template
        with open(html_template_path, 'w', encoding='utf-8') as f:
            f.write(source_html)
        print("Created index.html template")

if __name__ == "__main__":
    # Get the music directory path from user input
    music_dir = input("Enter the path to your music directory: ")
    
    # Validate the path
    if os.path.exists(music_dir):
        scan_music_directory(music_dir)
    else:
        print("Invalid directory path. Please check and try again.")
        