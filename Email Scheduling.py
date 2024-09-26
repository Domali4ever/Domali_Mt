
import schedule
import time
from Email_Campaign_Updated import run_campaign  # Import the campaign script to run

# Schedule the email campaign to run daily at 9:00 AM
schedule.every().day.at("09:00").do(run_campaign)

# Continuously run the schedule
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
