import tkinter as tk
from tkinter import ttk

def on_scroll(*args):
    canvas.yview(*args)

root = tk.Tk()
root.title("Scrollable Frame Example")

# Create a Canvas widget
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar widget and attach it to the Canvas
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Canvas to use the Scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the Canvas
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Add some widgets to the scrollable frame
for i in range(20):
    ttk.Label(frame, text=f"Label {i}").pack(pady=5)

# Bind the Canvas to the frame size
frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

# Bind the Scrollbar to the Canvas
scrollbar.config(command=on_scroll)

root.mainloop()

