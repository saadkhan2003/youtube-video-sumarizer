from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import main  # Import the main.py file as a module
import requests

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://saadyoutubesummarizer.netlify.app"])

@app.route('/')
def hello_world():
    return "<h1>YouTube Summarizer Backend is Running!</h1>"

def get_video_details(video_id):
    # Using oEmbed API which doesn't require an API key
    url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    print(f"Fetching video details from: {url}")
    
    try:
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"Response data: {data}")
        
        return {
            'title': data['title'],
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'author': data['author_name']
        }
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

@app.route('/summarize', methods=['GET'])
def summarize_video():
    try:
        print("Summarize video function called")
        video_id = request.args.get('videoID')
        if not video_id:
            return jsonify({'error': 'Video ID is required'}), 400

        print(f"Processing video ID: {video_id}")
        video_details = get_video_details(video_id)
        if not video_details:
            return jsonify({'error': 'Could not fetch video details. Please check if the video ID is correct.'}), 500

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Getting transcript for: {video_url}")
        transcript = main.get_transcript(video_url)
        if "Error:" in transcript:
            return jsonify({'error': f'Transcript error: {transcript}'}), 500

        print("Generating summary...")
        summary = main.summarize(transcript)
        if not summary:
            return jsonify({'error': 'Failed to generate summary'}), 500

        print("Summary generated successfully")
        return jsonify({
            'summary': summary,
            'title': video_details['title'],
            'thumbnail': video_details['thumbnail'],
            'author': video_details['author']
        })
    except Exception as e:
        print(f"Unexpected error in summarize_video: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)