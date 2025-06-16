import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<Motion>", self.motion)
        self.after_id = None
        self.last_x = 0
        self.last_y = 0

    def enter(self, event=None):
        self.last_x = event.x_root
        self.last_y = event.y_root
        self.schedule_tooltip()

    def motion(self, event=None):
        # Only update if mouse has moved significantly
        if abs(event.x_root - self.last_x) > 5 or abs(event.y_root - self.last_y) > 5:
            self.last_x = event.x_root
            self.last_y = event.y_root
            if self.tooltip:
                self.update_tooltip_position()

    def schedule_tooltip(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
        self.after_id = self.widget.after(100, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2)
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(self.tooltip, style="Tooltip.TFrame")
        frame.pack()
        
        label = ttk.Label(frame, text=self.text, style="Tooltip.TLabel")
        label.pack(padx=5, pady=2)

    def update_tooltip_position(self):
        if not self.tooltip:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2)
        self.tooltip.wm_geometry(f"+{x}+{y}")

    def leave(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class InsertionSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Insertion Sort Visualizer")
        # Set window to full screen and disable restore down
        self.root.state('zoomed')  # For Windows
        self.root.attributes('-fullscreen', True)  # For cross-platform support
        self.root.minsize(800, 500)
        
        # Default theme is dark
        self.is_dark_theme = True
        
        # Canvas dimensions - will be updated in build_ui
        self.canvas_width = 0
        self.canvas_height = 0
        self.speed = 100
        self.data = []
        self.initial_data = None  # Store initial data
        self.paused = False
        self.sorting = False
        self.step_by_step = False
        self.current_step_completed = True  # Track if current step is completed
        self.current_animation = None  # Track current animation
        
        # Statistics
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = 0
        self.step_count = 0  # Track total steps taken
        
        # Animation properties
        self.animation_frames = 30
        self.current_frame = 0
        self.animation_data = None
        self.animation_type = None
        self.animation_colors = None
        self.current_step = None
        self.animation_queue = []
        self.is_animating = False
        self.animation_speed_factor = 1.0
        self.animation_start_time = 0
        self.animation_duration = 500  # 500ms for each animation
        self.animation_timer = None  # Store animation timer ID
        
        # Performance optimization
        self._cached_colors = {}
        self._last_draw_time = 0
        self._min_frame_time = 16  # ~60 FPS
        self._target_fps = 60
        self._frame_time = 1000 / self._target_fps
        
        # Sorting state
        self.sorting_state = {
            'current_i': 0,
            'current_j': 0,
            'current_element': None,
            'is_comparing': False,
            'is_moving': False
        }
        
        # Color definitions - using more vibrant colors
        self.colors = {
            'default': "#5E81AC",    # Brighter blue for unsorted
            'current': "#FFD700",    # Bright yellow for current
            'compare': "#FF6B6B",    # Bright red for comparison
            'sorted': "#98FB98",     # Bright green for sorted
            'insert': "#87CEEB",     # Sky blue for insertion
            'text': "#FFFFFF",       # White text
            'text_bg': "#2E3440"     # Dark background for text
        }

        self.style = ttk.Style()
        self.configure_style()

        self.current_step_number = 0  # Track current step number
        self.total_steps = 0  # Track total steps
        self.step_history = []  # Store step history
        self.current_substep = 0  # Track current substep
        self.total_substeps = 0  # Track total substeps
        
        # Initialize UI elements
        self.speed_indicator = None
        self.prev_step_button = None
        self.next_step_button = None
        self.step_label = None
        self.substep_label = None

        self.build_ui()

    def configure_style(self):
        self.style.theme_use('clam')
        
        if self.is_dark_theme:
            # Dark theme colors
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
            
            # Enhanced radio button styling for dark theme
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
            # Light theme colors
            bg_color = "#F5F5F5"
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
            
            # Enhanced radio button styling for light theme
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
        self.add_tooltip(self.input_entry, "Enter a comma-separated list of integers")
        
        # Add submit button for user input
        submit_btn = ttk.Button(input_frame, text="Submit", command=self.submit_input)
        submit_btn.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(submit_btn, "Submit your array for sorting")
        
        # Bind Enter key to submit
        self.input_entry.bind('<Return>', lambda e: self.submit_input())

        # Random generation section
        random_frame = ttk.Frame(control_frame)
        random_frame.pack(side=tk.LEFT, padx=20)
        
        self.length_spinbox = ttk.Spinbox(random_frame, from_=5, to=50, width=5)
        self.length_spinbox.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(self.length_spinbox, "Set the length for random list generation")
        self.length_spinbox.bind('<Return>', lambda e: self.generate_random())

        generate_btn = ttk.Button(random_frame, text="Generate Random", command=self.generate_random)
        generate_btn.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(generate_btn, "Click to generate a random list")

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
            self.add_tooltip(radio, f"Set animation speed to {text.lower()}")
        
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
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<r>', lambda e: self.reset())
        self.root.bind('<s>', lambda e: self.start_sort())
        self.root.bind('<t>', lambda e: self.toggle_theme())
        self.root.bind('<b>', lambda e: self.toggle_step_by_step())
        self.root.bind('<n>', lambda e: self.next_step())  # Add keyboard shortcut for next step

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
        
        start_btn = ttk.Button(left_buttons, text="Start Sort (S)", command=self.start_sort)
        start_btn.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(start_btn, "Start sorting (Shortcut: S)")
        
        self.pause_button = ttk.Button(left_buttons, text="Pause (Space)", command=self.toggle_pause, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(self.pause_button, "Pause/Resume sorting (Shortcut: Space)")
        
        reset_btn = ttk.Button(left_buttons, text="Reset (R)", command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(reset_btn, "Reset visualization (Shortcut: R)")
        
        step_btn = ttk.Button(left_buttons, text="Step-by-Step (B)", command=self.toggle_step_by_step)
        step_btn.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(step_btn, "Toggle step-by-step mode (Shortcut: B)")

        # Add step navigation buttons
        step_nav_frame = ttk.Frame(left_buttons)
        step_nav_frame.pack(side=tk.LEFT, padx=20)
        
        self.next_step_button = ttk.Button(step_nav_frame, text="Next Step (N)", command=self.next_step)
        self.next_step_button.pack(side=tk.LEFT, padx=5)
        self.add_tooltip(self.next_step_button, "Proceed to next step (Shortcut: N)")

        # Right side theme toggle
        self.theme_button = ttk.Button(button_frame, text="Switch Theme (T)", command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT, padx=5)
        self.add_tooltip(self.theme_button, "Switch between light and dark themes (Shortcut: T)")

        # Add close button
        close_btn = ttk.Button(button_frame, text="Close Window", command=self.close_window)
        close_btn.pack(side=tk.RIGHT, padx=5)
        self.add_tooltip(close_btn, "Close the application")

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                    text="",
                                    font=("Segoe UI", 11, "bold"),
                                    foreground="#A3BE8C" if self.is_dark_theme else "#2E3440")
        self.status_label.pack(side=tk.LEFT)

        # Add keyboard shortcuts help
        shortcuts_frame = ttk.Frame(main_frame)
        shortcuts_frame.pack(fill=tk.X, pady=(5, 0))
        shortcuts_text = "Keyboard Shortcuts: Space (Pause/Resume) | S (Start) | R (Reset) | T (Theme) | B (Step-by-Step) | N (Next Step)"
        ttk.Label(shortcuts_frame, text=shortcuts_text, font=("Segoe UI", 8)).pack(side=tk.LEFT)

    def update_speed(self, val):
        try:
            speed_val = float(val)
            if speed_val <= 0.2:
                self.speed = 5
                self.speed_indicator.config(text="Speed: Fastest")
            elif speed_val <= 0.5:
                self.speed = 100
                self.speed_indicator.config(text="Speed: Fast")
            elif speed_val <= 0.8:
                self.speed = 500
                self.speed_indicator.config(text="Speed: Normal")
            else:
                self.speed = 2000
                self.speed_indicator.config(text="Speed: Slow")
        except Exception:
            pass

    def set_speed(self, speed_value, speed_text):
        """Set the animation speed and update the speed label."""
        self.speed = speed_value
        self.speed_indicator.config(text=f"Speed: {speed_text}")
        # Adjust animation duration based on speed
        self.animation_duration = max(200, min(1000, int(1000 * (speed_value / 500))))
        # Adjust animation frames based on duration
        self.animation_frames = max(15, min(60, int(self.animation_duration / self._frame_time)))

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

    def add_tooltip(self, widget, text):
        Tooltip(widget, text)

    def submit_input(self):
        """Handle user input submission."""
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
                            if isinstance(button, ttk.Button) and button.cget('text') == "Start Sort (S)":
                                button.config(state='normal')

    def parse_input(self):
        """Parse and validate user input."""
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

    def update_statistics(self):
        self.comparisons_label.config(text=f"Comparisons: {self.comparisons}")
        self.swaps_label.config(text=f"Swaps: {self.swaps}")
        self.iteration_label.config(text=f"Iteration: {self.current_iteration}/{self.total_iterations}")
        self.step_label.config(text=f"Step: {self.current_step_number}/{self.total_steps}")
        self.substep_label.config(text=f"Substep: {self.current_substep}/{self.total_substeps}")
        if self.total_iterations > 0:
            progress = (self.current_iteration / self.total_iterations) * 100
            self.progress_var.set(progress)

    def reset(self):
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

    def start_sort(self):
        """Start the sorting process."""
        if self.sorting:
            return

        if not self.data:
            if not self.parse_input():
                return

        # Clear any existing animations and state
        self.animation_queue.clear()
        self.is_animating = False
        self.current_step_completed = True

        # Store the initial data for reference
        self.initial_data = self.data.copy()
        self.sorting = True
        self.pause_button.config(state='normal')
        self.status_label.config(text="Sorting in progress...")
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = len(self.data)
        self.update_statistics()
        
        # Reset sorting state
        self.sorting_state = {
            'current_i': 1,  # Start from second element
            'current_j': 0,
            'current_element': None,
            'is_comparing': False,
            'is_moving': False
        }
        
        self.continue_sorting()

    def toggle_pause(self):
        if not self.sorting:
            return
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused and not self.step_by_step:
            if self.animation_queue:
                self.process_animation_queue()
            self.root.after(self.speed, lambda: self.continue_sorting())

    def toggle_step_by_step(self):
        self.step_by_step = not self.step_by_step
        if self.step_by_step:
            self.status_label.config(text="Step-by-Step mode enabled - Press 'Next Step' to proceed")
            if self.sorting and not self.paused:
                self.paused = True
                self.current_step_completed = True
        else:
            self.status_label.config(text="Step-by-Step mode disabled")
            if self.sorting:
                self.paused = False
                if self.animation_queue:
                    self.process_animation_queue()
                self.root.after(self.speed, lambda: self.continue_sorting())

    def toggle_theme(self):
        try:
            self.is_dark_theme = not self.is_dark_theme
            self.configure_style()  # Update styles based on theme
            self.canvas.config(bg="#3B4252" if self.is_dark_theme else "#ECEFF4")
            self.status_label.config(foreground="#A3BE8C" if self.is_dark_theme else "#2E3440")
            if self.data:  # Redraw with new theme
                self.draw_bars(self.data, self.animation_colors)
        except Exception as e:
            print(f"Error toggling theme: {str(e)}")
            messagebox.showerror("Error", "Failed to switch theme")

    def interpolate_color(self, color1, color2, factor):
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

    def queue_animation(self, start_data, end_data, colors, animation_type, step_description=None):
        """Queue an animation to be played."""
        animation = {
            'start_data': start_data.copy(),
            'end_data': end_data.copy(),
            'colors': colors.copy(),
            'type': animation_type,
            'step': step_description
        }
        
        self.animation_queue.append(animation)
        
        if not self.is_animating:
            self._process_next_animation()

    def _process_next_animation(self):
        """Process the next animation in the queue."""
        if not self.animation_queue or self.is_animating:
            return

        animation = self.animation_queue.pop(0)
        
        def on_complete():
            if animation['type'] == 'move':
                self.data = animation['end_data'].copy()
            self.is_animating = False
            if self.animation_queue:
                self.root.after(50, self._process_next_animation)
            elif self.step_by_step:
                self.paused = True
                self.current_step_completed = True

        self.animate_transition(
            animation['start_data'],
            animation['end_data'],
            animation['colors'],
            animation['type'],
            animation['step'],
            on_complete
        )

    def _validate_data(self, data, operation="unknown"):
        """Validate data integrity before any operation."""
        try:
            if not isinstance(data, list):
                print(f"Error in {operation}: data is not a list")
                return False
                
            if not data:
                print(f"Error in {operation}: data is empty")
                return False
                
            if not all(isinstance(x, (int, float)) for x in data):
                print(f"Error in {operation}: data contains non-numeric values")
                return False
                
            if len(data) != len(self.data):
                print(f"Error in {operation}: data length mismatch")
                return False
                
            # Validate data values
            if not all(0 <= x <= 100 for x in data):
                print(f"Error in {operation}: data values must be between 0 and 100")
                return False
                
            return True
        except Exception as e:
            print(f"Error in {operation}: {str(e)}")
            return False

    def _validate_indices(self, i, j, operation="unknown"):
        """Validate array indices before any operation."""
        try:
            if not isinstance(i, int) or not isinstance(j, int):
                print(f"Error in {operation}: invalid index types")
                return False
                
            # Allow j to be -1 for insertion at the beginning
            if i < 0 or i >= len(self.data):
                print(f"Error in {operation}: index i out of bounds")
                return False
                
            if j < -1 or j >= len(self.data):
                print(f"Error in {operation}: index j out of bounds")
                return False
                
            # Validate index relationship
            if j >= i:
                print(f"Error in {operation}: invalid index relationship (j >= i)")
                return False
                
            return True
        except Exception as e:
            print(f"Error in {operation}: {str(e)}")
            return False

    def _validate_state(self, operation="unknown"):
        """Validate the current state of the visualizer."""
        try:
            if not hasattr(self, 'data') or not self.data:
                print(f"Error in {operation}: no data available")
                return False
                
            # Only check sorting state for operations that require active sorting
            if operation in ["_compare_and_shift", "_insert_element", "_process_current_element", "_complete_sorting"]:
                if not hasattr(self, 'sorting') or not self.sorting:
                    print(f"Error in {operation}: sorting not active")
                    return False
                    
                if not hasattr(self, 'sorting_state'):
                    print(f"Error in {operation}: sorting state not initialized")
                    return False
                    
                # Validate sorting state
                required_keys = ['current_i', 'current_j', 'current_element', 'is_comparing', 'is_moving']
                if not all(key in self.sorting_state for key in required_keys):
                    print(f"Error in {operation}: invalid sorting state")
                    return False
                
            return True
        except Exception as e:
            print(f"Error in {operation}: {str(e)}")
            return False

    def animate_transition(self, start_data, end_data, colors, animation_type, step_description=None, on_complete=None):
        """Start a new animation transition with validation."""
        if not self._validate_data(start_data, "animate_transition start") or not self._validate_data(end_data, "animate_transition end"):
            print("Animation cancelled due to data validation failure")
            return

        if self.is_animating:
            self.animation_queue.append({
                'start_data': start_data.copy(),
                'end_data': end_data.copy(),
                'colors': colors.copy(),
                'type': animation_type,
                'step': step_description,
                'on_complete': on_complete
            })
            return

        self.animation_data = (start_data.copy(), end_data.copy())
        self.animation_colors = colors.copy()
        self.animation_type = animation_type
        self.current_frame = 0
        self.current_animation = step_description
        self.on_complete = on_complete
        self.animation_start_time = time.time() * 1000
        self.is_animating = True

        if step_description:
            self.current_step = step_description

        self.draw_bars(start_data, colors)
        self.root.update_idletasks()
        self.animate_frame()

    def animate_frame(self):
        """Animate a single frame of the current transition."""
        if not self.is_animating:
            return

        current_time = time.time() * 1000
        elapsed = current_time - self.animation_start_time

        if elapsed >= self.animation_duration:
            # Ensure we show the final state
            self.draw_bars(self.animation_data[1], self.animation_colors)
            self.current_step_completed = True
            self.is_animating = False

            # Call on_complete callback if provided
            if self.on_complete:
                self.on_complete()

            # Process next animation in queue
            if self.animation_queue:
                self.root.after(50, self._process_next_animation)
            elif self.step_by_step:
                self.paused = True
                self.current_step_completed = True
            return

        # Calculate progress based on elapsed time
        progress = min(1.0, elapsed / self.animation_duration)

        # Frame rate limiting
        if current_time - self._last_draw_time < self._frame_time:
            self.root.after(int(self._frame_time - (current_time - self._last_draw_time)), self.animate_frame)
            return

        start_data, end_data = self.animation_data

        # Interpolate between start and end positions
        current_data = []
        for i in range(len(start_data)):
            if self.animation_type == "move":
                # Use easing function for smoother movement
                eased_progress = self.ease_in_out_quad(progress)
                current_data.append(start_data[i] + (end_data[i] - start_data[i]) * eased_progress)
            else:
                current_data.append(start_data[i])

        # Use the same color positions throughout the animation
        self.draw_bars(current_data, self.animation_colors)
        self._last_draw_time = current_time

        # Schedule next frame
        self.root.after(int(self._frame_time), self.animate_frame)

    def ease_in_out_quad(self, t):
        """Smooth easing function for animations."""
        t = max(0, min(1, t))  # Clamp t between 0 and 1
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    def validate_sorted_section(self, data):
        """Validate if the array is properly sorted."""
        try:
            if not isinstance(data, list):
                print(f"Error: data is not a list")
                return False
                
            if not data:
                print(f"Error: data is empty")
                return False
                
            if not all(isinstance(x, (int, float)) for x in data):
                print(f"Error: data contains non-numeric values")
                return False
                
            # Check if array is sorted
            for i in range(1, len(data)):
                if data[i-1] > data[i]:
                    print(f"Error: Array not sorted at index {i} ({data[i-1]} > {data[i]})")
                    return False
                    
            # For partial sorted sections, only validate that the elements exist in the original array
            if len(data) < len(self.initial_data):
                # Check if all elements in the sorted section exist in the original array
                original_elements = set(self.initial_data)
                current_elements = set(data)
                if not current_elements.issubset(original_elements):
                    print("Error: Sorted section contains elements not in original array")
                    print(f"Original elements: {original_elements}")
                    print(f"Current elements: {current_elements}")
                    return False
            else:
                # For complete array, validate that all elements are preserved
                if sorted(data) != sorted(self.initial_data):
                    print("Error: Array elements changed during sorting")
                    print(f"Original: {self.initial_data}")
                    print(f"Current: {data}")
                    return False
                
            return True
        except Exception as e:
            print(f"Error in validate_sorted_section: {str(e)}")
            return False

    def on_canvas_resize(self, event):
        try:
            # Update canvas dimensions
            self.canvas_width = max(100, event.width)  # Ensure minimum width
            self.canvas_height = max(100, event.height)  # Ensure minimum height
            
            # Redraw if we have data
            if self.data:
                self.root.after(100, lambda: self.draw_bars(self.data, self.animation_colors))
        except Exception as e:
            print(f"Error during canvas resize: {str(e)}")

    def next_step(self):
        """Proceed to the next step in the sorting process."""
        if not self.sorting or not self.step_by_step:
            return
            
        if not self.current_step_completed:
            return
            
        self.paused = False
        self.current_step_completed = False
        
        # Process any pending animations first
        if self.animation_queue:
            self.process_animation_queue()
        else:
            # Continue with sorting
            self.continue_sorting()

    def close_window(self):
        """Close the application window."""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.destroy()

    def continue_sorting(self):
        """Continue the sorting process from the current state."""
        if not self.sorting:
            return
            
        if self.paused and not self.step_by_step:
            return
            
        if not self.current_step_completed:
            return
            
        i = self.sorting_state['current_i']
        if i >= len(self.data):
            self._complete_sorting()
            return
            
        self._process_current_element(i)

    def _complete_sorting(self):
        """Complete the sorting process with validation."""
        if not self._validate_state("_complete_sorting"):
            return

        # Clear any pending animations
        self.animation_queue.clear()
        self.is_animating = False

        # Make a copy of the data for validation
        current_data = self.data.copy()
        
        if not self.validate_sorted_section(current_data):
            if hasattr(self, 'initial_data'):
                self.data = self.initial_data.copy()
                self.draw_bars(self.data)
            self.status_label.config(text="Error: Sorting validation failed - Restored original data")
            self.sorting = False
            self.paused = False
            self.step_by_step = False
            self.current_step_completed = True
            return

        # Queue final animation
        self.queue_animation(
            self.data.copy(), 
            self.data.copy(),
            {"sorted": list(range(len(self.data)))},
            "color",
            "Sorting Complete"
        )
        self.status_label.config(text=f"Sorted: {self.data}")
        self.sorting = False
        self.paused = False
        self.step_by_step = False
        self.current_step_completed = True

    def _process_current_element(self, i):
        """Process the current element with validation."""
        try:
            if not self._validate_state("_process_current_element"):
                self._handle_sorting_error("Invalid state during element processing")
                return

            if not self._validate_indices(i, i-1, "_process_current_element"):
                self._handle_sorting_error("Invalid indices during element processing")
                return

            current = self.data[i]
            
            # Validate current element
            if not isinstance(current, (int, float)) or not (0 <= current <= 100):
                self._handle_sorting_error("Invalid current element value")
                return
                
            j = i - 1
            
            # Optimize: If current element is already in correct position, skip processing
            if j >= 0 and self.data[j] <= current:
                self.current_iteration = i + 1
                self.current_step_completed = True
                self.update_statistics()
                
                step_desc = f"Step {i}: Element {current} already in correct position"
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
                    return
                    
                if i + 1 < len(self.data):
                    self.root.after(self.speed, lambda: self._process_current_element(i + 1))
                else:
                    self._complete_sorting()
                return
            
            self.sorting_state.update({
                'current_i': i,
                'current_j': j,
                'current_element': current,
                'is_comparing': True,
                'is_moving': False
            })
            
            self.current_iteration = i
            self.current_step_completed = False
            self.update_statistics()

            step_desc = f"Step {i}: Selecting element {current} at position {i}"
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [i], "sorted": list(range(i))},
                "color",
                step_desc
            )

            self._insert_element(i, j, current)
        except Exception as e:
            self._handle_sorting_error(f"Error processing element: {str(e)}")

    def _insert_element(self, i, j, current):
        """Insert element with strict validation."""
        try:
            if not self._validate_state("_insert_element"):
                self._handle_sorting_error("Invalid state during insertion")
                return

            if not self._validate_indices(i, j, "_insert_element"):
                self._handle_sorting_error("Invalid indices during insertion")
                return
                
            if not isinstance(current, (int, float)) or not (0 <= current <= 100):
                self._handle_sorting_error("Invalid current element during insertion")
                return

            def insert_at_position(pos):
                try:
                    # Create a copy of the data for animation
                    new_data = self.data.copy()
                    new_data[pos] = current

                    if not self._validate_data(new_data, "_insert_element new_data"):
                        self._handle_sorting_error("Invalid data during insertion")
                        return

                    def update_after_insert():
                        try:
                            if not self._validate_state("update_after_insert"):
                                self._handle_sorting_error("Invalid state after insertion")
                                return

                            # Update the data
                            self.data[pos] = current
                            self.swaps += 1
                            self.update_statistics()

                            # Validate the current state
                            if not self._validate_data(self.data, "update_after_insert"):
                                self._handle_sorting_error("Invalid data state after insertion")
                                return

                            # Validate the sorted section up to the current position
                            sorted_section = self.data[:i + 1]
                            if not self.validate_sorted_section(sorted_section):
                                self._handle_sorting_error("Invalid sorted section after insertion")
                                return

                            # Optimize: Check if next element is already in correct position
                            next_i = i + 1
                            if next_i < len(self.data) and self.data[next_i] >= current:
                                step_desc = f"Step {i}: Completed insertion of {current} at position {pos} (Next element already in position)"
                            else:
                                step_desc = f"Step {i}: Completed insertion of {current} at position {pos}"

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
                                self.draw_bars(self.data.copy(), {"sorted": list(range(i + 1))})
                                self.current_iteration = i + 1
                                self.current_step_completed = True
                                return

                            i_next = i + 1
                            if i_next < len(self.data):
                                self.root.after(self.speed, lambda: self._process_current_element(i_next))
                            else:
                                self._complete_sorting()
                        except Exception as e:
                            self._handle_sorting_error(f"Error after insertion: {str(e)}")

                    # Queue animations in sequence with optimized timing
                    step_desc = f"Step {i}.{pos}: Selecting element {current} at position {i}"
                    self.queue_animation(
                        self.data.copy(),
                        self.data.copy(),
                        {"current": [i], "sorted": list(range(i))},
                        "color",
                        step_desc
                    )

                    step_desc = f"Step {i}.{pos}: Found insertion point at position {pos} for element {current}"
                    self.queue_animation(
                        self.data.copy(),
                        self.data.copy(),
                        {"current": [i], "insert": [pos], "sorted": list(range(i))},
                        "color",
                        step_desc
                    )

                    step_desc = f"Step {i}.{pos}: Moving {current} to position {pos}"
                    self.queue_animation(
                        self.data.copy(),
                        new_data,
                        {"current": [i], "insert": [pos], "sorted": list(range(i))},
                        "move",
                        step_desc
                    )

                    # Wait for animation to complete before updating data
                    self.root.after(self.animation_duration, update_after_insert)
                except Exception as e:
                    self._handle_sorting_error(f"Error during position insertion: {str(e)}")

            def shift_and_compare(pos):
                try:
                    if pos < 0:
                        # Insert at beginning
                        insert_at_position(0)
                        return

                    # Compare current element with the element at position pos
                    self.comparisons += 1
                    self.update_statistics()

                    # Optimize: If we find a smaller element, we can stop shifting
                    if self.data[pos] <= current:
                        insert_at_position(pos + 1)
                        return

                    # Create a copy of the data for animation
                    new_data = self.data.copy()
                    new_data[pos + 1] = self.data[pos]

                    if not self._validate_data(new_data, "shift_and_compare new_data"):
                        self._handle_sorting_error("Invalid data during shift")
                        return

                    def update_after_shift():
                        try:
                            if not self._validate_state("update_after_shift"):
                                self._handle_sorting_error("Invalid state after shift")
                                return

                            # Update the data
                            self.data[pos + 1] = self.data[pos]
                            self.swaps += 1
                            self.update_statistics()

                            # Validate the current state
                            if not self._validate_data(self.data, "update_after_shift"):
                                self._handle_sorting_error("Invalid data state after shift")
                                return

                            if self.step_by_step:
                                self.paused = True
                                self.status_label.config(text=step_desc)
                                self.current_step_completed = True
                                return

                            if self.paused and not self.step_by_step:
                                return

                            # Continue shifting
                            shift_and_compare(pos - 1)
                        except Exception as e:
                            self._handle_sorting_error(f"Error after shift: {str(e)}")

                    # Queue animations in sequence with optimized timing
                    step_desc = f"Step {i}.{pos}: Selecting element {current} at position {i}"
                    self.queue_animation(
                        self.data.copy(),
                        self.data.copy(),
                        {"current": [i], "sorted": list(range(i))},
                        "color",
                        step_desc
                    )

                    step_desc = f"Step {i}.{pos}: Comparing {current} with {self.data[pos]} at position {pos}"
                    self.queue_animation(
                        self.data.copy(),
                        self.data.copy(),
                        {"current": [i], "compare": [pos], "sorted": list(range(i))},
                        "color",
                        step_desc
                    )

                    step_desc = f"Step {i}.{pos}: Moving {self.data[pos]} from position {pos} to {pos+1}"
                    self.queue_animation(
                        self.data.copy(),
                        new_data,
                        {"current": [i], "compare": [pos], "sorted": list(range(i))},
                        "move",
                        step_desc
                    )

                    # Wait for animation to complete before updating data
                    self.root.after(self.animation_duration, update_after_shift)
                except Exception as e:
                    self._handle_sorting_error(f"Error during shift and compare: {str(e)}")

            # Start the insertion process
            shift_and_compare(j)
        except Exception as e:
            self._handle_sorting_error(f"Error during insertion: {str(e)}")

    def _handle_sorting_error(self, error_message):
        """Handle sorting errors gracefully."""
        try:
            print(f"Sorting error: {error_message}")
            self.status_label.config(text=f"Error: {error_message}")
            
            # Restore initial data if available
            if hasattr(self, 'initial_data') and self.initial_data is not None:
                self.data = self.initial_data.copy()
                self.draw_bars(self.data)
            
            # Reset sorting state
            self.sorting = False
            self.paused = False
            self.step_by_step = False
            self.current_step_completed = True
            self.animation_queue.clear()
            self.is_animating = False
            
            # Reset sorting state dictionary
            self.sorting_state = {
                'current_i': 0,
                'current_j': 0,
                'current_element': None,
                'is_comparing': False,
                'is_moving': False
            }
            
            # Update UI
            self.pause_button.config(state='disabled')
            self.next_step_button.config(state='disabled')
            self.update_statistics()
            
            # Clear any pending animations
            if hasattr(self, 'animation_timer') and self.animation_timer:
                self.root.after_cancel(self.animation_timer)
                self.animation_timer = None
        except Exception as e:
            print(f"Error in error handler: {str(e)}")
            # Last resort: try to reset everything
            self.reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = InsertionSortVisualizer(root)
    root.mainloop()
   