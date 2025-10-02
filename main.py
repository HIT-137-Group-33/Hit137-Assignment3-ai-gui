import tkinter as tk
from gui.main_window import MainWindow

def main():
    """Main function to run the Tkinter AI GUI application"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()