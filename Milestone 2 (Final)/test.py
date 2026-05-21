import tkinter as tk

root = tk.Tk()
root.geometry("400x200")
tk.Label(root, text="CAN YOU SEE THIS?", font=("Arial", 20)).pack(pady=20)
tk.Entry(root, highlightbackground="black", highlightthickness=2).pack(pady=20)
root.mainloop()