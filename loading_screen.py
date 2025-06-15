import tkinter as tk
from tkinter import ttk
import math
import time
from insertion_sort_visualizer import InsertionSortVisualizer

class LoadingScreen(tk.Frame):
    """
    A loading screen with animated progress bar and smooth transitions.
    Provides visual feedback during application initialization.
    """
    
    # Window configuration
    WINDOW_SIZE = "1000x600"
    MIN_SIZE = (800, 500)
    
    # Theme colors
    THEME = {
        'bg_color': "#000000",      # Black background
        'text_color': "#FFFFFF",    # White text
        'accent_color': "#FFFFFF",  # White for accents
        'button_hover': "#333333",  # Dark gray for button hover
        'progress_bg': "#000000",   # Black progress background
        'progress_fill': "#FFFFFF", # White progress bar
        'border_color': "#333333"   # Dark gray for borders
    }
    
    # Font configurations
    FONTS = {
        'title': ("Segoe UI", 24, "bold"),
        'loading': ("Segoe UI", 24, "bold"),
        'progress': ("Segoe UI", 16, "bold"),
        'button': ("Segoe UI", 12, "bold")
    }
    
    def __init__(self, root):
        """Initialize the loading screen with window setup and UI components."""
        super().__init__(root)
        self.root = root
        self._setup_window()
        self._setup_animation_control()
        self._create_widgets()
        self._initialize_animation_variables()
        self._start_animations()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title("Loading...")
        self.root.geometry(self.WINDOW_SIZE)
        self.root.minsize(*self.MIN_SIZE)
        self.configure(bg=self.THEME['bg_color'])
        self.pack(fill=tk.BOTH, expand=True)
    
    def _setup_animation_control(self):
        """Initialize animation control variables."""
        self.is_animating = True
        self.after_ids = []
    
    def _create_widgets(self):
        """Create and arrange all UI widgets."""
        # Center container for loading elements
        self.center_frame = tk.Frame(self, bg=self.THEME['bg_color'])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Loading text
        self.loading_label = tk.Label(
            self.center_frame,
            text="Loading, please wait...",
            font=self.FONTS['loading'],
            fg=self.THEME['text_color'],
            bg=self.THEME['bg_color']
        )
        self.loading_label.pack(pady=(0, 40))
        
        # Progress bar container
        self.progress_container = tk.Frame(self.center_frame, bg=self.THEME['bg_color'])
        self.progress_container.pack(pady=25, fill=tk.X, padx=25)
        
        # Progress bar canvas
        self.progress_canvas = tk.Canvas(
            self.progress_container,
            height=30,
            bg=self.THEME['progress_bg'],
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X, padx=3, pady=3)
        
        # Progress percentage label
        self.progress_label = tk.Label(
            self.center_frame,
            text="0%",
            font=self.FONTS['progress'],
            fg=self.THEME['text_color'],
            bg=self.THEME['bg_color']
        )
        self.progress_label.pack(pady=(15, 0))
        
        # Restart button
        self.restart_button = tk.Button(
            self.center_frame,
            text="Restart Loading",
            font=self.FONTS['button'],
            bg=self.THEME['accent_color'],
            fg=self.THEME['bg_color'],
            activebackground=self.THEME['button_hover'],
            activeforeground=self.THEME['text_color'],
            command=self.restart_loading
        )
        self.restart_button.pack(pady=(20, 0))
    
    def _initialize_animation_variables(self):
        """Initialize all animation-related variables."""
        self.progress = 0
        self.loading_dots = ""
        self.dot_count = 0
        self.fade_alpha = 1.0
    
    def _start_animations(self):
        """Start all animation sequences."""
        self.update_loading_text()
        self.simulate_loading()
    
    def _draw_rounded_rectangle(self, x1, y1, x2, y2, radius, fill_color, outline_color=""):
        """Draw a rounded rectangle on the progress canvas."""
        outline_width = 1 if outline_color else 0

        # Draw the main horizontal rectangle
        self.progress_canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2,
                                           fill=fill_color, outline=outline_color, width=outline_width)

        # Draw the vertical rectangles
        self.progress_canvas.create_rectangle(x1, y1 + radius, x1 + radius, y2 - radius,
                                           fill=fill_color, outline=outline_color, width=outline_width)
        self.progress_canvas.create_rectangle(x2 - radius, y1 + radius, x2, y2 - radius,
                                           fill=fill_color, outline=outline_color, width=outline_width)

        # Draw the corner circles
        self.progress_canvas.create_oval(x1, y1, x1 + 2 * radius, y1 + 2 * radius,
                                       fill=fill_color, outline=outline_color, width=outline_width)
        self.progress_canvas.create_oval(x2 - 2 * radius, y1, x2, y1 + 2 * radius,
                                       fill=fill_color, outline=outline_color, width=outline_width)
        self.progress_canvas.create_oval(x1, y2 - 2 * radius, x1 + 2 * radius, y2,
                                       fill=fill_color, outline=outline_color, width=outline_width)
        self.progress_canvas.create_oval(x2 - 2 * radius, y2 - 2 * radius, x2, y2,
                                       fill=fill_color, outline=outline_color, width=outline_width)
    
    def update_progress_bar(self, event=None, fill_color=None, outline_color=None):
        """Update the progress bar with rounded corners and moving circle."""
        if not self.is_animating:
            return

        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()

        self.progress_canvas.delete("all")
        self.progress_canvas.configure(bg=self.THEME['progress_bg'])

        bar_height = 8
        bar_y_center = height / 2
        trough_radius = bar_height / 2

        # Determine colors
        trough_outline_color = outline_color if outline_color is not None else self.THEME['text_color']
        animated_fill_color = fill_color if fill_color is not None else self.THEME['text_color']
        animated_outline_color = outline_color if outline_color is not None else ""

        # Draw the static trough
        trough_x1 = trough_radius + 2
        trough_y1 = bar_y_center - trough_radius
        trough_x2 = width - trough_radius - 2
        trough_y2 = bar_y_center + trough_radius
        self._draw_rounded_rectangle(trough_x1, trough_y1, trough_x2, trough_y2, 
                                   trough_radius, "", trough_outline_color)

        # Calculate and draw progress
        progress_total_length = (width - 2 * trough_radius - 4)
        progress_current_length = progress_total_length * (self.progress / 100)

        filled_x1 = trough_x1
        filled_y1 = trough_y1
        filled_x2 = min(filled_x1 + progress_current_length, trough_x2)
        filled_y2 = trough_y2

        self._draw_rounded_rectangle(filled_x1, filled_y1, filled_x2, filled_y2,
                                   trough_radius, animated_fill_color, animated_outline_color)

        # Draw the moving circle
        circle_radius = 8
        circle_center_x = filled_x2
        circle_center_y = bar_y_center
        self.progress_canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                                       circle_center_x + circle_radius, circle_center_y + circle_radius,
                                       fill=animated_fill_color, outline=animated_outline_color)
    
    def update_loading_text(self):
        """Update the loading text with animated dots."""
        if not self.is_animating:
            return
            
        self.dot_count = (self.dot_count + 1) % 4
        self.loading_dots = "." * self.dot_count
        if self.loading_label.winfo_exists():
            self.loading_label.config(text=f"Loading, please wait{self.loading_dots}")
        self.after_ids.append(self.root.after(500, self.update_loading_text))
    
    def simulate_loading(self):
        """Simulate loading progress with smooth animation."""
        if not self.is_animating:
            return
            
        if self.progress < 100:
            remaining = 100 - self.progress
            increment = remaining * 0.06
            self.progress = min(100, self.progress + increment)
            
            if self.progress_label.winfo_exists():
                self.progress_label.config(text=f"{int(self.progress)}%")
            
            self.update_progress_bar()
            
            if self.progress >= 99.9:
                self.progress = 100
                if self.progress_label.winfo_exists():
                    self.progress_label.config(text="100%")
                self.update_progress_bar()
                self.after_ids.append(self.root.after(1000, self.fade_out))
            else:
                self.after_ids.append(self.root.after(40, self.simulate_loading))
    
    def fade_out(self):
        """Fade out the loading screen elements with a grayscale effect."""
        if not self.is_animating:
            return
            
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 0.05)
            eased_alpha = self.ease_out_quad(self.fade_alpha)
            
            color_value = max(0, min(255, int(255 * eased_alpha)))
            fade_color = f'#{color_value:02x}{color_value:02x}{color_value:02x}'
            
            if self.loading_label.winfo_exists():
                self.loading_label.config(foreground=fade_color)
            
            if self.progress_label.winfo_exists():
                self.progress_label.config(foreground=fade_color)
            
            if self.progress_canvas.winfo_exists():
                self.update_progress_bar(fill_color=fade_color, outline_color=fade_color)
            
            self.after_ids.append(self.root.after(30, self.fade_out))
        else:
            self.transition_to_main()
    
    def ease_out_quad(self, t):
        """Easing function for smoother animation."""
        return 1 - (1 - t) * (1 - t)
    
    def restart_loading(self):
        """Restart the loading animation from the beginning."""
        # Stop all current animations
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        self.after_ids.clear()
        
        # Reset animation variables
        self.progress = 0
        self.loading_dots = ""
        self.dot_count = 0
        self.fade_alpha = 1.0
        self.is_animating = True
        
        # Reset labels
        self.loading_label.config(text="Loading, please wait...", foreground=self.THEME['text_color'])
        self.progress_label.config(text="0%", foreground=self.THEME['text_color'])
        
        # Restart animations
        self.update_loading_text()
        self.simulate_loading()
    
    def transition_to_main(self):
        """Transition to the main application."""
        self.is_animating = False
        
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        self.after_ids.clear()
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        app = InsertionSortVisualizer(self.root)

def main():
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main() 