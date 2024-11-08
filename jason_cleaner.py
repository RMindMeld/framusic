import json
import re

# Load the JSON data
with open('c:/Users/Fernando/Documents/GitHub/framusic/music_data.json', 'r') as file:
  data = json.load(file)

# Function to process the title
def process_title(title):
  # Replace underscores with spaces
  title = title.replace('_', ' ')
  # Remove ".mp3" and stray commas
  title = re.sub(r',\s*', ' ', title).replace('.mp3', '')
  return title

# Iterate over the data and update titles
for category, songs in data.items():
  for song in songs:
    song['title'] = process_title(song['title'])

# Save the updated JSON data
with open('c:/Users/Fernando/Documents/GitHub/framusic/music_data_updated.json', 'w') as file:
  json.dump(data, file, indent=2)