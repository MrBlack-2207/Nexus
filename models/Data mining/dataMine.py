import requests

# Replace YOUR_API_KEY with your actual API key from Google Cloud Console
API_KEY = 'AIzaSyB-ur7-FSbHeXVCSJJt70j9rk9my289wq4'

# Replace SEARCH_QUERY with the topic or keywords you want to search for
SEARCH_QUERY = 'python tutorial'

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

    # Iterate over the search results
    for item in data['items']:
        # Extract the video title and thumbnail URL
        video_title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']

        # Print the video title and thumbnail URL
        print(f'Title: {video_title}')
        print(f'Thumbnail URL: {thumbnail_url}')
        print('---')
else:
    print(f'Error: {response.status_code} - {response.text}')