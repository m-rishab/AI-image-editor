# models/dalle_transform.py
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with direct API key
api_key = "your-api-key"
client = OpenAI(api_key=api_key)

def apply_dalle_transform(image_file, prompt):
    try:
        # Open and prepare the image
        image = Image.open(image_file)
        
        # Convert the image to bytes
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        
        response = client.images.edit(
            image=buffered.getvalue(),
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Get the URL of the generated image
        edited_image_url = response.data[0].url
        
        # Download the edited image
        edited_image_response = requests.get(edited_image_url)
        edited_image = Image.open(BytesIO(edited_image_response.content))
        
        return edited_image
        
    except Exception as e:
        print(f"Error in DALL-E processing: {str(e)}")
        raise Exception(f"Failed to process image with DALL-E: {str(e)}")