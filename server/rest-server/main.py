import io
import time
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import os
from PIL import Image

app = FastAPI()


class SpacialImage(BaseModel):
    imageData: str
    focalLength: float
    position: dict
    rotation: list = None

@app.post("/uploadSpacialImage")
def upload_spacial_image(spacial_image: SpacialImage):
    """Receive spatial image from Android app and process it"""
    
    try:
        process_spacial_image(spacial_image)
        return {"status": "success", "message": "Image processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def process_spacial_image(spacial_image: SpacialImage):
    """Process the received spatial image"""
    try:
        # Decode base64 image
        image = Image.open(io.BytesIO(base64.b64decode(spacial_image.imageData)))
        image = image.rotate(-90, expand=True)
        
        # Create output directory if it doesn't exist
        output_dir = "processed_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp and position
        timestamp = round(time.time() * 1000)
        filename = f"{output_dir}/image_{timestamp}.jpg"
        
        # Save decoded image to file
        image.save(filename, "JPEG")
        
        print(f"Image saved to: {filename}")
        
        # Add your further processing logic here
        # e.g., ML inference, object detection, database storage, etc.
        
    except base64.binascii.Error as e:
        print(f"Base64 decoding failed: {e}")
        raise
    except IOError as e:
        print(f"File I/O error: {e}")
        raise
    except Exception as e:
        print(f"Error processing spatial image: {e}")
        import traceback
        traceback.print_exc()
        raise