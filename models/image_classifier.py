from models.base_model import AIModel, ModelCacheMixin
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch

class ImageClassifierModel(AIModel, ModelCacheMixin):
    """Image Classification model demonstrating Multiple Inheritance"""
    
    def __init__(self):
        # Multiple Inheritance
        AIModel.__init__(self,
                        "ViT Base Patch16-224",
                        "Image Classification",
                        "Classifies images into various categories")
        ModelCacheMixin.__init__(self)
        self.processor = None
        self.model = None
    
    def load_model(self):
        """Method Overriding: Specific implementation for image classification"""
        if not self._is_loaded:
            try:
                self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
                self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
                self._is_loaded = True
                return "Model loaded successfully"
            except Exception as e:
                return f"Error loading model: {str(e)}"
        return "Model already loaded"
    
    def process_input(self, image_path):
        """Polymorphism: Different implementation for image input"""
        if not self._is_loaded:
            return "Please load the model first"
        
        # Check cache first
        cached = self.get_cached_result(image_path)
        if cached:
            return cached
        
        try:
            image = Image.open(image_path)
            inputs = self.processor(images=image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            top_prob, top_class = torch.topk(probabilities, 5)
            
            results = []
            for i in range(5):
                class_name = self.model.config.id2label[top_class[0][i].item()]
                prob = top_prob[0][i].item()
                results.append(f"{class_name}: {prob:.4f}")
            
            result_text = "\n".join(results)
            self.cache_result(image_path, result_text)
            return result_text
            
        except Exception as e:
            return f"Error classifying image: {str(e)}"