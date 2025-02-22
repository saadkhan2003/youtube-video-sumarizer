# YouTube Video Summarizer Deployment Instructions

## Backend Deployment (PythonAnywhere)

1.  **Create a PythonAnywhere account (if you haven't already)**
    *   Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
    *   Sign up/Login with username: saadkhan2003

2.  **Upload your files**
    *   Go to the "Files" tab
    *   Upload these files to `/home/saadkhan2003/mysite/appnew/`:
        - `app.py`
        - `main.py`
        - `.env`
        - `requirements.txt`

3.  **Set up virtual environment**
    *   Go to the "Consoles" tab
    *   Click "New Console" → "Bash"
    *   Run these commands:
        ```bash
        cd /home/saadkhan2003/mysite/appnew
        python3 -m venv venv
        source venv/bin/activate
        # Install required packages explicitly
        pip install flask python-dotenv pytube google-generativeai
        # Install any additional requirements
        pip install -r requirements.txt
        # Verify installations
        pip list
        ```

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

6.  **Reload web app**
    *   Go back to "Web" tab
    *   Click "Reload saadkhan2003.pythonanywhere.com"

## Frontend Setup

1.  **Update the backend URL**
    *   Open `script.js`
    *   Find the fetch URL line
    *   Replace it with: `https://saadkhan2003.pythonanywhere.com/summarize`

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
    *   Paste a YouTube video ID or URL
    *   Click Summarize

## Troubleshooting

If you see "Error loading your PythonAnywhere-hosted site":

1.  **Check the log files**
    *   Go to the "Web" tab
    *   Look for the "Log files" section
    *   Click on these links to view the logs:
        - `saadkhan2003.pythonanywhere.com.error.log`
        - `saadkhan2003.pythonanywhere.com.server.log`

2.  **Fix for Module Not Found Errors**

    For "ModuleNotFoundError: No module named 'google.generativeai'":
    *   This means the Google Generative AI package is not installed. Run:
        ```bash
        cd /home/saadkhan2003/mysite/appnew
        source venv/bin/activate
        pip install google-generativeai
        ```
    *   Go back to "Web" tab and click "Reload"

    For "ModuleNotFoundError: No module named 'app'":
    *   This error means Python cannot find your `app.py` file. Follow these steps:
    
    a. **Check file location**
       * Go to Files tab
       * Navigate to `/home/saadkhan2003/mysite/appnew/`
       * Verify `app.py` is in this directory
       * If not, upload it again
    
    b. **Check WSGI configuration**
       * Go to Web tab
       * Under "Code" section:
           - Set "Source code" to: `/home/saadkhan2003/mysite/appnew`
           - Set "Working directory" to: `/home/saadkhan2003/mysite/appnew`
       * Click Save
    
    c. **Verify file permissions and content**
       * Open a Bash console
       * Run these commands:
         ```bash
         cd /home/saadkhan2003/mysite/appnew
         ls -l app.py
         # Should show read permissions (-rw-r--r--)
         cat app.py
         # Should show your Flask application code
         python3
         >>> import app
         >>> # If no error, the file is found and valid
         >>> exit()
         ```
    
    d. **Test the environment**
       * Still in the Bash console:
         ```bash
         source venv/bin/activate
         pip list | grep Flask
         # Should show Flask is installed
         python3 -c "import sys; print(sys.path)"
         # Should include /home/saadkhan2003/mysite/appnew
         ```

3.  **Try these steps**
    *   Go to "Consoles" tab
    *   Start a new Bash console
    *   Run these commands:
        ```bash
        cd /home/saadkhan2003/mysite/appnew
        source venv/bin/activate
        pip install -r requirements.txt
        ```
    *   Go back to "Web" tab
    *   Click "Reload saadkhan2003.pythonanywhere.com"

4.  **Additional checks**
    *   Verify the URL in `script.js` matches your PythonAnywhere domain
    *   Look for errors in browser's developer console (F12)

## Understanding the URLs

- Backend URL: `https://saadkhan2003.pythonanywhere.com`
- API Endpoint: `/summarize`
- Full API URL: `https://saadkhan2003.pythonanywhere.com/summarize?videoID=your_video_id`

The `/summarize` endpoint is defined in `app.py` and handles the video summarization requests.
