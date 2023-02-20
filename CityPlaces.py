import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

style = st.markdown("""
<style>
.big-font{
    font-size:100px ;
}
.med-font{
    font-size:50px;
}
.small-font[
    font-size:16px
]
</style>
""",unsafe_allow_html=True)

places_dict = pickle.load(open('./pickle_files/places_dict.pkl','rb'))
locs = pd.DataFrame(places_dict)


def show_city_places(city):
    col1,col2,col3 = st.columns(3)
    col_n = city.index
    for place in col_n:        
        if(place%3==0):
            with col1:
                if st.button(city.iloc[place]['Place'], key=f"col1_button_{place}_{city.iloc[place]['Place']}"):
                    st.experimental_set_query_params(city_place_id=place)
                    st.session_state['place_clicked'] = city.iloc[place]['City_Place']
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                
        if(place%3==1):
            with col2:
                if st.button(city.iloc[place]['Place'], key=f"col1_button_{place}_{city.iloc[place]['Place']}"):
                    st.experimental_set_query_params(city_place_id=place)
                    st.session_state['place_clicked'] = city.iloc[place]['City_Place']
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if(place%3==2):
            with col3:
                if st.button(city.iloc[place]['Place'], key=f"col1_button_{place}_{city.iloc[place]['Place']}"):
                    st.experimental_set_query_params(city_place_id=place)
                    st.session_state['place_clicked'] = city.iloc[place]['City_Place']
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                                        
    params = st.experimental_get_query_params()
    city_place_id = params.get("city_place_id", None)

    # Reset key argument and reload the page
    if city_place_id is not None:
        st.experimental_set_query_params()
        st.experimental_rerun()
        

def show_places(places):
    col1, col2, col3 = st.columns(3)
    col_n = len(places)
    for p in range(col_n):
        if p % 3 == 0:
            with col1:
                if st.button(places[p], key=f"col1_button_{p}_{places[p]}"):
                    st.experimental_set_query_params(place_id=p)
                    st.session_state['place_clicked'] = places[p]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if p % 3 == 1:
            with col2:
                if st.button(places[p], key=f"col2_button_{p}_{places[p]}"):
                    st.experimental_set_query_params(place_id=p)
                    st.session_state['place_clicked'] = places[p]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if p % 3 == 2:
            with col3:
                if st.button(places[p], key=f"col3_button_{p}_{places[p]}"):
                    st.experimental_set_query_params(place_id=p)
                    st.session_state['place_clicked'] = places[p]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                    
    params = st.experimental_get_query_params()
    place_id = params.get("place_id", None)

    # Reset key argument and reload the page
    if place_id is not None:
        st.experimental_set_query_params()
        st.experimental_rerun()


def show_cities(city):
    col1,col2,col3 = st.columns(3)
    col_n = len(city)
    for c in range(col_n):
        if(c%3==0):
            with col1:
                if st.button(city[c], key=f"col1_button_{c}_{city[c]}"):
                    st.experimental_set_query_params(city_id=c)
                    st.session_state['city_clicked'] = city[c]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if(c%3==1):
            with col2:
                if st.button(city[c], key=f"col1_button_{c}_{city[c]}"):
                    st.experimental_set_query_params(city_id=c)
                    st.session_state['city_clicked'] = city[c]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if(c%3==2):
            with col3:
                if st.button(city[c], key=f"col1_button_{c}_{city[c]}"):
                    st.experimental_set_query_params(city_id=c)
                    st.session_state['city_clicked'] = city[c]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                    
    params = st.experimental_get_query_params()
    city_id = params.get("city_id", None)

    # Reset key argument and reload the page
    if city_id is not None:
        st.experimental_set_query_params()
        st.experimental_rerun()


def place_description(place):
    if place in locs['Place'].unique():
        p = locs[locs['Place']==place]        
    else:
        p = locs[locs['City_Place']==place]

    s= p.iloc[0]['City_Place']
    p_desc = p.iloc[0]['Place_desc'] 

    c= st.container()
    c.markdown(f'<p class= med-font style= color:orange;>{s}</p>',unsafe_allow_html=True)
    c.markdown(f'<p class= small-font>{p_desc}</p><br><br>',unsafe_allow_html=True)

def city_description(city):
    ct=locs[locs['City']==city].reset_index()
    ct_desc = ct.iloc[0]['City_desc']
    st.markdown(f'<p class= big-font style= color:pink;>{city}</p><p class= small-font>{ct_desc}</p><br>',unsafe_allow_html=True)
    show_city_places(ct)
