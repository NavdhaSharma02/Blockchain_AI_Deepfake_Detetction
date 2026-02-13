"""
AI Models Package
Separate models for audio, image, and video deepfake detection
"""

from .image_model import ImageDeepfakeModel
from .video_model import VideoDeepfakeModel
from .audio_model import AudioDeepfakeModel

__all__ = [
    'ImageDeepfakeModel',
    'VideoDeepfakeModel',
    'AudioDeepfakeModel'
]
