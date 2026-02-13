"""
Audio Deepfake Detection Model
Spectrogram-based CNN for detecting audio deepfakes
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any
import warnings


class AudioDeepfakeModel(nn.Module):
    """
    CNN-based deepfake classifier for audio
    Uses ResNet-inspired architecture on mel-spectrograms
    """
    def __init__(self):
        super().__init__()
        # Using ResNet18 architecture adapted for spectrograms
        from torchvision.models import resnet18
        
        self.model = resnet18(pretrained=True)
        
        # Modify first layer to accept 1-channel spectrogram input
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        
        # Modify final layer for binary classification
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 2)  # Binary: Real / Fake

    def forward(self, x):
        return self.model(x)


class AudioDeepfakeDetector:
    """
    Audio deepfake detector with spectrogram preprocessing
    Analyzes frequency and time domains
    """
    
    def __init__(self, model_path: str = None, confidence_threshold: float = 0.7, device: str = None):
        """
        Initialize audio deepfake detector
        
        Args:
            model_path: Path to pretrained model weights (optional)
            confidence_threshold: Minimum confidence for classification (0.0-1.0)
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        self.confidence_threshold = confidence_threshold
        
        # Load model
        self.model = AudioDeepfakeModel().to(self.device)
        
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"✔ Loaded trained audio model from {model_path}")
            except Exception as e:
                print(f"⚠ Could not load custom audio model: {e}")
                print("  Using pretrained base model")
        
        self.model.eval()
        
        # Try to import audio libraries
        try:
            import librosa
            import soundfile as sf
            self.librosa = librosa
            self.soundfile = sf
            self.audio_available = True
        except ImportError as e:
            warnings.warn(f"Audio libraries not available: {e}. Install librosa and soundfile for audio processing.")
            self.audio_available = False
    
    def audio_to_spectrogram(self, audio_path: str, n_mels: int = 128, duration: float = 5.0):
        """
        Convert audio file to mel-spectrogram
        
        Args:
            audio_path: Path to audio file
            n_mels: Number of mel bands
            duration: Duration to analyze (seconds)
            
        Returns:
            Spectrogram tensor ready for model
        """
        if not self.audio_available:
            raise ImportError("Audio libraries (librosa, soundfile) not installed")
        
        # Load audio
        y, sr = self.librosa.load(audio_path, duration=duration, sr=None)
        
        # Generate mel-spectrogram
        mel_spec = self.librosa.feature.melspectrogram(
            y=y, 
            sr=sr, 
            n_mels=n_mels,
            fmax=sr/2
        )
        
        # Convert to log scale (dB)
        mel_spec_db = self.librosa.power_to_db(mel_spec, ref=np.max)
        
        # Normalize to [0, 1]
        mel_spec_norm = (mel_spec_db - mel_spec_db.min()) / (mel_spec_db.max() - mel_spec_db.min() + 1e-8)
        
        # Resize to model input size (224x224)
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224))
        ])
        
        spec_tensor = transform(mel_spec_norm.astype(np.float32))
        
        return spec_tensor.unsqueeze(0).to(self.device), sr, len(y) / sr
    
    def detect(self, audio_path: str) -> Dict[str, Any]:
        """
        Detect if audio is a deepfake
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary with detection results
        """
        if not self.audio_available:
            return {
                "classification": "Error",
                "error": "Audio libraries (librosa, soundfile) not installed. Run: pip install librosa soundfile",
                "model_type": "Audio"
            }
        
        try:
            # Convert to spectrogram
            spec_tensor, sample_rate, audio_duration = self.audio_to_spectrogram(audio_path)
            
            # Run inference
            with torch.no_grad():
                logits = self.model(spec_tensor)
                probs = torch.softmax(logits, dim=1)
                real_prob = probs[0][0].item()
                fake_prob = probs[0][1].item()
            
            # Classify based on threshold
            is_fake = fake_prob > self.confidence_threshold
            is_real = real_prob > self.confidence_threshold
            
            if is_fake:
                classification = "Fake"
                confidence = fake_prob
            elif is_real:
                classification = "Real"
                confidence = real_prob
            else:
                classification = "Unverifiable"
                confidence = max(real_prob, fake_prob)
            
            return {
                "classification": classification,
                "confidence_score": round(confidence * 100, 2),
                "fake_probability": round(fake_prob * 100, 2),
                "real_probability": round(real_prob * 100, 2),
                "is_deepfake": is_fake,
                "model_type": "Audio",
                "details": {
                    "model": "ResNet18",
                    "architecture": "CNN on Mel-Spectrogram",
                    "analysis_type": "Frequency + Time",
                    "sample_rate": sample_rate,
                    "duration_seconds": round(audio_duration, 2),
                    "spectrogram_shape": "224x224",
                    "mel_bands": 128,
                    "threshold": self.confidence_threshold,
                    "device": str(self.device)
                }
            }
        
        except Exception as e:
            return {
                "classification": "Error",
                "error": str(e),
                "model_type": "Audio"
            }
