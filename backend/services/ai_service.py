"""
Multi-Modal Deepfake Detection Service
Supports image, video, and audio deepfake detection
"""

import os
from typing import Dict, Any
from models.image_model import ImageDeepfakeDetector
from models.video_model import VideoDeepfakeDetector
from models.audio_model import AudioDeepfakeDetector


class MultiModalDeepfakeDetector:
    """
    Multi-modal deepfake detector supporting image, video, and audio
    Each modality uses a specialized model:
    - Image: Xception CNN for spatial texture artifacts
    - Video: Xception CNN + temporal aggregation
    - Audio: Mel-spectrogram + ResNet18 CNN
    """
    
    def __init__(self, 
                 image_model_path: str = None,
                 video_model_path: str = None,
                 audio_model_path: str = None,
                 confidence_threshold: float = 0.7):
        """
        Initialize multi-modal deepfake detector
        
        Args:
            image_model_path: Path to image model weights (optional)
            video_model_path: Path to video model weights (optional)
            audio_model_path: Path to audio model weights (optional)
            confidence_threshold: Minimum confidence for classification (0.0-1.0)
        """
        print("🚀 Initializing Multi-Modal Deepfake Detector...")
        
        # Initialize image detector
        print("  📸 Loading Image Model...")
        self.image_detector = ImageDeepfakeDetector(
            model_path=image_model_path,
            confidence_threshold=confidence_threshold
        )
        
        # Initialize video detector
        print("  🎥 Loading Video Model...")
        self.video_detector = VideoDeepfakeDetector(
            model_path=video_model_path,
            confidence_threshold=confidence_threshold
        )
        
        # Initialize audio detector
        print("  🔊 Loading Audio Model...")
        self.audio_detector = AudioDeepfakeDetector(
            model_path=audio_model_path,
            confidence_threshold=confidence_threshold
        )
        
        self.confidence_threshold = confidence_threshold
        print("✅ Multi-Modal Detector Ready!")
    
    def detect_image(self, image_path: str) -> Dict[str, Any]:
        """
        Detect deepfakes in images
        
        Args:
            image_path: Path to image file
            
        Returns:
            Detection results with image-specific metadata
        """
        return self.image_detector.detect(image_path)
    
    def detect_video(self, video_path: str, max_frames: int = 30) -> Dict[str, Any]:
        """
        Detect deepfakes in videos
        
        Args:
            video_path: Path to video file
            max_frames: Maximum frames to analyze
            
        Returns:
            Detection results with video-specific metadata
        """
        return self.video_detector.detect(video_path, max_frames)
    
    def detect_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Detect deepfakes in audio
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Detection results with audio-specific metadata
        """
        return self.audio_detector.detect(audio_path)
    
    def detect(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Auto-route detection based on file type
        
        Args:
            file_path: Path to the media file
            file_type: Type of file ('image', 'video', or 'audio')
            
        Returns:
            Detection results
        """
        file_type_lower = file_type.lower()
        
        # Image types
        if file_type_lower in ['image', 'jpg', 'jpeg', 'png', 'bmp', 'gif']:
            return self.detect_image(file_path)
        
        # Video types
        elif file_type_lower in ['video', 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']:
            return self.detect_video(file_path)
        
        # Audio types
        elif file_type_lower in ['audio', 'mp3', 'wav', 'm4a', 'flac', 'ogg', 'aac']:
            return self.detect_audio(file_path)
        
        else:
            return {
                "classification": "Error",
                "error": f"Unsupported file type: {file_type}",
                "model_type": "Unknown"
            }


# Backward compatibility - alias to old name
DeepfakeDetector = MultiModalDeepfakeDetector
