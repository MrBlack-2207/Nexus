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