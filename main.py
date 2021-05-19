import requests
from datetime import datetime
import smtplib
import time


# Option 1: Have user input information
# asking user to enter their email
# email = input("Enter your email: ")
# asking user to enter their password
# password = input("Enter your password: ")
# asking user to enter their latitude
# MY_LAT = float(input("Enter your latitude: "))
# asking user to enter their longitude
# MY_LONG = float(input("Enter your longitude: "))

# Option 2: Hardcode information
# email = "YOUR EMAIL HERE"
# password = "YOUR PASSWORD HERE"
# MY_LAT = YOUR LATITUDE HERE
# MY_LONG = YOUR LONGITUDE HERE

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if ((MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5)) and ((MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5)):
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    # if statement that checks if it is nigh time
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    # If the ISS is close to my current position
    # and it is currently dark
    # sleeping for 60 seconds
    time.sleep(60)
    if is_iss_overhead() and is_night():
        # send email
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg="Subject:🛰 Look Up 🛰\n\nThe ISS is above you in the sky!")
