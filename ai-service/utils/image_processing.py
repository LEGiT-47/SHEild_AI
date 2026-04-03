import cv2
import numpy as np


def load_image_from_bytes(image_bytes: bytes):
    """Decode raw image bytes into an OpenCV BGR image."""
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def resize_for_analysis(img, max_dim: int = 1024):
    """Resize large images while preserving aspect ratio for stable scoring."""
    if img is None:
        return img

    h, w = img.shape[:2]
    largest = max(h, w)
    if largest <= max_dim:
        return img

    scale = max_dim / float(largest)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(img):
    """Convert BGR image to grayscale."""
    if img is None:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
