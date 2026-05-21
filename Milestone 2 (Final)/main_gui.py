import tkinter as tk
from tkinter import ttk


class MainGUI:
    """Main navigation window for the reservation system."""
    
    def __init__(self, root):
        """Initialize the main menu window."""
        self.root = root
        self.root.title("Antique Hotel and Spa - Reservation System")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="Antique Hotel and Spa",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Reservation Management System",
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)
        
        menu_label = tk.Label(
            content_frame,
            text="Main Menu",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            fg="#000000"
        )
        menu_label.pack(pady=20)
        
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        guest_button = tk.Button(
            button_frame,
            text="Guest Management",
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=15,
            cursor="hand2",
            command=self.open_guest_gui,
            relief=tk.RAISED,
            bd=2
        )
        guest_button.pack(fill=tk.X, pady=10)
        
        reservation_button = tk.Button(
            button_frame,
            text="Reservation Management",
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=15,
            cursor="hand2",
            command=self.open_reservation_gui,
            relief=tk.RAISED,
            bd=2
        )
        reservation_button.pack(fill=tk.X, pady=10)
        
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.root.quit,
            relief=tk.RAISED,
            bd=2
        )
        exit_button.pack(fill=tk.X, pady=10)
    
    def open_guest_gui(self):
        """Open the Guest Management window."""
        from guest_gui import GuestGUI
        guest_window = tk.Toplevel(self.root)
        GuestGUI(guest_window)
    
    def open_reservation_gui(self):
        """Open the Reservation Management window."""
        from reservation_gui import ReservationGUI
        reservation_window = tk.Toplevel(self.root)
        ReservationGUI(reservation_window)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    main_gui = MainGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
