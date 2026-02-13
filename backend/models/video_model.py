"""
Video Deepfake Detection Model
Frame-based Xception CNN with temporal aggregation
"""

import cv2
import torch
import numpy as np
from typing import Dict, Any
from .image_model import ImageDeepfakeModel, ImageDeepfakeDetector


class VideoDeepfakeModel(ImageDeepfakeModel):
    """
    Video deepfake classifier using same Xception architecture as images
    Inherits from ImageDeepfakeModel for frame-level analysis
    """
    pass


class VideoDeepfakeDetector:
    """
    Video deepfake detector with temporal modeling
    Analyzes frames using CNN and aggregates results across time
    """
    
    def __init__(self, model_path: str = None, confidence_threshold: float = 0.7, device: str = None):
        """
        Initialize video deepfake detector
        
        Args:
            model_path: Path to pretrained model weights (optional)
            confidence_threshold: Minimum confidence for classification (0.0-1.0)
            device: Device to run model on ('cuda' or 'cpu')
        """
        # Use the image detector for frame-level analysis
        self.image_detector = ImageDeepfakeDetector(
            model_path=model_path,
            confidence_threshold=confidence_threshold,
            device=device
        )
        self.confidence_threshold = confidence_threshold
        self.device = self.image_detector.device
    
    def extract_frames(self, video_path: str, max_frames: int = 30):
        """
        Extract frames from video for analysis
        
        Args:
            video_path: Path to video file
            max_frames: Maximum number of frames to extract
            
        Yields:
            Frame images as numpy arrays
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, total_frames // max_frames)
        
        frame_idx = 0
        frames_extracted = 0
        
        while cap.isOpened() and frames_extracted < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames at intervals
            if frame_idx % interval == 0:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                yield frame_rgb
                frames_extracted += 1
            
            frame_idx += 1
        
        cap.release()
    
    def detect(self, video_path: str, max_frames: int = 30) -> Dict[str, Any]:
        """
        Detect if a video is a deepfake
        Uses frame-level CNN analysis with temporal aggregation
        
        Args:
            video_path: Path to the video file
            max_frames: Maximum number of frames to analyze
            
        Returns:
            Dictionary with detection results (aggregated across frames)
        """
        try:
            # Get video metadata
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            cap.release()
            
            # Analyze frames
            frame_probs = []  # Store (real_prob, fake_prob) tuples
            
            for frame in self.extract_frames(video_path, max_frames):
                result = self.image_detector.detect(frame)
                
                if "error" not in result:
                    frame_probs.append((
                        result["real_probability"] / 100.0,
                        result["fake_probability"] / 100.0
                    ))
            
            # Check if any frames were analyzed
            if len(frame_probs) == 0:
                return {
                    "classification": "Error",
                    "error": "No frames could be analyzed from video",
                    "model_type": "Video",
                    "details": {
                        "frames_analyzed": 0,
                        "total_frames": total_frames,
                        "duration": round(duration, 2),
                        "fps": round(fps, 2)
                    }
                }
            
            # Temporal aggregation: mean pooling across frames
            avg_real_prob = float(np.mean([p[0] for p in frame_probs]))
            avg_fake_prob = float(np.mean([p[1] for p in frame_probs]))
            
            # Classify based on threshold
            is_fake = avg_fake_prob > self.confidence_threshold
            is_real = avg_real_prob > self.confidence_threshold
            
            if is_fake:
                classification = "Fake"
                confidence = avg_fake_prob
            elif is_real:
                classification = "Real"
                confidence = avg_real_prob
            else:
                classification = "Unverifiable"
                confidence = max(avg_real_prob, avg_fake_prob)
            
            return {
                "classification": classification,
                "confidence_score": round(confidence * 100, 2),
                "fake_probability": round(avg_fake_prob * 100, 2),
                "real_probability": round(avg_real_prob * 100, 2),
                "is_deepfake": is_fake,
                "model_type": "Video",
                "details": {
                    "model": "Xception",
                    "architecture": "CNN + Temporal Aggregation",
                    "analysis_type": "Spatial + Temporal",
                    "frames_analyzed": len(frame_probs),
                    "total_frames": total_frames,
                    "duration_seconds": round(duration, 2),
                    "fps": round(fps, 2),
                    "threshold": self.confidence_threshold,
                    "device": str(self.device)
                }
            }
        
        except Exception as e:
            return {
                "classification": "Error",
                "error": str(e),
                "model_type": "Video"
            }
