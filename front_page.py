import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import math
import subprocess
import sys

class RoundedRectangleCanvas(tk.Canvas):
    # Inits
    def __init__(self, parent, corner_radius, fill_color, border_color=None, border_width=0, **kwargs):
        super().__init__(parent, highlightthickness=0, bg=fill_color, **kwargs)
        self.corner_radius = corner_radius
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width
        self.bind("<Configure>", self._draw_rounded_rectangle)

    # Draw shape
    def _draw_rounded_rectangle(self, event=None):
        self.delete("rect")
        width = self.winfo_width()
        height = self.winfo_height()
        points = [self.corner_radius, 0,
                  width - self.corner_radius, 0,
                  width, self.corner_radius,
                  width, height - self.corner_radius,
                  width - self.corner_radius, height,
                  self.corner_radius, height,
                  0, height - self.corner_radius,
                  0, self.corner_radius]
        if self.border_color and self.border_width > 0:
            self.create_polygon(points, smooth=True, fill=self.border_color, tags="border")
            self.tag_lower("border")
            shrink = self.border_width
            points = [self.corner_radius + shrink, shrink,
                      width - self.corner_radius - shrink, shrink,
                      width - shrink, self.corner_radius + shrink,
                      width - shrink, height - self.corner_radius - shrink,
                      width - self.corner_radius - shrink, height - shrink,
                      self.corner_radius + shrink, height - shrink,
                      shrink, height - self.corner_radius - shrink,
                      shrink, self.corner_radius + shrink]
        self.create_polygon(points, smooth=True, fill=self.fill_color, tags="rect")
        self.tag_lower("rect")

class App:
    # Init
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', True)
        self.root.minsize(800, 500)
        self.root.config(bg="#232334")
        self.header_bar = tk.Frame(self.root, bg="#18181b")
        self.header_bar.pack(side="top", fill="x")
        header_inner = tk.Frame(self.header_bar, bg="#18181b")
        header_inner.pack(side="left", padx=32, pady=(0, 8), anchor="center")
        try:
            image_path = os.path.join(os.path.dirname(__file__), 'dist', 'Cavite_State_University_(CvSU).png')
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((54, 54), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(pil_image)
            self.logo_label = tk.Label(header_inner, image=self.logo_image, bg="#18181b")
            self.logo_label.pack(side="left", pady=0)
        except Exception:
            self.logo_label = tk.Label(header_inner, text="Logo", bg="#18181b", fg="white")
            self.logo_label.pack(side="left", pady=0)
        header_text_frame = tk.Frame(header_inner, bg="#18181b")
        header_text_frame.pack(side="left", padx=(18, 0), anchor="center", pady=(0, 8))
        tk.Label(header_text_frame, text="CAVITE STATE UNIVERSITY", font=("Arial", 13, "bold"), fg="white", bg="#18181b").pack(anchor="w")
        tk.Label(header_text_frame, text="SILANG CAMPUS", font=("Arial", 18, "bold"), fg="#7ee787", bg="#18181b").pack(anchor="w")
        tk.Label(header_text_frame, text="TRUTH | EXCELLENCE | SERVICE", font=("Arial", 13, "bold"), fg="white", bg="#18181b").pack(anchor="w")
        self.center_frame = tk.Frame(self.root, bg="#232334")
        self.center_frame.pack(expand=True)
        panel_width = 560
        panel_height = 420
        gap = 56
        panel_color = "#444b5a"
        border_color = "#232334"
        self.right_panel = tk.Frame(
            self.center_frame, width=panel_width, height=panel_height,
            bg=panel_color, highlightbackground=border_color, highlightthickness=2, bd=0
        )
        self.right_panel.pack(side="left", padx=(0, 0), pady=0)
        self.right_panel.pack_propagate(False)
        self.right_panel.config(relief="ridge")
        self.right_panel.after(10, lambda: self.right_panel.config(highlightbackground=border_color))
        self.right_panel.update()
        self.right_panel_canvas = tk.Canvas(self.right_panel, width=panel_width, height=panel_height, bg=panel_color, highlightthickness=0, bd=0)
        self.right_panel_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.right_panel_canvas.create_rectangle(8, 8, panel_width-8, panel_height-8, outline=border_color, width=2, fill=panel_color)
        self.right_panel_canvas.create_rectangle(8, 8, panel_width-8, panel_height-8, outline='', width=0, fill='', tags='shadow')
        self.right_panel_canvas.lower('all')
        self.exit_btn = tk.Canvas(self.right_panel, width=36, height=36, bg=panel_color, highlightthickness=0)
        self.exit_btn.place(relx=1.0, y=18, anchor="ne")
        self.exit_oval = self.exit_btn.create_oval(2, 2, 34, 34, fill="#fff", outline="#fff", width=2)
        self.exit_btn.create_oval(4, 4, 32, 32, fill='', outline="#232334", width=1)
        self.exit_text = self.exit_btn.create_text(18, 18, text="✕", fill="#D9534F", font=("Arial", 15, "bold"))
        self.exit_btn.bind("<Button-1>", lambda e: self.root.destroy())
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.itemconfig(self.exit_oval, outline="#C9302C"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.itemconfig(self.exit_oval, outline="#fff"))
        right_content = tk.Frame(self.right_panel, bg=panel_color)
        right_content.place(relx=0, rely=0, relwidth=1, relheight=1)
        subtitle = tk.Label(
            right_content,
            text="DCIT 25 - Data Structure and Algorithms",
            font=("Arial", 10, "italic"), fg="#bfc7d5", bg=panel_color
        )
        subtitle.pack(anchor="w", padx=30, pady=(24, 0))
        right_title = tk.Label(
            right_content,
            text="INSERTION SORT VISUALIZER",
            font=("Arial", 14, "bold"), fg="white", bg=panel_color
        )
        right_title.pack(anchor="w", padx=30, pady=(6, 8))
        dev_label = tk.Label(
            right_content,
            text="Developers:", font=("Arial", 10, "bold"), fg="#bfc7d5", bg=panel_color
        )
        dev_label.pack(anchor="w", padx=30)
        devs = [
            "• Joson, Ivan",
            "• Mamorno, Joshua",
            "• Miano, Mike Jester",
            "• Pilar, Mark Aljon",
            "• Santos, Dave Ulrich",
            "• Toledana, Cedrick"
        ]
        for dev in devs:
            tk.Label(right_content, text=dev, font=("Arial", 10), fg="#e0e6f0", bg=panel_color).pack(anchor="w", padx=48, pady=0)
        tk.Label(right_content, bg=panel_color).pack(pady=8)
        self.go_sort_button = tk.Button(
            right_content,
            text="Go sort",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#232334",
            activebackground="#33CCFF",
            relief="flat",
            command=self.on_go_sort_click
        )
        self.go_sort_button.pack(pady=(0, 0), ipadx=60, ipady=12, anchor="center")
        self.go_sort_button.bind("<Enter>", lambda e: self.go_sort_button.config(bg="#33CCFF"))
        self.go_sort_button.bind("<Leave>", lambda e: self.go_sort_button.config(bg="#232334"))
        self.left_panel = tk.Frame(
            self.center_frame, width=panel_width, height=panel_height,
            bg=panel_color, highlightbackground=border_color, highlightthickness=2, bd=0
        )
        self.left_panel.pack(side="left", padx=(0, gap), pady=0)
        self.left_panel.pack_propagate(False)
        self.left_panel.config(relief="ridge")
        self.left_panel.after(10, lambda: self.left_panel.config(highlightbackground=border_color))
        self.left_panel.update()
        self.left_panel_canvas = tk.Canvas(self.left_panel, width=panel_width, height=panel_height, bg=panel_color, highlightthickness=0, bd=0)
        self.left_panel_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.left_panel_canvas.create_rectangle(8, 8, panel_width-8, panel_height-8, outline=border_color, width=2, fill=panel_color)
        self.left_panel_canvas.create_rectangle(8, 8, panel_width-8, panel_height-8, outline='', width=0, fill='', tags='shadow')
        self.left_panel_canvas.lower('all')
        left_content = tk.Frame(self.left_panel, bg=panel_color)
        left_content.place(relx=0.5, rely=0.5, anchor="center")
        left_title = tk.Label(
            left_content,
            text="Welcome to the Insertion Sort Visualizer!",
            font=("Arial", 14, "bold"),
            fg="white", bg=panel_color, pady=4
        )
        left_title.pack(pady=(0, 8))
        left_desc = tk.Label(
            left_content,
            text=(
                "Insertion Sort builds the final sorted array (or list) one item at a time.\n"
                "It iterates through the input elements and removes one element per iteration,\n"
                "finds the place within the sorted array, and inserts it there.\n\n"
                "This visualization will help you understand:\n"
                "- How elements are compared and shifted.\n"
                "- The 'sorted' and 'unsorted' portions of the array.\n"
                "- The step-by-step process of placing an element in its correct position.\n\n"
                "Insertion Sort is efficient for small data sets or data sets that are already substantially sorted."
            ),
            font=("Arial", 10), fg="white", bg=panel_color, justify="center", wraplength=410
        )
        left_desc.pack(pady=(0, 0), padx=8)
    # Button click
    def on_go_sort_click(self):
        print("Redirecting to loading screen...")
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            loading_screen_path = os.path.join(current_dir, "loading_screen.py")
            subprocess.Popen([sys.executable, loading_screen_path])
            self.root.destroy()
        except Exception as e:
            print(f"Error launching loading screen: {e}")
            tk.messagebox.showerror("Error", f"Could not launch loading screen: {e}")

# Main run
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()