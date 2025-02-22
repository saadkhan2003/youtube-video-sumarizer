import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import json

load_dotenv()

def get_transcript(video_url):
    try:
        video_id = video_url.split("watch?v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ""
        for entry in transcript:
            text += entry["text"] + " "
        return text
    except Exception as e:
        print(f"Transcript error: {str(e)}")
        return f"Error: Could not fetch transcript. Please check the video ID and try again. Original error: {e}"

def summarize(transcript):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{
                "text": f"Summarize the following transcript in Markdown bullet points:\\n{transcript}"
                            }]
                        }],
                        "generationConfig": {
                            "maxOutputTokens": 200
                        }
                    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request failed: {e}")
        return f"Error: API request failed. Please check your API key and network connection. Original error: {e}"
    except (KeyError, IndexError) as e:
        print(f"Gemini API response parsing error: {e}")
        return f"Error: Could not parse API response. Please check the API response format. Original error: {e}"
    except Exception as e:
        print(f"Gemini API unexpected error: {e}")
        return f"Error: An unexpected error occurred during summarization. Original error: {e}"