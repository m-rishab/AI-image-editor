from flask import Flask, request, jsonify, render_template
from models.background_removal import remove_background
from models.dalle_transform import apply_dalle_transform
from models.gpt_prompt import process_gpt_prompt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    image = request.files['image']
    prompt = request.form['prompt']
    
    # Use GPT to understand the prompt and select the appropriate function
    task = process_gpt_prompt(prompt)
    
    # Perform the required operation based on the prompt
    if task == 'remove_background':
        result_image = remove_background(image)
    elif task == 'dalle_transform':
        result_image = apply_dalle_transform(image, prompt)
    else:
        return jsonify({'error': 'Unknown task specified'})

    # Convert result to a format suitable for response
    result_image_path = f"static/results/{task}_output.png"
    result_image.save(result_image_path)
    
    return jsonify({'result_image_url': result_image_path})

if __name__ == '__main__':
    app.run(debug=True)
