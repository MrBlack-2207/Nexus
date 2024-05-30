import tensorflow as tf
from keras.applications import ResNet50
from keras.preprocessing import image
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained ResNet50 model
resnet_model = ResNet50(weights='imagenet', include_top=False, input_shape=(90, 120, 3))

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Function to preprocess and analyze a thumbnail
def analyze_thumbnail(thumbnail_url, search_query):
    try:
        # Load and preprocess the thumbnail image
        img = image.load_img(thumbnail_url, target_size=(90, 120))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.

        # Use the ResNet model to extract features from the thumbnail
        features = resnet_model.predict(img_array)

        # Custom scoring logic
        quality_threshold = 0.7  # Adjust this value as needed
        quality_score = np.mean(features)  # Compute mean of visual features

        # Relevancy checking based on search query
        relevancy_score = check_relevancy(thumbnail_url, search_query)

        if quality_score >= quality_threshold and relevancy_score >= 0.5:
            score_or_label = 'High Quality and Relevant'
        elif quality_score >= quality_threshold:
            score_or_label = 'High Quality but Irrelevant'
        else:
            score_or_label = 'Low Quality'

        return score_or_label
    except Exception as e:
        print(f"Error processing thumbnail {thumbnail_url}: {e}")
        return None

# Function for relevancy checking
def check_relevancy(thumbnail_url, search_query):
    # Load video metadata from data.json
    video_metadata = get_video_metadata(thumbnail_url)
    if not video_metadata:
        return 0.0  # Assign a low relevancy score if metadata is not available

    # Vectorize the search query and video metadata
    query_vector = vectorizer.fit_transform([search_query])
    metadata_vector = vectorizer.transform([video_metadata])

    # Compute cosine similarity between query and metadata vectors
    similarity_score = cosine_similarity(query_vector, metadata_vector)[0][0]

    return similarity_score

# Function to fetch video metadata from data.json
def get_video_metadata(thumbnail_url):
    with open('data.json', 'r') as f:
        data = json.load(f)
        video_data = next((video for video in data if video['thumbnail_url'] == thumbnail_url), None)
        if video_data:
            metadata = ' '.join([video_data.get('title', ''), video_data.get('description', '')])
            return metadata
    return None

# Read thumbnail URLs and search query from data.json
with open('data.json', 'r') as f:
    data = json.load(f)
    thumbnail_urls = [video['thumbnail_url'] for video in data]
    search_query = data.get('search_query', '')

# Curated video list
curated_videos = []

# Analyze each thumbnail and filter videos
for thumbnail_url in thumbnail_urls:
    score_or_label = analyze_thumbnail(thumbnail_url, search_query)
    if score_or_label == 'High Quality and Relevant':
        # Keep this video in the curated list
        curated_videos.append(thumbnail_url)

print("Curated videos:", curated_videos)