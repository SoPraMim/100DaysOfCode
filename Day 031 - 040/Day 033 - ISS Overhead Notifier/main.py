# --- Imports --- #
from iss_manager import ISS
from time_manager import TimeManager
from GenericFunctions import send_mail
import time

# --- Global Variables --- #
MY_LAT = 55.676098 # Your latitude
MY_LONG = -12.568337 # Your longitude

iss = ISS()
time_manager = TimeManager(MY_LAT,MY_LONG)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    if iss.is_close(MY_LAT,MY_LONG) and time_manager.is_dark():
        subject = "The ISS is above you."
        body = "Look up! The ISS is above you and it is now visible in the sky."
        recipient = ["andrediastest@yahoo.com"]
        send_mail(subject=subject,body=body,recipients=recipient)
    time.sleep(60)
    iss.update_position()
    time_manager.update_sunrise_sunset()




