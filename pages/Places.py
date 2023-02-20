import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pickle
import numpy as np
import Recommendations
import CityPlaces

add_logo("images/icons/place-app-walking-tour.png")


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

options = locs['City_Place'].to_list()
options.insert(0,'')
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
    

if 'place_clicked' in st.session_state:
    if st.session_state['place_clicked'] is not None:
        click = st.session_state['place_clicked']
        place_clicked = click
        places_load(place_clicked)

