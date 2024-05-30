import requests
from dotenv import load_dotenv
import json
import csv
import os

load_dotenv()

# Replace YOUR_API_KEY with your actual API key from Google Cloud Console
API_KEY = os.getenv("obscured_value")

# Replace SEARCH_QUERY with the topic or keywords you want to search for
SEARCH_QUERY = 'node js'

# Set the API endpoint and parameters
url = f'https://www.googleapis.com/youtube/v3/search'
params = {
    'part': 'snippet',
    'maxResults': 25,  # Maximum number of results to return
    'q': SEARCH_QUERY,
    'key': API_KEY,
    'type': 'video'  # Specify that we want to search for videos
}

# Send the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Save the JSON data to a file
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Open the CSV file for writing
    with open('data.csv', 'w', newline='', encoding='utf-8', errors='ignore') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header row
        csv_writer.writerow(['id', 'title', 'thumbnails'])
        
        # Iterate over the search results and write to CSV
        for idx, item in enumerate(data['items'], start=1):
            # Extract the video title and thumbnail URL
            video_title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            
            # Write the data to the CSV file
            csv_writer.writerow([idx, video_title, thumbnail_url])
else:
    print(f'Error: {response.status_code} - {response.text}')