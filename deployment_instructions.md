# Deployment Instructions

## Frontend Deployment (Netlify)

1.  **Create a Netlify account:**
    *   Go to [https://www.netlify.com/](https://www.netlify.com/) and sign up for a free account.
2.  **Connect to your GitHub repository (Recommended):**
    *   If you have your frontend files in a GitHub repository, connect your Netlify account to the repository.
    *   Netlify will automatically deploy your website whenever you push changes to the repository.
3.  **Manually deploy files (Alternative):**
    *   If you don't want to use a GitHub repository, you can manually upload the `index.html`, `style.css`, and `script.js` files to Netlify.
    *   Drag and drop the files into the Netlify dashboard.
4.  **Your website is now deployed!**
    *   Netlify will provide you with a unique URL for your website.

## Backend Deployment (PythonAnywhere)

1.  **Create a PythonAnywhere account:**
    *   Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/) and sign up for a free account.
2.  **Create a new web app:**
    *   Log in to your PythonAnywhere account.
    *   Click on the "Web" tab.
    *   Click "Add a new web app".
    *   Select "Flask" as the web framework.
    *   Choose Python 3.9 (or a later version).
3.  **Upload your files:**
    *   Go to the "Files" tab.
    *   Upload the `app.py`, `main.py`, `.env`, and `requirements.txt` files to your PythonAnywhere account.
4.  **Create a virtual environment and install dependencies:**
    *   Go to the "Consoles" tab.
    *   Start a new console.
    *   Create a virtual environment: `python3 -m venv venv`
    *   Activate the virtual environment: `source venv/bin/activate`
    *   Install the dependencies: `pip install -r requirements.txt`
5.  **Configure your web app:**
    *   Go back to the "Web" tab.
    *   Find the section "Code".
    *   Set the "Source code" directory to the directory where you uploaded your files.
    *   Set the "WSGI configuration file" to `/var/www/<your_username>_pythonanywhere_com_wsgi.py`.
    *   **Important:** Replace `<your_username>` with your actual PythonAnywhere username.
6.  **Create and modify the WSGI file:**
    *   Go back to the "Files" tab.
    *   If the WSGI file (`/var/www/<your_username>_pythonanywhere_com_wsgi.py`) doesn't exist, create a new file with that name.
    *   **Important:** Replace `<your_username>` with your actual PythonAnywhere username.
    *   Open the WSGI file and replace the existing content with the following:

    ```python
    import os
    import sys

    # Replace <your_username> with your PythonAnywhere username
    # Replace <your_project_directory> with the name of your project directory (e.g., youtube-video-summarizer)
    path = os.path.expanduser('~/<your_username>/<your_project_directory>')
    if path not in sys.path:
        sys.path.append(path)

    # Replace "app" with the name of your Flask app instance (if it's different)
    # This is usually "app" if you followed the instructions
    from app import app as application
    ```
    *   **Important:** Replace `<your_username>` with your PythonAnywhere username in the `path` variable.
    *   **Important:** Replace `<your_project_directory>` with the name of your project directory (e.g., `youtube-video-summarizer`) in the `path` variable.
    *   **Important:** Replace `"app"` with the name of your Flask app instance (if it's different). This is usually `"app"` if you followed the instructions.
7.  **Reload your web app:**
    *   Go back to the "Web" tab.
    *   Click the "Reload" button to restart your web app.

## Connecting Frontend and Backend

1.  **Update the `script.js` file:**
    *   In the `script.js` file, replace the URL `/summarize` with the URL of your deployed PythonAnywhere app (e.g., `https://<your_username>.pythonanywhere.com/summarize`).

## Installing Requirements

1.  **Create a virtual environment:**
    *   Open a console in your PythonAnywhere account.
    *   Run the following command: `python3 -m venv venv`
2.  **Activate the virtual environment:**
    *   Run the following command: `source venv/bin/activate`
3.  **Install the requirements:**
    *   Run the following command: `pip install -r requirements.txt`
4.  **Run the Flask application:**
    *   Make sure the virtual environment is activated.
    *   Run the following command: `python app.py`
    *   **Keep this terminal window open and running.**

## Debugging Tips

If you are encountering a "404 Not Found" error, it likely means that the frontend is not correctly connecting to the backend API. Here are some things to check:

1.  **Ensure that the backend API is running correctly on PythonAnywhere:**
    *   Go to the "Web" tab on PythonAnywhere and make sure that your web app is running.
    *   Check the error logs for any errors.
2.  **Ensure that the frontend `script.js` file is correctly pointing to the backend API URL:**
    *   Open the `script.js` file and make sure that the `fetch` URL is correct. It should be pointing to your PythonAnywhere app URL (e.g., `https://<your_username>.pythonanywhere.com/summarize`).
    *   Make sure that you have replaced `<your_username>` with your actual PythonAnywhere username.
3.  **Check your browser's developer console for errors:**
    *   Open your browser's developer console (usually by pressing F12).
    *   Look for any errors related to the API request.
    *   Check the "Network" tab to see if the API request is being sent and what the response is.

## Running Locally

1.  **Backend:**
    *   Open a terminal in the project directory.
    *   Create a virtual environment: `python3 -m venv venv`
    *   Activate the virtual environment: `source venv/bin/activate`
    *   Install the requirements: `pip install -r requirements.txt`
   *   **Make sure the virtual environment is activated.**
   *   Run the Flask application: `python app.py`
   *   The backend API will be running at `http://127.0.0.1:5000`.
2.  **Frontend:**
   *   Open the `index.html` file in your browser.
   *   Update the `script.js` file to point to the local backend API URL (`http://127.0.0.1:5000/summarize`).

**What is a WSGI file?**

WSGI (Web Server Gateway Interface) is a standard interface between web servers and Python web applications. The WSGI file is a Python script that tells the web server how to run your Flask application. It essentially acts as a bridge between the web server and your application code.

Now you should have a working YouTube video summarizer deployed on a website!