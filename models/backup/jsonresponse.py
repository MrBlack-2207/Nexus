if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    video_ids = [item['id']['videoId'] for item in data['items']]
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'contentDetails',
        'id': ','.join(video_ids),
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    video_durations = response.json()

    # Save the JSON data to a file
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Open the CSV file for writing
    with open('data.csv', 'w', newline='', encoding='utf-8', errors='ignore') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header row
        csv_writer.writerow(['id', 'title', 'duration'])
        
        # Iterate over the search results and write to CSV
        for idx, item in enumerate(data['items'], start=1):
            # Extract the video title and thumbnail URL
            video_title = item['snippet']['title']
            
            # Find the corresponding video duration
            video_id = item['id']['videoId']
            for video in video_durations['items']:
                if video['id'] == video_id:
                    duration = video['contentDetails']['duration']
                    break
            # Write the data to the CSV file
            csv_writer.writerow([idx, video_title, duration])
else:
    print(f'Error: {response.status_code} - {response.text}')