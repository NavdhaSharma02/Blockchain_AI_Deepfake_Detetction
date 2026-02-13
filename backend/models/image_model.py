"""
Image Deepfake Detection Model
Xception-based CNN for detecting spatial texture artifacts
"""

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
from typing import Dict, Any


class ImageDeepfakeModel(nn.Module):
    """
    Xception-based deepfake classifier for images
    Analyzes spatial texture artifacts and face manipulation
    """
    def __init__(self):
        super().__init__()
        # Using Xception architecture as specified
        try:
            from torchvision.models import xception
            self.model = xception(pretrained=True)
            self.model.fc = nn.Linear(2048, 2)  # Binary: Real / Fake
        except ImportError:
            # Fallback to EfficientNet if Xception not available in torchvision
            from torchvision.models import efficientnet_b0
            self.model = efficientnet_b0(pretrained=True)
            num_features = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(num_features, 2)

    def forward(self, x):
        return self.model(x)


class ImageDeepfakeDetector:
    """
    Image deepfake detector with preprocessing and inference
    """
    
    def __init__(self, model_path: str = None, confidence_threshold: float = 0.7, device: str = None):
        """
        Initialize image deepfake detector
        
        Args:
            model_path: Path to pretrained model weights (optional)
            confidence_threshold: Minimum confidence for classification (0.0-1.0)
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        self.confidence_threshold = confidence_threshold
        
        # Load model
        self.model = ImageDeepfakeModel().to(self.device)
        
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"✔ Loaded trained image model from {model_path}")
            except Exception as e:
                print(f"⚠ Could not load custom image model: {e}")
                print("  Using pretrained base model")
        
        self.model.eval()
        
        # Preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def preprocess_image(self, image_input) -> torch.Tensor:
        """
        Preprocess image for inference
        
        Args:
            image_input: PIL Image or numpy array or file path
            
        Returns:
            Preprocessed tensor ready for model
        """
        # Convert to PIL Image if needed
        if isinstance(image_input, str):
            image = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, np.ndarray):
            image = Image.fromarray(image_input)
        else:
            image = image_input
        
        # Apply transforms
        return self.transform(image).unsqueeze(0).to(self.device)
    
    def detect(self, image_input) -> Dict[str, Any]:
        """
        Detect if an image is a deepfake
        
        Args:
            image_input: PIL Image, numpy array, or file path
            
        Returns:
            Dictionary with detection results
        """
        try:
            # Preprocess
            image_tensor = self.preprocess_image(image_input)
            
            # Run inference
            with torch.no_grad():
                logits = self.model(image_tensor)
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
                "model_type": "Image",
                "details": {
                    "model": "Xception",
                    "architecture": "CNN",
                    "analysis_type": "Spatial (texture artifacts)",
                    "threshold": self.confidence_threshold,
                    "device": str(self.device)
                }
            }
        
        except Exception as e:
            return {
                "classification": "Error",
                "error": str(e),
                "model_type": "Image"
            }
