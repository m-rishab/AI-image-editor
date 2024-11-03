# models/background_removal.py
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import ssl

# Set default SSL context to use certifi certificates
ssl._create_default_https_context = ssl._create_unverified_context

# Load the DeepLabV3 model
model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
model.eval()

def remove_background(image_path):
    # Load and preprocess the image
    image = Image.open(image_path).convert('RGB')
    
    # Get the original size for later resizing
    original_size = image.size
    
    # Preprocess the image
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((520, 520)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(image).unsqueeze(0)
    
    # Move tensor to the same device as the model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    input_tensor = input_tensor.to(device)
    model.to(device)
    
    # Get the prediction
    with torch.no_grad():
        output = model(input_tensor)['out'][0]
    output_predictions = output.argmax(0).cpu().numpy()
    
    # Create the mask
    mask = np.zeros_like(output_predictions, dtype=np.uint8)
    mask[output_predictions == 15] = 255  # person class
    
    # Resize mask back to original image size
    mask_image = Image.fromarray(mask).resize(original_size, Image.LANCZOS)
    
    # Create the final image with transparency
    result_image = Image.new("RGBA", original_size)
    result_image.paste(image, (0, 0))
    
    # Convert mask to RGBA for proper alpha channel
    mask_image = mask_image.convert('L')
    result_image.putalpha(mask_image)
    
    return result_image