import tkinter as tk
from tkinter import ttk, messagebox
from guest_dao import GuestDAO
from validation import Validation

class GuestGUI:
    """GUI for managing guest records."""
    
    def __init__(self, root=None):
        """Initialize the guest management window."""
        # If root is provided (tk.Toplevel), use it. Otherwise create our own.
        if root is not None:
            self.root = root
            self.owns_window = False
        else:
            self.root = tk.Tk()
            self.owns_window = True
        
        self.root.title("Guest Management")
        self.root.geometry("900x600")
        
        self.guest_dao = GuestDAO()
        self.validation = Validation()
        
        self.current_guest_id = None
        self.guest_data = []
        
        self._build_ui()
        
        if self.owns_window:
            self.root.mainloop()
    
    def _build_ui(self):
        """Build the UI - separated from __init__ for cleanliness."""
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(self.main_frame, text="Guest Management", font=("Helvetica", 18, "bold"), bg="white")
        title.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self.main_frame, bg="white")
        form_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        form_title = tk.Label(form_frame, text="Guest Profile Management", font=("Arial", 12, "bold"), bg="white")
        form_title.pack(anchor="w")
        
        # Create form fields
        self.guest_id_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.credit_card_var = tk.StringVar()
        
        fields = [
            ("Guest ID", self.guest_id_var, True),
            ("First Name", self.first_name_var, False),
            ("Last Name", self.last_name_var, False),
            ("Phone Number", self.phone_var, False),
            ("Email", self.email_var, False),
            ("Credit Card", self.credit_card_var, False),
        ]
        
        for label_text, var, disabled in fields:
            row_frame = tk.Frame(form_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=3)
            
            label = tk.Label(row_frame, text=label_text + ":", width=15, anchor="e", bg="white")
            label.pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(row_frame, textvariable=var, width=40)
            if disabled:
                entry.config(state=tk.DISABLED)
            if label_text == "Credit Card":
                entry.config(show="*")
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Listbox frame
        list_frame = tk.Frame(self.main_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        list_title = tk.Label(list_frame, text="Registered Guests", font=("Arial", 10, "bold"), bg="white")
        list_title.pack(anchor="w")
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.guest_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=12)
        self.guest_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.guest_listbox.bind('<<ListboxSelect>>', self.on_guest_select)
        scrollbar.config(command=self.guest_listbox.yview)
        
        # Button frame
        btn_frame = tk.Frame(self.main_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save", command=self.save, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete, width=10).pack(side=tk.LEFT, padx=5)
        
        self.load_guests()

    def load_guests(self):
        """Load and display guest list."""
        result = self.guest_dao.find_all()
        if result['status'] == 'Success':
            self.guest_listbox.delete(0, tk.END)
            self.guest_data = result['data']
            for guest in self.guest_data:
                display_text = f"ID: {guest['GuestID']} | {guest['FirstName']} {guest['LastName']}"
                self.guest_listbox.insert(tk.END, display_text)
    
    def on_guest_select(self, event):
        """Handle guest selection from listbox."""
        selection = self.guest_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.guest_data):
                guest = self.guest_data[index]
                
                self.current_guest_id = guest['GuestID']
                self.guest_id_var.set(str(guest['GuestID']))
                self.first_name_var.set(guest['FirstName'])
                self.last_name_var.set(guest['LastName'])
                self.phone_var.set(guest['PhoneNumber'])
                self.email_var.set(guest['Email'])
                self.credit_card_var.set(guest['CreditCardNum'])
    
    def save(self):
        """Save guest data."""
        data = {
            'FirstName': self.first_name_var.get(),
            'LastName': self.last_name_var.get(),
            'PhoneNumber': self.phone_var.get(),
            'Email': self.email_var.get(),
            'CreditCardNum': self.credit_card_var.get()
        }
        
        if not data['FirstName'] or not self.validation.is_alphabetic(data['FirstName']):
            messagebox.showwarning("Validation Error", "First Name must contain only letters.")
            return
        
        if self.current_guest_id:
            result = self.guest_dao.update(self.current_guest_id, data)
        else:
            result = self.guest_dao.create(data)
        
        if result['status'] == 'Success':
            messagebox.showinfo("Success", result['message'])
            self.clear_form()
            self.load_guests()
        else:
            messagebox.showerror("Error", result['message'])
    
    def clear_form(self):
        """Clear all form fields."""
        self.guest_id_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.credit_card_var.set("")
        self.current_guest_id = None
        self.guest_listbox.selection_clear(0, tk.END)
    
    def delete(self):
        """Delete selected guest."""
        if not self.current_guest_id:
            messagebox.showwarning("Warning", "Please select a guest.")
            return
        
        if messagebox.askyesno("Confirm", "Delete this record?"):
            result = self.guest_dao.delete(self.current_guest_id)
            if result['status'] == 'Success':
                self.clear_form()
                self.load_guests()