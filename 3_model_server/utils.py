import base64
from io import BytesIO
from PIL import Image
import base64

def base64_to_pillow_image(base64_string):
    # Remove the data URI prefix if present
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Create a BytesIO object to hold the image data
    image_buffer = BytesIO(image_data)

    # Open the image using Pillow
    image = Image.open(image_buffer)

    return image

def pillow_image_to_base64(image):
    # Create a BytesIO object to hold the image data
    image_buffer = BytesIO()

    # Save the image to the buffer in PNG format
    image.save(image_buffer, format="PNG")

    # Get the image data from the buffer
    image_data = image_buffer.getvalue()

    # Encode the image data in base64
    base64_string = base64.b64encode(image_data).decode("utf-8")

    return base64_string
