
import os
import time
import pyautogui
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def open_voxsun():
    # Path to the Voxsun shortcut
    voxsun_shortcut_path = r"C:\Users\Gyslain Lalonde\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\VoxSun Pro.lnk"
    
    if os.path.exists(voxsun_shortcut_path):
        try:
            # Open Voxsun using the shortcut
            os.startfile(voxsun_shortcut_path)
            time.sleep(15)  # Wait for the application to open
            print("Voxsun opened successfully.")
        except Exception as e:
            print(f"Failed to open Voxsun: {e}")
    else:
        print("Voxsun shortcut not found.")

def get_next_phone_number():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='ProspectDB',
            user='root',
            password='DOMALIsql130822!'
        )

        if connection.is_connected():
            print("Connected to the database successfully")

            cursor = connection.cursor()

            # Query to get the next phone number with Pending status
            query = '''
            SELECT * FROM prospectdb.crm_data
            WHERE CallStatus = 'Pending'
            ORDER BY LastContacted ASC
            LIMIT 1;
            '''
            cursor.execute(query)
            row = cursor.fetchone()

            if row:
                print(f"Next contact to call: {row}")
                return row
            else:
                # If no Pending contacts, reset the CallStatus to Pending for all records
                print("All contacts have been called. Resetting the list...")
                reset_query = "UPDATE prospectdb.crm_data SET CallStatus = 'Pending';"
                cursor.execute(reset_query)
                connection.commit()
                return None  # Return None and let the next iteration pick up from the reset list

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def update_contact_status(record_id):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='ProspectDB',
            user='root',
            password='DOMALIsql130822!'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Update the contact status to Completed after the call
            update_query = f"UPDATE prospectdb.crm_data SET CallStatus = 'Completed', LastContacted = NOW() WHERE id = {record_id};"
            cursor.execute(update_query)
            connection.commit()
            print(f"Updated contact {record_id} to Completed.")

    except Error as e:
        print(f"Error while updating contact status in MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def monitor_voxsun_for_call_end():
    # Function to monitor the Voxsun app to detect when a call ends.
    # This can be implemented by checking window status, logs, or process.
    # For now, this is simulated with a placeholder.
    
    print("Monitoring Voxsun app for call end...")
    
    # Placeholder logic (actual detection needs to be implemented):
    time.sleep(10)  # Simulate waiting for a call to end
    print("Call ended. Proceeding to fetch the next phone number...")
    
    # Call ended, so we get the next phone number
    return get_next_phone_number()

if __name__ == "__main__":
    open_voxsun()  # Open the Voxsun application
    while True:
        next_contact = monitor_voxsun_for_call_end()  # Monitor for call end and get the next contact
        if next_contact:
            # Process the next contact (e.g., get phone number and call)
            print("Processing next contact:", next_contact)
            
            # Simulate that the call was made successfully
            record_id = next_contact[0]  # Assuming the first column is the record ID
            update_contact_status(record_id)  # Mark the contact as completed

        time.sleep(5)  # Wait before checking again, adjust as needed
