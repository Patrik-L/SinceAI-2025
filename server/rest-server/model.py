import numpy as np
import torch
import cv2
from PIL import Image
from ultralytics import YOLO
from transformers import DepthProImageProcessorFast, DepthProForDepthEstimation, infer_device

def executeModel(imagePath):
    #loading yolo model
    yolo_model = YOLO('yolo11n.pt')
    image_path = imagePath
    image = Image.open(imagePath)
    yolo_input = cv2.imread(image_path)
    results = yolo_model(yolo_input)

    device = infer_device()


    print(torch.__version__)
    print(torch.cuda.is_available(), device);


    detected_items = [] #box around identified object
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy() # get bounding boxes
        classes = result.boxes.cls.cpu().numpy() # get class labels
    for box, cls in zip(boxes, classes):
        object_name=yolo_model.names[int(cls)]
        x1, y1, x2, y2 = map(int, box[:4])
        detected_items.append((x1, y1, x2, y2, object_name))
        cv2.rectangle(yolo_input, (x1, y1), (x2, y2), (255, 0, 230), 2) # Draws rectangle


    # #loading depth model and prepare image
    # depth_model, transform = depth_pro.create_model_and_transforms()
    # depth_model.eval()

    # image, icc_profile, f_px = depth_pro.load_rgb(image_path)
    # print(len(image), icc_profile, f_px)
    # depth_input = transform(image)
    # print("depth_input")

    # # perform depth inference

    # prediction = depth_model.infer(depth_input, f_px=f_px)
    # print("prediction done", prediction)


    image_processor = DepthProImageProcessorFast.from_pretrained("apple/DepthPro-hf")
    model = DepthProForDepthEstimation.from_pretrained("apple/DepthPro-hf").to(device)

    inputs = image_processor(images=image, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model(**inputs)

    post_processed_output = image_processor.post_process_depth_estimation(
        outputs, target_sizes=[(image.height, image.width)],
    )

    print(post_processed_output[0])

    depth = post_processed_output[0]["predicted_depth"]
    depth_np = depth.squeeze().cpu().numpy()

    detected_matches = []
    # Calculate depth for detected persons and display on image
    for x1, y1, x2, y2, name in detected_items:
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        print(center_x, center_y)
        # Extract depth value at the center of the bounding box
        depth_value = depth_np[center_y, center_x]
        text = f'{name} - Depth: {depth_value:.2f}m'
        # Define font properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        # Set text position
        text_x = x1
        text_y = y1 - 10
        # Create a rectangle for text background
        rect_x1 = text_x - 10
        rect_y1 = text_y - text_size[1] - 5
        rect_x2 = text_x + text_size[0] + 5
        rect_y2 = text_y + 5
        # Draw the background rectangle and add text
        cv2.rectangle(yolo_input, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
        cv2.putText(yolo_input, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        detected_matches.append(dict(bounding_boxes = (x1, y1, x2, y2), item_name = name, estimated_depth = depth_value))

    # Display person detection with depth values
    # Save the image with detection and depth annotations
    output_image = cv2.imwrite('object_detection_with_depth.jpg', yolo_input)

    return detected_matches, output_image 