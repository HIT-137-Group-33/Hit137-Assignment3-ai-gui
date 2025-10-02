from abc import ABC, abstractmethod
import logging
from functools import wraps

def handle_model_errors(func):
    """Decorator for error handling in model methods"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return f"Error: {str(e)}"
    return wrapper

class AIModel(ABC):
    """
    Abstract base class for AI models demonstrating OOP concepts
    Encapsulation: Private attributes with property getters
    """
    
    def __init__(self, model_name, category, description):
        # Encapsulation: Protected attributes
        self._model_name = model_name
        self._category = category
        self._description = description
        self._model = None
        self._is_loaded = False
    
    # Multiple decorators example
    @property
    @handle_model_errors
    def model_info(self):
        """Property getter for model information (Encapsulation)"""
        return {
            "name": self._model_name,
            "category": self._category,
            "description": self._description,
            "loaded": self._is_loaded
        }
    
    @abstractmethod
    def load_model(self):
        """Abstract method to be overridden by subclasses"""
        pass
    
    @abstractmethod
    @handle_model_errors
    def process_input(self, input_data):
        """Abstract method for processing input (Polymorphism)"""
        pass
    
    def __str__(self):
        return f"{self._model_name} ({self._category})"

class ModelCacheMixin:
    """
    Mixin class for model caching functionality
    Multiple Inheritance: This will be inherited by model classes
    """
    
    def __init__(self):
        self._cache = {}
        super().__init__()
    
    def cache_result(self, key, result):
        self._cache[key] = result
    
    def get_cached_result(self, key):
        return self._cache.get(key)