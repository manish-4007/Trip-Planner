import streamlit as st
from streamlit_extras.app_logo import add_logo
import datetime
import pandas as pd
import pickle
import numpy as np
import Recommendations
import CityPlaces
from pages import Places
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="MyApp")


add_logo("images/icons/cities_destination.png")

places_dict = pickle.load(open('./pickle_files/places_dict.pkl','rb'))
locs = pd.DataFrame(places_dict)

st.markdown("""
<style>
.big-font {
    font-size:100px !important;
}
.med-font{
    font-size:50px;
}
.small-font{
    font-size:16px
}
footer {
    visibility: hidden;}
</style>
""",unsafe_allow_html=True)
    
st.header('City')

options = locs['City']
cols = st.columns([10,2])
with cols[0]:
    option = st.selectbox('Enter Any Place Name',locs['City'].unique())
    df=locs[locs['City']==option].reset_index()
    df = df[['Place', 'City', 'City_Place','Rating']]

with cols[1]:
    st.markdown(' <br>', unsafe_allow_html=True)
    st.write('\n')
    search = st.button('Search', key='city_search')
if search:
    st.session_state['city_clicked']=option

st.markdown(' <br>', unsafe_allow_html=True)
st.markdown(' <br>', unsafe_allow_html=True)
st.markdown(' <br>', unsafe_allow_html=True)
st.subheader(' Enter the data of the passenger to estimate effective cost to visit the Destination Place', )
cols = st.columns(5)
with cols[0]:
    passengers = st.text_input('Enter Passengers', 1)
    
with cols[1]:
    choose_date = datetime.date.today() + datetime.timedelta(days=1)
    d = st.date_input(
        "Enter the travel date",choose_date,min_value=choose_date )

with cols[2]:
    curr_location = st.selectbox('Current City',locs['City'].unique())
with cols[3]:
    dest_location = st.selectbox('Destinaiton City',locs['City'].unique())

with cols[4]:
    st.markdown(' <br>', unsafe_allow_html=True)
    st.write('\n')
    search = st.button('Estimate Cost', key='pass_info')
if search:
    loc1 = geolocator.geocode(curr_location,timeout = None)
    loc2 = geolocator.geocode(dest_location,timeout = None)
    distance = geodesic((loc1.latitude,loc1.longitude),(loc2.latitude,loc2.longitude)).km
    days = str(d-datetime.date.today()).split()[0]
    st.session_state['passengers'] = int(passengers)
    st.session_state['days_remains'] = int(days)
    st.session_state['distance'] = distance
    st.session_state['city_clicked']=dest_location
    st.session_state['curr_loc']=curr_location


def city_load(city_clicked):
    CityPlaces.city_description(city_clicked)
    st.markdown(f'<p class= med-font>Destination you May Like</p>',unsafe_allow_html=True)
    rec_cities = Recommendations.recommend_cities(city_clicked)
    CityPlaces.show_cities(rec_cities)


if 'city_clicked' in st.session_state:
    city_clicked = st.session_state['city_clicked']
    city_load(city_clicked)

if 'place_clicked' in st.session_state:
    if st.session_state['place_clicked'] is not None:

        place_clicked = st.session_state['place_clicked']        
        df1 = locs[locs['City_Place']== place_clicked]
        df2 = locs[locs['Place']== place_clicked]

        if not df1.isnull().values.all():
            place_clicked = df1.iloc[0]['Place']
            
        Places.places_load(place_clicked)
st.session_state['place_clicked'] = None
        
