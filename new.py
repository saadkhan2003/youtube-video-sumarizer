import requests
response = requests.get("https://saadkhan2003.pythonanywhere.com/summarize?videoID=EgMcfcrOS0c")
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
    