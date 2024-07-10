# reports.py
#!/usr/env/bin python3

import database
import locale as lc

lc.setlocale(lc.LC_ALL, "en_US")

def generate_report(report_type):
    if report_type == "attendee":
        return generate_attendee_report()
    elif report_type == "menu":
        return generate_menu_report()
    else:
        return "Invalid report type specified."

def generate_attendee_report():
    guests = database.list_guests()
    if not guests:
        return "No guests found."

    total_members = total_guests = total_staff = total_fees = 0
    staff_types = ["Master of Ceremonies", "Keynote Speaker", "Usher", "Kitchen Staff"]

    report = []
    report.append("** Attendee List **")
    report.append("-" * 76)
    report.append("| Name                     | Type                  | Menu Choice | Fee Paid |")
    report.append("-" * 76)
    
    for guest in guests:
        name = f"{guest[1]} {guest[2]}"
        type_ = guest[3]
        menu_item = guest[5]
        fee_paid = f"${guest[4]:.2f}"

        report.append(f"| {name.ljust(24)} | {type_.ljust(21)} | {menu_item.ljust(11)} | {fee_paid.ljust(8)} |")

        if type_ == "Guest":
            total_guests += 1
        elif type_ == "Member":
            total_members += 1
        elif type_ in staff_types:
            total_staff += 1
        
        total_fees += guest[4]

    report.append("-" * 76)
    report.append(f"Total Members: {total_members}")
    report.append(f"Total Guests: {total_guests}")
    report.append(f"Total Staff: {total_staff}")
    report.append(f"Total Fees Paid: ${total_fees:.2f}")

    return "\n".join(report)

def generate_menu_report():
    guests = database.list_guests()
    if not guests:
        return "No guests found."

    menu_count = {
        "BEEF": 0,
        "CHICKEN": 0,
        "FISH": 0,
        "PORK": 0,
        "PASTA": 0,
        "VEGAN": 0
    }

    for guest in guests:
        menu_item = guest[5]
        if menu_item in menu_count:
            menu_count[menu_item] += 1

    report = ["** Menu Report **"]
    report.append("-" * 14)
    for item, count in menu_count.items():
        report.append(f"| {item.ljust(10)} | {str(count).ljust(5)} |")

    report.append("-" * 14)

    return "\n".join(report)
