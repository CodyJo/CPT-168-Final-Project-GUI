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

    def add_guest_window(self):
        """
        Open a new window to add a guest with fields for first name, last name, guest type, amount paid, and Menu Item.
        """
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

        ttk.Label(add_window, text="Menu Item:").grid(row=4, column=0, padx=5, pady=5)
        self.menu_choice_combobox = ttk.Combobox(add_window, values=["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"])
        self.menu_choice_combobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(add_window, text="Add Guest", command=self.add_guest).grid(row=5, column=0, columnspan=2, pady=10)

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
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Guest")

        ttk.Label(delete_window, text="Select Guest to Delete:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.guest_combobox = ttk.Combobox(delete_window, values=guest_list)
        self.guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(delete_window, text="Delete Guest", command=self.delete_guest).grid(row=1, column=0, columnspan=2, pady=10)

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
        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modify Guest")

        ttk.Label(modify_window, text="Select Guest to Modify:").grid(row=0, column=0, padx=5, pady=5)

        guests = guest_management.list_guests()
        guest_list = [f"{guest[0]}: {guest[1]} {guest[2]}" for guest in guests]

        self.modify_guest_combobox = ttk.Combobox(modify_window, values=guest_list)
        self.modify_guest_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(modify_window, text="Select", command=self.show_modify_options).grid(row=1, column=0, columnspan=2, pady=10)

    def show_modify_options(self):
        """
        Open a new window to select the field to modify for the selected guest.
        """
        selected_guest = self.modify_guest_combobox.get()
        if not selected_guest:
            messagebox.showerror("Error", "Please select a guest to modify.")
            return

        guest_id = int(selected_guest.split(":")[0])

        modify_options_window = tk.Toplevel(self.root)
        modify_options_window.title("Modify Guest Options")

        ttk.Label(modify_options_window, text="Select Item to Modify:").grid(row=0, column=0, padx=5, pady=5)

        options = ["First Name", "Last Name", "Guest Type", "Amount Paid", "Menu Item"]
        self.modify_option_combobox = ttk.Combobox(modify_options_window, values=options)
        self.modify_option_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(modify_options_window, text="Next", command=self.show_modify_input).grid(row=1, column=0, columnspan=2, pady=10)

    def show_modify_input(self):
        """
        Open a new window to enter the new value for the selected field to modify.
        """
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

        elif selected_option == "Menu Item":
            ttk.Label(modify_input_window, text=f"Select new {selected_option}:").grid(row=0, column=0, padx=5, pady=5)
            self.modify_combobox = ttk.Combobox(modify_input_window, values=["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"])
            self.modify_combobox.grid(row=0, column=1, padx=5, pady=5)

            ttk.Button(modify_input_window, text="Modify", command=lambda: self.modify_guest(guest_id, selected_option)).grid(row=1, column=0, columnspan=2, pady=10)

    def modify_guest(self, guest_id, selected_option):
        """
        Modify the selected field of the guest with the new value.

        Args:
            guest_id (int): The ID of the guest to modify.
            selected_option (str): The field to modify.
        """
        if selected_option == "First Name":
            field = "f_name"
        elif selected_option == "Last Name":
            field = "l_name"
        elif selected_option == "Guest Type":
            field = "member_type"
        elif selected_option == "Amount Paid":
            field = "amt_paid"
        elif selected_option == "Menu Item":
            field = "menu_item"
        else:
            messagebox.showerror("Error", "Invalid option selected.")
            return

        # Get the new value based on the selected option
        if selected_option in ["First Name", "Last Name", "Amount Paid"]:
            new_value = self.modify_entry.get()
        elif selected_option == "Guest Type":
            new_value = self.modify_combobox.get()
        elif selected_option == "Menu Item":
            new_value = self.modify_combobox.get()

        # Call guest_management to update the guest field
        success = guest_management.update_guest_field(guest_id, field, new_value)

        if success:
            messagebox.showinfo("Success", f"Guest {selected_option} modified successfully.")
        else:
            messagebox.showerror("Error", f"Failed to modify guest {selected_option}.")

    def reports_window(self):
        """
        Open a new window to select and generate reports.
        """
        report_window = tk.Toplevel(self.root)
        report_window.title("Reports")

        ttk.Label(report_window, text="Reports Menu", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        self.report_option = tk.StringVar()

        ttk.Radiobutton(report_window, text="Attendee's List", variable=self.report_option,
                        value="attendees_list").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(report_window, text="Menu Item Report", variable=self.report_option,
                        value="menu_choice").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(report_window, text="Generate Report", command=self.generate_report).grid(row=3, column=0, padx=5, pady=10, columnspan=2)

    def generate_report(self):
        """
        Generate the selected report based on the user's choice.
        """
        selected_option = self.report_option.get()

        if selected_option == "attendees_list":
            self.attendees_list_report()
        elif selected_option == "menu_choice":
            self.menu_choice_report()
        else:
            messagebox.showerror("Error", "Please select a report type.")

    def attendees_list_report(self):
        """
        Generate and display the Attendee's List report.
        """
        attendees_window = tk.Toplevel(self.root)
        attendees_window.title("Attendee's List Report")

        guests = guest_management.list_guests()

        if not guests:
            messagebox.showinfo("Info", "No guests found.")
            return

        # Create a table
        cols = ("Guest ID", "First Name", "Last Name", "Member Type", "Amount Paid", "Menu Item")
        tree = ttk.Treeview(attendees_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
        for guest in guests:
            tree.insert("", "end", values=guest)

        tree.grid(row=0, column=0, columnspan=2)

        # Summary
        total_guests = len(guests)
        total_paid = sum(guest[4] for guest in guests)
        member_type_count = {}
        for guest in guests:
            member_type = guest[3]
            if member_type in member_type_count:
                member_type_count[member_type] += 1
            else:
                member_type_count[member_type] = 1

        summary_text = f"Total Guests: {total_guests}\nTotal Amount Paid: ${total_paid:.2f}\n\nMember Type Counts:\n"
        for member_type, count in member_type_count.items():
            summary_text += f"{member_type}: {count}\n"

        ttk.Label(attendees_window, text=summary_text, justify="left").grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(attendees_window, text="Export to CSV", command=lambda: self.export_to_csv(guests, cols)).grid(row=2, column=0, columnspan=2, pady=10)

    def menu_choice_report(self):
        """
        Generate and display the Menu Item report.
        """
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu Item Report")

        guests = guest_management.list_guests()

        if not guests:
            messagebox.showinfo("Info", "No guests found.")
            return

        menu_choices = ["BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN"]
        menu_choice_count = {choice: 0 for choice in menu_choices}

        for guest in guests:
            menu_choice = guest[5]
            if menu_choice in menu_choice_count:
                menu_choice_count[menu_choice] += 1

        summary_text = "Menu Item Counts:\n"
        for choice, count in menu_choice_count.items():
            summary_text += f"{choice}: {count}\n"

        ttk.Label(menu_window, text=summary_text, justify="left").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(menu_window, text="Export to CSV", command=lambda: self.export_to_csv([(key, value) for key, value in menu_choice_count.items()], ["Menu Item", "Count"])).grid(row=1, column=0, columnspan=2, pady=10)

    def export_to_csv(self, data, headers):
        """
        Export data to a CSV file with the specified headers.

        Args:
            data (list): The data to export.
            headers (list): The headers for the CSV file.
        """
        file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            messagebox.showinfo("Success", "Data exported to CSV successfully.")


def main():
    """
    Main function to initialize the application.
    """
    root = tk.Tk()
    app = PartyPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
