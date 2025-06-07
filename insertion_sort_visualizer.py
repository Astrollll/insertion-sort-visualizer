import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from typing import List, Tuple
import threading
import math

class ModernTheme:
    # Color palette - Modern and minimalist
    BACKGROUND = "#ffffff"
    PRIMARY = "#1a1a1a"
    SECONDARY = "#0066cc"
    ACCENT = "#00b894"
    HIGHLIGHT = "#ff4757"
    TEXT = "#2d3436"
    CANVAS_BG = "#f8f9fa"
    BAR_COLORS = {
        "default": "#a4b0be",
        "current": "#ff4757",
        "comparing": "#0066cc",
        "sorted": "#00b894",
        "transition": "#ffa502"
    }
    
    # Font settings
    FONT_FAMILY = "Segoe UI"
    TITLE_FONT = (FONT_FAMILY, 32, "bold")
    HEADER_FONT = (FONT_FAMILY, 16, "bold")
    NORMAL_FONT = (FONT_FAMILY, 12)
    SMALL_FONT = (FONT_FAMILY, 10)

class ArrayType:
    RANDOM = "Random"
    NEARLY_SORTED = "Nearly Sorted"
    REVERSED = "Reversed"
    FEW_UNIQUE = "Few Unique"
    CUSTOM = "Custom"

class InsertionSortVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Insertion Sort Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernTheme.BACKGROUND)
        
        # Constants
        self.CANVAS_WIDTH = 1000
        self.CANVAS_HEIGHT = 500
        self.MIN_BAR_WIDTH = 20
        self.MAX_BAR_WIDTH = 50
        self.BAR_SPACING = 3
        self.ANIMATION_SPEED = 100  # milliseconds
        self.TRANSITION_STEPS = 10  # Number of steps for smooth transitions
        self.MIN_ARRAY_SIZE = 5
        self.MAX_ARRAY_SIZE = 50
        self.DEFAULT_ARRAY_SIZE = 20
        self.MIN_BAR_HEIGHT = 20  # Minimum height for bars

        # Variables
        self.array: List[int] = []
        self.is_sorting = False
        self.current_step = 0
        self.total_steps = 0
        self.animation_speed = tk.DoubleVar(value=1.0)
        self.array_size = tk.IntVar(value=self.DEFAULT_ARRAY_SIZE)
        self.array_type = tk.StringVar(value=ArrayType.RANDOM)
        self.sorted_indices = set()
        self.transitioning_indices = set()
        self.bar_positions = {}  # Store current positions of bars

        self._create_widgets()
        self._create_layout()
        self._configure_styles()
        self._generate_array()

    def _configure_styles(self):
        style = ttk.Style()
        
        # Configure button styles
        style.configure("Modern.TButton",
                       font=ModernTheme.NORMAL_FONT,
                       padding=10)
        
        # Configure label styles
        style.configure("Modern.TLabel",
                       font=ModernTheme.NORMAL_FONT,
                       background=ModernTheme.BACKGROUND,
                       foreground=ModernTheme.TEXT)
        
        # Configure frame styles
        style.configure("Modern.TFrame",
                       background=ModernTheme.BACKGROUND)
        
        # Configure title style
        style.configure("Title.TLabel",
                       font=ModernTheme.TITLE_FONT,
                       background=ModernTheme.BACKGROUND,
                       foreground=ModernTheme.PRIMARY)
        
        # Configure scale style
        style.configure("Modern.Horizontal.TScale",
                       background=ModernTheme.BACKGROUND)
        
        # Configure combobox style
        style.configure("Modern.TCombobox",
                       font=ModernTheme.NORMAL_FONT,
                       padding=5)

    def _create_widgets(self):
        # Main container for better organization
        self.main_container = ttk.Frame(self.root, style="Modern.TFrame")
        
        # Title Frame with subtitle
        self.title_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        self.title_label = ttk.Label(
            self.title_frame,
            text="Insertion Sort Visualizer",
            style="Title.TLabel"
        )
        self.subtitle_label = ttk.Label(
            self.title_frame,
            text="Watch the algorithm in action",
            style="Modern.TLabel"
        )

        # Control Panel Frame
        self.control_panel = ttk.Frame(self.main_container, style="Modern.TFrame")
        
        # Array Generation Controls
        self.array_control_frame = ttk.LabelFrame(
            self.control_panel,
            text="Array Controls",
            style="Modern.TFrame",
            padding=10
        )
        
        # Array Type Selection
        self.array_type_label = ttk.Label(
            self.array_control_frame,
            text="Array Type:",
            style="Modern.TLabel"
        )
        self.array_type_combo = ttk.Combobox(
            self.array_control_frame,
            textvariable=self.array_type,
            values=[ArrayType.RANDOM, ArrayType.NEARLY_SORTED, 
                   ArrayType.REVERSED, ArrayType.FEW_UNIQUE, ArrayType.CUSTOM],
            state="readonly",
            width=15,
            style="Modern.TCombobox"
        )
        self.array_type_combo.bind('<<ComboboxSelected>>', lambda e: self._on_array_type_change())
        
        # Array Size Control
        self.size_label = ttk.Label(
            self.array_control_frame,
            text="Array Size:",
            style="Modern.TLabel"
        )
        self.size_spinbox = ttk.Spinbox(
            self.array_control_frame,
            from_=self.MIN_ARRAY_SIZE,
            to=self.MAX_ARRAY_SIZE,
            textvariable=self.array_size,
            width=5,
            command=self._on_size_change
        )
        
        # Generate Button
        self.generate_button = ttk.Button(
            self.array_control_frame,
            text="Generate Array",
            command=self._generate_array,
            style="Modern.TButton"
        )

        # Action Buttons Frame
        self.action_frame = ttk.LabelFrame(
            self.control_panel,
            text="Actions",
            style="Modern.TFrame",
            padding=10
        )
        self.start_button = ttk.Button(
            self.action_frame,
            text="Start Sorting",
            command=self._start_sorting,
            style="Modern.TButton"
        )
        self.reset_button = ttk.Button(
            self.action_frame,
            text="Reset",
            command=self._reset_visualization,
            style="Modern.TButton"
        )

        # Speed Control Frame
        self.speed_frame = ttk.LabelFrame(
            self.control_panel,
            text="Animation Speed",
            style="Modern.TFrame",
            padding=10
        )
        self.speed_slider = ttk.Scale(
            self.speed_frame,
            from_=0.1,
            to=5.0,
            orient="horizontal",
            variable=self.animation_speed,
            length=200,
            style="Modern.Horizontal.TScale"
        )

        # Custom Array Input Frame
        self.input_frame = ttk.LabelFrame(
            self.control_panel,
            text="Custom Array",
            style="Modern.TFrame",
            padding=10
        )
        self.array_input = ttk.Entry(
            self.input_frame,
            width=40,
            font=ModernTheme.NORMAL_FONT
        )
        self.apply_input_button = ttk.Button(
            self.input_frame,
            text="Apply",
            command=self._apply_custom_array,
            style="Modern.TButton"
        )
        self.start_custom_button = ttk.Button(
            self.input_frame,
            text="Start Custom",
            command=self._start_custom_sorting,
            style="Modern.TButton",
            state="disabled"
        )

        # Canvas for visualization
        self.canvas_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=ModernTheme.CANVAS_BG,
            highlightthickness=0
        )

        # Status Frame
        self.status_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        self.status_label = ttk.Label(
            self.status_frame,
            text="Status: Ready",
            style="Modern.TLabel"
        )
        self.step_label = ttk.Label(
            self.status_frame,
            text="Step: 0/0",
            style="Modern.TLabel"
        )

    def _create_layout(self):
        # Main container layout
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title Layout
        self.title_frame.pack(fill="x", pady=(0, 10))
        self.title_label.pack()
        self.subtitle_label.pack(pady=(0, 5))

        # Control Panel Layout - All controls in a single row at the top
        self.control_panel.pack(fill="x", pady=(0, 10))
        
        # Array Controls Layout - Left side
        self.array_control_frame.pack(side="left", padx=5)
        self.array_type_label.pack(side="left", padx=2)
        self.array_type_combo.pack(side="left", padx=2)
        self.size_label.pack(side="left", padx=2)
        self.size_spinbox.pack(side="left", padx=2)
        self.generate_button.pack(side="left", padx=2)
        
        # Action Buttons Layout - Middle
        self.action_frame.pack(side="left", padx=5)
        self.start_button.pack(side="left", padx=2)
        self.reset_button.pack(side="left", padx=2)
        
        # Speed Control Layout - Middle
        self.speed_frame.pack(side="left", padx=5)
        self.speed_slider.pack(side="left", padx=2)
        
        # Custom Array Input Layout - Right side
        self.input_frame.pack(side="left", padx=5, fill="x", expand=True)
        self.array_input.pack(side="left", padx=2, fill="x", expand=True)
        self.apply_input_button.pack(side="left", padx=2)
        self.start_custom_button.pack(side="left", padx=2)

        # Status Frame - Right side
        self.status_frame.pack(side="right", padx=5)
        self.status_label.pack(side="left", padx=2)
        self.step_label.pack(side="left", padx=2)

        # Canvas Layout - Takes remaining space
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas.pack(fill="both", expand=True)

    def _on_array_type_change(self):
        if self.array_type.get() == ArrayType.CUSTOM:
            self.array_input.config(state="normal")
            self.apply_input_button.config(state="normal")
        else:
            self.array_input.config(state="disabled")
            self.apply_input_button.config(state="disabled")
            self._generate_array()

    def _generate_array(self):
        size = self.array_size.get()
        array_type = self.array_type.get()
        
        if array_type == ArrayType.RANDOM:
            self.array = random.sample(range(1, 101), size)
        elif array_type == ArrayType.NEARLY_SORTED:
            self.array = list(range(1, size + 1))
            # Swap a few elements to make it nearly sorted
            for _ in range(size // 4):
                i, j = random.sample(range(size), 2)
                self.array[i], self.array[j] = self.array[j], self.array[i]
        elif array_type == ArrayType.REVERSED:
            self.array = list(range(size, 0, -1))
        elif array_type == ArrayType.FEW_UNIQUE:
            unique_values = random.sample(range(1, 101), 5)
            self.array = [random.choice(unique_values) for _ in range(size)]
        
        self._reset_visualization()
        self._draw_array()

    def _on_size_change(self):
        if self.array_type.get() != ArrayType.CUSTOM:
            self._generate_array()

    def _apply_custom_array(self):
        try:
            input_text = self.array_input.get().strip()
            if not input_text:
                messagebox.showerror("Error", "Please enter numbers separated by commas")
                return

            numbers = [int(x.strip()) for x in input_text.split(",")]
            if not numbers:
                messagebox.showerror("Error", "Please enter at least one number")
                return

            if len(numbers) < self.MIN_ARRAY_SIZE:
                messagebox.showerror("Error", f"Array must have at least {self.MIN_ARRAY_SIZE} elements")
                return
            if len(numbers) > self.MAX_ARRAY_SIZE:
                messagebox.showerror("Error", f"Array cannot have more than {self.MAX_ARRAY_SIZE} elements")
                return

            self.array = numbers
            self.array_size.set(len(numbers))
            self.array_type.set(ArrayType.CUSTOM)
            self._reset_visualization()
            self._draw_array()
            self.start_custom_button.config(state="normal")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers separated by commas")

    def _start_custom_sorting(self):
        if self.array_type.get() == ArrayType.CUSTOM:
            self._start_sorting()

    def _reset_visualization(self):
        self.is_sorting = False
        self.current_step = 0
        self.total_steps = 0
        self.sorted_indices.clear()
        self.transitioning_indices.clear()
        self.status_label.config(text="Status: Ready")
        self.step_label.config(text="Step: 0/0")
        self.start_custom_button.config(state="disabled")
        self._draw_array()

    def _draw_array(self, current_idx: int = -1, comparing_idx: int = -1):
        self.canvas.delete("all")
        
        if not self.array:
            return

        # Calculate bar dimensions
        num_bars = len(self.array)
        max_value = max(self.array)
        min_value = min(self.array)
        value_range = max_value - min_value
        
        # Ensure minimum height for visualization
        effective_max = max_value + (value_range * 0.1)  # Add 10% padding
        effective_min = max(0, min_value - (value_range * 0.1))  # Add 10% padding
        
        bar_width = min(
            self.MAX_BAR_WIDTH,
            (self.CANVAS_WIDTH - (num_bars + 1) * self.BAR_SPACING) // num_bars
        )
        bar_width = max(bar_width, self.MIN_BAR_WIDTH)

        # Draw bars with enhanced visual effects
        for i, value in enumerate(self.array):
            # Calculate bar height and position with minimum height
            height = max(
                self.MIN_BAR_HEIGHT,
                ((value - effective_min) / (effective_max - effective_min)) * (self.CANVAS_HEIGHT - 40)
            )
            x1 = i * (bar_width + self.BAR_SPACING) + self.BAR_SPACING
            y1 = self.CANVAS_HEIGHT - height
            x2 = x1 + bar_width
            y2 = self.CANVAS_HEIGHT

            # Store current position
            self.bar_positions[i] = (x1, y1, x2, y2)

            # Determine bar color with enhanced visual effects
            if i == current_idx:
                color = ModernTheme.BAR_COLORS["current"]
            elif i == comparing_idx:
                color = ModernTheme.BAR_COLORS["comparing"]
            elif i in self.sorted_indices:
                color = ModernTheme.BAR_COLORS["sorted"]
            elif i in self.transitioning_indices:
                color = ModernTheme.BAR_COLORS["transition"]
            else:
                color = ModernTheme.BAR_COLORS["default"]

            # Draw bar with enhanced visual effects
            # Main bar
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="",
                width=0
            )

            # Add gradient effect
            gradient_height = 5
            for h in range(gradient_height):
                alpha = 1 - (h / gradient_height)
                gradient_color = self._adjust_color_alpha(color, alpha)
                self.canvas.create_rectangle(
                    x1, y1 + h, x2, y1 + h + 1,
                    fill=gradient_color,
                    outline="",
                    width=0
                )

            # Add subtle shadow effect
            shadow_height = 3
            for h in range(shadow_height):
                alpha = 0.1 - (h / shadow_height) * 0.1
                shadow_color = self._adjust_color_alpha("#000000", alpha)
                self.canvas.create_rectangle(
                    x1, y2 + h, x2, y2 + h + 1,
                    fill=shadow_color,
                    outline="",
                    width=0
                )

            # Draw value with enhanced styling
            self.canvas.create_text(
                x1 + bar_width/2,
                y1 - 10,
                text=str(value),
                font=ModernTheme.SMALL_FONT,
                fill=ModernTheme.TEXT
            )

    def _adjust_color_alpha(self, color: str, alpha: float) -> str:
        """Convert hex color to rgba with alpha"""
        # Convert hex to rgb
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _start_sorting(self):
        if self.is_sorting:
            return

        self.is_sorting = True
        self.start_button.config(state="disabled")
        self.status_label.config(text="Status: Sorting...")
        
        # Start sorting in a separate thread
        threading.Thread(target=self._insertion_sort, daemon=True).start()

    def _insertion_sort(self):
        n = len(self.array)
        self.total_steps = n * (n - 1) // 2
        self.sorted_indices = set()
        
        for i in range(1, n):
            key = self.array[i]
            j = i - 1
            
            while j >= 0 and self.array[j] > key:
                # Update visualization
                self.current_step += 1
                self.root.after(0, self._update_step_label)
                
                # Animate the transition
                self._animate_transition(j, j + 1)
                
                # Perform swap
                self.array[j + 1] = self.array[j]
                j -= 1
                
                if not self.is_sorting:
                    return

            self.array[j + 1] = key
            self.sorted_indices.add(j + 1)
            
            # Update visualization after insertion
            self.root.after(0, lambda: self._draw_array(i, -1))
            time.sleep(1 / (self.animation_speed.get() * 10))

        self.is_sorting = False
        self.root.after(0, self._sorting_completed)

    def _update_step_label(self):
        self.step_label.config(text=f"Step: {self.current_step}/{self.total_steps}")

    def _sorting_completed(self):
        self.start_button.config(state="normal")
        self.status_label.config(text="Status: Sorting Completed")
        self._draw_array()

    def _animate_transition(self, from_idx: int, to_idx: int):
        if from_idx == to_idx:
            return

        self.transitioning_indices.add(from_idx)
        self.transitioning_indices.add(to_idx)

        # Calculate steps for smooth animation
        steps = self.TRANSITION_STEPS
        speed_factor = self.animation_speed.get()
        delay = 1 / (speed_factor * 30)  # Increased animation speed

        # Get current positions
        from_pos = self.bar_positions[from_idx]
        to_pos = self.bar_positions[to_idx]

        for step in range(steps + 1):
            if not self.is_sorting:
                break

            progress = step / steps
            # Enhanced easing function for smoother animation
            progress = self._ease_in_out_cubic(progress)

            # Calculate intermediate positions
            x1 = from_pos[0] + (to_pos[0] - from_pos[0]) * progress
            y1 = from_pos[1] + (to_pos[1] - from_pos[1]) * progress
            x2 = from_pos[2] + (to_pos[2] - from_pos[2]) * progress
            y2 = from_pos[3] + (to_pos[3] - from_pos[3]) * progress

            # Update positions
            self.bar_positions[from_idx] = (x1, y1, x2, y2)
            self._draw_array()
            time.sleep(delay)

        self.transitioning_indices.remove(from_idx)
        self.transitioning_indices.remove(to_idx)

    def _ease_in_out_cubic(self, x: float) -> float:
        """Enhanced easing function for smoother animations"""
        if x < 0.5:
            return 4 * x * x * x
        else:
            return 1 - pow(-2 * x + 2, 3) / 2

def main():
    root = tk.Tk()
    app = InsertionSortVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 