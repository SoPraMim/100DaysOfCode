##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

# --- Imports --- #
import pandas as pd
import datetime as dt
import random
from motivational_quote_sender import send_mail

# --- Variables --- #
ROOT = "Day 031 - 040/Day 032 - Birthday Wisher/"
sender = "Andre"

# --- Program --- #
# 1. Read the csv.
birthdays_df = pd.read_csv(ROOT + "birthdays.csv")

# 2. Check current date and compare to the list.
now = dt.datetime.now()

for _,row in birthdays_df.iterrows():
    if now.month == row["month"] and now.day == row["day"]:
        
        # 3. If the date matches, pick a random letter.
        letter_index = random.randint(1,3)
        with open(ROOT + f"letter_templates/letter_{letter_index}.txt") as file:
            text = file.read()
            # 4. Replace the placeholders with the data from the table.
            subject = "Happy Birthday!!!"
            text = text.replace("[NAME]", row["name"])
            text = text.replace("[USER]", sender)
            recipients = [row["email"]]
        send_mail(subject,text,recipients)