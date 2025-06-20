import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import math # Not strictly needed for this change, but keeping for flap disc if used
import subprocess
import sys

class RoundedRectangleCanvas(tk.Canvas):
    """
    A custom Canvas widget that draws a rounded rectangle as its background.
    Useful for creating UI elements with rounded corners.
    """
    def __init__(self, parent, corner_radius, fill_color, **kwargs):
        # Set the canvas background to match the fill_color for a consistent look.
        # This is crucial for ensuring the entire area of the custom canvas matches its intended color.
        super().__init__(parent, highlightthickness=0, bg=fill_color, **kwargs)
        self.corner_radius = corner_radius
        self.fill_color = fill_color # This is used for the polygon fill
        self.bind("<Configure>", self._draw_rounded_rectangle)

    def _draw_rounded_rectangle(self, event=None):
        self.delete("rect") # Clear previous drawing
        width = self.winfo_width()
        height = self.winfo_height()

        # Define points for the rounded rectangle
        points = [self.corner_radius, 0,
                  width - self.corner_radius, 0,
                  width, self.corner_radius,
                  width, height - self.corner_radius,
                  width - self.corner_radius, height,
                  self.corner_radius, height,
                  0, height - self.corner_radius,
                  0, self.corner_radius]

        self.create_polygon(points, smooth=True, fill=self.fill_color, tags="rect")
        self.tag_lower("rect") # Ensure other widgets placed on canvas are on top


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")

        # --- Calculate dimensions and position to center the window ---
        window_width = 1000
        window_height = 600

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the top-left corner to center the window
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the window geometry: "widthxheight+x+y"
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # --- End of centering calculation ---

        self.root.minsize(800, 500) # Minimum size
        self.root.config(bg="#1A1A2E") # Dark blue background

        # Configure root grid for responsive layout
        self.root.grid_rowconfigure(0, weight=0) # Header row, fixed height
        self.root.grid_rowconfigure(1, weight=1) # Main content row, expands
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # --- Header Section (Logo and Text) ---
        self.header_frame = tk.Frame(self.root, bg=self.root['bg'])
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nw", padx=30, pady=20)
        self.header_frame.grid_columnconfigure(0, weight=0) # Column for logo (fixed)
        self.header_frame.grid_columnconfigure(1, weight=1) # Column for text (expands)

        # Load the image using PIL and convert it to PhotoImage
        try:
             image_path = 'C:/Users/PC5/Documents/Project/Img/Cavite_State_University_(CvSU).png'
             pil_image = Image.open(image_path)
             pil_image = pil_image.resize((60, 60), Image.Resampling.LANCZOS) # Smaller size for logo
             self.logo_image = ImageTk.PhotoImage(pil_image)
            
             self.logo_label = tk.Label(self.header_frame, image=self.logo_image, bg=self.root['bg'])
             self.logo_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=(0, 10)) # Span 3 rows for vertical alignment
        except FileNotFoundError:
             print(f"Error: Image file not found at {image_path}")
             self.logo_label = tk.Label(self.header_frame, text="Logo Missing", bg=self.root['bg'], fg="red", font=("Arial", 10))
             self.logo_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=(0, 10))

        # Text next to the logo - now split into multiple labels for different fonts
        self.cvsu_label = tk.Label(
            self.header_frame,
            text="CAVITE STATE UNIVERSITY",
            font=("Arial", 12, "bold"), # h4 equivalent
            fg="white",
            bg=self.root['bg']
        )
        self.cvsu_label.grid(row=0, column=1, sticky="w")

        self.silang_label = tk.Label(
            self.header_frame,
            text="SILANG CAMPUS",
            font=("Arial", 18, "bold"), # h2 equivalent (larger)
            fg="white",
            bg=self.root['bg']
        )
        self.silang_label.grid(row=1, column=1, sticky="w") # Placed below CvSU label

        self.motto_label = tk.Label(
            self.header_frame,
            text="TRUTH | EXCELLENCE | SERVICE",
            font=("Arial", 12, "bold"), # h4 equivalent
            fg="white",
            bg=self.root['bg']
        )
        self.motto_label.grid(row=2, column=1, sticky="w") # Placed below Silang Campus label


        # --- Left Panel ---
        self.left_panel_container = RoundedRectangleCanvas(
            self.root, corner_radius=30, fill_color="#2d8bba", # Lighter blue for the left panel
            width=450 # Initial width, will expand with weight
        )
        # Changed padx from 20 to 10
        self.left_panel_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=20)
        
        # Configure left panel's internal grid to center content
        self.left_panel_container.grid_rowconfigure(0, weight=1) # Row for description
        self.left_panel_container.grid_columnconfigure(0, weight=1)

        # Description text inside the left panel, centered and about Insertion Sort
        self.description_label = tk.Label(
            self.left_panel_container,
            text=(
                "Welcome to the Insertion Sort Visualizer!\n\n"
                "Insertion Sort builds the final sorted array (or list) one item at a time.\n"
                "It iterates through the input elements and removes one element per iteration,\n"
                "finds the place within the sorted array, and inserts it there.\n\n"
                "This visualization will help you understand:\n"
                "- How elements are compared and shifted.\n"
                "- The 'sorted' and 'unsorted' portions of the array.\n"
                "- The step-by-step process of placing an element in its correct position.\n\n"
                "Insertion Sort is efficient for small data sets or data sets that are already substantially sorted."
            ),
            font=("Arial", 12),
            fg="white",
            bg="#2d8bba", # Match panel fill color
            justify="center",
            wraplength=350 # Wrap text to fit within the panel
        )
        self.description_label.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        

        # --- Right Panel (Frame container for the RoundedRectangleCanvas) ---
        # This frame ensures a consistent background color for the margins of its children
        self.right_panel_frame = tk.Frame(self.root, bg="#2d8bba") # Explicitly set background for the frame
        self.right_panel_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        self.right_panel_frame.grid_rowconfigure(0, weight=1)
        self.right_panel_frame.grid_columnconfigure(0, weight=1)

        # The actual RoundedRectangleCanvas for the right panel is now a child of the frame
        self.right_panel_container = RoundedRectangleCanvas(
            self.right_panel_frame, corner_radius=30, fill_color="#2d8bba"
        )
        # Use pack to make the RoundedRectangleCanvas fill its parent frame
        self.right_panel_container.pack(fill="both", expand=True)

        # Configure right panel's internal grid for the new design (inside self.right_panel_container)
        self.right_panel_container.grid_rowconfigure(0, weight=0) # For "Insert sort" label and circle
        self.right_panel_container.grid_rowconfigure(1, weight=0) # For first horizontal rectangle
        self.right_panel_container.grid_rowconfigure(2, weight=0) # For second horizontal rectangle
        self.right_panel_container.grid_rowconfigure(3, weight=1) # For the large bottom container (expands)
        self.right_panel_container.grid_columnconfigure(0, weight=1) # Single column for most elements

        # "Insert sort" label at top-left with yellow background
        self.insert_sort_label = tk.Label(
            self.right_panel_container,
            text="Insert sort",
            font=("Arial", 12, "bold"),
            bg="#FFFACD", # Lemon Chiffon (light yellow)
            fg="#1A1A2E", # Dark blue for text
            relief="flat",
            padx=10,
            pady=5
        )
        self.insert_sort_label.grid(row=0, column=0, sticky="nw", padx=30, pady=30)

        # Circular element at top-right
        self.circle_canvas = tk.Canvas(
            self.right_panel_container,
            width=50, height=50,
            bg=self.right_panel_container.fill_color, # Match panel background
            highlightthickness=0
        )
        self.circle_canvas.create_oval(5, 5, 45, 45, fill="white", outline="white", width=2)
        self.circle_canvas.grid(row=0, column=0, sticky="ne", padx=30, pady=30)

        # First horizontal rounded rectangle
        self.rect1 = RoundedRectangleCanvas(
            self.right_panel_container, corner_radius=15, fill_color="white",
            height=40
        )
        self.rect1.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))

        # Second horizontal rounded rectangle
        self.rect2 = RoundedRectangleCanvas(
            self.right_panel_container, corner_radius=15, fill_color="white",
            height=40
        )
        self.rect2.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 20))
        

        # Large bottom rounded rectangle (outer white)
        self.bottom_outer_rect = RoundedRectangleCanvas(
            self.right_panel_container, corner_radius=30, fill_color="white",
            # No fixed height, let it expand with weight=1
        )
        self.bottom_outer_rect.grid(row=3, column=0, sticky="nsew", padx=30, pady=(0, 30))

        # Inner light blue rounded rectangle inside the white one
        self.bottom_inner_rect = RoundedRectangleCanvas(
            self.bottom_outer_rect, corner_radius=25, fill_color="#4DC1D8", # A lighter blue
            # Use place to position it relative to its parent (bottom_outer_rect)
        )
        self.bottom_inner_rect.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)


        # "Go sort" button moved inside the new inner light blue rectangle
        self.go_sort_button = tk.Button(
            self.bottom_inner_rect,
            text="Go sort",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#00BFFF", # Keep DeepSkyBlue for the button itself
            relief="flat",
            command=self.on_go_sort_click
        )
        # Center the button within its new parent (bottom_inner_rect)
        self.go_sort_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.6)

    #button redirection
    def on_go_sort_click(self):
        print("Redirecting to loading screen...")
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            loading_screen_path = os.path.join(current_dir, "loading_screen.py")
            
            # Launch the loading screen using the same Python interpreter
            subprocess.Popen([sys.executable, loading_screen_path])
            
            # Close the current window
            self.root.destroy()
        except Exception as e:
            print(f"Error launching loading screen: {e}")
            # Fallback: show an error message
            tk.messagebox.showerror("Error", f"Could not launch loading screen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()