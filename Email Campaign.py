
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import mysql.connector
import logging
import time

# Batch settings
BATCH_SIZE = 50  # Number of emails to send per batch
BATCH_DELAY = 900  # Delay between batches in seconds (15 minutes)

# Set up logging
logging.basicConfig(filename='email_campaign.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to MySQL database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ProspectDB',
            user='root',
            password=os.getenv('MYSQL_PASSWORD')  # Using environment variable for MySQL password
        )
        logging.info("Connected to MySQL successfully.")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None

# Function to send email using Outlook SMTP
def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = "glalonde@catglobal.ca"
        msg['To'] = to_email

        # Connect to Outlook's SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            outlook_password = os.getenv('OUTLOOK_PASSWORD')  # Using environment variable for Outlook password
            smtp.login("glalonde@catglobal.ca", outlook_password)
            smtp.sendmail("glalonde@catglobal.ca", to_email, msg.as_string())

        logging.info(f"Email sent to {to_email}: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")

# Function to schedule and send follow-up emails based on sequence_step
def schedule_emails():
    connection = connect_db()
    if not connection:
        logging.error("Failed to connect to MySQL. Email scheduling aborted.")
        return

    cursor = connection.cursor()

    try:
        while True:
            # Select a batch of BATCH_SIZE contacts who haven't opted out and are due for their next email
            query = ("SELECT id, email, name, sequence_step, last_email_sent FROM prospectdb.crm_data "
                     "WHERE opted_out = 0 AND next_followup_date <= NOW() LIMIT %s")
            cursor.execute(query, (BATCH_SIZE,))
            prospects = cursor.fetchall()

            if not prospects:
                logging.info("No prospects due for follow-up emails.")
                break

            for prospect in prospects:
                prospect_id, email, name, sequence_step, last_email_sent = prospect
                initial_email_date = last_email_sent.strftime('%Y-%m-%d') if last_email_sent else 'N/A'
                send_email_to_prospect(prospect_id, email, name, sequence_step, initial_email_date)

            logging.info(f"Batch of {len(prospects)} emails sent. Waiting for the next batch...")
            connection.commit()  # Commit changes for the batch
            time.sleep(BATCH_DELAY)  # Delay between batches

    except Exception as e:
        logging.error(f"Error in scheduling emails: {e}")

    finally:
        cursor.close()
        connection.close()

# Function to send email to an individual prospect
def send_email_to_prospect(prospect_id, email, name, sequence_step, initial_email_date):
    # Define email templates based on the sequence_step
    email_templates = [
        {
            'subject': "Let’s Schedule a Quick 30-Minute Call to Discuss Opportunities",
            'body': f"Good day {name},

I hope you're doing well.
I wanted to follow up on my previous email sent on {initial_email_date}. "
                    "I hope it didn’t get buried in your inbox. I’m eager to connect with you to better understand how CAT Global can support "
                    "your logistics needs.
Would you have 30 minutes this week or next for a quick Teams call?

Best regards,
Justin Lalonde
CAT Global"
        },
        # Add more templates here for different sequence steps
    ]

    # Select the appropriate template based on the sequence step
    template = email_templates[sequence_step % len(email_templates)]  # Cycle through templates if needed

    # Send the email
    send_email(email, template['subject'], template['body'])

    # Update the database for the next step
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        next_followup_date = datetime.now() + timedelta(days=[0, 3, 5, 7, 10][sequence_step])
        next_step = sequence_step + 1
        query = "UPDATE prospectdb.crm_data SET sequence_step = %s, last_email_sent = NOW(), next_followup_date = %s WHERE id = %s"
        cursor.execute(query, (next_step, next_followup_date, prospect_id))
        connection.commit()
        cursor.close()
        connection.close()

# Main function to run the email campaign
def run_campaign():
    schedule_emails()

# Run the campaign
run_campaign()
