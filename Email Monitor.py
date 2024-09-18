
import win32com.client
import configparser
import mysql.connector
import logging

# Set up logging
logging.basicConfig(filename='email_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read credentials from the config file
config = configparser.ConfigParser()
config.read('config.ini')

mysql_password = config['credentials']['mysql_password']

# Connect to MySQL database using credentials from config file
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ProspectDB',
            user='root',
            password=mysql_password
        )
        logging.info("Connected to MySQL successfully.")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None

# Monitor Outlook inbox for replies
def monitor_outlook_inbox():
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.Folders["glalonde@catglobal.ca"].Folders["Inbox"]
        messages = inbox.Items

        for message in messages:
            subject = message.Subject.lower()
            body = message.Body.lower()
            sender = message.SenderEmailAddress

            if "out of office" in subject:
                handle_out_of_office(sender)
            elif "opt-out" in body:
                handle_opt_out(sender)
            elif "bad email" in body:
                handle_bad_email(sender)
            elif "follow-up" in subject:
                handle_follow_up_request(sender)

            message.UnRead = False  # Mark email as read

    except Exception as e:
        logging.error(f"Error in Outlook monitoring: {e}")

# Handle different email replies
def handle_out_of_office(sender):
    logging.info(f"Out of office detected from {sender}")
    # Logic to handle out of office (e.g., postpone emails)

def handle_opt_out(sender):
    logging.info(f"Opt-out request from {sender}")
    connection = connect_db()
    if not connection:
        logging.error("Failed to connect to MySQL. Opt-out process aborted.")
        return

    cursor = connection.cursor()
    query = "UPDATE prospectdb.crm_data SET opted_out = 1 WHERE email = %s"
    cursor.execute(query, (sender,))
    connection.commit()
    cursor.close()
    connection.close()

def handle_bad_email(sender):
    logging.info(f"Bad email detected for {sender}")
    # Logic to flag the email as invalid

def handle_follow_up_request(sender):
    logging.info(f"Follow-up request from {sender}")
    # Logic to prioritize this prospect for follow-up

# Monitor the inbox periodically
monitor_outlook_inbox()
