document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('summaryForm');
    const summaryDiv = document.getElementById('summary');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const videoDetails = document.querySelector('.video-details');
    const thumbnail = document.getElementById('thumbnail');
    const videoTitle = document.getElementById('video-title');
    const videoAuthor = document.getElementById('video-author');
    const input = document.getElementById('videoID');

    function showLoading() {
            loadingSpinner.style.display = 'flex';
            summaryDiv.style.display = 'none';
            videoDetails.style.display = 'none';
        }
    
        function hideLoading() {
            loadingSpinner.style.display = 'none';
            summaryDiv.style.display = 'block';
            videoDetails.style.display = 'block';
        }

    function showError(message) {
        summaryDiv.innerHTML = `
            <div class="error-message" style="color: #dc3545; padding: 1rem; background: #fff; border-radius: 8px; text-align: center;">
                <i class="fas fa-exclamation-circle"></i>
                <p>${message}</p>
            </div>
        `;
        videoDetails.style.display = 'none';
    }

    form.addEventListener('submit', function(event) {
            event.preventDefault();
            let videoID = input.value.trim();
            
            if (videoID === "") {
                showError('Please enter a YouTube video ID or link');
                return;
            }
    
            // Check if the input is a YouTube link
            if (videoID.includes("youtube.com") || videoID.includes("youtu.be")) {
                // Extract the video ID from the link
                const url = new URL(videoID);
                videoID = url.searchParams.get("v");
                if (!videoID) {
                    // Handle short YouTube links
                    videoID = url.pathname.substring(1);
                }
            }
            
            if (!videoID) {
                showError('Invalid YouTube video ID or link');
                return;
            }

        showLoading();

        fetch('https://saadkhan2003.pythonanywhere.com/summarize?videoID=' + videoID)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                hideLoading();
                
                // Update video details
                thumbnail.src = data.thumbnail;
                thumbnail.alt = data.title;
                videoTitle.textContent = data.title;
                videoAuthor.textContent = data.author;
                
                // Update summary
                const summary = data.summary;
                summaryDiv.innerHTML = `
                    <h2 style="margin-bottom: 1rem;">Summary</h2>
                    ${marked.parse(summary)}
                `;
            })
            .catch(error => {
                hideLoading();
                showError(error.message || 'Failed to generate summary');
            });
    });

    // Add input validation and formatting
    input.addEventListener('input', function(e) {
        const value = e.target.value;
        // Remove any non-alphanumeric characters
        e.target.value = value.replace(/[^a-zA-Z0-9-_]/g, '');
    });

    // Paste button functionality
   const pasteButton = document.getElementById('pasteButton');
   pasteButton.addEventListener('click', async () => {
       try {
           const text = await navigator.clipboard.readText();
           input.value = text;
       } catch (err) {
           console.error('Failed to read clipboard contents: ', err);
           showError(`Failed to read clipboard contents: ${err}. Please paste manually.`);
       }
   });
});