import io
import time
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import os
import model
from PIL import Image

app = FastAPI()


class SpacialImage(BaseModel):
    imageData: str
    focalLength: float
    position: dict
    rotation: list = None

class ProcessedImage():
    outputImage: str
    focalLength: float
    position: dict
    rotation: list = None
    detectedMatches: list

@app.post("/uploadSpacialImage")
def upload_spacial_image(spacial_image: SpacialImage):
    """Receive spatial image from Android app and process it"""
    
    try:
        process_spacial_image(spacial_image)
        return {"status": "success", "message": "Image processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def process_spacial_image(spacial_image: SpacialImage, processed_image: ProcessedImage):
    """Process the received spatial image"""
    try:
        # Decode base64 image
        image = Image.open(io.BytesIO(base64.b64decode(spacial_image.imageData)))
        image = image.rotate(-90, expand=True)
        
        # Create output directory if it doesn't exist
        output_dir = "original_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp and position
        timestamp = round(time.time() * 1000)
        filename = f"{output_dir}/image_{timestamp}.jpg"
        
        # Save decoded image to file
        image.save(filename, "JPEG")
        
        print(f"Image saved to: {filename}")
        
        det_matches, outImageName = model.executeModel(filename)

        outputtedImage = Image.open(outImageName)

        processed_image.outputImage = outputtedImage.save("output_image.jpg")
        processed_image.detectedMatches = det_matches

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



def post_processed_image(spacial_image: SpacialImage, processed_image: ProcessedImage):
    print(f"[DEBUG] Spacial image postion: ({spacial_image.position['x']}, {spacial_image.position['y']}, {spacial_image.position['z']})")
    print(f"[DEBUG] Image data length: {len(spacial_image.image)}")
    print(f"[DEBUG] Focal length: {spacial_image.focalLength}")
    print(f"[DEBUG] Rotation: {spacial_image.rotation}")
    print(f"[DEBUG] Processed image detected item list: ({processed_image.detectedMatches})")
    print(f"[DEBUG] Processed image's data length: {processed_image.outputImage}")

    processed_image.position = spacial_image.position
    processed_image.focalLength = spacial_image.focalLength
    processed_image.rotation = spacial_image.rotation

    try:
        # Encode to base64 image
        image = Image.open(io.BytesIO(base64.b64encode(processed_image.outputImage)))
        processed_image.outputImage = image

    except base64.binascii.Error as e:
        print(f"Base64 encoding failed: {e}")
        raise
    except IOError as e:
        print(f"File I/O error: {e}")
        raise
    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback
        traceback.print_exc()
        raise

    return processed_image