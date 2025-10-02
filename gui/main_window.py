import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os

class MainWindow:
    """Main GUI window demonstrating OOP concepts"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Model GUI - HIT137 Assignment 3")
        self.root.geometry("1000x700")
        
        # Encapsulation: Private attributes
        self._current_model = None
        
        # Import models (demonstrating modularity)
        from models.text_to_image import TextToImageModel
        from models.text_generator import TextGeneratorModel
        
        self._models = {
            "Text-to-Image": TextToImageModel(),
            "Text Generation": TextGeneratorModel()
        }
        
        self._setup_gui()
        self._setup_oop_explanations()
        self._on_model_change(None)  # Initialize with default model
    
    def _setup_gui(self):
        """Setup the main GUI layout"""
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(header_frame, text="Tkinter AI GUI", font=('Arial', 16, 'bold')).pack()
        
        # Model selection frame
        model_frame = ttk.LabelFrame(main_frame, text="Model Selection", padding="5")
        model_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(model_frame, text="Select Model:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value="Text-to-Image")
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                 values=list(self._models.keys()), state="readonly", width=20)
        model_combo.grid(row=0, column=1, padx=(10, 0))
        model_combo.bind('<<ComboboxSelected>>', self._on_model_change)
        
        ttk.Button(model_frame, text="Load Model", 
                  command=self._load_model).grid(row=0, column=2, padx=(10, 0))
        
        # Input and Output sections
        io_frame = ttk.Frame(main_frame)
        io_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        io_frame.columnconfigure(0, weight=1)
        io_frame.columnconfigure(1, weight=1)
        io_frame.rowconfigure(0, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(io_frame, text="User Input Section", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=15, width=45)
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.input_text.insert(1.0, "Enter your text here...")
        
        # Output section
        output_frame = ttk.LabelFrame(io_frame, text="Model Output Section", padding="10")
        output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=0)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=45, state=tk.DISABLED)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.image_label = ttk.Label(output_frame, text="Image output will appear here")
        self.image_label.grid(row=1, column=0, pady=(10, 0))
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Run Model 1 (Text-to-Image)", 
                  command=lambda: self._run_model("Text-to-Image")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Run Model 2 (Text Generation)", 
                  command=lambda: self._run_model("Text Generation")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Clear Output", 
                  command=self._clear_output).pack(side=tk.LEFT, padx=(0, 10))
        
        # Information section
        info_frame = ttk.LabelFrame(main_frame, text="Model Information & Explanation", padding="10")
        info_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        self._setup_info_section(info_frame)
    
    def _setup_info_section(self, parent):
        """Setup information and OOP explanations section"""
        # Model info
        model_info_frame = ttk.Frame(parent)
        model_info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        model_info_frame.columnconfigure(0, weight=1)
        model_info_frame.rowconfigure(1, weight=1)
        
        ttk.Label(model_info_frame, text="Selected Model Info:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.model_info_text = scrolledtext.ScrolledText(model_info_frame, height=8, width=45)
        self.model_info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # OOP explanations
        oop_frame = ttk.Frame(parent)
        oop_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        oop_frame.columnconfigure(0, weight=1)
        oop_frame.rowconfigure(1, weight=1)
        
        ttk.Label(oop_frame, text="OOP Concepts Explanation:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.oop_explanation_text = scrolledtext.ScrolledText(oop_frame, height=8, width=45)
        self.oop_explanation_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Populate OOP explanations
        self._populate_oop_explanations()
    
    def _setup_oop_explanations(self):
        """Setup OOP concepts explanations"""
        self.oop_explanations = {
            "Multiple Inheritance": {
                "where": "TextToImageModel and TextGeneratorModel inherit from both AIModel and ModelCacheMixin",
                "why": "To combine core AI model functionality with caching capabilities without code duplication"
            },
            "Encapsulation": {
                "where": "Private attributes (_model_name, _category) and properties in AIModel class",
                "why": "To protect internal state and control access to model attributes, ensuring data integrity"
            },
            "Polymorphism": {
                "where": "process_input() method implemented differently in each subclass",
                "why": "To allow different models to process inputs in their specific ways while maintaining a common interface"
            },
            "Method Overriding": {
                "where": "load_model() method overridden in TextToImageModel and TextGeneratorModel",
                "why": "To provide model-specific loading logic while maintaining the same method signature across all models"
            },
            "Multiple Decorators": {
                "where": "@property + @handle_model_errors decorators in AIModel class methods",
                "why": "To combine property functionality with automatic error handling in a reusable way"
            }
        }
    
    def _populate_oop_explanations(self):
        """Populate OOP explanations in the text widget"""
        explanations = "OOP Concepts Implementation:\n\n"
        for concept, info in self.oop_explanations.items():
            explanations += f"• {concept}:\n"
            explanations += f"  WHERE: {info['where']}\n"
            explanations += f"  WHY: {info['why']}\n\n"
        
        self.oop_explanation_text.config(state=tk.NORMAL)
        self.oop_explanation_text.delete(1.0, tk.END)
        self.oop_explanation_text.insert(1.0, explanations)
        self.oop_explanation_text.config(state=tk.DISABLED)
    
    def _on_model_change(self, event):
        """Handle model selection change"""
        model_name = self.model_var.get()
        self._current_model = self._models[model_name]
        
        # Update model info
        if self._current_model:
            info = self._current_model.model_info
            info_text = f"Model Name: {info['name']}\n"
            info_text += f"Category: {info['category']}\n"
            info_text += f"Description: {info['description']}\n"
            info_text += f"Status: {'Loaded' if info['loaded'] else 'Not Loaded'}\n\n"
            info_text += f"Hugging Face Model:\n"
            if model_name == "Text-to-Image":
                info_text += "runwayml/stable-diffusion-v1-5"
            else:
                info_text += "microsoft/DialoGPT-medium"
            
            self.model_info_text.config(state=tk.NORMAL)
            self.model_info_text.delete(1.0, tk.END)
            self.model_info_text.insert(1.0, info_text)
            self.model_info_text.config(state=tk.DISABLED)
    
    def _load_model(self):
        """Load the selected model"""
        if self._current_model:
            result = self._current_model.load_model()
            messagebox.showinfo("Model Load", result)
            self._on_model_change(None)  # Refresh model info
    
    def _run_model(self, model_name):
        """Run specified model"""
        model = self._models[model_name]
        
        if not model._is_loaded:
            messagebox.showerror("Error", f"Please load {model_name} model first")
            return
        
        input_data = self.input_text.get(1.0, tk.END).strip()
        
        if not input_data or input_data == "Enter your text here...":
            messagebox.showerror("Error", "Please provide input data")
            return
        
        # Show processing message
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, "Processing... Please wait.")
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
        
        # Process input
        result = model.process_input(input_data)
        
        # Display result
        self._display_result(result, model_name)
    
    def _display_result(self, result, model_name):
        """Display model result"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        
        if model_name == "Text-to-Image" and hasattr(result, 'save'):
            # Display image
            try:
                # Resize image for display
                display_size = (300, 300)
                result.thumbnail(display_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(result)
                self.image_label.configure(image=photo)
                self.image_label.image = photo  # Keep a reference
                self.output_text.insert(1.0, "Image generated successfully!\n\n")
                self.output_text.insert(tk.END, f"Image size: {result.size}")
            except Exception as e:
                self.output_text.insert(1.0, f"Error displaying image: {str(e)}")
        else:
            # Display text result
            self.image_label.configure(image='')
            self.image_label.configure(text="Image output will appear here")
            self.output_text.insert(1.0, str(result))
        
        self.output_text.config(state=tk.DISABLED)
    
    def _clear_output(self):
        """Clear output section"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.image_label.configure(image='')
        self.image_label.configure(text="Image output will appear here")