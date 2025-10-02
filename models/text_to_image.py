import tkinter as tk
from PIL import Image, ImageTk
from models.base_model import AIModel, ModelCacheMixin

try:
    from diffusers import StableDiffusionPipeline
    import torch
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

class TextToImageModel(AIModel, ModelCacheMixin):
    """
    Text-to-Image model demonstrating Multiple Inheritance
    Inherits from both AIModel and ModelCacheMixin
    """
    
    def __init__(self):
        # Multiple Inheritance: Calling both parent constructors
        AIModel.__init__(self, 
                        "Stable Diffusion v1.5", 
                        "Text-to-Image", 
                        "Generates images from text descriptions using runwayml/stable-diffusion-v1-5")
        ModelCacheMixin.__init__(self)
        self.pipeline = None
    
    def load_model(self):
        """Method Overriding: Specific implementation for text-to-image"""
        if not DIFFUSERS_AVAILABLE:
            return "Error: diffusers library not available. Please install with: pip install diffusers"
            
        if not self._is_loaded:
            try:
                # Using pipeline as shown in Hugging Face instructions
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                self.pipeline = self.pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
                self._is_loaded = True
                return "Text-to-Image model loaded successfully!"
            except Exception as e:
                return f"Error loading model: {str(e)}"
        return "Model already loaded"
    
    def process_input(self, text_prompt):
        """Polymorphism: Different implementation for text input"""
        if not self._is_loaded:
            return "Please load the model first"
        
        # Check cache first
        cached = self.get_cached_result(text_prompt)
        if cached:
            return cached
        
        try:
            # Generate image
            with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
                image = self.pipeline(text_prompt, num_inference_steps=20).images[0]
            
            # Cache the result
            self.cache_result(text_prompt, image)
            return image
        except Exception as e:
            return f"Error generating image: {str(e)}"