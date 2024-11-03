// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const promptInput = document.getElementById('promptInput');
    const processButton = document.getElementById('processButton');
    const previewImage = document.getElementById('previewImage');
    const loadingSpinner = document.getElementById('loading');

    // Hide loading spinner initially
    loadingSpinner.style.display = 'none';

    // Preview uploaded image
    imageUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle image processing
    processButton.addEventListener('click', async function() {
        const file = imageUpload.files[0];
        const prompt = promptInput.value.trim();

        if (!file) {
            alert('Please upload an image first');
            return;
        }

        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }

        // Show loading spinner
        loadingSpinner.style.display = 'block';
        processButton.disabled = true;

        try {
            const formData = new FormData();
            formData.append('image', file);
            formData.append('prompt', prompt);

            const response = await fetch('/process-image', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Update preview with processed image
            previewImage.src = data.result_image_url + '?t=' + new Date().getTime();
            previewImage.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            alert('Error processing image: ' + error.message);
        } finally {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            processButton.disabled = false;
        }
    });
});