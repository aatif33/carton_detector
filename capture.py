import cv2
import os
import time

# ==========================================
# SETTINGS
# ==========================================

CAMERA_INDEX = 0

CAPTURE_INTERVAL = 2
THRESHOLD_VALUE = 15

# Minimum contour area to be considered an object
MIN_OBJECT_AREA = 1000

SAVE_FOLDER = "captured_images"

# ==========================================
# CREATE FOLDER
# ==========================================

os.makedirs(SAVE_FOLDER, exist_ok=True)

# ==========================================
# CAMERA
# ==========================================

camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():
    print("ERROR: Camera could not be opened")
    exit()

print("Camera started")
print("Automatic inspection started")
print("Press Q to quit")

image_count = 0
last_capture_time = 0

capture_time_ms = 0
processing_time_ms = 0

object_count = 0
status = "WAITING"

white_percentage = 0


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read frame")
        break

    # Resize
    frame = cv2.resize(frame, (800, 600))

    current_time = time.time()

    # ======================================
    # AUTOMATIC CAPTURE
    # ======================================

    if current_time - last_capture_time >= CAPTURE_INTERVAL:

        image_count += 1

        filename = os.path.join(
            SAVE_FOLDER,
            f"box_{image_count:04d}.jpg"
        )

        # ==================================
        # CAPTURE TIME
        # ==================================

        capture_start = time.perf_counter()

        success = cv2.imwrite(
            filename,
            frame
        )

        capture_end = time.perf_counter()

        capture_time_ms = (
            capture_end - capture_start
        ) * 1000


        # ==================================
        # IMAGE PROCESSING
        # ==================================

        processing_start = time.perf_counter()

        # ----------------------------------
        # GRAYSCALE
        # ----------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------
        # THRESHOLD
        # ----------------------------------

        _, threshold = cv2.threshold(
            gray,
            THRESHOLD_VALUE,
            255,
            cv2.THRESH_BINARY
        )

        # ==================================
        # MORPHOLOGICAL CLEANING
        # ==================================

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (5, 5)
        )

        threshold_clean = cv2.morphologyEx(
            threshold,
            cv2.MORPH_OPEN,
            kernel
        )

        threshold_clean = cv2.morphologyEx(
            threshold_clean,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ==================================
        # FIND OBJECTS
        # ==================================

        contours, hierarchy = cv2.findContours(
            threshold_clean,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        object_count = 0

        # ==================================
        # DRAW OBJECTS
        # ==================================

        for contour in contours:

            area = cv2.contourArea(contour)

            # Ignore tiny noise
            if area < MIN_OBJECT_AREA:
                continue

            object_count += 1

            x, y, w, h = cv2.boundingRect(contour)

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            # Object number
            cv2.putText(
                frame,
                f"Object {object_count}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        # ==================================
        # WHITE PIXEL PERCENTAGE
        # ==================================

        white_pixels = cv2.countNonZero(
            threshold_clean
        )

        total_pixels = (
            threshold_clean.shape[0]
            * threshold_clean.shape[1]
        )

        white_percentage = (
            white_pixels / total_pixels
        ) * 100

        # ==================================
        # SEALED / OPEN
        # ==================================

        # Temporary logic.
        # We will calibrate this using
        # your actual box images.

        if object_count >= 1:

            status = "SEALED"

        else:

            status = "OPEN"

        # ==================================
        # PROCESSING TIME
        # ==================================

        processing_end = time.perf_counter()

        processing_time_ms = (
            processing_end
            - processing_start
        ) * 1000

        # ==================================
        # TERMINAL OUTPUT
        # ==================================

        print(
            f"Image: {image_count} | "
            f"Objects: {object_count} | "
            f"Capture: {capture_time_ms:.2f} ms | "
            f"Processing: {processing_time_ms:.2f} ms | "
            f"Status: {status}"
        )

        last_capture_time = current_time


    # ======================================
    # DISPLAY
    # ======================================

    cv2.putText(
        frame,
        "AUTO CARTON INSPECTION",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Images: {image_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"OBJECT COUNT: {object_count}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Capture: {capture_time_ms:.2f} ms",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Processing: {processing_time_ms:.2f} ms",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Threshold: {THRESHOLD_VALUE}",
        (20, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"White: {white_percentage:.2f}%",
        (20, 280),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # STATUS
    cv2.putText(
        frame,
        f"STATUS: {status}",
        (20, 335),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    # ======================================
    # WINDOWS
    # ======================================

    cv2.imshow(
        "Cart Box Inspection",
        frame
    )

    cv2.imshow(
        "Grayscale",
        gray
    )

    cv2.imshow(
        "Threshold - 15",
        threshold_clean
    )

    # ======================================
    # QUIT
    # ======================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ==========================================
# CLEANUP
# ==========================================

camera.release()

cv2.destroyAllWindows()

print("Inspection stopped")