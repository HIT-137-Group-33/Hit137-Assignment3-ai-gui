from models.base_model import AIModel, ModelCacheMixin
from transformers import pipeline

class TextGeneratorModel(AIModel, ModelCacheMixin):
    """
    Text Generation model with real Hugging Face integration
    Demonstrating Multiple Inheritance and Method Overriding
    """
    
    def __init__(self):
        # Multiple Inheritance
        AIModel.__init__(self,
                        "DialoGPT Medium",
                        "Text Generation", 
                        "Generates conversational text using microsoft/DialoGPT-medium")
        ModelCacheMixin.__init__(self)
        self.pipeline = None
    
    def load_model(self):
        """Method Overriding: Real model loading with error handling"""
        try:
            # Real Hugging Face pipeline
            self.pipeline = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                tokenizer="microsoft/DialoGPT-medium"
            )
            self._is_loaded = True
            return "Text Generation model loaded successfully from Hugging Face!"
        except Exception as e:
            return f"Error loading model: {str(e)}\n\nPlease install: pip install transformers torch"
    
    def process_input(self, user_input):
        """Polymorphism: Real text generation"""
        if not self._is_loaded:
            return "Please load the model first"
        
        # Check cache first
        cached = self.get_cached_result(user_input)
        if cached:
            return cached
        
        try:
            # Real text generation
            response = self.pipeline(
                user_input,
                max_length=150,
                num_return_sequences=1,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                temperature=0.7
            )
            
            generated_text = response[0]['generated_text']
            # Remove the input from response to get only the new text
            if user_input in generated_text:
                bot_response = generated_text[len(user_input):].strip()
            else:
                bot_response = generated_text.strip()
            
            result = f"🤖 AI Response:\n\n{bot_response}\n\n(Generated using DialoGPT-medium from Hugging Face)"
            
            self.cache_result(user_input, result)
            return result
            
        except Exception as e:
            return f"Error generating text: {str(e)}"
