#member_types.py
#!/usr/env/bin python3

def select_member_type():
    """
    Presents a menu for selecting a member type.

    Returns:
        str: Selected member type.
    """
    member_types = [
        "Guest",
        "Member",
        "Master of Ceremonies",
        "Keynote Speaker",
        "Kitchen Staff",
        "Waiter",
        "Usher"
    ]

    print("\n** Member Types **\n")
    for i, member_type in enumerate(member_types):
        print(f"{i+1}. {member_type}")

    while True:
        try:
            choice = int(input("Enter your choice (1-7): "))
            if 1 <= choice <= len(member_types):
                return member_types[choice - 1]  # Return the selected member type
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")
