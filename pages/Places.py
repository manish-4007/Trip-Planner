import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pickle
import numpy as np
import Recommendations
import CityPlaces,places_details
import folium
from streamlit_folium import st_folium

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")

add_logo("images/icons/place-app-walking-tour.png")


# places_dict = pickle.load(open('./Dataset/pop_locs.csv','rb'))
# locs = pd.DataFrame(places_dict)
locs = pd.read_csv('./Dataset/pop_locs.csv')
hotels = pd.read_csv('./Dataset/Hotels.csv')
df_hotel_loc = pd.read_csv('Dataset/final_hotel_data.csv')

df_hotel_loc.dropna(subset=['latitude', 'longitude'], inplace=True)
df_hotel_loc=df_hotel_loc[~(df_hotel_loc['latitude']==0)]
df_hotel_loc = df_hotel_loc[~(df_hotel_loc['longitude']==0)]
df = df_hotel_loc

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

def convert_place(place_clicked):
    df1 = locs[locs['City_Place']== place_clicked]
    df2 = locs[locs['Place']== place_clicked]

    if not df1.isnull().values.all():
        return df1.iloc[0]['Place']

    elif not df2.isnull().values.all():
        return place_clicked

def places_load(place_clicked):
    CityPlaces.place_description(place_clicked)

    st.markdown(f'<p class= med-font style= color:red;>Other destination places you May Like</p>',unsafe_allow_html=True)
    rec_places = Recommendations.recommend_place(convert_place(place_clicked))
    CityPlaces.show_places(rec_places)

def show_hotel_map(city,df):
    # iterate over each row and delete rows that contain zero in the identified column
    location = geolocator.geocode(city,timeout=None)
    data=df.loc[df['city']==city]
    map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)
   
    # loop through the rows of the data frame and add a marker for each location
    for index, row in data.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        name = row['property_name']
        marker = folium.Circle([lat, lon],radius = 100, popup=name,tooltip=name,color = 'black')
        marker.add_to(map)
    
    st_map = st_folium(map, width=700, height = 400)
    
    

def places_hotel_map(place,city,df):
    # iterate over each row and delete rows that contain zero in the identified column
    location = geolocator.geocode(place,timeout=None)
    p_lat = locs.loc[locs['City_Place']== place, 'latitude'].values[0]
    p_lon = locs.loc[locs['City_Place']== place, 'longitude'].values[0]
    data=df.head(10)
    data_hotel =df

    fg_hotel = folium.FeatureGroup(name = 'Nearby Hotels',show = False)
    map = folium.Map(location=[p_lat, p_lon], zoom_start=12, color= 'red')
    folium.Marker(location=[p_lat, p_lon], zoom_start=12,icon=folium.Icon( color='black'), tooltip=place).add_to(map)

    # loop through the rows of the data frame and add a marker for each location
    for index, row in data.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        name = row['property_name']
        rating = row['rating']
        marker = folium.Marker([lat, lon], popup=name, tooltip=name + f'({rating})', )
        marker.add_to(map)

    data_hotel.apply(
        lambda ll: folium.Circle(
                                location=[ll.latitude, ll.longitude],
                                zoom_start = 12,
                                fill=True,
                                color='black',radius = 100,tooltip=ll.property_name,
                                popup=ll.property_name).add_to(fg_hotel), axis='columns')

    fg_hotel.add_to(map)
    map.add_child(folium.LayerControl())
    st_map = st_folium(map, width=700, height = 400)
    
def show_option(options):
    if 'place_clicked' not in st.session_state:
        st.session_state['place_clicked']= options[0]
    cols = st.columns([10,2])
    with cols[0]:
        option = st.selectbox('Enter Any Place Name',options)

    with cols[1]:
        st.markdown(' <br>', unsafe_allow_html=True)
        st.write('\n')
        search = st.button('Search', key='place_search')
    if search:
        if option=="":
            st.markdown(f"**Enter valid name!!**")
        else:
            st.session_state['place_clicked']= option

if 'city_clicked' in st.session_state:
    options = locs.loc[locs['City'] == st.session_state['city_clicked'], 'City_Place'].to_list()
else:
    options = locs['City_Place'].to_list()

show_option(options)

if 'place_clicked' in st.session_state:
    if st.session_state['place_clicked'] is not None:
        click = st.session_state['place_clicked']
        place_clicked = click
        places_load(place_clicked)
        # show_place_map(place_clicked)

    if 'city_clicked' in st.session_state:
        click = st.session_state['place_clicked']

        p_lat = locs.loc[locs['City_Place']== click, 'latitude'].values[0]
        p_lon = locs.loc[locs['City_Place']== click, 'longitude'].values[0]

        if np.isnan(p_lat):
            location = geolocator.geocode(click)
            if location:
                p_lat = location.latitude
                p_long = location.longitude
                
        city_clicked = locs.loc[locs['City_Place']== click, 'City'].values[0]

        
        data=df.loc[df['city']==city_clicked]
        if data.empty:
            st.subheader("No Hotels Found")
        else:
            centroids = places_details.find_hotels(data)

            if p_lat and np.isnan(p_lat) == False and np.any(centroids):
            
                df = places_details.dist(p_lat,p_lon,centroids, data)
                for i, row in df.iterrows():
                    lat = row['latitude']
                    lon = row['longitude']
                    name = row['property_name']
                    if geodesic((p_lat,p_lon),(lat,lon)).km >5:
                        df = df.drop(i)
                sorted_df = df.sort_values('rating',ascending=False)
                if df.empty== False:
                    places_hotel_map(click,city_clicked,sorted_df)
                    hide_table_row_index = """
                                <style>
                                thead tr th:first-child {display:none}
                                tbody th {display:none}
                                </style>
                                """
                    # Inject CSS with Markdown
                    st.markdown(hide_table_row_index, unsafe_allow_html=True)

                    # Display a static table
                    st.write(sorted_df[['rating', 'price','property_address','property_name']])
                else:
                    show_hotel_map(city_clicked,data)

            else:
                show_hotel_map(city_clicked,data)