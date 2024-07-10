import database

def add_guest(data):
    """
    Add a new guest to the database.

    Args:
        data (tuple): Tuple containing guest information (f_name, l_name, member_type, amt_paid, menu_item).

    Returns:
        bool: True if the guest is added successfully, False otherwise.
    """
    return database.add_guest(data)

def modify_guest(guest_id, field, new_value):
    """
    Modify a specific field of an existing guest in the database.

    Args:
        guest_id (int): ID of the guest to modify.
        field (str): The field to modify.
        new_value (str): The new value for the field.

    Returns:
        bool: True if the guest is modified successfully, False otherwise.
    """
    return database.modify_guest_field(guest_id, field, new_value)

def delete_guest(guest_id):
    """
    Delete a guest from the database based on guest_id.

    Args:
        guest_id (int): ID of the guest to delete.

    Returns:
        bool: True if the guest is deleted successfully, False otherwise.
    """
    return database.delete_guest(guest_id)

def list_guests():
    """
    List all guests in the database.

    Returns:
        list: List of tuples containing guest information (party_id, f_name, l_name, member_type, amt_paid, menu_item).
    """
    return database.list_guests()

def get_guest_details(guest_id):
    """
    Fetch details of a specific guest from the database based on guest_id.

    Args:
        guest_id (int): ID of the guest.

    Returns:
        tuple: Tuple containing guest information (party_id, f_name, l_name, member_type, amt_paid, menu_item).
    """
    return database.get_guest_details(guest_id)
