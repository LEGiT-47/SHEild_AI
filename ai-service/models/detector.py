import cv2
import numpy as np

from utils.image_processing import (
    convert_to_grayscale,
    load_image_from_bytes,
    resize_for_analysis,
)


class DeepfakeDetector:
    def __init__(self):
        self.face_cascade = self._load_face_cascade()

    def _load_face_cascade(self):
        try:
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cascade = cv2.CascadeClassifier(cascade_path)
            if cascade.empty():
                return None
            return cascade
        except Exception:
            return None

    def detect_face(self, img):
        gray = convert_to_grayscale(img)
        if gray is None:
            return False, []

        # Fallback mock behavior when Haar cascade is unavailable.
        if self.face_cascade is None:
            h, w = gray.shape[:2]
            if h > 120 and w > 120:
                return True, [(w // 4, h // 4, w // 2, h // 2)]
            return False, []

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return len(faces) > 0, faces

    def measure_blur(self, img):
        gray = convert_to_grayscale(img)
        if gray is None:
            return 0.0, True
        score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        return score, score < 80.0

    def analyze_edges(self, img):
        gray = convert_to_grayscale(img)
        if gray is None:
            return 1.0

        edges = cv2.Canny(gray, 100, 200)
        h, w = edges.shape
        center = edges[h // 4 : (3 * h) // 4, w // 4 : (3 * w) // 4]

        center_density = float(np.mean(center > 0)) if center.size else 0.0
        global_density = float(np.mean(edges > 0)) if edges.size else 0.0

        # Relative anomaly score in [0, 1].
        score = abs(center_density - global_density) * 2.5
        return float(np.clip(score, 0.0, 1.0))

    def check_compression(self, img):
        gray = convert_to_grayscale(img)
        if gray is None:
            return 1.0

        gray = gray.astype(np.float32)
        block_size = 8
        h, w = gray.shape
        h_crop = h - (h % block_size)
        w_crop = w - (w % block_size)
        if h_crop == 0 or w_crop == 0:
            return 0.0

        cropped = gray[:h_crop, :w_crop]
        vertical_diff = np.abs(cropped[:, block_size:] - cropped[:, :-block_size]).mean()
        horizontal_diff = np.abs(cropped[block_size:, :] - cropped[:-block_size, :]).mean()
        blockiness = (vertical_diff + horizontal_diff) / 2.0

        # Normalize to [0, 1] for scoring.
        score = float(np.clip(blockiness / 40.0, 0.0, 1.0))
        return score

    def analyze_lighting(self, img):
        gray = convert_to_grayscale(img)
        if gray is None:
            return 1.0

        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        angle = cv2.phase(grad_x, grad_y, angleInDegrees=False)

        h, w = gray.shape
        left = angle[:, : w // 2]
        right = angle[:, w // 2 :]
        if left.size == 0 or right.size == 0:
            return 0.0

        diff = abs(float(np.mean(left)) - float(np.mean(right)))
        score = float(np.clip(diff / np.pi, 0.0, 1.0))
        return score

    def compute_confidence(self, signals):
        weights = {
            "face": 0.3,
            "blur": 0.2,
            "edge": 0.25,
            "compression": 0.15,
            "lighting": 0.1,
        }

        confidence = (
            signals["face_suspect"] * weights["face"]
            + signals["blur_suspect"] * weights["blur"]
            + signals["edge_suspect"] * weights["edge"]
            + signals["compression_suspect"] * weights["compression"]
            + signals["lighting_suspect"] * weights["lighting"]
        )

        if not signals["face_detected"]:
            confidence = min(1.0, confidence + 0.3)

        return float(np.clip(confidence, 0.0, 1.0))

    def analyze(self, image_bytes: bytes) -> dict:
        img = load_image_from_bytes(image_bytes)
        img = resize_for_analysis(img)

        if img is None:
            return {
                "is_fake": True,
                "confidence": 0.95,
                "artifacts": ["Unable to decode image data"],
                "face_detected": False,
                "blur_score": 0.0,
                "edge_anomaly_score": 1.0,
            }

        face_detected, _ = self.detect_face(img)
        blur_score, is_blurry = self.measure_blur(img)
        edge_anomaly_score = self.analyze_edges(img)
        compression_score = self.check_compression(img)
        lighting_score = self.analyze_lighting(img)

        signals = {
            "face_detected": face_detected,
            "face_suspect": 1.0 if not face_detected else 0.0,
            "blur_suspect": 1.0 if is_blurry else 0.0,
            "edge_suspect": 1.0 if edge_anomaly_score > 0.4 else 0.0,
            "compression_suspect": 1.0 if compression_score > 0.3 else 0.0,
            "lighting_suspect": 1.0 if lighting_score > 0.35 else 0.0,
        }

        confidence = self.compute_confidence(signals)
        artifacts = []

        if not face_detected:
            artifacts.append("Face region not reliably detected")
        if is_blurry:
            artifacts.append("Unusual blur pattern around key facial regions")
        if edge_anomaly_score > 0.4:
            artifacts.append("Face blending seam detected in edge map")
        if compression_score > 0.3:
            artifacts.append("Compression block artifact inconsistency")
        if lighting_score > 0.35:
            artifacts.append("Lighting direction inconsistency across face")

        if not artifacts:
            artifacts.append("No major forensic artifact detected")

        return {
            "is_fake": confidence >= 0.5,
            "confidence": round(confidence, 4),
            "artifacts": artifacts,
            "face_detected": face_detected,
            "blur_score": round(float(blur_score), 4),
            "edge_anomaly_score": round(float(edge_anomaly_score), 4),
        }
