import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time

def main():
    # Main run
    root = tk.Tk()
    app = InsertionSortVisualizer(root)
    root.mainloop()

class InsertionSortVisualizer:
    # Init
    def __init__(self, root):
        self.root = root
        self.root.title("Insertion Sort Visualizer")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', True)
        self.root.minsize(800, 500)
        self.is_dark_theme = True
        self.canvas_width = 0
        self.canvas_height = 0
        self.speed = 100
        self.data = []
        self.initial_data = None
        self.paused = False
        self.sorting = False
        self.step_by_step = False
        self.current_step_completed = True
        self.current_animation = None
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = 0
        self.step_count = 0
        self.animation_frames = 30
        self.current_frame = 0
        self.animation_data = None
        self.animation_type = None
        self.animation_colors = None
        self.current_step = None
        self.animation_queue = []
        self.is_animating = False
        self.animation_speed_factor = 1.0
        self._cached_colors = {}
        self._last_draw_time = 0
        self._min_frame_time = 16
        self.colors = {
            'default': "#4C566A",
            'current': "#EBCB8B",
            'compare': "#BF616A",
            'sorted': "#A3BE8C",
            'insert': "#81A1C1",
            'text': "#ECEFF4",
            'text_bg': "#2E3440"
        }
        self.style = ttk.Style()
        self.configure_style()
        self.current_step_number = 0
        self.total_steps = 0
        self.step_history = []
        self.current_substep = 0
        self.total_substeps = 0
        self.speed_indicator = None
        self.prev_step_button = None
        self.next_step_button = None
        self.step_label = None
        self.substep_label = None
        self.build_ui()

    # Style
    def configure_style(self):
        self.style.theme_use('clam')
        if self.is_dark_theme:
            bg_color = "#1E1E1E"
            fg_color = "#FFFFFF"
            accent_color = "#007ACC"
            button_color = "#2D2D2D"
            hover_color = "#3E3E3E"
            canvas_bg = "#252526"
            text_color = "#D4D4D4"
            border_color = "#3E3E3E"
            radio_bg = "#2D2D2D"
            radio_fg = "#FFFFFF"
            radio_selected = "#007ACC"
            radio_hover = "#3E3E3E"
            radio_border = "#404040"
            radio_container_bg = "#252526"
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
            self.style.configure("TButton",
                               background=button_color,
                               foreground=text_color,
                               font=("Segoe UI", 10),
                               borderwidth=0,
                               focusthickness=0,
                               padding=8)
            self.style.map("TButton",
                          background=[('active', hover_color)],
                          foreground=[('active', fg_color)])
            self.style.configure("TEntry",
                               fieldbackground=button_color,
                               foreground=text_color,
                               padding=8,
                               font=("Segoe UI", 10))
            self.style.configure("Tooltip.TFrame", background="#2D2D2D")
            self.style.configure("Tooltip.TLabel", background="#2D2D2D", foreground="#FFFFFF")
            self.style.configure("CanvasBorder.TFrame", background=border_color)
            self.style.configure("Speed.TFrame",
                               background=radio_container_bg,
                               relief="flat",
                               borderwidth=1)
            self.style.configure("Speed.TRadiobutton",
                               background=radio_bg,
                               foreground=radio_fg,
                               font=("Segoe UI", 10, "bold"),
                               padding=(15, 8),
                               indicatorcolor=radio_selected,
                               indicatorbackground=radio_bg,
                               indicatorrelief="flat",
                               borderwidth=1,
                               relief="flat",
                               focusthickness=0)
            self.style.map("Speed.TRadiobutton",
                          background=[('active', radio_hover),
                                    ('selected', radio_selected)],
                          foreground=[('active', radio_fg),
                                    ('selected', "#FFFFFF")],
                          indicatorcolor=[('selected', "#FFFFFF")],
                          indicatorbackground=[('selected', radio_selected)],
                          relief=[('selected', 'flat')],
                          borderwidth=[('selected', 0)],
                          focusthickness=[('selected', 0)])
        else:
            bg_color = "#AAAAAA"
            fg_color = "#333333"
            accent_color = "#0078D4"    
            button_color = "#E1E1E1"
            hover_color = "#D0D0D0"
            canvas_bg = "#FFFFFF"
            text_color = "#333333"
            border_color = "#CCCCCC"
            radio_bg = "#FFFFFF"
            radio_fg = "#333333"
            radio_selected = "#0078D4"
            radio_hover = "#F0F0F0"
            radio_border = "#E0E0E0"
            radio_container_bg = "#F8F8F8"
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
            self.style.configure("TButton",
                               background=button_color,
                               foreground=text_color,
                               font=("Segoe UI", 10),
                               borderwidth=0,
                               focusthickness=0,
                               padding=8)
            self.style.map("TButton",
                          background=[('active', hover_color)],
                          foreground=[('active', fg_color)])
            self.style.configure("TEntry",
                               fieldbackground=button_color,
                               foreground=text_color,
                               padding=8,
                               font=("Segoe UI", 10))
            self.style.configure("Tooltip.TFrame", background="#2D2D2D")
            self.style.configure("Tooltip.TLabel", background="#2D2D2D", foreground="#FFFFFF")
            self.style.configure("CanvasBorder.TFrame", background=border_color)
            self.style.configure("Speed.TFrame",
                               background=radio_container_bg,
                               relief="flat",
                               borderwidth=1)
            self.style.configure("Speed.TRadiobutton",
                               background=radio_bg,
                               foreground=radio_fg,
                               font=("Segoe UI", 10, "bold"),
                               padding=(15, 8),
                               indicatorcolor=radio_selected,
                               indicatorbackground=radio_bg,
                               indicatorrelief="flat",
                               borderwidth=1,
                               relief="flat",
                               focusthickness=0)
            self.style.map("Speed.TRadiobutton",
                          background=[('active', radio_hover),
                                    ('selected', radio_selected)],
                          foreground=[('active', radio_fg),
                                    ('selected', "#FFFFFF")],
                          indicatorcolor=[('selected', "#FFFFFF")],
                          indicatorbackground=[('selected', radio_selected)],
                          relief=[('selected', 'flat')],
                          borderwidth=[('selected', 0)],
                          focusthickness=[('selected', 0)])

    # UI
    def build_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top Controls with better spacing
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))

        # Input section
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(input_frame, text="Enter Numbers:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.input_entry = ttk.Entry(input_frame, width=40)
        self.input_entry.pack(side=tk.LEFT, padx=5)
        
        # Add submit button for user input
        submit_btn = ttk.Button(input_frame, text="Submit", command=self.submit_input)
        submit_btn.pack(side=tk.LEFT, padx=5)

        # Random generation section
        random_frame = ttk.Frame(control_frame)
        random_frame.pack(side=tk.LEFT, padx=20)
        
        self.length_spinbox = ttk.Spinbox(random_frame, from_=5, to=50, width=5)
        self.length_spinbox.pack(side=tk.LEFT, padx=5)
        self.length_spinbox.bind('<Return>', lambda e: self.generate_random())

        generate_btn = ttk.Button(random_frame, text="Generate Random", command=self.generate_random)
        generate_btn.pack(side=tk.LEFT, padx=5)

        # Speed control section
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(side=tk.RIGHT)
        
        # Create a container for speed controls
        speed_container = ttk.Frame(speed_frame)
        speed_container.pack(side=tk.RIGHT)
        
        # Add speed label with icon
        speed_label = ttk.Label(speed_container, 
                              text="⚡ Speed:", 
                              font=("Segoe UI", 10, "bold"))
        speed_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Create a frame for radio buttons with a subtle border
        speed_radio_frame = ttk.Frame(speed_container, style="Speed.TFrame")
        speed_radio_frame.pack(side=tk.LEFT)
        
        # Create a variable to hold the selected speed
        self.speed_var = tk.StringVar(value="normal")
        
        # Create radio buttons with custom styling
        speeds = [
            ("Slow", "slow", 2000),
            ("Normal", "normal", 500),
            ("Fast", "fast", 5)
        ]
        
        for text, value, speed in speeds:
            radio = ttk.Radiobutton(
                speed_radio_frame,
                text=text,
                value=value,
                variable=self.speed_var,
                command=lambda s=speed, t=text: self.set_speed(s, t),
                style="Speed.TRadiobutton"
            )
            radio.pack(side=tk.LEFT, padx=1)
        
        # Set initial speed
        self.speed = 500  # Default to normal speed

        # Canvas Frame with border
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Add canvas border
        canvas_border = ttk.Frame(canvas_frame, style="CanvasBorder.TFrame")
        canvas_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.canvas = tk.Canvas(canvas_border, 
                              bg="#3B4252" if self.is_dark_theme else "#FFFFFF",
                              bd=0,
                              highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        
        # Add keyboard shortcuts
        self.root.bind('<t>', lambda e: self.toggle_theme())

        # Statistics Frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(stats_frame, 
                                          variable=self.progress_var,
                                          maximum=100,
                                          mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Statistics labels
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill=tk.X)
        
        self.comparisons_label = ttk.Label(stats_container, 
                                         text="Comparisons: 0",
                                         font=("Segoe UI", 9))
        self.comparisons_label.pack(side=tk.LEFT, padx=5)
        
        self.swaps_label = ttk.Label(stats_container,
                                   text="Swaps: 0",
                                   font=("Segoe UI", 9))
        self.swaps_label.pack(side=tk.LEFT, padx=5)
        
        self.iteration_label = ttk.Label(stats_container,
                                       text="Iteration: 0/0",
                                       font=("Segoe UI", 9))
        self.iteration_label.pack(side=tk.LEFT, padx=5)

        # Add step counter to statistics
        self.step_label = ttk.Label(stats_container,
                                  text="Step: 0/0",
                                  font=("Segoe UI", 9))
        self.step_label.pack(side=tk.LEFT, padx=5)

        # Add substep counter
        self.substep_label = ttk.Label(stats_container,
                                     text="Substep: 0/0",
                                     font=("Segoe UI", 9))
        self.substep_label.pack(side=tk.LEFT, padx=5)

        # Add speed indicator
        self.speed_indicator = ttk.Label(stats_container,
                                       text="Speed: Normal",
                                       font=("Segoe UI", 9))
        self.speed_indicator.pack(side=tk.RIGHT, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        start_btn = ttk.Button(left_buttons, text="Start Sort", command=self.start_sort)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(left_buttons, text="Pause", command=self.toggle_pause, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(left_buttons, text="Reset", command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.step_btn = ttk.Button(left_buttons, text="Step-by-Step", command=self.toggle_step_by_step)
        self.step_btn.pack(side=tk.LEFT, padx=5)

        # Add step navigation buttons
        step_nav_frame = ttk.Frame(left_buttons)
        step_nav_frame.pack(side=tk.LEFT, padx=20)
        
        self.next_step_button = ttk.Button(step_nav_frame, text="Next Step", command=self.next_step)
        self.next_step_button.pack(side=tk.LEFT, padx=5)

        # Right side theme toggle
        self.theme_button = ttk.Button(button_frame, text="Switch Theme (T)", command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT, padx=5)

        # Add close button
        close_btn = ttk.Button(button_frame, text="Close Window", command=self.close_window)
        close_btn.pack(side=tk.RIGHT, padx=5)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                    text="",
                                    font=("Segoe UI", 11, "bold"),
                                    foreground="#A3BE8C" if self.is_dark_theme else "#2E3440")
        self.status_label.pack(side=tk.LEFT)

    # Speed
    def set_speed(self, speed_value, speed_text):
        try:
            self.speed = speed_value
            self.speed_indicator.config(text=f"Speed: {speed_text}")
            # Adjust animation duration based on speed
            self.animation_duration = max(200, min(1000, int(1000 * (speed_value / 500))))
            # Adjust animation frames based on duration
            self.animation_frames = max(15, min(60, int(self.animation_duration / self._min_frame_time)))
            # Update animation speed factor for smooth transitions
            self.animation_speed_factor = min(1.0, 1000 / self.speed)
        except Exception as e:
            print(f"Error setting speed: {str(e)}")
            # Set default values if error occurs
            self.speed = 500
            self.animation_duration = 500
            self.animation_frames = 30
            self.animation_speed_factor = 1.0

    # Random
    def generate_random(self):
        if self.sorting:
            messagebox.showwarning("Warning", "Cannot generate new array while sorting is in progress.")
            return
            
        try:
            length = int(self.length_spinbox.get())
            if length < 5 or length > 50:
                messagebox.showerror("Input Error", "Length must be between 5 and 50")
                return
                
            # Clear existing data and animation state
            self.data = []
            self.animation_colors = None
            self.current_step = None
            
            # Generate new data
            self.data = [random.randint(10, 100) for _ in range(length)]
            self.initial_data = self.data.copy()  # Store initial data
            
            # Ensure canvas is ready
            if self.canvas_width == 0 or self.canvas_height == 0:
                self.canvas_width = self.canvas.winfo_width()
                self.canvas_height = self.canvas.winfo_height()
            
            # Draw the bars
            self.root.update_idletasks()  # Ensure canvas is updated
            self.draw_bars(self.data)
            self.status_label.config(text=f"Generated {length} random numbers")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for length")
        except Exception as e:
            print(f"Error generating random array: {str(e)}")
            messagebox.showerror("Error", "Failed to generate random array")

    # Bar color
    def get_bar_color(self, index, color_positions):
        if not color_positions:
            return self.colors['default']
            
        if index in color_positions.get('current', []):
            return self.colors['current']
        elif index in color_positions.get('compare', []):
            return self.colors['compare']
        elif index in color_positions.get('sorted', []):
            return self.colors['sorted']
        elif index in color_positions.get('insert', []):
            return self.colors['insert']
        return self.colors['default']

    # Draw bars
    def draw_bars(self, data, color_positions=None):
        try:
            if not self.canvas.winfo_exists():
                return
                
            self.canvas.delete("all")
            if not data:
                return

            # Ensure we have valid canvas dimensions
            if self.canvas_width <= 0 or self.canvas_height <= 0:
                self.canvas_width = self.canvas.winfo_width()
                self.canvas_height = self.canvas.winfo_height()
                if self.canvas_width <= 0 or self.canvas_height <= 0:
                    return

            # Calculate dimensions
            max_val = max(data)
            if max_val == 0:  # Prevent division by zero
                return

            bar_width = (self.canvas_width - 40) / len(data)  # Leave some padding on sides
            bar_spacing = 2  # Space between bars
            effective_bar_width = max(2, bar_width - bar_spacing)  # Ensure minimum bar width
            top_margin = 60  # Space for text
            bottom_margin = 20
            available_height = self.canvas_height - top_margin - bottom_margin

            # Draw background grid
            grid_spacing = 50
            for i in range(0, self.canvas_height, grid_spacing):
                self.canvas.create_line(20, i, self.canvas_width - 20, i, 
                                      fill="#2E3440" if self.is_dark_theme else "#E5E9F0", 
                                      dash=(2, 4))

            # First pass: draw all bars
            for i, val in enumerate(data):
                x0 = 20 + (i * bar_width)  # Start with padding
                x1 = x0 + effective_bar_width
                y0 = self.canvas_height - bottom_margin
                y1 = y0 - (val / max_val * available_height)

                # Get color based on state
                color = self.get_bar_color(i, color_positions)

                # Draw bar with rounded corners
                self.canvas.create_rectangle(x0, y0, x1, y1, 
                                          fill=color, outline="", width=0)

            # Second pass: draw all text
            for i, val in enumerate(data):
                x0 = 20 + (i * bar_width)
                x1 = x0 + effective_bar_width
                y0 = self.canvas_height - bottom_margin
                y1 = y0 - (val / max_val * available_height)

                # Calculate text positions
                text_x = x0 + (effective_bar_width / 2)
                value_y = max(top_margin, y1 - 10)  # Ensure value text is visible
                step_y = max(top_margin + 20, y1 - 30)  # Ensure step text is visible

                # Add value text with background
                text = str(int(val))
                text_bbox = self.canvas.create_text(text_x, value_y, 
                                                 text=text, 
                                                 fill=self.colors['text'], 
                                                 font=("Segoe UI", 9))
                bbox = self.canvas.bbox(text_bbox)
                if bbox:
                    self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2,
                                              fill=self.colors['text_bg'],
                                              outline="")
                    self.canvas.tag_raise(text_bbox)
                
                # Add step description if available
                if self.current_animation and color_positions and i in color_positions.get('current', []):
                    step_bbox = self.canvas.create_text(text_x, step_y,
                                                      text=self.current_animation,
                                                      fill=self.colors['text'],
                                                      font=("Segoe UI", 8))
                    bbox = self.canvas.bbox(step_bbox)
                    if bbox:
                        self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2,
                                                  fill=self.colors['text_bg'],
                                                  outline="")
                        self.canvas.tag_raise(step_bbox)

            self.root.update_idletasks()
            
        except Exception as e:
            print(f"Error drawing bars: {str(e)}")
            # Don't show error message for drawing errors to avoid spam
            # Just log it and continue

    # Input
    def submit_input(self):
        """
        Handle user input.
        """
        if self.sorting:
            messagebox.showwarning("Warning", "Cannot submit new array while sorting is in progress.")
            return
            
        if not self.parse_input():
            return
            
        # Store the initial data for reference
        self.initial_data = self.data.copy()
        
        # Draw the bars
        self.root.update_idletasks()  # Ensure canvas is updated
        self.draw_bars(self.data)
        self.status_label.config(text=f"Array submitted: {self.data}")
        
        # Enable start button if not already enabled
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for button in child.winfo_children():
                            if isinstance(button, ttk.Button) and button.cget('text') == "Start Sort":
                                button.config(state='normal')

    # Parse
    def parse_input(self):
        """
        Check input.
        """
        raw = self.input_entry.get().strip()
        try:
            if not raw:
                messagebox.showerror("Input Error", "Please enter some numbers.")
                return False
                
            # Split by comma and clean up each number
            numbers = [num.strip() for num in raw.split(',')]
            self.data = []
            
            for num in numbers:
                if not num:
                    continue
                try:
                    value = int(num)
                    if value < 0:
                        messagebox.showerror("Input Error", "Please enter only positive integers.")
                        return False
                    self.data.append(value)
                except ValueError:
                    messagebox.showerror("Input Error", f"Invalid number: {num}")
                    return False
            
            if not self.data:
                messagebox.showerror("Input Error", "Please enter at least one valid number.")
                return False
                
            if len(self.data) > 50:
                messagebox.showerror("Input Error", "Maximum array length is 50 numbers.")
                return False
                
            return True
        except Exception as e:
            messagebox.showerror("Input Error", f"Error parsing input: {str(e)}")
            return False

    # Stats
    def update_statistics(self):
        """
        Update stats.
        """
        self.comparisons_label.config(text=f"Comparisons: {self.comparisons}")
        self.swaps_label.config(text=f"Swaps: {self.swaps}")
        self.iteration_label.config(text=f"Iteration: {self.current_iteration}/{self.total_iterations}")
        self.step_label.config(text=f"Step: {self.current_step_number}/{self.total_steps}")
        self.substep_label.config(text=f"Substep: {self.current_substep}/{self.total_substeps}")
        if self.total_iterations > 0:
            progress = (self.current_iteration / self.total_iterations) * 100
            self.progress_var.set(progress)

    # Reset
    def reset(self):
        """
        Reset everything.
        """
        self.canvas.delete("all")
        if hasattr(self, 'initial_data') and self.initial_data is not None:
            self.data = self.initial_data.copy()
            self.draw_bars(self.data)
        else:
            self.data = []
        self.sorting = False
        self.paused = False
        self.step_by_step = False
        self.current_step_completed = True
        self.current_animation = None
        self.status_label.config(text="")
        self.pause_button.config(text="Pause", state='disabled')
        self.next_step_button.config(state='disabled')
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = 0
        self.step_count = 0
        self.progress_var.set(0)
        self.animation_queue = []  # Clear animation queue
        self.is_animating = False
        self.update_statistics()
        self.step_btn.config(state='normal')  # Enable Step-by-Step after reset

    # Start
    def start_sort(self):
        """
        Start sorting.
        """
        if self.sorting:
            return

        if not self.data:
            if not self.parse_input():
                self.step_btn.config(state='normal')  # Enable Step-by-Step if sorting aborted
                return

        self.sorting = True
        self.pause_button.config(state='normal')
        self.next_step_button.config(state='disabled')
        self.status_label.config(text="Sorting in progress...")
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = len(self.data)
        self.current_step_completed = True
        self.step_history = []  # Clear step history
        
        # Initialize step counters
        self.current_step_number = 0
        self.current_substep = 0
        self.total_steps = 0
        self.total_substeps = 0
        
        self.update_statistics()
        self.step_btn.config(state='disabled')  # Disable Step-by-Step when sorting starts
        if self.step_by_step:
            self.step_i = 1
            self.step_j = None
            self.step_current = None
            self.step_mode = 'select'  # select, compare, shift, insert, complete
            self.paused = True
            self.pause_button.config(text="Resume", state='disabled')
            self.next_step_button.config(state='normal')
            self.step_by_step_sort()
        else:
            self.step_by_step = False  # disable step-by-step if normal sorting
            self.next_step_button.config(state='disabled')
            self.pause_button.config(text="Pause", state='normal')
            self.insertion_sort(1)

    # Pause
    def toggle_pause(self):
        """
        Pause or resume.
        """
        if not self.sorting:
            return
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        # Always disable step-by-step button during automatic sorting
        if hasattr(self, 'step_btn'):
            self.step_btn.config(state='disabled')
        if not self.paused and not self.step_by_step:
            # If an animation is in paused and press resume, continue it
            if self.is_animating:
                self.animate_frame()
            elif self.animation_queue:
                self.process_animation_queue()
            else:
                # If nothing is animating or queued, continue sorting
                self.insertion_sort(self.current_iteration)

    # Step by step mode
    def toggle_step_by_step(self):
        # Only allow clicking if not currently sorting
        if self.sorting:
            messagebox.showinfo("Info", "Cannot use Step-by-Step mode while automatic sorting is in progress.")
            return
        self.step_by_step = not self.step_by_step
        if self.step_by_step:
            self.status_label.config(text="Step-by-Step mode enabled - Press 'Start' button to start sorting and 'Next Step' to proceed")
            self.paused = True
            self.pause_button.config(text="Resume", state='disabled')
            self.next_step_button.config(state='normal')
        else:
            self.status_label.config(text="Step-by-Step mode disabled")
            self.pause_button.config(text="Pause", state='normal')
            self.next_step_button.config(state='disabled')

    # Theme
    def toggle_theme(self):
        """
        Switch theme.
        """
        try:
            self.is_dark_theme = not self.is_dark_theme
            self.configure_style()  # Update colors based on theme
            self.canvas.config(bg="#3B4252" if self.is_dark_theme else "#ECEFF4")
            self.status_label.config(foreground="#A3BE8C" if self.is_dark_theme else "#2E3440")
            if self.data:  # Redraw with new theme
                self.draw_bars(self.data, self.animation_colors)
        except Exception as e:
            print(f"Error toggling theme: {str(e)}")
            messagebox.showerror("Error", "Failed to switch theme")

    # Color mix
    def interpolate_color(self, color1, color2, factor):
        """
        Mix two colors.
        """
        # Check cache first
        cache_key = (color1, color2, factor)
        if cache_key in self._cached_colors:
            return self._cached_colors[cache_key]

        # Convert hex colors to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

        # Convert colors to RGB
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        # Interpolate each component
        r = rgb1[0] + (rgb2[0] - rgb1[0]) * factor
        g = rgb1[1] + (rgb2[1] - rgb1[1]) * factor
        b = rgb1[2] + (rgb2[2] - rgb1[2]) * factor

        result = rgb_to_hex((r, g, b))
        self._cached_colors[cache_key] = result
        return result

    # Easing
    def ease_in_out_quad(self, t):
        """
        Smooth easing.
        """
        return t * t * (3 - 2 * t)

    # Queue anim
    def queue_animation(self, start_data, end_data, colors, animation_type, step_description=None):
        """
        Add animation step.
        """
        # Ensure colors are properly copied and maintained
        colors_copy = {}
        for key, value in colors.items():
            if isinstance(value, list):
                colors_copy[key] = value.copy()
            else:
                colors_copy[key] = value

        # Create deep copies of the data
        start_data_copy = start_data.copy()
        end_data_copy = end_data.copy()

        animation = {
            'start_data': start_data_copy,
            'end_data': end_data_copy,
            'colors': colors_copy,
            'type': animation_type,
            'step': step_description
        }
        
        # Store step in history for step-by-step mode
        if self.step_by_step:
            # Increment step counters before storing history
            self.current_step_number += 1
            self.current_substep += 1
            self.total_steps = max(self.total_steps, self.current_step_number)
            self.total_substeps = max(self.total_substeps, self.current_substep)
            
            self.step_history.append({
                'data': start_data_copy,
                'step_i': getattr(self, 'step_i', 0),
                'step_j': getattr(self, 'step_j', 0),
                'step_current': getattr(self, 'step_current', 0),
                'step_mode': getattr(self, 'step_mode', ''),
                'step_number': self.current_step_number,
                'substep': self.current_substep,
                'comparisons': self.comparisons,
                'swaps': self.swaps,
                'description': step_description
            })
        
        self.animation_queue.append(animation)
        self.step_count += 1
        self.update_statistics()
        
        if not self.is_animating:
            self.process_animation_queue()

    # Process anim
    def process_animation_queue(self):
        """
        Run next animation.
        """
        if not self.animation_queue:
            self.is_animating = False
            # Don't automatically continue in step-by-step mode
            # Let the user control it with the next button
            return

        self.is_animating = True
        animation = self.animation_queue.pop(0)
        self.animate_transition(
            animation['start_data'],
            animation['end_data'],
            animation['colors'],
            animation['type'],
            animation['step']
        )

    # Animate
    def animate_transition(self, start_data, end_data, colors, animation_type, step_description=None):
        """
        Animate data.
        """
        self.animation_data = (start_data, end_data)
        self.animation_colors = colors
        self.animation_type = animation_type
        self.current_frame = 0
        self.current_animation = step_description
        if step_description:
            self.current_step = step_description
        self.animate_frame()

    # Frame
    def animate_frame(self):
        """
        Draw animation frame.
        """
        if self.paused and not self.step_by_step:
            return
            
        if self.current_frame >= self.animation_frames:
            self.draw_bars(self.animation_data[1], self.animation_colors)
            self.current_step_completed = True
            
            if self.step_by_step:
                self.paused = True
                # Ensure we show the final state before moving to next step
                self.draw_bars(self.animation_data[1], self.animation_colors)
                # Don't automatically continue to next iteration in step-by-step mode
                # Let the user control it with the next button
            elif not self.paused:
                self.root.after(50, self.process_animation_queue)
            return

        # Frame rate limiting
        current_time = time.time() * 1000
        elapsed = current_time - self._last_draw_time
        if elapsed < self._min_frame_time:
            if not self.paused or self.step_by_step:
                self.root.after(int(self._min_frame_time - elapsed), self.animate_frame)
            return

        start_data, end_data = self.animation_data
        factor = self.current_frame / self.animation_frames

        # Interpolate between start and end positions
        current_data = []
        for i in range(len(start_data)):
            if self.animation_type == "move":
                # Use easing function for smoother movement
                eased_factor = self.ease_in_out_quad(factor)
                current_data.append(start_data[i] + (end_data[i] - start_data[i]) * eased_factor)
            else:
                current_data.append(start_data[i] + (end_data[i] - start_data[i]) * factor)

        # Use the same color positions throughout the animation
        self.draw_bars(current_data, self.animation_colors)
        self.current_frame += 1
        self._last_draw_time = current_time
        
        # Calculate next frame delay based on speed
        next_frame_delay = int(self._min_frame_time * self.animation_speed_factor)
        if not self.paused or self.step_by_step:
            self.root.after(next_frame_delay, self.animate_frame)

    # Sort step
    def insertion_sort(self, i):
        """
        Do one sort step.
        """
        if not self.sorting:
            return

        if i >= len(self.data):
            self.queue_animation(
                self.data.copy(), 
                self.data.copy(),
                {"sorted": list(range(len(self.data)))},
                "color",
                "Sorting Complete"
            )
            self.status_label.config(text=f"Sorted: {self.data}")
            self.sorting = False
            self.pause_button.config(state='disabled')
            self.next_step_button.config(state='disabled')
            self.step_btn.config(state='normal')  # Enable Step-by-Step after sorting
            return

        if self.paused and not self.step_by_step:
            self.root.after(100, lambda: self.insertion_sort(i))
            return

        current = self.data[i]
        j = i - 1
        self.current_iteration = i
        self.current_step_completed = False
        self.update_statistics()

        # Step 1: Highlight current element
        step_desc = f"Step {i}: Selecting element {current} at position {i}"
        self.queue_animation(
            self.data.copy(),
            self.data.copy(),
            {"current": [i], "sorted": list(range(i))},
            "color",
            step_desc
        )

        if self.step_by_step:
            self.paused = True
            self.status_label.config(text=step_desc)
            return

        # Step 2: Start comparison loop
        while j >= 0:
            self.comparisons += 1
            self.update_statistics()

            # Step 2.1: Show comparison
            step_desc = f"Step {i}.{j}: Comparing {current} with {self.data[j]} at position {j}"
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [i], "compare": [j], "sorted": list(range(i))},
                "color",
                step_desc
            )

            if self.step_by_step:
                self.paused = True
                self.status_label.config(text=step_desc)
                return

            # Step 2.2: Check if we need to shift
            if self.data[j] > current:
                # Step 2.2.1: Show that we need to shift
                step_desc = f"Step {i}.{j}: {self.data[j]} > {current}, need to shift {self.data[j]} right"
                self.queue_animation(
                    self.data.copy(),
                    self.data.copy(),
                    {"current": [i], "compare": [j], "sorted": list(range(i))},
                    "color",
                    step_desc
                )

                if self.step_by_step:
                    self.paused = True
                    self.status_label.config(text=step_desc)
                    return

                # Step 2.2.2: Perform the shift
                new_data = self.data.copy()
                new_data[j + 1] = self.data[j]
                step_desc = f"Step {i}.{j}: Shifting {self.data[j]} from position {j} to {j+1}"
                self.queue_animation(
                    self.data.copy(),
                    new_data,
                    {"current": [i], "compare": [j], "sorted": list(range(i))},
                    "move",
                    step_desc
                )

                if self.step_by_step:
                    self.paused = True
                    self.status_label.config(text=step_desc)
                    return

                # Step 2.2.3: Update the data
                self.data[j + 1] = self.data[j]
                j -= 1
                self.swaps += 1
                self.update_statistics()
            else:
                # Step 2.3: Show that we found the correct position
                step_desc = f"Step {i}.{j}: {self.data[j]} <= {current}, found insertion point"
                self.queue_animation(
                    self.data.copy(),
                    self.data.copy(),
                    {"current": [i], "compare": [j], "sorted": list(range(i))},
                    "color",
                    step_desc
                )
                break

            if self.step_by_step:
                self.paused = True
                self.status_label.config(text=step_desc)
                return

            if self.paused and not self.step_by_step:
                self.root.after(100, lambda: self.insertion_sort(i))
                return

        # Step 3: Show insertion point
        step_desc = f"Step {i}.{j+1}: Found insertion point at position {j+1} for element {current}"
        self.queue_animation(
            self.data.copy(),
            self.data.copy(),
            {"current": [i], "insert": [j + 1], "sorted": list(range(i))},
            "color",
            step_desc
        )

        if self.step_by_step:
            self.paused = True
            self.status_label.config(text=step_desc)
            return

        # Step 4: Insert the current element
        new_data = self.data.copy()
        new_data[j + 1] = current
        step_desc = f"Step {i}.{j+1}: Inserting {current} at position {j+1}"
        self.queue_animation(
            self.data.copy(),
            new_data,
            {"current": [i], "insert": [j + 1], "sorted": list(range(i))},
            "move",
            step_desc
        )

        if self.step_by_step:
            self.paused = True
            self.status_label.config(text=step_desc)
            return

        # Step 5: Update the data
        self.data[j + 1] = current
        self.swaps += 1
        self.update_statistics()

        # Step 6: Show completion
        step_desc = f"Step {i}: Completed insertion of {current} at position {j+1}"
        self.queue_animation(
            self.data.copy(),
            self.data.copy(),
            {"sorted": list(range(i + 1))},
            "color",
            step_desc
        )

        if self.step_by_step:
            self.paused = True
            self.status_label.config(text=step_desc)
            # Ensure we show the final state before moving to next iteration
            self.draw_bars(self.data.copy(), {"sorted": list(range(i + 1))})
            # Move to next iteration after completing current element
            self.current_iteration = i + 1
            return

        # Continue with next element
        self.root.after(self.speed, lambda: self.insertion_sort(i + 1))

    # Resize
    def on_canvas_resize(self, event):
        """
        Redraw bars.
        """
        try:
            # Update canvas dimensions
            self.canvas_width = max(100, event.width)  # Ensure minimum width
            self.canvas_height = max(100, event.height)  # Ensure minimum height
            
            # Redraw if we have data
            if self.data:
                self.root.after(100, lambda: self.draw_bars(self.data, self.animation_colors))
        except Exception as e:
            print(f"Error during canvas resize: {str(e)}")

    # Next
    def next_step(self):
        """
        Next step.
        """
        if not self.sorting or not self.step_by_step:
            return
        
        # If there are animations in queue, process them first
        if self.animation_queue:
            self.paused = False
            self.process_animation_queue()
        else:
            # If no animations, advance to next step
            self.step_by_step_sort()

    # Step sort
    def step_by_step_sort(self):
        """
        Step-by-step sort.
        """
        # If sorting is done
        if not self.sorting or self.step_i >= len(self.data):
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"sorted": list(range(len(self.data)))},
                "color",
                "Sorting Complete"
            )
            self.status_label.config(text=f"Sorting Complete! Final array: {self.data}")
            self.sorting = False
            self.pause_button.config(state='disabled')
            self.next_step_button.config(state='disabled')
            self.step_btn.config(state='normal')  # Enable Step-by-Step after sorting
            return

        # Step 1: Select current element
        if self.step_mode == 'select':
            self.step_current = self.data[self.step_i]
            self.step_j = self.step_i - 1
            self.current_iteration = self.step_i
            
            step_desc = f"Step {self.step_i}: Selecting element {self.step_current} at position {self.step_i}"
            
            # Queue animation instead of direct draw
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [self.step_i], "sorted": list(range(self.step_i))},
                "color",
                step_desc
            )
            
            self.status_label.config(text=step_desc)
            self.step_mode = 'compare'
            return

        # Step 2: Compare
        if self.step_mode == 'compare':
            if self.step_j >= 0:
                self.comparisons += 1
                
                step_desc = f"Step {self.step_i}.{self.step_j}: Comparing {self.step_current} with {self.data[self.step_j]} at position {self.step_j}"
                
                # Queue animation instead of direct draw
                self.queue_animation(
                    self.data.copy(),
                    self.data.copy(),
                    {"current": [self.step_i], "compare": [self.step_j], "sorted": list(range(self.step_i))},
                    "color",
                    step_desc
                )
                
                self.status_label.config(text=step_desc)
                
                if self.data[self.step_j] > self.step_current:
                    self.step_mode = 'shift'
                else:
                    self.step_mode = 'insert_point'
                return
            else:
                self.step_mode = 'insert_point'
                self.step_by_step_sort()
                return

        # Step 3: Shift
        if self.step_mode == 'shift':
            step_desc = f"Step {self.step_i}.{self.step_j}: {self.data[self.step_j]} > {self.step_current}, need to shift {self.data[self.step_j]} right"
            
            # Queue animation instead of direct draw
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [self.step_i], "compare": [self.step_j], "sorted": list(range(self.step_i))},
                "color",
                step_desc
            )
            
            self.status_label.config(text=step_desc)
            self.step_mode = 'shift_move'
            return
            
        if self.step_mode == 'shift_move':
            # Create new data with the shift
            new_data = self.data.copy()
            new_data[self.step_j + 1] = self.data[self.step_j]
            
            step_desc = f"Step {self.step_i}.{self.step_j}: Shifting {self.data[self.step_j]} from position {self.step_j} to {self.step_j+1}"
            
            # Queue animation with movement
            self.queue_animation(
                self.data.copy(),
                new_data,
                {"current": [self.step_i], "compare": [self.step_j], "sorted": list(range(self.step_i))},
                "move",
                step_desc
            )
            
            # Update the actual data
            self.data[self.step_j + 1] = self.data[self.step_j]
            self.swaps += 1
            
            self.status_label.config(text=step_desc)
            self.step_j -= 1
            self.step_mode = 'compare'
            return

        # Step 4: Insert point
        if self.step_mode == 'insert_point':
            step_desc = f"Step {self.step_i}.{self.step_j+1}: Found insertion point at position {self.step_j+1} for element {self.step_current}"
            
            # Queue animation instead of direct draw
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [self.step_i], "insert": [self.step_j + 1], "sorted": list(range(self.step_i))},
                "color",
                step_desc
            )
            
            self.status_label.config(text=step_desc)
            self.step_mode = 'insert'
            return
            
        # Step 5: Insert
        if self.step_mode == 'insert':
            # Create new data with the insertion
            new_data = self.data.copy()
            new_data[self.step_j + 1] = self.step_current
            
            step_desc = f"Step {self.step_i}.{self.step_j+1}: Inserting {self.step_current} at position {self.step_j+1}"
            
            # Queue animation with movement
            self.queue_animation(
                self.data.copy(),
                new_data,
                {"current": [self.step_i], "insert": [self.step_j + 1], "sorted": list(range(self.step_i))},
                "move",
                step_desc
            )
            
            # Update the actual data
            self.data[self.step_j + 1] = self.step_current
            self.swaps += 1
            
            self.status_label.config(text=step_desc)
            self.step_mode = 'complete'
            return
            
        # Step 6: Complete
        if self.step_mode == 'complete':
            step_desc = f"Step {self.step_i}: Completed insertion of {self.step_current} at position {self.step_j+1}"
            
            # Queue animation instead of direct draw
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"sorted": list(range(self.step_i + 1))},
                "color",
                step_desc
            )
            
            self.status_label.config(text=step_desc)
            self.step_i += 1
            self.step_mode = 'select'
            return

    # Close
    def close_window(self):
        """
        Close the app.
        """
        try:
            # Clear any pending animations
            if hasattr(self, 'animation_timer') and self.animation_timer:
                self.root.after_cancel(self.animation_timer)
                self.animation_timer = None
            
            # Clear animation queue
            self.animation_queue.clear()
            self.is_animating = False
            
            if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
                self.root.destroy()
        except Exception as e:
            print(f"Error during window close: {str(e)}")
            self.root.destroy()

if __name__ == "__main__":
    main()

    # --- Step-by-step mode quick test/demo ---
    # To use, uncomment the following lines and run this file.
    # It will automatically enable step-by-step mode, start sorting, and perform a few steps.
    #
    # import time
    # app.toggle_step_by_step()
    # app.data = [64, 34, 25, 12, 22, 11, 90]
    # app.initial_data = app.data.copy()
    # app.draw_bars(app.data)
    # app.start_sort()
    # for _ in range(5):
    #     app.next_step()
    #     root.update()
    #     time.sleep(0.5)
    # print("Step-by-step demo complete. You can now interact with the GUI.")
   