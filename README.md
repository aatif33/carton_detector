# 📦 Automated Carton Seal Detection using Raspberry Pi 5 & Computer Vision

An automated computer-vision system that uses a **Raspberry Pi 5 and webcam** to inspect a carton/box and determine whether it is **SEALED or OPEN**.

The system automatically captures images, converts them to grayscale, applies a configurable threshold, detects objects using contours, measures processing time in milliseconds, and displays the inspection results in real time.

---

## 📌 Project Overview

In manufacturing and packaging environments, cartons must be checked before they move to the next stage of production.

Manual inspection can be:

- Slow
- Inconsistent
- Dependent on human attention
- Difficult to monitor continuously

This project attempts to automate the inspection process using:

```text
                 USB WEBCAM
                     │
                     ▼
             ┌───────────────┐
             │ Raspberry Pi 5│
             └───────┬───────┘
                     │
                     ▼
              Image Capture
                     │
                     ▼
                 Grayscale
                     │
                     ▼
             Threshold = 15
                     │
                     ▼
              Image Cleaning
                     │
                     ▼
              Contour Detection
                     │
                     ▼
               Object Counting
                     │
                     ▼
             Seal Inspection
                     │
              ┌──────┴──────┐
              ▼             ▼
           SEALED          OPEN
```

---

# 🎯 Objectives

The main objectives are:

1. Capture carton images automatically using a webcam.
2. Process the images directly on a Raspberry Pi 5.
3. Convert captured images to grayscale.
4. Apply binary thresholding.
5. Limit the threshold value to `15`.
6. Detect objects using contours.
7. Count detected objects.
8. Display the inspection result.
9. Measure image-capture time in milliseconds.
10. Measure image-processing time in milliseconds.
11. Store captured images locally.
12. Provide a foundation for automated industrial carton inspection.

---

# 🧰 Hardware Requirements

## Required Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi 5 | Main processing device |
| USB Webcam | Captures carton images |
| Monitor | Displays live inspection |
| Keyboard | Raspberry Pi control |
| Mouse | Raspberry Pi control |
| Carton/Box | Object being inspected |
| Proper lighting | Consistent image quality |

### Optional Hardware

The project can later be extended with:

- Red LED
- Green LED
- Buzzer
- Conveyor belt
- IR sensor
- Ultrasonic sensor
- Relay
- Motor controller

---

# 💻 Software Requirements

The project uses:

- Raspberry Pi OS
- Python 3
- OpenCV
- NumPy
- Git
- GitHub

---

# 🗂️ Project Structure

A typical project structure is:

```text
carton_detector/
│
├── README.md
├── .gitignore
│
├── camera_test.py
├── capture.py
├── auto_capture.py
├── detector.py
│
├── Images/
│   └── Reference/demo images
│
├── captured_images/
│   └── Automatically captured images
│
├── opened.png
├── sealed.png
├── proof.png
└── proof1.png
```

> `captured_images/` is used for locally captured inspection images. These images do not need to be uploaded to GitHub for normal operation.

---

# 🔌 Hardware Setup

Connect the USB webcam to one of the USB ports on the Raspberry Pi 5.

```text
       ┌──────────────────────┐
       │      USB WEBCAM      │
       └──────────┬───────────┘
                  │ USB
                  ▼
       ┌──────────────────────┐
       │   RASPBERRY PI 5     │
       │                      │
       │   Python + OpenCV    │
       └──────────┬───────────┘
                  │
                  ▼
              HDMI / Display
```

Position the webcam so that the carton is visible consistently.

### Recommended camera setup

The camera should:

- Remain fixed.
- Point toward the carton inspection area.
- Maintain a constant distance.
- Avoid excessive reflections.
- Have consistent lighting.
- Capture the same region of the carton every time.

Consistent camera positioning is extremely important for threshold-based computer vision.

---

# 🔍 Check the Webcam

Open a terminal on Raspberry Pi.

Run:

```bash
ls /dev/video*
```

You should see something similar to:

```text
/dev/video0
/dev/video1
```

Usually `/dev/video0` is the webcam.

To obtain detailed camera information:

```bash
v4l2-ctl --list-devices
```

If `v4l2-ctl` is not installed:

```bash
sudo apt update
sudo apt install v4l-utils
```

Then run:

```bash
v4l2-ctl --list-devices
```

---

# 🐍 Install Python Dependencies

Update Raspberry Pi packages:

```bash
sudo apt update
```

Install OpenCV and NumPy:

```bash
sudo apt install python3-opencv python3-numpy
```

Check OpenCV:

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

Check NumPy:

```bash
python3 -c "import numpy; print(numpy.__version__)"
```

---

# 📷 Test the Camera

The project contains:

```text
camera_test.py
```

Run:

```bash
python3 camera_test.py
```

The webcam feed should appear.

The basic operation is:

```text
Camera
   ↓
Capture Frame
   ↓
Display Frame
```

Press:

```text
q
```

to close the camera window.

---

# 📸 Image Capture

The project supports automatic image capture.

Instead of manually pressing a button for every image, the system periodically captures an image from the webcam.

Example:

```text
Camera running
       │
       ▼
Wait for capture interval
       │
       ▼
Capture image
       │
       ▼
Save image
       │
       ▼
Continue monitoring
```

Captured images are saved in:

```text
captured_images/
```

Example:

```text
captured_images/
│
├── box_0001.jpg
├── box_0002.jpg
├── box_0003.jpg
├── box_0004.jpg
└── ...
```

---

# ⏱️ Capture Time Measurement

The system measures how long it takes to save an image.

Python's high-resolution performance timer is used:

```python
start_time = time.perf_counter()

success = cv2.imwrite(filename, frame)

end_time = time.perf_counter()

capture_time_ms = (
    end_time - start_time
) * 1000
```

The result is displayed in milliseconds.

Example:

```text
Capture Time: 18.42 ms
```

This provides a basic performance measurement of the image-saving operation.

---

# 🖼️ Grayscale Processing

After capturing the image, the system converts the image from BGR/RGB representation into grayscale.

```python
gray = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2GRAY
)
```

A color image contains multiple channels.

A grayscale image contains a single intensity value for each pixel.

Conceptually:

```text
COLOR IMAGE
    │
    ▼
┌───────────────┐
│ Red           │
│ Green         │
│ Blue          │
└───────┬───────┘
        │
        ▼
   GRAYSCALE
        │
        ▼
Intensity values
```

This simplifies subsequent image processing.

---

# ⚫ Threshold Processing

The current project uses a threshold value of:

```text
15
```

The configuration is:

```python
THRESHOLD_VALUE = 15
```

The threshold operation is:

```python
_, threshold = cv2.threshold(
    gray,
    THRESHOLD_VALUE,
    255,
    cv2.THRESH_BINARY
)
```

The basic concept is:

```text
Pixel intensity <= 15
        ↓
      BLACK

Pixel intensity > 15
        ↓
      WHITE
```

This produces a binary image containing primarily black and white regions.

---

# 🧹 Morphological Processing

Thresholding can create small unwanted regions caused by:

- Camera noise
- Lighting variations
- Reflections
- Small objects
- Sensor noise

The project uses morphological operations to clean the binary image.

A kernel is created:

```python
kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (5, 5)
)
```

Opening:

```python
threshold_clean = cv2.morphologyEx(
    threshold,
    cv2.MORPH_OPEN,
    kernel
)
```

Closing:

```python
threshold_clean = cv2.morphologyEx(
    threshold_clean,
    cv2.MORPH_CLOSE,
    kernel
)
```

The general processing flow becomes:

```text
Grayscale
   ↓
Threshold
   ↓
Binary Image
   ↓
Morphological Opening
   ↓
Morphological Closing
   ↓
Clean Binary Image
```

---

# 🔎 Contour Detection

Contours are used to identify connected regions in the processed image.

The system uses:

```python
contours, hierarchy = cv2.findContours(
    threshold_clean,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

The system then checks the area of each contour:

```python
area = cv2.contourArea(contour)
```

Very small contours are treated as noise.

The current minimum area is:

```python
MIN_OBJECT_AREA = 1000
```

Therefore:

```text
Contour Area < 1000
        ↓
      Ignore

Contour Area >= 1000
        ↓
      Object
```

---

# 🔢 Object Counting

Every contour that passes the minimum-area filter is counted.

```python
object_count = 0

for contour in contours:

    area = cv2.contourArea(contour)

    if area < MIN_OBJECT_AREA:
        continue

    object_count += 1
```

The result is displayed on the screen:

```text
OBJECT COUNT: 1
```

The system also draws a bounding box around detected objects.

Example:

```text
┌─────────────────────────────┐
│                             │
│     ┌─────────────────┐     │
│     │                 │     │
│     │     OBJECT 1    │     │
│     │                 │     │
│     └─────────────────┘     │
│                             │
└─────────────────────────────┘
```

---

# 📦 Carton Seal Detection

The final objective is to classify the carton as:

```text
SEALED
```

or:

```text
OPEN
```

The current implementation provides the image-processing foundation for this classification.

The intended pipeline is:

```text
Captured Image
      ↓
Grayscale
      ↓
Threshold = 15
      ↓
Morphological Filtering
      ↓
Contour Detection
      ↓
Object/Region Detection
      ↓
Seal Region Analysis
      ↓
┌───────────────┐
│               │
▼               ▼
SEALED          OPEN
```

## Important

The exact `SEALED` / `OPEN` decision must be calibrated using real images from the actual carton.

The threshold value, region of interest, contour area, and classification rule depend on:

- Carton color
- Tape color
- Tape position
- Lighting
- Camera angle
- Camera distance
- Carton dimensions
- Background
- Webcam exposure

Therefore, the current classification should be treated as a prototype until calibrated using representative sealed and open images.

---

# 📊 Live Display

The Raspberry Pi display provides live inspection information.

Example:

```text
┌──────────────────────────────────────────┐
│ AUTO CARTON INSPECTION                   │
│                                          │
│              CARTON IMAGE                │
│                                          │
│ OBJECT COUNT: 1                          │
│ Capture: 18.42 ms                        │
│ Processing: 5.17 ms                      │
│ Threshold: 15                            │
│ White: 64.32%                            │
│                                          │
│ STATUS: SEALED                           │
└──────────────────────────────────────────┘
```

The displayed measurements include:

### Image count

Number of images captured during the current execution.

### Object count

Number of contours that pass the minimum-area filter.

### Capture time

Time required to save the captured image.

Example:

```text
Capture: 18.42 ms
```

### Processing time

Time required for the image-processing operations.

Example:

```text
Processing: 5.17 ms
```

### Threshold

Current grayscale threshold:

```text
Threshold: 15
```

### White percentage

Percentage of white pixels in the thresholded image.

This is useful during calibration.

---

# ⏱️ Processing-Time Measurement

Processing time is measured using:

```python
processing_start = time.perf_counter()

# image processing

processing_end = time.perf_counter()

processing_time_ms = (
    processing_end - processing_start
) * 1000
```

This allows the Raspberry Pi's processing performance to be evaluated.

Example terminal output:

```text
Image: 15 |
Objects: 1 |
Capture: 18.42 ms |
Processing: 5.17 ms |
Status: SEALED
```

---

# ▶️ Running the Project

Clone the repository:

```bash
git clone https://github.com/aatif33/carton_detector.git
```

Enter the project:

```bash
cd carton_detector
```

Run the camera test:

```bash
python3 camera_test.py
```

If the camera works, run the automatic capture/inspection program:

```bash
python3 auto_capture.py
```

or run the latest detector program:

```bash
python3 detector.py
```

depending on which version is being used.

---

# ⚙️ Important Configuration Values

The main parameters can be changed in the Python program.

## Camera

```python
CAMERA_INDEX = 0
```

If the webcam is not detected at camera index `0`, try:

```python
CAMERA_INDEX = 1
```

---

## Automatic Capture Interval

Current example:

```python
CAPTURE_INTERVAL = 2
```

This means the system attempts to capture an image every two seconds.

For one-second intervals:

```python
CAPTURE_INTERVAL = 1
```

For five-second intervals:

```python
CAPTURE_INTERVAL = 5
```

---

## Threshold

Current threshold:

```python
THRESHOLD_VALUE = 15
```

This is intentionally limited to `15` for the current experiment.

---

## Minimum Object Area

Current value:

```python
MIN_OBJECT_AREA = 1000
```

If too many small regions are detected:

```python
MIN_OBJECT_AREA = 2000
```

If the actual object is being ignored, the value may need to be reduced.

---

# 💡 Calibration Procedure

Before using the system for real inspection, calibration should be performed.

## Step 1 — Fix the camera

Keep the webcam at a fixed position.

## Step 2 — Fix the lighting

Use consistent lighting.

Avoid changing the light source between inspections.

## Step 3 — Capture sealed cartons

Capture several images of correctly sealed cartons.

## Step 4 — Capture open cartons

Capture several images of incorrectly sealed/open cartons.

## Step 5 — Compare grayscale images

Observe the grayscale representation.

## Step 6 — Compare threshold images

Observe the thresholded image using:

```text
Threshold = 15
```

## Step 7 — Tune the ROI

Only process the area containing the carton/sealing region.

## Step 8 — Tune contour filtering

Adjust:

```python
MIN_OBJECT_AREA
```

until small noise is removed.

## Step 9 — Establish the classification rule

Determine the visual measurement that reliably separates:

```text
SEALED
```

from:

```text
OPEN
```

---

# 🎥 Recommended Inspection Setup

A controlled setup is strongly recommended.

```text
                 WEBCAM
                    │
                    │
                    ▼
              ┌───────────┐
              │           │
              │  CARTON   │
              │           │
              └───────────┘
                    │
                    ▼
             Inspection Area
```

The carton should be placed in approximately the same position for every inspection.

---

# 🚀 Future Improvements

The current system can be expanded significantly.

## 1. Automatic Box Detection

Instead of capturing every two seconds:

```text
Detect carton
     ↓
Wait until stable
     ↓
Capture once
```

This prevents repeated images of the same carton.

---

## 2. Region of Interest

Instead of processing the entire image:

```text
Full Camera Image
        ↓
     Crop ROI
        ↓
 Seal Inspection Region
```

This improves speed and reduces false detections.

---

## 3. Better Seal Detection

The system can use:

- Edge detection
- Line detection
- Contour analysis
- Tape-region analysis
- Template matching
- Feature extraction

---

## 4. Machine Learning

If classical image processing is not sufficiently reliable, a machine-learning model can be introduced.

Possible architecture:

```text
Webcam
   ↓
Raspberry Pi 5
   ↓
Image Preprocessing
   ↓
ML Model
   ↓
┌──────────┴──────────┐
▼                     ▼
SEALED                OPEN
```

A dataset containing:

```text
sealed/
open/
```

can be created and used to train a classification model.

---

## 5. Raspberry Pi GPIO Output

The system can control physical indicators.

Example:

```text
SEALED
   ↓
GREEN LED

OPEN
   ↓
RED LED
   +
BUZZER
```

---

## 6. Conveyor-Belt Integration

For an industrial-style implementation:

```text
             CONVEYOR
─────────────────────────────────>

       ┌─────────────┐
       │   CARTON    │
       └─────────────┘
              │
              ▼
          WEBCAM
              │
              ▼
       Raspberry Pi 5
              │
       ┌──────┴──────┐
       ▼             ▼
    SEALED          OPEN
       │             │
       ▼             ▼
    Continue       Reject
```

---

# 🛠️ Troubleshooting

## Camera doesn't open

Check:

```bash
ls /dev/video*
```

Then:

```bash
v4l2-ctl --list-devices
```

Try changing:

```python
CAMERA_INDEX = 0
```

to:

```python
CAMERA_INDEX = 1
```

---

## OpenCV is missing

Run:

```bash
sudo apt update
sudo apt install python3-opencv
```

Test:

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

---

## NumPy is missing

Run:

```bash
sudo apt install python3-numpy
```

---

## Too many objects detected

Increase:

```python
MIN_OBJECT_AREA
```

For example:

```python
MIN_OBJECT_AREA = 2000
```

---

## Object is not detected

Decrease:

```python
MIN_OBJECT_AREA
```

For example:

```python
MIN_OBJECT_AREA = 500
```

---

## Threshold image is incorrect

The current threshold is:

```python
THRESHOLD_VALUE = 15
```

Check the threshold window and inspect whether the carton/sealing region is sufficiently separated from the background.

If the project requirement strictly requires a maximum threshold of `15`, keep the value within that limit and improve the result through:

- Better lighting
- Camera positioning
- ROI selection
- Image normalization
- Morphological filtering

---

# 🔐 GitHub Notes

Large automatically generated image collections should generally not be committed to Git.

The `.gitignore` should contain:

```gitignore
captured_images/
dataset/
__pycache__/
*.pyc
.env
```

This keeps generated images and Python cache files out of the repository.

Reference/demo images can be stored separately if they are intentionally part of the documentation.

---

# 🧪 Current Project Status

### Implemented

- [x] Raspberry Pi 5 setup
- [x] USB webcam connection
- [x] Live camera feed
- [x] Automatic image capture
- [x] Image saving
- [x] Capture-time measurement
- [x] Grayscale conversion
- [x] Threshold processing
- [x] Threshold value limited to 15
- [x] Morphological image processing
- [x] Contour detection
- [x] Object counting
- [x] Bounding boxes
- [x] Processing-time measurement
- [x] Live inspection information

### Under Development

- [ ] Reliable sealed/open classification
- [ ] Automatic carton/stability detection
- [ ] ROI-based seal inspection
- [ ] Multiple-condition testing
- [ ] Accuracy measurement
- [ ] False-positive/false-negative analysis
- [ ] LED indication
- [ ] Buzzer indication
- [ ] Conveyor integration

---

# 📈 Performance Metrics

The system records:

```text
Capture Time
Processing Time
Object Count
White Pixel Percentage
Classification Result
```

Example:

```text
Image: 20
Objects: 1
Capture: 18.42 ms
Processing: 5.17 ms
Threshold: 15
White: 64.32%
Status: SEALED
```

These values can be used to evaluate the performance of the Raspberry Pi 5 computer-vision system.

---

# 🧠 How the System Works

The complete processing pipeline is:

```text
┌──────────────────────┐
│      USB Webcam      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Capture Frame      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Grayscale        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Threshold = 15       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Morphological        │
│ Filtering            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Contour Detection    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Object Counting      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Seal Region Analysis │
└──────────┬───────────┘
           │
       ┌───┴────┐
       ▼        ▼
    SEALED      OPEN
```

---

# 📚 Technologies Used

| Technology | Purpose |
|---|---|
| Raspberry Pi 5 | Edge computing |
| Python | Application development |
| OpenCV | Computer vision |
| NumPy | Numerical/image processing |
| USB Webcam | Image acquisition |
| Git | Version control |
| GitHub | Source-code hosting |

---

# 👨‍💻 Project Purpose

This project demonstrates how **edge computer vision** can be used for automated quality inspection.

Instead of sending images to a cloud server, image processing is performed locally on the Raspberry Pi 5.

This provides:

- Local processing
- Reduced network dependency
- Low-latency inspection
- Direct hardware integration
- Real-time feedback

---

# 📄 License

This project is intended for educational and prototype development purposes.

Add an appropriate open-source license if the project is later released publicly for reuse.

---

# 👤 Author

**Aatif**

Raspberry Pi 5  
Computer Vision  
Python  
OpenCV  
Automated Carton Inspection
