from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import os
import model
from datetime import datetime

app = FastAPI()


class SpacialImage(BaseModel):
    image: str
    focalLength: float
    position: dict
    rotation: list = None

class ProcessedImage():
    outputImage: str
    focalLength: float
    position: dict
    rotation: list = None
    detectedMatches: list


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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
    print(f"[DEBUG] Processing spatial image at position: ({spacial_image.position['x']}, {spacial_image.position['y']}, {spacial_image.position['z']})")
    print(f"[DEBUG] Image data length: {len(spacial_image.image)}")
    print(f"[DEBUG] Focal length: {spacial_image.focalLength}")
    print(f"[DEBUG] Rotation: {spacial_image.rotation}")
    
    try:
        # Decode base64 image
        print("[DEBUG] Attempting to decode base64 image...")
        image_data = base64.b64decode(spacial_image.image)
        print(f"[DEBUG] Successfully decoded image. Byte size: {len(image_data)}")
        
        # Create output directory if it doesn't exist
        output_dir = "processed_images"
        os.makedirs(output_dir, exist_ok=True)
        print(f"[DEBUG] Output directory created/verified: {output_dir}")
        
        # Generate filename with timestamp and position
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/image_{timestamp}_x{spacial_image.position['x']}_y{spacial_image.position['y']}_z{spacial_image.position['z']}.jpg"
        print(f"[DEBUG] Generated filename: {filename}")
        
        # Save decoded image to file
        print("[DEBUG] Writing image to file...")
        with open(filename, "wb") as f:
            bytes_written = f.write(image_data)
            print(f"[DEBUG] Successfully wrote {bytes_written} bytes to file")
        
        print(f"[DEBUG] Image saved to: {filename}")
        
        det_matches, outImage = model.executeModel(filename)

        processed_image.outputImage = outImage

    except base64.binascii.Error as e:
        print(f"[ERROR] Base64 decoding failed: {e}")
        raise
    except IOError as e:
        print(f"[ERROR] File I/O error: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error processing spatial image: {e}")
        import traceback
        traceback.print_exc()
        raise



def post_processed_image(spacial_image: SpacialImage, processed_image: ProcessedImage):
    print(f"[DEBUG] Spacial image postion: ({spacial_image.position['x']}, {spacial_image.position['y']}, {spacial_image.position['z']})")
    print(f"[DEBUG] Image data length: {len(spacial_image.image)}")
    print(f"[DEBUG] Focal length: {spacial_image.focalLength}")
    print(f"[DEBUG] Rotation: {spacial_image.rotation}")
    print(f"[DEBUG] Processed image detected item list: ({process_spacial_image.detected_matches})")
    print(f"[DEBUG] Processed image's data length: {process_spacial_image.outputImage}")