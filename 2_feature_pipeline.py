import pandas as pd
from datetime import datetime
from functions import *

date_today = datetime.now().strftime("%Y-%m-%d")
cities = ['Helsinki']
data_air_quality = [get_air_quality_data("Helsinki")]
data_weather = [get_weather_data("Helsinki", date_today)]

df_air_quality = get_air_quality_df(data_air_quality)
print(df_air_quality.head())

df_air_quality.drop(['iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'o3_max', 'o3_min', 'pm10_max', 'pm10_min', 'pm25_max', 'pm25_min', 'uvi_avg', 'uvi_max', 'uvi_min'], axis=1, inplace=True)
print(df_air_quality.head())
df_air_quality.rename(
    columns={"o3_avg": "o3", "pm10_avg": "pm10", "pm25_avg": "pm25"}, inplace=True)

df_air_quality['pm25'] = df_air_quality['pm25'].astype(float)
df_air_quality['pm10'] = df_air_quality['pm10'].astype(float)
df_air_quality['o3'] = df_air_quality['o3'].astype(float)
df_air_quality['aqi'] = df_air_quality['aqi'].astype(float)

df_weather = get_weather_df(data_weather)
df_weather = df_weather.drop(columns=["precipprob", "uvindex"])
df_weather.rename(
    columns={"pressure": "sealevelpressure"}, inplace=True)
print(df_weather.head())

#Connect to Hopsworks and upload data
import hopsworks
project = hopsworks.login()
fs = project.get_feature_store() 

air_quality_fg = fs.get_or_create_feature_group(
    name = 'air_quality_fg',
    primary_key = ['date'],
    version = 1
)
air_quality_fg.insert(df_air_quality)

weather_fg = fs.get_or_create_feature_group(
   name = 'weather_fg',
    primary_key = ['city', 'date'],
   version = 1
)
weather_fg.insert(df_weather)