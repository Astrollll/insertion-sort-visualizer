"""
Loading screen module for the Insertion Sort Visualizer.
Provides a smooth loading animation with progress bar.
"""

import tkinter as tk
import math
import time
from insertion_sort_visualizer import InsertionSortVisualizer

class LoadingScreen(tk.Frame):
    """A loading screen with animated progress bar and smooth transitions."""
    
    def __init__(self, root):
        """Initialize the loading screen."""
        super().__init__(root)
        self.root = root
        self._setup_window()
        self._create_widgets()
        self._initialize_animation_variables()
        self._start_animations()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title("Loading...")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.configure(bg="#000000")
        self.pack(fill=tk.BOTH, expand=True)
    
    def _create_widgets(self):
        """Create and arrange all UI widgets."""
        # Center container for loading elements
        self.center_frame = tk.Frame(self, bg="#000000")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Loading text
        self.loading_label = tk.Label(
            self.center_frame,
            text="Loading, please wait...",
            font=("Segoe UI", 24, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        self.loading_label.pack(pady=(0, 40))
        
        # Progress bar container
        self.progress_container = tk.Frame(self.center_frame, bg="#000000")
        self.progress_container.pack(pady=25, fill=tk.X, padx=25)
        
        # Progress bar canvas
        self.progress_canvas = tk.Canvas(
            self.progress_container,
            height=30,
            bg="#000000",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X)
        
        # Progress percentage label
        self.progress_label = tk.Label(
            self.center_frame,
            text="0%",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        self.progress_label.pack(pady=(15, 0))
        
        # Restart button
        self.restart_button = tk.Button(
            self.center_frame,
            text="Restart Loading",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#333333",
            activeforeground="#FFFFFF",
            command=self.restart_loading
        )
        self.restart_button.pack(pady=(30, 0))
    
    def _initialize_animation_variables(self):
        """Initialize variables for animations."""
        self.progress = 0
        self.animation_id = None
        self.loading_texts = [
            "Loading, please wait...",
            "Preparing visualization...",
            "Setting up algorithms...",
            "Almost there..."
        ]
        self.current_text_index = 0
    
    def _start_animations(self):
        """Start all animations."""
        self.simulate_loading()
        self.update_loading_text()
    
    def update_progress_bar(self, progress, fill_color=None, outline_color=None):
        """Update the progress bar with animation."""
        self.progress = progress
        
        # Clear previous progress bar
        self.progress_canvas.delete("all")
        self.progress_canvas.configure(bg="#000000")
        
        bar_height = 8
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        # Calculate bar dimensions
        bar_width = width - 4
        bar_y = (height - bar_height) / 2
        
        # Draw progress bar background
        self.progress_canvas.create_rectangle(
            2, bar_y,
            width - 2, bar_y + bar_height,
            fill="#000000",
            outline="#FFFFFF"
        )
        
        # Draw progress fill
        fill_width = (bar_width * progress) / 100
        self.progress_canvas.create_rectangle(
            2, bar_y,
            2 + fill_width, bar_y + bar_height,
            fill="#FFFFFF"
        )
        
        # Update progress label
        self.progress_label.config(text=f"{int(progress)}%")
    
    def update_loading_text(self):
        """Update the loading text with animation."""
        if self.current_text_index < len(self.loading_texts):
            self.loading_label.config(text=self.loading_texts[self.current_text_index])
            self.current_text_index += 1
            self.root.after(2000, self.update_loading_text)
    
    def simulate_loading(self):
        """Simulate loading progress."""
        if self.progress < 100:
            # Simulate variable loading speed
            increment = max(0.1, min(2.0, (100 - self.progress) / 20))
            self.progress += increment
            self.update_progress_bar(self.progress)
            
            # Schedule next update with variable delay
            delay = max(20, min(100, int(100 - self.progress)))
            self.animation_id = self.root.after(delay, self.simulate_loading)
        else:
            # Loading complete
            self.update_progress_bar(100)
            self.root.after(500, self.fade_out)
    
    def fade_out(self):
        """Fade out the loading screen and transition to main app."""
        self.loading_label.config(text="Complete!")
        self.root.after(1000, self._start_main_app)
    
    def _start_main_app(self):
        """Start the main application."""
        self.destroy()
        app = InsertionSortVisualizer(self.root)
    
    def restart_loading(self):
        """Restart the loading animation."""
        # Cancel any ongoing animations
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        
        # Reset progress
        self.progress = 0
        self.current_text_index = 0
        
        # Reset progress bar
        self.progress_canvas.delete("all")
        self.progress_canvas.configure(bg="#000000")
        
        # Reset labels
        self.loading_label.config(text="Loading, please wait...", foreground="#FFFFFF")
        self.progress_label.config(text="0%", foreground="#FFFFFF")
        
        # Restart animations
        self._start_animations()

def main():
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main() 