# Mobile 3D object detection (SinceAI 2025 Valmet challenge)

Android application with YOLO11n based object detection with depth analysis.

## Valmet challenge and our idea

The SinceAI 2025 Valmet challenge was to find a way to combine 3D virtual environments of factories, and digital twins of technical devices in an automatic way. With techniques like Gaussian splatting you can efficiently create virtual environments, but it lacks the capability to automatically detect technical devices. Factories can have up to thousands of different devices, so manually adding those would be time consuming. 

Our idea is to make a way to detect technical devices during the 3D scanning process, and use the location data we gather during that to accurately combine the virtual environment and the digital twins of technical devices.


## Usage

The build can be downloaded to the phone to try it out. With the application you'll take a photo, the photo will be processed by a model through fastAPI, and sent back to the phone. The processed photo has the identified objects marked with information. It currently uses generic data to identify any objects.

## Future plans

The application would be able to receive segmented video, process it, and turn it into a 3d gaussian splatting environment. The application would also be able to take single pictures for detecting singular items and adding them to the gaussian splatting as well as into the AI model training. Also specified AI model for industrial needs, would be made for better detection rate.

For these future plans, the current application has been build with future in mind. The current application collects the taken photos' coordinates and the FOV. With this information, a 3d visualization would be possible, since the collected images hold depth information about the environment and detected objects.

