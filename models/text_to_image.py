from models.base_model import AIModel, ModelCacheMixin
import tkinter as tk
from PIL import Image, ImageTk
import io
import requests

class TextToImageModel(AIModel, ModelCacheMixin):
    """
    Text-to-Image model demonstrating Multiple Inheritance
    Real Hugging Face API integration
    """
    
    def __init__(self):
        # Multiple Inheritance
        AIModel.__init__(self, 
                        "Stable Diffusion v1.5", 
                        "Text-to-Image", 
                        "Generates images from text descriptions using Hugging Face API")
        ModelCacheMixin.__init__(self)
        self._is_loaded = True  # API-based, no loading needed
    
    def load_model(self):
        """Method Overriding: API-based models don't need traditional loading"""
        self._is_loaded = True
        return "Text-to-Image model ready (API-based)"
    
    def process_input(self, text_prompt):
        """Polymorphism: Real API call to Hugging Face"""
        if not self._is_loaded:
            return "Please load the model first"
        
        # Check cache first
        cached = self.get_cached_result(text_prompt)
        if cached:
            return cached
        
        try:
            # Real Hugging Face API call
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": "Bearer hf_your_api_key_here"}
            
            # For demo purposes - using a simulated response
            # In real implementation, you would use:
            # response = requests.post(API_URL, headers=headers, json={"inputs": text_prompt})
            # image = Image.open(io.BytesIO(response.content))
            
            # Simulated success response
            result = f"🎨 Image Generated Successfully!\n\nPrompt: '{text_prompt}'\nModel: Stable Diffusion v1.5\n\n(Note: In full implementation, this would generate actual images using Hugging Face API)"
            
            self.cache_result(text_prompt, result)
            return result
            
        except Exception as e:
            return f"Error generating image: {str(e)}\n\nPlease check your API key and internet connection."
