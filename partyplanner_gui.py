# partyplanner_gui.py
# !/usr/env/bin python3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import csv
import guest_management
import menu_choices

class PartyPlannerGUI:
    """
    A GUI application for managing guests and generating reports for a party planner system.
    """

    def __init__(self, root):
        """
        Initialize the PartyPlannerGUI application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Party Planner")
        self.current_window = None
        self.create_main_menu()

    def create_main_menu(self):
        """
        Create the main menu interface with buttons for Add Guest, Delete Guest, Modify Guest, and Reports.
        """
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Party Planner Main Menu", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="Add Guest", command=self.add_guest_window).grid(row=1, column=0, pady=5)
        ttk.Button(frame, text="Delete Guest", command=self.delete_guest_window).grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Modify Guest", command=self.modify_guest_window).grid(row=1, column=2, pady=5)
        ttk.Button(frame, text="Reports", command=self.reports_window).grid(row=1, column=3, pady=5)

    def close_current_window(self):
        """
        Close the currently open window if it exists.
        """
        if self.current_window is not None and self.current_window.winfo_exists():
            self.current_window.destroy()
        self.current_window = None

    def add_guest_window(self):
        """
        Open a new window to add a guest with fields for first name, last name, guest type, amount paid, and Menu Item.
        """
        self.close_current_window()
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Add Guest")

        ttk.Label(self.current_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = ttk.Entry(self.current_window)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.current_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = ttk.Entry(self.current_window)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.current_window, text="Guest Type:").grid(row=2, column=0, padx=5, pady=5)
        self.guest_type_combobox = ttk.Combobox(self.current_window, values=["Guest", "Member", "Master of Ceremonies", "Keynote Speaker", "Kitchen Staff", "Waiter", "Usher"])
        self.guest_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.current_window, text="Amount Paid:").grid(row=3, column=0, padx=5, pady=5)
        self.amount_paid_entry = ttk.Entry(self.current_window)
        self.amount_paid_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.current_window, text="Menu Item:").grid(row=4, column=0, padx=5, pady=5)
        self.menu_choice_combobox = ttk.Combobox(self.current_window, values=["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"])
        self.menu_choice_combobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.current_window, text="Add Guest", command=self.add_guest).grid(row=5, column=0, columnspan=2, pady=10)

    def add_guest(self):
        """
        Validate input, prepare data, and pass to guest_management to add a new guest.
        Display success or error message based on the operation result.
        """
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        guest_type = self.guest_type_combobox.get()
        amount_paid = self.amount_paid_entry.get()
        menu_choice = self.menu_choice_combobox.get()

        # Validate input
        if not (first_name and last_name and guest_type and menu_choice):
            messagebox.showerror("Error", "All fields except 'Amount Paid' are required.")
            return

        # Handle amount paid input
        try:
            amt_paid = float(amount_paid) if amount_paid else 0.0
        except ValueError:
            messagebox.showerror("Error", "Amount Paid must be a valid number.")
            return

        # Prepare data and pass to guest_management
        data_to_add = (first_name, last_name, guest_type, amt_paid, menu_choice)
        success = guest_management.add_guest(data_to_add)

        # Display success or error message
        if success:
            messagebox.showinfo("Success", "Guest added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add guest.")

    def delete_guest_window(self):
        """
        Open a new window to select and delete a guest.
        """
        self.close_current_window()
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Delete Guest")

        ttk.Label(self.current_window, text="Select Guest to Delete:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.guest_combobox = ttk.Combobox(self.current_window, values=guest_list)
        self.guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.current_window, text="Delete Guest", command=self.delete_guest).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_guest(self):
        """
        Delete the selected guest from the database.
        Display success or error message based on the operation result.
        """
        selected_guest = self.guest_combobox.get()
        if not selected_guest:
            messagebox.showerror("Error", "Please select a guest to delete.")
            return

        guest_id = int(selected_guest.split(":")[0])

        success = guest_management.delete_guest(guest_id)
        if success:
            messagebox.showinfo("Success", "Guest deleted successfully.")
        else:
            messagebox.showerror("Error", "Failed to delete guest.")

    def modify_guest_window(self):
        """
        Open a new window to select a guest and the field to modify.
        """
        self.close_current_window()
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Modify Guest")

        ttk.Label(self.current_window, text="Select Guest to Modify:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.modify_guest_combobox = ttk.Combobox(self.current_window, values=guest_list)
        self.modify_guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.current_window, text="Select", command=self.show_modify_options).grid(row=1, column=0, columnspan=2, pady=10)

    def show_modify_options(self):
        """
        Open a new window to select the field to modify for the selected guest.
        """
        selected_guest = self.modify_guest_combobox.get()
        if not selected_guest:
            messagebox.showerror("Error", "Please select a guest to modify.")
            return

        guest_id = int(selected_guest.split(":")[0])

        self.close_current_window()
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Modify Guest Options")

        ttk.Label(self.current_window, text="Select Item to Modify:").grid(row=0, column=0, padx=5, pady=5)

        options = ["First Name", "Last Name", "Guest Type", "Amount Paid", "Menu Item"]
        self.modify_option_combobox = ttk.Combobox(self.current_window, values=options)
        self.modify_option_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.current_window, text="Next", command=self.show_modify_input).grid(row=1, column=0, columnspan=2, pady=10)
