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
        self.root.geometry("1000x600")
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
        self.animation_speed_factor = 1.0  # For smooth speed transitions
        
        # Performance optimization
        self._cached_colors = {}  # Cache for interpolated colors
        self._last_draw_time = 0  # For frame rate limiting
        self._min_frame_time = 16  # ~60 FPS
        
        # Color definitions
        self.colors = {
            'default': "#4C566A",    # Gray for unsorted
            'current': "#EBCB8B",    # Yellow for current
            'compare': "#BF616A",    # Red for comparison
            'sorted': "#A3BE8C",     # Green for sorted
            'insert': "#81A1C1",     # Blue for insertion
            'text': "#ECEFF4",       # Text color
            'text_bg': "#2E3440"     # Text background color
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
        
        ttk.Label(speed_frame, text="Speed:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        # Initialize speed label before slider
        self.speed_label = ttk.Label(speed_frame, text=f"{self.speed}ms", font=("Segoe UI", 10), width=8, anchor="w")
        self.speed_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.speed_slider = ttk.Scale(speed_frame, from_=5, to=2000, orient=tk.HORIZONTAL, command=self.update_speed, length=200)
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(side=tk.LEFT)
        self.add_tooltip(self.speed_slider, "Control the speed of the sorting animation (5ms - 2000ms)")

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
            self.speed = int(float(val))
            self.speed_label.config(text=f"{self.speed:4d}ms")
            # Adjust animation frames based on speed
            self.animation_frames = max(15, min(40, int(40 * (1000 / self.speed))))
            # Update animation speed factor for smooth transitions
            self.animation_speed_factor = min(1.0, 1000 / self.speed)
            
            # Update speed indicator
            if self.speed_indicator:  # Check if speed_indicator exists
                if self.speed <= 200:
                    speed_text = "Fast"
                elif self.speed <= 500:
                    speed_text = "Normal"
                else:
                    speed_text = "Slow"
                self.speed_indicator.config(text=f"Speed: {speed_text}")
        except Exception as e:
            print(f"Error updating speed: {str(e)}")

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
            # Don't show error message for drawing errors to avoid spam
            # Just log it and continue

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

        # Store the initial data for reference
        self.initial_data = self.data.copy()
        self.sorting = True
        self.pause_button.config(state='normal')
        self.status_label.config(text="Sorting in progress...")
        self.comparisons = 0
        self.swaps = 0
        self.current_iteration = 0
        self.total_iterations = len(self.data)
        self.current_step_completed = True
        self.update_statistics()
        self.insertion_sort(1)

    def toggle_pause(self):
        if not self.sorting:
            return
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused and not self.step_by_step:
            self.process_animation_queue()
            self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration))

    def toggle_step_by_step(self):
        self.step_by_step = not self.step_by_step
        if self.step_by_step:
            self.status_label.config(text="Step-by-Step mode enabled - Press 'Next Step' to proceed")
            if self.sorting and not self.paused:
                self.paused = True
        else:
            self.status_label.config(text="Step-by-Step mode disabled")
            if self.sorting:
                self.paused = False
                self.process_animation_queue()
                self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration))

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
            # Only store the step if it's a move animation or a color change that affects the data
            if animation_type == 'move' or (animation_type == 'color' and 'current' in colors):
                self.step_history.append({
                    'data': end_data_copy,  # Store the end state
                    'colors': colors_copy.copy(),
                    'description': step_description,
                    'substep': self.current_substep,
                    'iteration': self.current_iteration,
                    'comparisons': self.comparisons,
                    'swaps': self.swaps
                })
                self.current_step_number += 1
                self.total_steps = max(self.total_steps, self.current_step_number)
                self.current_substep += 1
                self.total_substeps = max(self.total_substeps, self.current_substep)
                self.next_step_button.config(state='normal')
        
        self.animation_queue.append(animation)
        self.step_count += 1
        self.update_statistics()
        
        if not self.is_animating:
            self.process_animation_queue()

    def process_animation_queue(self):
        """Process the next animation in the queue."""
        if not self.animation_queue:
            self.is_animating = False
            if self.step_by_step and self.sorting:
                # If in step-by-step mode and still sorting, continue with next iteration
                self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration))
            return

        self.is_animating = True
        animation = self.animation_queue.pop(0)
        
        # Update the data if this is a move animation
        if animation['type'] == 'move':
            # Update the data array with the end state
            self.data = animation['end_data'].copy()
            
        self.animate_transition(
            animation['start_data'],
            animation['end_data'],
            animation['colors'],
            animation['type'],
            animation['step']
        )

    def animate_transition(self, start_data, end_data, colors, animation_type, step_description=None):
        self.animation_data = (start_data, end_data)
        self.animation_colors = colors
        self.animation_type = animation_type
        self.current_frame = 0
        self.current_animation = step_description
        if step_description:
            self.current_step = step_description
        self.animate_frame()

    def animate_frame(self):
        """Animate a single frame of the current transition."""
        if self.paused and not self.step_by_step:
            return
            
        if self.current_frame >= self.animation_frames:
            self.draw_bars(self.animation_data[1], self.animation_colors)
            self.current_step_completed = True
            
            if self.step_by_step:
                self.paused = True
                # Ensure we show the final state before moving to next step
                self.draw_bars(self.animation_data[1], self.animation_colors)
                if not self.animation_queue:  # If no more animations in queue
                    self.root.after(50, lambda: self.insertion_sort(self.current_iteration))
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

    def ease_in_out_quad(self, t):
        return t * t * (3 - 2 * t)

    def insertion_sort(self, i):
        """Perform one step of insertion sort."""
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
            return

        if self.paused and not self.step_by_step:
            self.root.after(100, lambda: self.insertion_sort(i))
            return

        current = self.data[i]
        j = i - 1
        self.current_iteration = i
        self.current_step_completed = False  # Reset step completion flag
        self.update_statistics()

        # Highlight current element and show step description
        step_desc = f"Step {i}: Selecting element {current} at position {i}"
        self.queue_animation(
            self.data.copy(),
            self.data.copy(),
            {"current": [i], "sorted": list(range(i))},
            "color",
            step_desc
        )

        # Compare and shift elements
        while j >= 0 and self.data[j] > current:
            self.comparisons += 1
            self.update_statistics()
            
            # Show comparison with detailed step description
            step_desc = f"Step {i}.{j}: Comparing {current} with {self.data[j]} at position {j}"
            self.queue_animation(
                self.data.copy(),
                self.data.copy(),
                {"current": [i], "compare": [j], "sorted": list(range(i))},
                "color",
                step_desc
            )

            # Create a copy of the data for animation
            new_data = self.data.copy()
            # Move the element at j to j+1
            new_data[j + 1] = self.data[j]
            # Update the source position with the current element
            new_data[j] = current
            
            # Animate the movement with detailed step description
            step_desc = f"Step {i}.{j}: Moving {self.data[j]} from position {j} to {j+1}"
            self.queue_animation(
                self.data.copy(),
                new_data,
                {"current": [i], "compare": [j], "sorted": list(range(i))},
                "move",
                step_desc
            )
            
            # Update the actual data
            self.data[j + 1] = self.data[j]
            self.data[j] = current  # Update the source position
            j -= 1
            self.swaps += 1
            self.update_statistics()

            if self.step_by_step:
                self.paused = True
                self.status_label.config(text=step_desc)
                return

            if self.paused and not self.step_by_step:
                self.root.after(100, lambda: self.insertion_sort(i))
                return

        # Show insertion point with detailed step description
        step_desc = f"Step {i}.{j+1}: Found insertion point at position {j+1} for element {current}"
        self.queue_animation(
            self.data.copy(),
            self.data.copy(),
            {"current": [i], "insert": [j + 1], "sorted": list(range(i))},
            "color",
            step_desc
        )

        # Insert the current element with detailed step description
        new_data = self.data.copy()
        # Move the current element to its final position
        new_data[j + 1] = current
        step_desc = f"Step {i}.{j+1}: Moving {current} to position {j+1}"
        self.queue_animation(
            self.data.copy(),
            new_data,
            {"current": [i], "insert": [j + 1], "sorted": list(range(i))},
            "move",
            step_desc
        )
        
        # Update the actual data
        self.data[j + 1] = current
        self.swaps += 1
        self.update_statistics()

        # Show completion of current element with detailed step description
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
            
        self.paused = False
        self.current_step_completed = False
        
        # Process any pending animations first
        if self.animation_queue:
            self.process_animation_queue()
        else:
            # If no animations in queue, continue with sorting
            # Instead of moving to next element, check if current element needs to be moved further
            if self.current_iteration > 0:
                # Check if the current element needs to be moved further back
                current = self.data[self.current_iteration]
                j = self.current_iteration - 1
                if j >= 0 and self.data[j] > current:
                    # Continue with current iteration to move element further back
                    self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration))
                else:
                    # Move to next element
                    self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration + 1))
            else:
                # Move to next element
                self.root.after(self.speed, lambda: self.insertion_sort(self.current_iteration + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = InsertionSortVisualizer(root)
    root.mainloop()
   