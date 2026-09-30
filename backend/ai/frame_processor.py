"""
OpenCV Frame Processor — Prepares video frames for AI inference.
Provides functions for resizing, color normalization, and simulated edge-like processing.
"""

import cv2
import numpy as np
from typing import Tuple

class FrameProcessor:
    def __init__(self, target_resolution: Tuple[int, int] = (640, 640)):
        self.target_resolution = target_resolution

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess a frame for YOLO/ONNX inference:
        1. Resize
        2. Convert BGR to RGB
        3. Normalize
        """
        # Resize frame
        resized = cv2.resize(frame, self.target_resolution, interpolation=cv2.INTER_LINEAR)
        
        # OpenCV loads in BGR, AI usually needs RGB
        rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        normalized = rgb_frame.astype(np.float32) / 255.0
        
        # Transpose to Channel, Height, Width (CHW) format often used by AI
        chw_frame = np.transpose(normalized, (2, 0, 1))
        
        # Add batch dimension
        batch_frame = np.expand_dims(chw_frame, axis=0)
        return batch_frame

    def extract_frames_from_video(self, video_path: str, max_frames: int = 100):
        """
        Simulates offline video file analysis for the 'Track Innovation' goal.
        """
        cap = cv2.VideoCapture(video_path)
        frames = []
        count = 0
        
        while cap.isOpened() and count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed = self.process_frame(frame)
            frames.append(processed)
            count += 1
            
        cap.release()
        return frames
