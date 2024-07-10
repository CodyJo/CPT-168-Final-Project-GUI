#database.py
#!/usr/env/bin python3

'''
mysql-connector-python module is required to communicate with the MySQL database.
Test to see if mysql-connector-python is present and if not, offer to install it.
'''
try:
    import mysql.connector
except ImportError:
    install = input("Required module 'mysql-connector-python' is missing. Install it now? (y/n)")

    if install.lower == 'y':
        print("Installing mysql-connector-python using pip...")
        #Run subprocess for pip to install mysql-connector-python
        import subprocess
        subprocess.check_call(["pip", "install", "mysql-connector-python"])
    else:
        print("Unable to proceed. Required module is not present and will not be installed. Exiting program.")
        exit()

"""
This module attempts to search for a MySQL server instance on the local machine. If this fails, it will connect to a remote MySQL server to handle data processing.

Variables: 
        LOCAL_HOST  - The address of the local MySQL Server Instance to test
        REMOTE_HOST - The address (Domain or IP) of the remote MySQL Server Instance to test
        USER        - The username to use when connecting to the MySQL Server Instance
        PASSWORD    - The password to use when connecting to the MySQL Server Instance
        DATABASE    - The name of the MySQL schema (database) used by this program
        TABLE_NAME  - The name of the MySQL table used by this program

The default values provided 
"""
# Define global variables for the connector
LOCAL_HOST = "localhost"
REMOTE_HOST = "lollis-home.ddns.net"
USER = "CPT168"
PASSWORD = "Password12#$"
DATABASE = "cpt168"
TABLE_NAME = "party_info"

def connect_to_database():
    """
    connect_to_database()

    Connects to the MySQL database.

    Returns:
        connection: MySQL database connection object if successful, otherwise None.
    """
    try:
        # Try connecting to local MySQL instance
        connection = mysql.connector.connect(
            host=LOCAL_HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        print("Connected to local MySQL instance")
        return connection

    except mysql.connector.Error as err:
        print("Connection to local MySQL instance failed:", err)
        # Fallback to remote connection in a new try block
        try:
            connection = mysql.connector.connect(
                host=REMOTE_HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            print("Connected to remote MySQL instance (lollis-home.ddns.net)")
            return connection

        except mysql.connector.Error as err:
            print("Connection to remote MySQL instance failed:", err)
            return None

def add_guest(data):
    """
    add_guest

    Adds a new guest to the database.

    Args:
        data (tuple): Tuple containing guest information (f_name, l_name, member_type, amt_paid, menu_item).

    Returns:
        bool: True if the guest is added successfully, False otherwise.
    """
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        insert_query = f"INSERT INTO {TABLE_NAME} (f_name, l_name, member_type, amt_paid, menu_item) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (data[0], data[1], data[2], data[3], data[4]))

        connection.commit()
        print("Guest added successfully.")
        return True

    except mysql.connector.Error as err:
        print("Error adding guest:", err)
        return False

    finally:
        if connection:
            connection.close()

def modify_guest(data):
    """
    modify_guest

    Modifies an existing guest in the database.

    Args:
        data (tuple): Tuple containing guest information to modify (must include "UPDATE" flag, guest_id, and updated fields).

    Returns:
        bool: True if the guest is modified successfully, False otherwise.
    """
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        guest_id = data[1]
        update_fields = []
        data_for_update = []

        if data[2] is not None:
            update_fields.append("f_name = %s")
            data_for_update.append(data[2])
        if data[3] is not None:
            update_fields.append("l_name = %s")
            data_for_update.append(data[3])
        if data[4] is not None:
            update_fields.append("member_type = %s")
            data_for_update.append(data[4])
        if data[5] is not None:
            update_fields.append("amt_paid = %s")
            data_for_update.append(data[5])
        if data[6] is not None:
            update_fields.append("menu_item = %s")
            data_for_update.append(data[6])

        if update_fields:
            update_query = f"UPDATE {TABLE_NAME} SET {', '.join(update_fields)} WHERE party_id = %s"
            data_for_update.append(guest_id)
            cursor.execute(update_query, tuple(data_for_update))
            connection.commit()
            print("Guest modified successfully.")
            return True
        else:
            print("No data provided to modify the guest.")
            return False

    except mysql.connector.Error as err:
        print("Error modifying guest:", err)
        return False

    finally:
        if connection:
            connection.close()

def delete_guest(guest_id):
    """
    delete_guest

    Deletes a guest from the database based on guest_id.

    Args:
        guest_id (int): ID of the guest to delete.

    Returns:
        bool: True if the guest is deleted successfully, False otherwise.
    """
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        delete_query = f"DELETE FROM {TABLE_NAME} WHERE party_id = %s"
        cursor.execute(delete_query, (guest_id,))
        connection.commit()
        print("Guest deleted successfully.")
        return True

    except mysql.connector.Error as err:
        print("Error deleting guest:", err)
        return False

    finally:
        if connection:
            connection.close()

def list_guests():
    """
    list_guests
    
    Lists all guests in the database.

    Returns:
        list: List of tuples containing guest information (party_id, f_name, l_name, member_type, amt_paid, menu_item).
    """
    connection = connect_to_database()
    if not connection:
        return None

    try:
        cursor = connection.cursor()

        select_query = f"SELECT party_id, f_name, l_name, member_type, amt_paid, menu_item FROM {TABLE_NAME}"
        cursor.execute(select_query)

        guests = cursor.fetchall()
        return guests

    except mysql.connector.Error as err:
        print("Error listing guests:", err)
        return None

    finally:
        if connection:
            connection.close()
