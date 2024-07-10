#menu_choices.py
#!/usr/env/bin python3

def select_menu_item():
    """
    Presents a menu and allows the user to select a food item.

    Returns:
        str: The selected food item name.
    """
    food_options = ("BEEF", "CHICKEN", "FISH", "PORK", "PASTA", "VEGAN")

    print("\n** Food Menu **\n")
    for i, option in enumerate(food_options):
        print(f"{i+1}. {option}")

    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if 1 <= choice <= len(food_options):
                return food_options[choice - 1]  # Return the selected food item name
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def confirm_modification(menu_item):
    """
    Asks the user for confirmation before modifying the menu item.

    Args:
        menu_item (str): The new menu item being considered for modification.

    Returns:
        bool: True if the user confirms the modification, False otherwise.
    """
    confirmation = input(f"Are you sure you want to change the menu item to {menu_item}? (Y/N): ").upper()
    return confirmation == "Y"
