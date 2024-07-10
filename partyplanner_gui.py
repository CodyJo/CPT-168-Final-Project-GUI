#partyplanner_gui.py
#!/usr/env/bin python3

import tkinter as tk
from tkinter import ttk, messagebox
import guest_management
import menu_choices

class PartyPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Party Planner")
        self.create_main_menu()

    def create_main_menu(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Party Planner Main Menu", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="Add Guest", command=self.add_guest_window).grid(row=1, column=0, pady=5)
        ttk.Button(frame, text="Delete Guest", command=self.delete_guest_window).grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Modify Guest", command=self.modify_guest_window).grid(row=1, column=2, pady=5)

    def add_guest_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Guest")

        ttk.Label(add_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = ttk.Entry(add_window)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = ttk.Entry(add_window)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Guest Type:").grid(row=2, column=0, padx=5, pady=5)
        self.guest_type_combobox = ttk.Combobox(add_window, values=["Guest", "Member", "Master of Ceremonies", "Keynote Speaker", "Kitchen Staff", "Waiter", "Usher"])
        self.guest_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Amount Paid:").grid(row=3, column=0, padx=5, pady=5)
        self.amount_paid_entry = ttk.Entry(add_window)
        self.amount_paid_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Menu Choice:").grid(row=4, column=0, padx=5, pady=5)
        self.menu_choice_combobox = ttk.Combobox(add_window, values=["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"])
        self.menu_choice_combobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(add_window, text="Add Guest", command=self.add_guest).grid(row=5, column=0, columnspan=2, pady=10)

    def add_guest(self):
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
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Guest")

        ttk.Label(delete_window, text="Select Guest to Delete:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.guest_combobox = ttk.Combobox(delete_window, values=guest_list)
        self.guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(delete_window, text="Delete Guest", command=self.delete_guest).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_guest(self):
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
        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modify Guest")

        ttk.Label(modify_window, text="Select Guest to Modify:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.modify_guest_combobox = ttk.Combobox(modify_window, values=guest_list)
        self.modify_guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(modify_window, text="Select", command=self.show_modify_options).grid(row=1, column=0, columnspan=2, pady=10)

    def show_modify_options(self):
        selected_guest = self.modify_guest_combobox.get()
        if not selected_guest:
            messagebox.showerror("Error", "Please select a guest to modify.")
            return

        guest_id = int(selected_guest.split(":")[0])

        modify_options_window = tk.Toplevel(self.root)
        modify_options_window.title("Modify Guest Options")

        ttk.Label(modify_options_window, text="Select Item to Modify:").grid(row=0, column=0, padx=5, pady=5)

        options = ["First Name", "Last Name", "Guest Type", "Amount Paid", "Menu Choice"]
        self.modify_option_combobox = ttk.Combobox(modify_options_window, values=options)
        self.modify_option_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(modify_options_window, text="Next", command=self.show_modify_input).grid(row=1, column=0, columnspan=2, pady=10)

    def show_modify_input(self):
        selected_option = self.modify_option_combobox.get()
        if not selected_option:
            messagebox.showerror("Error", "Please select an item to modify.")
            return

        selected_guest = self.modify_guest_combobox.get()
        if not selected_guest:
            messagebox.showerror("Error", "Please select a guest to modify.")
            return

        guest_id = int(selected_guest.split(":")[0])

        modify_input_window = tk.Toplevel(self.root)
        modify_input_window.title("Modify Guest Input")

        if selected_option in ["First Name", "Last Name", "Amount Paid"]:
            ttk.Label(modify_input_window, text=f"Enter new {selected_option}:").grid(row=0, column=0, padx=5, pady=5)
            self.modify_entry = ttk.Entry(modify_input_window)
            self.modify_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Button(modify_input_window, text="Modify", command=lambda: self.modify_guest(guest_id, selected_option)).grid(row=1, column=0, columnspan=2, pady=10)

        elif selected_option == "Guest Type":
            ttk.Label(modify_input_window, text=f"Select new {selected_option}:").grid(row=0, column=0, padx=5, pady=5)
            self.modify_combobox = ttk.Combobox(modify_input_window, values=["Guest", "Member", "Master of Ceremonies", "Keynote Speaker", "Kitchen Staff", "Waiter", "Usher"])
            self.modify_combobox.grid(row=0, column=1, padx=5, pady=5)

            ttk.Button(modify_input_window, text="Modify", command=lambda: self.modify_guest(guest_id, selected_option)).grid(row=1, column=0, columnspan=2, pady=10)

        elif selected_option == "Menu Choice":
            ttk.Label(modify_input_window, text=f"Select new {selected_option}:").grid(row=0, column=0, padx=5, pady=5)
            self.modify_combobox = ttk.Combobox(modify_input_window, values=["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"])
            self.modify_combobox.grid(row=0, column=1, padx=5, pady=5)

            ttk.Button(modify_input_window, text="Modify", command=lambda: self.modify_guest(guest_id, selected_option)).grid(row=1, column=0, columnspan=2, pady=10)

    def modify_guest(self, guest_id, selected_option):
        if selected_option in ["First Name", "Last Name", "Amount Paid"]:
            new_value = self.modify_entry.get()
        elif selected_option == "Guest Type":
            new_value = self.modify_combobox.get()
        elif selected_option == "Menu Choice":
            new_value = self.modify_combobox.get()

        success = guest_management.modify_guest(guest_id, selected_option.lower().replace(" ", "_"), new_value)

        if success:
            messagebox.showinfo("Success", f"Guest {selected_option} modified successfully.")
        else:
            messagebox.showerror("Error", f"Failed to modify guest {selected_option}.")

def main():
    root = tk.Tk()
    app = PartyPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()