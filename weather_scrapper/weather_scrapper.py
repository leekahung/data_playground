###############################################################################
# Name: WeatherScrapper                                                       #
# File Name: weather_scrapper.py                                              #
# Description: Program that scrape for weather forecast for any city in the   #
#              US through the National Weather Service's website:             # 
#              forecast.weather.gov                                           #
###############################################################################
# Usage: python weather_scrapper.py                                           # 
#        Code will ask for city location in the US                            #
# Input Format: city name, state(optional)                                    #
###############################################################################
# By: Ka Hung Lee                                                             #
# Programming Language: Python3                                               #
# Version: 1.3.3                                                              #
# Version Date: 12/16/2021                                                    #
###############################################################################

# Import Dependencies
import requests
import re
import pandas as pd
import numpy as np
import dateutil.parser as parser
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

# Retrieve location coordinates
def get_location():
    address = input("Enter city name in the US: ")
    geolocator = Nominatim(user_agent="my_application")
    location = geolocator.geocode(address)
    while "United States" not in str(location):
        address = input("Please enter a city in the US: ")
        location = geolocator.geocode(address)
    else:
        return location

location = get_location()

print("----------------------------------------------------------------------") 
print("Obtaining geo-coordinates for: {}...".format(location.address))
print("----------------------------------------------------------------------")

loc_lat = round(location.latitude, 4)
loc_long = round(location.longitude, 4)

print("Location Coordinates")
print("Location Latitude: {}".format(loc_lat))
print("Location Longitude: {}".format(loc_long))

# Retrieve weather source
link = ("https://forecast.weather.gov/MapClick.php?lat=" 
        + str(loc_lat)
        + "&lon="
        + str(loc_long))

page = requests.get(link)

print("----------------------------------------------------------------------") 
print("Server Status")
print("Response: {}".format(page.status_code))
print("----------------------------------------------------------------------") 

# Parse Webpage
soup = BeautifulSoup(page.content, "html.parser")

# Retrieve Current Weather Conditions and Details
current_conditions = soup.find(id="current_conditions-summary")
current_cond_detailed = soup.find(id="current_conditions_detail")

current_weather = (current_conditions
                   .find(class_="myforecast-current")
                   .get_text())
current_temp_F = (current_conditions
                  .find(class_="myforecast-current-lrg")
                  .get_text())
current_temp_C = (current_conditions
                  .find(class_="myforecast-current-sm")
                  .get_text())

print("Current Weather Status")
print("Weather: {}".format(current_weather))
print("Temperature (°F): {}".format(current_temp_F))
print("Temperature (°C): {}".format(current_temp_C))
print("")

details = []

for detail in current_cond_detailed.find_all("tr"):
    details.append(detail.find_all("td"))

print("Current Weather Details")
for detail in list(details):
    if detail[0].get_text() == "Last update":
        print("")
        date = detail[1].get_text().replace("\n", "").strip()
        print("{}: {}".format(detail[0].get_text(), date))
    else:
        print("{}: {}".format(detail[0].get_text(), detail[1].get_text()))

# Date/Time Extraction (might be useful in the future)
local_time = parser.parse(date, ignoretz=True)

# Retrieve Weather Advisories and Forecasts
seven_day_forecast = soup.find(id="seven-day-forecast-body")
forecast_items = seven_day_forecast.find_all(class_="tombstone-container")

period = []
short_desc = []
temp = []
desc = []

for forecast in forecast_items:
    try:
        period.append(forecast.find(class_="period-name").get_text())
    except AttributeError:
        period.append(np.nan)
    try:
        short_desc.append(forecast.find(class_="short-desc").get_text())
    except AttributeError:
        short_desc.append(np.nan)
    try:
        temp.append(forecast.find(class_="temp").get_text())
    except AttributeError:
        temp.append(np.nan)
    img = forecast.find("img")
    desc.append(img["title"])

# Output Framework
weather_df = pd.DataFrame({"Period": period,
                           "Short Description": short_desc,
                           "Temp (°F)": temp,
                           "Description": desc})

weather_advisories = weather_df[weather_df["Temp (°F)"].isna()]

print("----------------------------------------------------------------------") 
print("Weather Advisories:")
if weather_advisories.empty == True:
    print("No advisories at this time.")
else:
    print(weather_advisories)
print("----------------------------------------------------------------------")

weather_df.dropna(inplace=True)

weather_df["Temp"] = weather_df["Temp (°F)"].str.extract('(\d+)').astype(int)
temp_C = round((5./9) * (weather_df["Temp"] - 32), 0)
weather_df["Temp (°C)"] = temp_C.astype(int)

is_night = weather_df["Period"].str.contains("ight")
weather_df["is_night"] = is_night

# Defining function to add spaces before capitalized words in text
def space_before_capital(text):
   return re.sub(r"(\w)([A-Z])", r"\1 \2", text)

for column in ["Period", "Short Description"]:
    weather_df[column] = weather_df[column].apply(space_before_capital)

weather_df = weather_df.set_index("Period")

print("Weather Forecasts:")
print(weather_df)
print("----------------------------------------------------------------------") 
