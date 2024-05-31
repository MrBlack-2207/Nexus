import requests
from dotenv import load_dotenv
import json
import csv
import os

load_dotenv()

# Replace YOUR_API_KEY with your actual API key from Google Cloud Console
API_KEY = os.getenv("obscured_value")

# Replace SEARCH_QUERY with the topic or keywords you want to search for
SEARCH_QUERY = 'mern stack'

# Set the API endpoint and parameters
url = f'https://www.googleapis.com/youtube/v3/search'
def search_videos(duration):
    params = {
        'part': 'snippet,id',
        'maxResults': 5,
        'q': SEARCH_QUERY,
        'key': API_KEY,
        'type': 'video',
        'order': 'relevance',
        'videoDuration': duration
    }
    response = requests.get(url, params=params)
    return response.json()

# Prepare data for CSV
short_videos = search_videos('short')['items']
medium_videos = search_videos('medium')['items']
long_videos = search_videos('long')['items']

video_data = {
    'short': [{'title': video['snippet']['title'], 'videoId': video['id']['videoId']} for video in short_videos],
    'medium': [{'title': video['snippet']['title'], 'videoId': video['id']['videoId']} for video in medium_videos],
    'long': [{'title': video['snippet']['title'], 'videoId': video['id']['videoId']} for video in long_videos]
}

# Find the maximum number of videos in any category for CSV row alignment
max_length = max(len(video_data['short']), len(video_data['medium']), len(video_data['long']))

# Fill shorter lists with empty values to match the maximum length
for category in video_data:
    while len(video_data[category]) < max_length:
        video_data[category].append({'title': '', 'videoId': ''})


# Generate HTML table
html_table = "<table border='1'>\n"
html_table += "<tr><th>Short Videos</th><th>Medium Videos</th><th>Long Videos</th></tr>\n"

for i in range(max_length):
    html_table += "<tr>"
    for category in ['short', 'medium', 'long']:
        video = video_data[category][i]
        if video['videoId']:
            video_link = f"https://www.youtube.com/watch?v={video['videoId']}"
            html_table += f"<td><a href='{video_link}' target='_blank'>{video['title']}</a></td>"
    html_table += "</tr>\n"

html_table += "</table>"

# Write HTML table to a file
with open('youtube_videos.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_table)

print("HTML file 'youtube_videos.html' created successfully.")