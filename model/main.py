import numpy as np
import cv2
from ultralytics import YOLO

#loading yolo model
yolo_model = YOLO('yolov11.pt') #might not work
image_path = '' #fill later
yolo_input = cv2.imread(image_path)
results = yolo_model(yolo_input)

object_box = [] #box around identified object
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy() # get bounding boxes
    classes = result.boxes.cls.cpu().numpy() # get class labels
for box, cls in zip(boxes, classes):
    x1, y1, x2, y2 = map(int, box[:4])
    detected_items.append((x1, y1, x2, y2))
    cv2.rectagle(yolo_input, (x1, y1), (x2, y2), (255, 0, 230), 2) # Draws rectangle


#loading depth model and prepare image

depth_model, transform = depth_pro.create_model_and_transform()
depth_model.eval()

image, f_px = depth_pro.load_rgb(image_path)
depth_input = transform(image)

# perform depth inference

prediction = depth_model.infer(depth_input, f_px=f_px)
