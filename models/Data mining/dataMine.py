import requests
from dotenv import load_dotenv
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


with open('youtube_videos.csv', 'w', newline='',encoding='utf-8') as csvfile:
    fieldnames = ['short', 'medium', 'long']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for i in range(max_length):
        writer.writerow({
            'short': f"{video_data['short'][i]['title']} (ID: {video_data['short'][i]['videoId']})",
            'medium': f"{video_data['medium'][i]['title']} (ID: {video_data['medium'][i]['videoId']})",
            'long': f"{video_data['long'][i]['title']} (ID: {video_data['long'][i]['videoId']})"
        })

print("CSV file 'youtube_videos.csv' created successfully.")