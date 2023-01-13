import pandas as pd
from functions import *

# Load air quality data
df_air_quality = pd.read_csv('helsinki-air-quality.csv')
print(df_air_quality.head())

df_air_quality = add_aqi_column(df_air_quality)
df_air_quality = add_city_column(df_air_quality, 'Helsinki')

df_air_quality.date = df_air_quality.date.apply(timestamp_2_time)
df_air_quality.sort_values(by = ['date'], inplace = True, ignore_index = True)
print(df_air_quality.head())

# Load weather data
df_weather = pd.read_csv('helsinki-weather-quality.csv')
print(df_weather.head())

df_weather.rename(
    columns={"name": "city", "datetime": "date"}, inplace=True)

df_weather.date = df_weather.date.apply(timestamp_2_time_weather)
df_weather.sort_values(by=['date'], inplace=True, ignore_index=True)

print(df_weather.head())

#Replace NaNs with 0
df_air_quality = remove_nans_in_csv(df_air_quality)
df_weather = remove_nans_in_csv(df_weather)

#Remove features that we don't get from the API
df_weather = df_weather.drop(columns=["precipprob", "preciptype", "uvindex",
                             "severerisk", "sunrise", "sunset", "moonphase", "description", "icon", "stations"])
df_air_quality = df_air_quality.drop(columns=["no2", "so2"])


print("DF AIR ---------------------------------------------")
print(df_air_quality.head())
print("DF WEATHER -----------------------------------------")
print(df_weather.head())

#Connect to Hopsworks, create and upload feature groups
import hopsworks
project = hopsworks.login()
fs = project.get_feature_store() 

air_quality_fg = fs.get_or_create_feature_group(
        name = 'air_quality_fg',
        description = 'Air Quality characteristics of each day',
        version = 1,
        primary_key = ['city','date'],
        online_enabled = True,
        event_time = 'date'
    )    
air_quality_fg.insert(df_air_quality)

weather_fg = fs.get_or_create_feature_group(
        name = 'weather_fg',
        description = 'Weather characteristics of each day',
        version = 1,
        primary_key = ['city','date'],
        online_enabled = True,
        event_time = 'date'
    )
weather_fg.insert(df_weather)