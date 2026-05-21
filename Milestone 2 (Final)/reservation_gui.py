import tkinter as tk
from tkinter import ttk, messagebox
from reservation_dao import ReservationDAO
from guest_dao import GuestDAO
from staff_dao import StaffDAO
from validation import Validation

class ReservationGUI:
    """GUI for managing reservation records."""
    
    def __init__(self, root=None):
        """Initialize the reservation management window."""
        # If root is provided (tk.Toplevel), use it. Otherwise create our own.
        if root is not None:
            self.root = root
            self.owns_window = False
        else:
            self.root = tk.Tk()
            self.owns_window = True
        
        self.root.title("Reservation Management")
        self.root.geometry("1100x700")
        self.root.configure(bg='#f4f5f7')
        
        self.reservation_dao = ReservationDAO()
        self.guest_dao = GuestDAO()
        self.staff_dao = StaffDAO()
        self.validation = Validation()
        
        self.current_reservation_id = None
        self.guest_data = []
        self.staff_data = []
        self.room_type_data = []
        self.num_rooms_var = tk.IntVar(self.root, value=1)
        self.room_type_var = tk.StringVar(self.root)
        self.status_var = tk.StringVar(self.root, value='Confirmed')
        
        self._build_ui()
        
        if self.owns_window:
            self.root.mainloop()
    
    def _build_ui(self):
        """Build the UI - separated from __init__ for cleanliness."""
        # Create main frame (uses pack for main containers)
        self.main_frame = tk.Frame(self.root, bg='#f4f5f7')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create card container (inner frame)
        card_frame = tk.Frame(self.main_frame, bg='white', relief=tk.FLAT)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title = ttk.Label(card_frame, text="Reservation Management", font=("Helvetica", 18, "bold"), background='white')
        title.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(card_frame, text="Process Room Reservation", padding=10)
        form_frame.pack(fill=tk.X, padx=0, pady=5)
        
        # Create variables bound to root
        self.reservation_id_var = tk.StringVar(self.root)
        self.guest_id_var = tk.StringVar(self.root)
        self.staff_id_var = tk.StringVar(self.root)
        self.check_in_var = tk.StringVar(self.root)
        self.check_out_var = tk.StringVar(self.root)
        self.num_adults_var = tk.IntVar(self.root, value=1)
        self.num_children_var = tk.IntVar(self.root, value=0)
        self.num_infants_var = tk.IntVar(self.root, value=0)
        self.promo_code_var = tk.StringVar(self.root)
        
        # Create form fields using grid layout
        row = 0
        
        # Reservation ID
        ttk.Label(form_frame, text="Reservation ID:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.reservation_id_var, state="disabled", width=40).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Guest Selection
        ttk.Label(form_frame, text="Guest Selection:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.guest_combo = ttk.Combobox(form_frame, textvariable=self.guest_id_var, state="readonly", width=37)
        self.guest_combo.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Staff Attendant
        ttk.Label(form_frame, text="Staff Attendant:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.staff_combo = ttk.Combobox(form_frame, textvariable=self.staff_id_var, state="readonly", width=37)
        self.staff_combo.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Room Type
        ttk.Label(form_frame, text="Room Type:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.room_combo = ttk.Combobox(form_frame, textvariable=self.room_type_var, state="readonly", width=23)
        self.room_combo.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1
        
        # Check-In Date
        ttk.Label(form_frame, text="Check-In (YYYY-MM-DD):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.check_in_var, width=40).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Check-Out Date
        ttk.Label(form_frame, text="Check-Out (YYYY-MM-DD):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.check_out_var, width=40).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Number of Rooms
        ttk.Label(form_frame, text="Number of Rooms:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Spinbox(form_frame, from_=1, to=5, textvariable=self.num_rooms_var, width=23).grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1
        
        # Adults
        ttk.Label(form_frame, text="Adults:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Spinbox(form_frame, from_=1, to=8, textvariable=self.num_adults_var, width=37).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Children
        ttk.Label(form_frame, text="Children:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Spinbox(form_frame, from_=0, to=6, textvariable=self.num_children_var, width=37).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Infants
        ttk.Label(form_frame, text="Infants:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Spinbox(form_frame, from_=0, to=2, textvariable=self.num_infants_var, width=37).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1
        
        # Status
        ttk.Label(form_frame, text="Status:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.status_combo = ttk.Combobox(form_frame, textvariable=self.status_var, state="readonly", width=23, values=['Confirmed', 'Checked-In', 'Cancelled', 'Completed'])
        self.status_combo.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1
        
        # Promo Code
        ttk.Label(form_frame, text="Promo Code:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.promo_code_var, width=40).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        
        # Configure grid column weights for form responsiveness
        form_frame.columnconfigure(1, weight=1)
        
        # Listbox frame (uses pack for main containers)
        list_frame = ttk.LabelFrame(card_frame, text="Active Bookings", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.reservation_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=12, font=("Courier", 9))
        self.reservation_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.reservation_listbox.bind('<<ListboxSelect>>', self.on_reservation_select)
        scrollbar.config(command=self.reservation_listbox.yview)
        
        # Button frame (uses pack for main containers)
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(fill=tk.X, padx=0, pady=10)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Book Now", command=self.save, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete, width=10).pack(side=tk.LEFT, padx=5)
        
        self.load_dropdown_data()
        self.load_reservations()
    
    def load_dropdown_data(self):
        """Load guest, staff, and room type data for dropdowns."""
        guest_result = self.guest_dao.find_ids()
        if guest_result['status'] == 'Success':
            self.guest_data = guest_result['data']
            guest_values = [f"{g['GuestID']}: {g['FullName']}" for g in self.guest_data]
            self.guest_combo['values'] = guest_values
        
        staff_result = self.staff_dao.find_ids()
        if staff_result['status'] == 'Success':
            self.staff_data = staff_result['data']
            staff_values = [f"{s['StaffID']}: {s['FullName']}" for s in self.staff_data]
            self.staff_combo['values'] = staff_values
        
        # Load room types (example: replace with actual DAO call if available)
        self.room_type_data = [
            {'RoomTypeID': 1, 'TypeName': 'Standard'},
            {'RoomTypeID': 2, 'TypeName': 'Deluxe'},
            {'RoomTypeID': 3, 'TypeName': 'Suite'}
        ]
        room_type_values = [f"{rt['RoomTypeID']}: {rt['TypeName']}" for rt in self.room_type_data]
        self.room_combo['values'] = room_type_values
    
    def load_reservations(self):
        """Load and display reservation list."""
        result = self.reservation_dao.find_all()
        if result['status'] == 'Success':
            self.reservation_listbox.delete(0, tk.END)
            for res in result['data']:
                display_text = (
                    f"ID: {res['ReservationID']:3} | "
                    f"Guest: {res['GuestName']:20} | "
                    f"Staff: {res['StaffName']:20} | "
                    f"Check-In: {res['CheckInDate']}"
                )
                self.reservation_listbox.insert(tk.END, display_text)
    
    def on_reservation_select(self, event):
        """Handle reservation selection from listbox."""
        selection = self.reservation_listbox.curselection()
        if selection:
            index = selection[0]
            display_text = self.reservation_listbox.get(index)
            reservation_id = int(display_text.split(" | ")[0].split(": ")[1])
            
            result = self.reservation_dao.find_by_id(reservation_id)
            if result['status'] == 'Success':
                res = result['data']
                self.current_reservation_id = res['ReservationID']
                self.reservation_id_var.set(str(res['ReservationID']))
                
                guest_display = f"{res['GuestID']}: {res['GuestName']}"
                self.guest_combo.set(guest_display)
                
                staff_display = f"{res['StaffID']}: {res['StaffName']}"
                self.staff_combo.set(staff_display)
                
                self.check_in_var.set(res['CheckInDate'])
                self.check_out_var.set(res['CheckOutDate'])
                self.num_adults_var.set(res['NumAdults'])
                self.num_children_var.set(res['NumChildren'])
                self.num_infants_var.set(res['NumInfants'])
                self.promo_code_var.set(res['PromoCode'] if res['PromoCode'] else "")
    
    def save(self):
        """Save reservation data."""
        guest_selection = self.guest_id_var.get()
        staff_selection = self.staff_id_var.get()
        
        if not guest_selection or not staff_selection:
            messagebox.showwarning("Validation Error", "Please select both Guest and Staff.")
            return
        
        try:
            guest_id = int(guest_selection.split(":")[0])
            staff_id = int(staff_selection.split(":")[0])
        except (ValueError, IndexError):
            messagebox.showwarning("Validation Error", "Invalid Guest or Staff selection.")
            return
        
        room_type_selection = self.room_type_var.get()
        if not room_type_selection:
            messagebox.showwarning("Validation Error", "Please select a Room Type.")
            return
        
        try:
            room_type_id = int(room_type_selection.split(":")[0])
        except (ValueError, IndexError):
            messagebox.showwarning("Validation Error", "Invalid Room Type selection.")
            return
        
        check_in = self.check_in_var.get()
        check_out = self.check_out_var.get()
        
        if not check_in or not self.validation.is_valid_date(check_in):
            messagebox.showwarning("Validation Error", "Check-In Date must be in YYYY-MM-DD format.")
            return
        
        if not check_out or not self.validation.is_valid_date(check_out):
            messagebox.showwarning("Validation Error", "Check-Out Date must be in YYYY-MM-DD format.")
            return
        
        if check_in >= check_out:
            messagebox.showwarning("Validation Error", "Check-In Date must be before Check-Out Date.")
            return
        
        data = {
            'GuestID': guest_id,
            'StaffID': staff_id,
            'RoomTypeID': room_type_id,
            'CheckInDate': check_in,
            'CheckOutDate': check_out,
            'NumRooms': self.num_rooms_var.get(),
            'NumAdults': self.num_adults_var.get(),
            'NumChildren': self.num_children_var.get(),
            'NumInfants': self.num_infants_var.get(),
            'Status': self.status_var.get(),
            'PromoCode': self.promo_code_var.get() if self.promo_code_var.get() else None
        }
        
        if self.current_reservation_id:
            result = self.reservation_dao.update(self.current_reservation_id, data)
        else:
            result = self.reservation_dao.create(data)
        
        if result['status'] == 'Success':
            messagebox.showinfo("Success", result['message'])
            self.clear_form()
            self.load_reservations()
        else:
            messagebox.showerror("Error", result['message'])
    
    def clear_form(self):
        """Clear all form fields."""
        self.reservation_id_var.set("")
        self.guest_id_var.set("")
        self.staff_id_var.set("")
        self.room_type_var.set("")
        self.check_in_var.set("")
        self.check_out_var.set("")
        self.num_rooms_var.set(1)
        self.num_adults_var.set(1)
        self.num_children_var.set(0)
        self.num_infants_var.set(0)
        self.status_var.set('Confirmed')
        self.promo_code_var.set("")
        self.current_reservation_id = None
        self.reservation_listbox.selection_clear(0, tk.END)
    
    def delete(self):
        """Delete selected reservation."""
        if not self.current_reservation_id:
            messagebox.showwarning("Warning", "Please select a reservation to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Reservation ID {self.current_reservation_id}?"):
            result = self.reservation_dao.delete(self.current_reservation_id)
            
            if result['status'] == 'Success':
                messagebox.showinfo("Success", result['message'])
                self.clear_form()
                self.load_reservations()
                messagebox.showinfo("Success", result['message'])
                self.clear_form()
                self.load_reservations()
            else:
                messagebox.showerror("Error", result['message'])

if __name__ == '__main__':
    root = tk.Tk()
    app = ReservationGUI(root)
    root.mainloop()