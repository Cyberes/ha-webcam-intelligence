import base64
import io
import time

import cv2
from PIL import Image


def fetch_latest_frame(hls_url, capture_duration=2):
    cap = cv2.VideoCapture(hls_url)
    if not cap.isOpened():
        raise ValueError(f"Unable to open HLS stream: {hls_url}")

    frame = None
    start_time = time.time()
    while time.time() - start_time < capture_duration:
        ret, temp_frame = cap.read()
        if ret:
            frame = temp_frame
        else:
            break  # No more frames

    cap.release()

    if frame is None:
        raise ValueError("No frames captured from the HLS stream.")

    return frame


def resize_image(frame) -> Image:
    # Convert OpenCV BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    resized_image = pil_image.resize((1092, 1092), Image.Resampling.LANCZOS)
    return resized_image


def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format='PNG')
    img_bytes = buffered.getvalue()
    base64_bytes = base64.standard_b64encode(img_bytes)
    base64_str = base64_bytes.decode("utf-8")
    return base64_str
