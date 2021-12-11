###############################################################################
# Name: WeatherScrapper                                                       #
# File Name: weather_scrapper.py                                              #
# Description: Program that scrape for weather forecast for any city in the   #
#              US through the National Weather Service's website:             # 
#              forecast.weather.gov                                           #
###############################################################################
# Usage: python weather_scrapper.py                                           # 
#        Code will ask for city location                                      #
# Input Format: city name, state(optional)                                    #
# Output Format: Pandas DataFrame (Index, Period, Short Description, Temp(str)#
#                , Description, Temp(int), is_night)                          #
###############################################################################
# By: Ka Hung Lee                                                             #
# Programming Language: Python                                                #
# Version: 1.1                                                                #
# Date: 12/10/2021                                                            #
###############################################################################

# Import Dependencies
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

# Retrieving your location
address = input("Enter city name: ")
geolocator = Nominatim(user_agent="my_application")
location = geolocator.geocode(address)
print("Obtaining geo-coordinates for: {}...".format(location.address))
loc_lat = round(location.latitude, 4)
loc_long = round(location.longitude, 4)
print("Location latitude: {}".format(loc_lat))
print("Location longitude: {}".format(loc_long))

# Weather page of interest
link = "https://forecast.weather.gov/MapClick.php?lat=" + str(loc_lat) + \
"&lon=" + str(loc_long)
page = requests.get(link)
print("Web status: {}".format(page.status_code))

# Forecast Parser
soup = BeautifulSoup(page.content, "html.parser")

seven_day_forecast = soup.find(id="seven-day-forecast-body")
forecast_items = seven_day_forecast.find_all(class_="tombstone-container")

period = []
short_desc = []
temp = []
desc = []

for item in forecast_items:
    try:
        period.append(item.find(class_="period-name").get_text())
    except AttributeError:
        period.append(np.nan)
    try:
        short_desc.append(item.find(class_="short-desc").get_text())
    except AttributeError:
        short_desc.append(np.nan)
    try:
        temp.append(item.find(class_="temp").get_text())
    except AttributeError:
        temp.append(np.nan)
    img = item.find("img")
    desc.append(img["title"])

weather_df = pd.DataFrame({"Period": period,
                           "Short Description": short_desc,
                           "Temp (°F)": temp,
                           "Description": desc})

weather_advisories = weather_df[weather_df["Temp (°F)"].isna()]
print("----------------------------------------------------------------------") 
print("Weather Advisories:")
print(weather_advisories)

print("----------------------------------------------------------------------")

weather_df.dropna(inplace=True)

weather_df["Temp"] = weather_df["Temp (°F)"].str.extract('(\d+)').astype(int)
temp_C = round((5./9) * (weather_df["Temp"] - 32), 0)
weather_df["Temp (°C)"] = temp_C.astype(int)

is_night = weather_df["Period"].str.contains("Night")
weather_df["is_night"] = is_night

print("Weather Forecasts:")
print(weather_df)
print("----------------------------------------------------------------------") 
