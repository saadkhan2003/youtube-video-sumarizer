# YouTube Video Summarizer Deployment Instructions

## Backend Deployment (PythonAnywhere)

1.  **Create a PythonAnywhere account (if you haven't already)**
    *   Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
    *   Sign up/Login with username: saadkhan2003

2.  **Upload your files**
    *   Go to the "Files" tab
    *   Upload these files to `/home/saadkhan2003/mysite/appnew/`:
        - `app.py` (Make sure it includes CORS configuration and uses pytube for video details)
        - `main.py` (Make sure it has the latest error handling)
        - `.env`
        - `requirements.txt`

3.  **IMPORTANT: Install Required Packages**
    *   Go to the "Consoles" tab
    *   Click "New Console" → "Bash"
    *   Copy and paste these commands one by one:
         ```bash
         # Step 1: Go to your project directory
         cd /home/saadkhan2003/mysite/appnew

         # Step 2: Create and activate virtual environment
         python3 -m venv venv
         source venv/bin/activate

         # Step 3: Install all required packages (THIS IS CRUCIAL, RUN ONE BY ONE)
         pip install flask
         pip install python-dotenv
         pip install pytube
         pip install google-generativeai
         pip install flask_cors
         pip install youtube-transcript-api

         # Step 4: Verify installations
         pip list | grep -E "flask|python-dotenv|pytube|google|flask_cors|youtube-transcript-api"
         ```
    *   Make sure no errors appear during installation

4.  **Configure web app**
    *   Go to the "Web" tab
    *   Click "Add a new web app"
    *   Choose "Manual Configuration"
    *   Choose Python 3.9
    *   Set "Source code" to: `/home/saadkhan2003/mysite/appnew`

5.  **Set up WSGI file**
    *   Go to the "Files" tab
    *   Open: `/var/www/saadkhan2003_pythonanywhere_com_wsgi.py`
    *   Replace everything with:
    ```python
    import os
    import sys

    # This path must exactly match where your app.py file is
    path = '/home/saadkhan2003/mysite/appnew'
    if path not in sys.path:
        sys.path.append(path)
        
    # Import the Flask application
    from app import app as application

    # Print debugging information
    print(f"Python path: {sys.path}")
    print(f"Working directory: {os.getcwd()}")
    ```

6.  **Final Steps**
    *   Verify all packages are installed:
        ```bash
        source venv/bin/activate
        pip list | grep -E "flask|python-dotenv|pytube|google"
        ```
    *   Go back to "Web" tab
    *   Click "Reload saadkhan2003.pythonanywhere.com"
    *   Check the error logs if any issues persist

## Frontend Setup

1.  **Update the backend URL**
    *   Open `script.js`
    *   Find the fetch URL line
    *   Replace it with: `https://saadkhan2003.pythonanywhere.com/summarize`
    *   **Important:** Make sure the URL is correct and matches your PythonAnywhere username.

2.  **Deploy frontend**
    *   Option 1: Use Netlify
        - Sign up at [https://www.netlify.com/](https://www.netlify.com/)
        - Upload `index.html`, `style.css`, and `script.js`
    *   Option 2: Run locally
        - Just open `index.html` in your browser

## Testing

1.  **Check if backend is running**
    *   Visit: `https://saadkhan2003.pythonanywhere.com`
    *   Should not show any error

2.  **Test the summarizer**
    *   Open your frontend (Netlify URL or local `index.html`)
    *   Open browser developer tools (F12)
    *   Go to Network tab in developer tools
    *   Paste a YouTube video ID or URL
    *   Click Summarize
    *   In Network tab:
        - Look for the request to `/summarize`
        - Check if CORS headers are present
        - Check response status code
        - If you see a 500 error, check response body for error details

## Troubleshooting

If you see "Error loading your PythonAnywhere-hosted site" or a 500 error from Netlify:

1.  **Check the log files**
    *   Go to the "Web" tab
    *   Look for the "Log files" section
    *   Click on these links to view the logs:
        - `saadkhan2003.pythonanywhere.com.error.log`
        - `saadkhan2003.pythonanywhere.com.server.log`
    *   Look for the latest error messages in the logs. They will usually indicate the cause of the 500 error.

2.  **Common causes and fixes for 500 Internal Server Error**
    *   **Missing API key:** Make sure you have set the `GEMINI_API_KEY` environment variable in your `.env` file.
    *   **Incorrect file paths:** Double-check that all file paths in your WSGI file and application code are correct.
    *   **Import errors:** If you see "ModuleNotFoundError" in the logs, make sure you have installed all the required packages.
    *   **Code errors:** Carefully review your `app.py` and `main.py` files for any syntax errors or logical errors.
    *   **Test the API manually:**
        ```bash
        # Test from the command line
        curl -v "https://saadkhan2003.pythonanywhere.com/summarize?videoID=EgMcfcrOS0c"
        
        # Or use Python to test
        python3 -c '
        import requests
        response = requests.get("https://saadkhan2003.pythonanywhere.com/summarize?videoID=EgMcfcrOS0c")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        '
        ```

3.  **Fix for "Something went wrong" Error**
    *   This usually means there's an error in your application. Follow these steps:
    
    a. **Check the error logs**
        ```bash
        cd /home/saadkhan2003/mysite/appnew
        source venv/bin/activate
        # Try running the app locally first
        python3 app.py
        ```
    
    b. **Check your .env file and API key**
        * Make sure your `.env` file is in the correct location: `/home/saadkhan2003/mysite/appnew/.env`
        * Verify it contains your API keys:
        ```bash
        cat .env
        # Should show: GEMINI_API_KEY=your_api_key_here
        
        # Test if Python can read the API key
        python3 -c "
        from dotenv import load_dotenv
        import os
        load_dotenv()
        print('API Key:', os.getenv('GEMINI_API_KEY'))
        "
        # Should print your API key
        ```
    
    c. **Check app.py permissions**
        ```bash
        ls -l app.py
        chmod 644 app.py
        ```

4.  **Fix for Module Not Found Errors**
    *   This means the Google Generative AI package is not installed. Run:
        ```bash
        cd /home/saadkhan2003/mysite/appnew
        source venv/bin/activate
        pip install google-generativeai
        ```
    *   Go back to "Web" tab and click "Reload"

5.  **Fix for CORS error**
    *   Make sure the `app.py` file includes the CORS configuration, allowing only `https://saadyoutubesummarizer.netlify.app`.

## Understanding the URLs

- Backend URL: `https://saadkhan2003.pythonanywhere.com`
- API Endpoint: `/summarize`
- Full API URL: `https://saadkhan2003.pythonanywhere.com/summarize?videoID=your_video_id`

The `/summarize` endpoint is defined in `app.py` and handles the video summarization requests.
