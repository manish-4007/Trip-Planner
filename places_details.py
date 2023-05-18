import streamlit as st
from streamlit_extras.app_logo import add_logo
from geopy.geocoders import Nominatim
import pandas as pd
import folium

import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")


# read the CSV file into a pandas dataframe

# identify the column that contains the zero value(s)

from geopy.geocoders import Nominatim

# initialize Nominatim geocoder
geolocator = Nominatim(user_agent='Ashish')

def hotel_map(city):
    df = pd.read_csv('Dataset/final_hotel_data.csv')
    column_to_check = 'longitude'
    l='latitude'
    # iterate over each row and delete rows that contain zero in the identified column
    for index, row in df.iterrows():
        if row[column_to_check] == 0:
            df.drop(index, inplace=True)
    for index, row in df.iterrows():   
        if row[l] == 0:
            df.drop(index, inplace=True)
    # specify the city name
    # city = st.session_state['city_clicked']

    # get the location data (latitude, longitude, altitude) of the city
    location = geolocator.geocode(city,timeout=None)
    data=df.loc[df['city']==city]
    data = data.dropna(subset=['latitude', 'longitude'])
    map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

    # loop through the rows of the data frame and add a marker for each location
    for index, row in data.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        name = row['property_name']
        marker = folium.Marker([lat, lon], popup=name)
        marker.add_to(map)
    return data

def find_hotels(data):
    try:
        k_rng= range(1,15)
        sse=[]
        for k in k_rng:
            km=KMeans(n_clusters=k)
            km.fit(data[['latitude','longitude']])
            sse.append(km.inertia_)
            sse

            km =KMeans(n_clusters=4)
            pre=km.fit_predict(data[['latitude','longitude']])
            pre

            data['cluster']= pre
            centroids=km.cluster_centers_
        return centroids
    except Exception as e:
        print('Clusters not found')
# centroids,data = hotel_map(city)    

from math import sin, cos, sqrt, atan2, radians

# # Approximate radius of earth in km
def dist(latitude ,longitude,centroids,data):
    R = 6373.0
    i=0
    minn=9223372036854775807
    distance=0
    for row in range(4):
        lt=radians(centroids[row][0])
        lg=radians(centroids[row][1])
        dlog=lg-longitude
        dlat=lt-latitude
        # global i
        
        a = sin(dlat / 2)**2 + cos(lt) * cos(latitude) * sin(dlog / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        # global minn
        distance = R * c
        
        if(distance<minn):
            i=row
        
            minn=distance
        data = data.loc[data['cluster']==i]
    return data
      
# lati=radians('user_location')
# longi=radians('user_location')

# df = dist(lati,longi)


# F = df.sort_values('rating',ascending=False)
# F
# s = df.sort_values('price')
# s