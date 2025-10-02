import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import traceback

class MainWindow:
    """Main GUI window demonstrating OOP concepts"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Model GUI - HIT137 Assignment 3")
        self.root.geometry("1000x700")
        
        # Encapsulation: Private attributes
        self._current_model = None
        self._models = {}
        
        self._setup_oop_explanations()  # Must be called first
        self._setup_menu()
        self._setup_gui()
        self._load_models()  # Load models after GUI setup
        self._on_model_change(None)  # Initialize with default model
    
    def _setup_menu(self):
        """Setup menu bar as shown in assignment example"""
        try:
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Exit", command=self.root.quit)
            
            # Models menu
            models_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Models", menu=models_menu)
            models_menu.add_command(label="Load All Models", command=self._load_all_models)
            
            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="About", command=self._show_about)
        except Exception as e:
            print(f"Menu setup error: {e}")
    
    def _load_models(self):
        """Load models with proper error handling"""
        try:
            # Try to import models with better error handling
            from models.text_to_image import TextToImageModel
            from models.text_generator import TextGeneratorModel
            
            self._models = {
                "Text-to-Image": TextToImageModel(),
                "Text Generation": TextGeneratorModel()
            }
            
            # Update combobox values if it exists
            if hasattr(self, 'model_var'):
                children = self.root.winfo_children()
                for child in children:
                    if isinstance(child, ttk.Frame):
                        for widget in child.winfo_children():
                            if isinstance(widget, ttk.Combobox):
                                widget['values'] = list(self._models.keys())
            
        except ImportError as e:
            error_msg = f"Failed to import models: {str(e)}\n\n"
            error_msg += "Please make sure:\n"
            error_msg += "1. All model files exist in models/ folder\n"
            error_msg += "2. Dependencies are installed: pip install transformers torch pillow\n"
            error_msg += f"3. Error details: {traceback.format_exc()}"
            
            messagebox.showerror("Import Error", error_msg)
            self._models = {}
    
    def _load_all_models(self):
        """Load all models at once"""
        if not self._models:
            messagebox.showerror("Error", "No models available to load")
            return
            
        results = []
        for model_name, model in self._models.items():
            try:
                result = model.load_model()
                results.append(f"{model_name}: {result}")
                print(f"{model_name}: {result}")
            except Exception as e:
                results.append(f"{model_name}: ERROR - {str(e)}")
        
        messagebox.showinfo("Models Loaded", "\n".join(results))
        self._on_model_change(None)
    
    def _show_about(self):
        """Show about information"""
        about_text = """AI Model GUI - HIT137 Assignment 3

This application demonstrates:
• Integration of Hugging Face AI models
• Object-Oriented Programming concepts
• Tkinter GUI development

Models:
• Text-to-Image: Stable Diffusion v1.5
• Text Generation: DialoGPT Medium"""
        messagebox.showinfo("About", about_text)
    
    def _setup_gui(self):
        """Setup the main GUI layout"""
        try:
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
            ttk.Label(header_frame, text="HIT137 Assignment 3 - AI Model Integration").pack()
            
            # Model selection frame
            model_frame = ttk.LabelFrame(main_frame, text="Model Selection", padding="5")
            model_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            ttk.Label(model_frame, text="Model Selection:").grid(row=0, column=0, sticky=tk.W)
            self.model_var = tk.StringVar(value="Text-to-Image")
            
            # Get available models or use defaults
            model_values = list(self._models.keys()) if self._models else ["Text-to-Image", "Text Generation"]
            
            model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                     values=model_values, state="readonly", width=20)
            model_combo.grid(row=0, column=1, padx=(10, 0))
            model_combo.bind('<<ComboboxSelected>>', self._on_model_change)
            
            ttk.Button(model_frame, text="✔ Load Model", 
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
            input_frame.rowconfigure(1, weight=1)
            
            # Input type selection (radio buttons)
            input_type_frame = ttk.Frame(input_frame)
            input_type_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
            
            self.input_type = tk.StringVar(value="text")
            ttk.Radiobutton(input_type_frame, text="💷 Text", variable=self.input_type, 
                           value="text").pack(side=tk.LEFT)
            ttk.Radiobutton(input_type_frame, text="💷 Image", variable=self.input_type, 
                           value="image").pack(side=tk.LEFT)
            ttk.Button(input_type_frame, text="Browse", 
                      command=self._browse_file).pack(side=tk.LEFT, padx=(10, 0))
            
            self.input_text = scrolledtext.ScrolledText(input_frame, height=12, width=45)
            self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.input_text.insert(1.0, "Enter your text here...")
            
            # Output section
            output_frame = ttk.LabelFrame(io_frame, text="Model Output Section", padding="10")
            output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
            output_frame.columnconfigure(0, weight=1)
            output_frame.rowconfigure(0, weight=1)
            output_frame.rowconfigure(1, weight=0)
            
            self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=45, state=tk.DISABLED)
            self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            self.image_label = ttk.Label(output_frame, text="Image output will appear here")
            self.image_label.grid(row=1, column=0, pady=(10, 0))
            
            # Control buttons
            control_frame = ttk.Frame(main_frame)
            control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            ttk.Button(control_frame, text="Run Model 1", 
                      command=lambda: self._run_model("Text-to-Image")).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(control_frame, text="Run Model 2", 
                      command=lambda: self._run_model("Text Generation")).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(control_frame, text="Clear", 
                      command=self._clear_output).pack(side=tk.LEFT, padx=(0, 10))
            
            # Information section
            info_frame = ttk.LabelFrame(main_frame, text="Model Information & Explanation", padding="10")
            info_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            info_frame.columnconfigure(0, weight=1)
            info_frame.columnconfigure(1, weight=1)
            info_frame.rowconfigure(0, weight=1)
            
            self._setup_info_section(info_frame)
            
            # Configure weights for proper resizing
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(2, weight=1)
            input_frame.rowconfigure(1, weight=1)
            output_frame.rowconfigure(0, weight=1)
            
        except Exception as e:
            messagebox.showerror("GUI Setup Error", f"Failed to setup GUI: {str(e)}")
    
    def _browse_file(self):
        """Browse for image files"""
        try:
            filename = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
            )
            if filename:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, filename)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to browse file: {str(e)}")
    
    def _setup_info_section(self, parent):
        """Setup information and OOP explanations section"""
        try:
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
            
        except Exception as e:
            print(f"Info section error: {e}")
    
    def _setup_oop_explanations(self):
        """Setup OOP concepts explanations with detailed implementation"""
        self.oop_explanations = {
            "Multiple Inheritance": {
                "where": "TextToImageModel and TextGeneratorModel inherit from both AIModel (abstract base class) and ModelCacheMixin (mixin class)",
                "why": "To combine core AI model functionality with caching capabilities without code duplication"
            },
            "Encapsulation": {
                "where": "Private attributes (_model_name, _category, _is_loaded) with @property getters in AIModel class",
                "why": "To protect internal state and control access to model attributes"
            },
            "Polymorphism": {
                "where": "process_input() method behaves differently in each subclass",
                "why": "To allow different models to process inputs in their specific ways"
            },
            "Method Overriding": {
                "where": "load_model() method overridden in both subclasses",
                "why": "To provide model-specific loading logic"
            },
            "Multiple Decorators": {
                "where": "@property + @handle_model_errors decorators in AIModel class",
                "why": "To combine property functionality with automatic error handling"
            }
        }
    
    def _populate_oop_explanations(self):
        """Populate OOP explanations in the text widget"""
        try:
            if not hasattr(self, 'oop_explanations'):
                self._setup_oop_explanations()
                
            explanations = "OOP Concepts Implementation:\n\n"
            for concept, info in self.oop_explanations.items():
                explanations += f"• {concept}:\n"
                explanations += f"  WHERE: {info['where']}\n"
                explanations += f"  WHY: {info['why']}\n\n"
            
            if hasattr(self, 'oop_explanation_text'):
                self.oop_explanation_text.config(state=tk.NORMAL)
                self.oop_explanation_text.delete(1.0, tk.END)
                self.oop_explanation_text.insert(1.0, explanations)
                self.oop_explanation_text.config(state=tk.DISABLED)
                
        except Exception as e:
            print(f"OOP explanations error: {e}")
    
    def _on_model_change(self, event):
        """Handle model selection change"""
        try:
            model_name = self.model_var.get()
            self._current_model = self._models.get(model_name)
            
            if not self._current_model:
                # Show default info if model not available
                info_text = f"• Model Name: {model_name}\n"
                info_text += f"• Category: {'Text-to-Image' if 'Image' in model_name else 'Text Generation'}\n"
                info_text += f"• Status: Not Loaded\n\n"
                info_text += "Please load the model first"
            else:
                # Update model info
                info = self._current_model.model_info
                info_text = f"• Model Name: {info['name']}\n"
                info_text += f"• Category: {info['category']}\n"
                info_text += f"• Short Description: {info['description']}\n"
                info_text += f"• Status: {'Loaded' if info['loaded'] else 'Not Loaded'}\n\n"
                info_text += f"Hugging Face Model:\n"
                if model_name == "Text-to-Image":
                    info_text += "runwayml/stable-diffusion-v1-5"
                else:
                    info_text += "microsoft/DialoGPT-medium"
            
            if hasattr(self, 'model_info_text'):
                self.model_info_text.config(state=tk.NORMAL)
                self.model_info_text.delete(1.0, tk.END)
                self.model_info_text.insert(1.0, info_text)
                self.model_info_text.config(state=tk.DISABLED)
                
        except Exception as e:
            print(f"Model change error: {e}")
    
    def _load_model(self):
        """Load the selected model"""
        try:
            if not self._current_model:
                messagebox.showerror("Error", "Please select a model first")
                return
                
            result = self._current_model.load_model()
            messagebox.showinfo("Model Load", result)
            self._on_model_change(None)
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load model: {str(e)}")
    
    def _run_model(self, model_name):
        """Run specified model"""
        try:
            model = self._models.get(model_name)
            
            if not model:
                messagebox.showerror("Error", f"Model '{model_name}' not available")
                return
                
            if not getattr(model, '_is_loaded', False):
                messagebox.showerror("Error", f"Please load {model_name} model first")
                return
            
            input_data = self.input_text.get(1.0, tk.END).strip()
            
            if not input_data or input_data == "Enter your text here...":
                messagebox.showerror("Error", "Please provide input data")
                return
            
            # Show processing message
            if hasattr(self, 'output_text'):
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, "Processing... Please wait.")
                self.output_text.config(state=tk.DISABLED)
                self.root.update()
            
            # Process input
            result = model.process_input(input_data)
            self._display_result(result, model_name)
            
        except Exception as e:
            error_msg = f"Error running {model_name}: {str(e)}"
            if hasattr(self, 'output_text'):
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, error_msg)
                self.output_text.config(state=tk.DISABLED)
            messagebox.showerror("Runtime Error", error_msg)
    
    def _display_result(self, result, model_name):
        """Display model result"""
        try:
            if not hasattr(self, 'output_text'):
                return
                
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            
            if model_name == "Text-to-Image" and hasattr(result, 'save'):
                # Display image
                try:
                    display_size = (300, 300)
                    result.thumbnail(display_size, Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(result)
                    self.image_label.configure(image=photo)
                    self.image_label.image = photo
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
            
        except Exception as e:
            print(f"Display result error: {e}")
    
    def _clear_output(self):
        """Clear output section"""
        try:
            if hasattr(self, 'output_text'):
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.config(state=tk.DISABLED)
            
            if hasattr(self, 'image_label'):
                self.image_label.configure(image='')
                self.image_label.configure(text="Image output will appear here")
                
        except Exception as e:
            print(f"Clear output error: {e}")
