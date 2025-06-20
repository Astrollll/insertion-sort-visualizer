"""
Loading screen module for the Insertion Sort Visualizer.
Provides a smooth loading animation with progress bar.
"""

import tkinter as tk
import math
import time
from insertion_sort_visualizer import InsertionSortVisualizer
import tkinter.messagebox as messagebox

def main():
    # Main run
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()

class LoadingScreen(tk.Frame):
    # Init
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self._setup_window()
        self._create_widgets()
        self._initialize_animation_variables()
        self._start_animations()

    # Window
    def _setup_window(self):
        self.root.title("Loading...")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', True)
        self.root.minsize(800, 500)
        self.configure(bg="#000000")
        self.pack(fill=tk.BOTH, expand=True)

    # Widgets
    def _create_widgets(self):
        self.center_frame = tk.Frame(self, bg="#000000")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_label = tk.Label(
            self.center_frame,
            text="Loading, please wait...",
            font=("Segoe UI", 24, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        self.loading_label.pack(pady=(0, 40))
        self.progress_container = tk.Frame(self.center_frame, bg="#000000")
        self.progress_container.pack(pady=25, fill=tk.X, padx=25)
        self.progress_canvas = tk.Canvas(
            self.progress_container,
            height=30,
            bg="#000000",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X)
        self.progress_label = tk.Label(
            self.center_frame,
            text="0%",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        self.progress_label.pack(pady=(15, 0))

    # Vars
    def _initialize_animation_variables(self):
        self.progress = 0
        self.animation_id = None
        self.loading_texts = [
            "Loading, please wait...",
            "Preparing visualization...",
            "Setting up algorithms...",
            "Almost there..."
        ]
        self.current_text_index = 0

    # Anim start
    def _start_animations(self):
        self.simulate_loading()
        self.update_loading_text()

    # Bar update
    def update_progress_bar(self, progress, fill_color=None, outline_color=None):
        if not self.winfo_exists():
            return
        self.progress = progress
        if self.progress_canvas.winfo_exists():
            self.progress_canvas.delete("all")
            self.progress_canvas.configure(bg="#000000")
        bar_height = 8
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        bar_width = width - 4
        bar_y = (height - bar_height) / 2
        self.progress_canvas.create_rectangle(
            2, bar_y,
            width - 2, bar_y + bar_height,
            fill="#000000",
            outline="#FFFFFF"
        )
        fill_width = (bar_width * progress) / 100
        self.progress_canvas.create_rectangle(
            2, bar_y,
            2 + fill_width, bar_y + bar_height,
            fill="#FFFFFF"
        )
        if self.progress_label.winfo_exists():
            self.progress_label.config(text=f"{int(progress)}%")

    # Text update
    def update_loading_text(self):
        if not self.winfo_exists():
            return
        if self.current_text_index < len(self.loading_texts):
            if self.loading_label.winfo_exists():
                self.loading_label.config(text=self.loading_texts[self.current_text_index])
            self.current_text_index += 1
            self.root.after(2000, self.update_loading_text)

    # Fake load
    def simulate_loading(self):
        if not self.winfo_exists():
            return
        if self.progress < 100:
            increment = max(0.1, min(2.0, (100 - self.progress) / 20))
            self.progress += increment
            self.update_progress_bar(self.progress)
            delay = max(20, min(100, int(100 - self.progress)))
            self.animation_id = self.root.after(delay, self.simulate_loading)
        else:
            self.update_progress_bar(100)
            self.root.after(500, self.fade_out)

    # Fade
    def fade_out(self):
        if not self.winfo_exists():
            return
        if self.loading_label.winfo_exists():
            self.loading_label.config(text="Complete!")
        self.root.after(1000, self._start_main_app)

    # App start
    def _start_main_app(self):
        self.destroy()
        app = InsertionSortVisualizer(self.root)

if __name__ == "__main__":
    main() 