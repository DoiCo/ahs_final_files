#!/usr/bin/env python3
"""
Minimal test to verify Tkinter widget rendering on macOS.
Run this directly to diagnose rendering issues.
"""
import tkinter as tk

def test_basic_render():
    """Test 1: Basic frame and label rendering."""
    root = tk.Tk()
    root.title("Test 1: Basic Rendering")
    root.geometry("400x300")
    
    frame = tk.Frame(root, bg="white")
    frame.pack(fill=tk.BOTH, expand=True)
    
    label = tk.Label(frame, text="LABEL VISIBLE?", font=("Arial", 16, "bold"), bg="white", fg="black")
    label.pack(pady=20)
    
    entry = tk.Entry(frame, font=("Arial", 12), width=30)
    entry.pack(pady=10)
    entry.insert(0, "CAN YOU SEE THIS?")
    
    button = tk.Button(frame, text="CLICK ME", font=("Arial", 12))
    button.pack(pady=10)
    
    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill=tk.BOTH, expand=True, pady=10)
    for i in range(5):
        listbox.insert(tk.END, f"Item {i+1}")
    
    root.mainloop()

if __name__ == "__main__":
    test_basic_render()
