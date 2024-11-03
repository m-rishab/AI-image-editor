# models/gpt_prompt.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with direct API key
api_key = "your-api-key"
client = OpenAI(api_key=api_key)

def process_gpt_prompt(prompt):
    try:
        # Updated system prompt to be more specific about task classification
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a classifier that determines if an image editing command is for:
                1. Background removal (respond with 'remove_background'): Only if the user explicitly mentions removing, deleting, or eliminating the background
                2. DALL-E transformation (respond with 'dalle_transform'): For any other image editing request like adding elements, changing styles, enhancing, or transforming the image
                
                Respond ONLY with either 'remove_background' or 'dalle_transform'. Default to 'dalle_transform' if uncertain."""},
                {"role": "user", "content": "make the background transparent"},
                {"role": "assistant", "content": "remove_background"},
                {"role": "user", "content": "add a dragon behind the person"},
                {"role": "assistant", "content": "dalle_transform"},
                {"role": "user", "content": f"Analyze this command: {prompt}"}
            ],
            max_tokens=60,
            temperature=0.3
        )
        
        # Get the response text
        task = response.choices[0].message.content.strip().lower()
        
        # Validate the response
        if task not in ['remove_background', 'dalle_transform']:
            return 'dalle_transform'  # Default to DALL-E transform if unclear
            
        return task
        
    except Exception as e:
        print(f"Error in GPT processing: {str(e)}")
        return 'dalle_transform'  # Default to DALL-E transform in case of error