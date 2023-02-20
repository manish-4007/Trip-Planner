import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo
from st_click_detector import click_detector
import pandas as pd
import pickle
import numpy as np
import Recommendations

add_logo("images/icons/app.png")

city20 = pd.DataFrame(pickle.load(open('./pickle_files/city20_dict.pkl','rb')))
places_to_visit25 = pd.DataFrame(pickle.load(open('./pickle_files/places_to_visit25_dict.pkl','rb')))

places_dict = pickle.load(open('./pickle_files/places_dict.pkl','rb'))
locs = pd.DataFrame(places_dict)
places = locs['City_Place']
cities = locs['City'].unique()

place_desc = pd.read_csv('./Dataset/Places.csv')
city_desc = pd.read_csv('./Dataset/City.csv')


st.title("Place Recommender System")
st.header('Best Cites to Visit')
s=""""""
for i in city20['City']:
    s += f"<a href='#' id='{i}' style = padding:10px;>{i}</a>"
    # s +=f"<a href='#' id={i}><img width='20%' src='https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=200'></a>"

city_clicked = click_detector(s)

style = st.markdown("""
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

city20places = locs[locs['City']==city_clicked].reset_index()

if city_clicked:
    st.session_state['city_clicked'] = city_clicked    
    switch_page('Cities')


st.header('Best Places to Visit')
s=""""""
for i in places_to_visit25['Place']:
    s += f"<a href='#' id='{i}' style = padding:10px;>{i}</a>"
    # s +=f"<a href='#' id={i}><img width='20%' src='https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=200'></a>"

place_clicked = click_detector(s)


if place_clicked:
    st.session_state['place_clicked'] = place_clicked    
    switch_page('Places')


st.write("\n\n")
place_selected = st.selectbox(
    'Enter the place name that you already visited or similar places ',
    places)

if st.button('Recommend Places'):
    place_selected = locs[locs['City_Place']==place_selected].iloc[0]["Place"]
    recommendations = Recommendations.recommend_place(place_selected)
    for i in recommendations:
        st.write(i)

st.header('\n\nBest Recommended Cities')
city_selected = st.selectbox(
    'Enter the City that you already visited or similar Cities ',
    cities)

if st.button('Recommend Cities'):
   recommendations = Recommendations.recommend_cities(city_selected)
   for i in recommendations:
    st.write(i)