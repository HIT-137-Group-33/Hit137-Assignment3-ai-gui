from models.base_model import AIModel, ModelCacheMixin

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class TextGeneratorModel(AIModel, ModelCacheMixin):
    """
    Text Generation model demonstrating Multiple Inheritance
    Using Microsoft's DialoGPT model for conversation
    """
    
    def __init__(self):
        # Multiple Inheritance
        AIModel.__init__(self,
                        "DialoGPT Medium",
                        "Text Generation", 
                        "Generates conversational text responses using microsoft/DialoGPT-medium")
        ModelCacheMixin.__init__(self)
        self.chat_pipeline = None
        self.history = []
    
    def load_model(self):
        """Method Overriding: Specific implementation for text generation"""
        if not TRANSFORMERS_AVAILABLE:
            return "Error: transformers library not available."
            
        if not self._is_loaded:
            try:
                # Using pipeline as shown in Hugging Face instructions
                self.chat_pipeline = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-medium",
                    tokenizer="microsoft/DialoGPT-medium"
                )
                self._is_loaded = True
                return "Text Generation model loaded successfully!"
            except Exception as e:
                return f"Error loading model: {str(e)}"
        return "Model already loaded"
    
    def process_input(self, user_input):
        """Polymorphism: Different implementation for text generation"""
        if not self._is_loaded:
            return "Please load the model first"
        
        # Check cache first
        cached = self.get_cached_result(user_input)
        if cached:
            return cached
        
        try:
            # Generate response using the model
            response = self.chat_pipeline(
                user_input,
                max_length=1000,
                pad_token_id=self.chat_pipeline.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8
            )[0]['generated_text']
            
            # Extract only the new response (remove the input)
            if user_input in response:
                bot_response = response[len(user_input):].strip()
            else:
                bot_response = response.strip()
            
            self.cache_result(user_input, bot_response)
            return bot_response
            
        except Exception as e:
            return f"Error generating text: {str(e)}"