from PIL import Image
from io import BytesIO
import base64

def encode_image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def decode_image_from_base64(base64_str):
    buffer = BytesIO(base64.b64decode(base64_str))
    return Image.open(buffer)
