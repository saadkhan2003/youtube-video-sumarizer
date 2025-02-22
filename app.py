from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import CORS
import os
from dotenv import load_dotenv
import main  # Import the main.py file as a module
import requests

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/summarize": {
        "origins": ["https://saadyoutubesummarizer.netlify.app", "http://localhost:5000"],
        "methods": ["GET", "OPTIONS"]
    }
})
CORS(app)  # Enable CORS for all routes

def get_video_details(video_id):
    try:
        # Using oEmbed API which doesn't require an API key
        url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'title': data['title'],
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'author': data['author_name']
        }
    except:
        return None

@app.route('/summarize', methods=['GET'])
def summarize_video():
    print("Summarize video function called - NEW")
    video_id = request.args.get('videoID')
    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    video_details = get_video_details(video_id)
    if not video_details:
        return jsonify({'error': 'Could not fetch video details'}), 500

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    transcript = main.get_transcript(video_url)
    if "Error:" in transcript:
        return jsonify({'error': transcript}), 500

    summary = main.summarize(transcript)
    return jsonify({
        'summary': summary,
        'title': video_details['title'],
        'thumbnail': video_details['thumbnail'],
        'author': video_details['author']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)