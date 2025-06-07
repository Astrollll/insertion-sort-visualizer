import tkinter as tk
from tkinter import ttk

class Activity6_Trees_Allen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("The Family Tree")
        self.geometry("300x400")

        tree = ttk.Treeview(self)

        henry = tree.insert("", "end", text="Henry", open=True)
        
        barry = tree.insert(henry, "end", text="Barry Allen")
        nora = tree.insert(barry, "end", text="Nora Allen")
        eobard = tree.insert(barry, "end", text="Eobard Allen")
        oliver = tree.insert(nora, "end", text="Oliver Queen")
        thea = tree.insert(nora, "end", text="Thea Queen")
        ray = tree.insert(eobard, "end", text="Ray Allen")
        cisco = tree.insert(eobard, "end", text="Cisco Allen")
        
        jay = tree.insert(henry, "end", text="Jay Allen")
        bruce = tree.insert(jay, "end", text="Bruce Allen")
        clark = tree.insert(jay, "end", text="Clark Allen")
        joe = tree.insert(bruce, "end", text="Joe Allen")
        wally = tree.insert(bruce, "end", text="Wally Allen")
        snow = tree.insert(clark, "end", text="Snow Allen")
        flakes = tree.insert(clark, "end", text="Flakes Allen")
        
        tree.pack(expand=True, fill='both')

if __name__ == "__main__":
    app = Activity6_Trees_Allen()
    app.mainloop()