import tkinter as tk
from tkinter import messagebox

# Create a new window
window = tk.Tk()
window.title("Hello World GUI")

# Create a button widget
button = tk.Button(window, text="Click me!", command=lambda: messagebox.showinfo("Hello", "Hello, World!"))
button.pack(padx=50, pady=20)

# Run the main event loop
window.mainloop()