import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

geolocator = Nominatim(user_agent="MyApp")

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

model = pickle.load(open('./pickle_files/xgb_model.pkl','rb'))
# places_dict = pickle.load(open('./pickle_files/places_dict.pkl','rb'))
# locs = pd.DataFrame(places_dict)

locs = pd.read_csv('./Dataset/pop_locs.csv')
hotels = pd.read_csv('./Dataset/Hotels.csv')
travel = pd.read_csv('./Dataset/travel_updated.csv')

def predict_cost(city, travel,passengers,days_remaining,distance):
    X = travel[['no_of_passengers',	'days_to_departure', 'distance_km']].values
    y = travel['INR_Amount'].values
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    pred = model.predict(sc.transform([[passengers,np.log(days_remaining),distance]]))

    a = locs[locs['City']==city]
    location = geolocator.geocode("Mumbai",timeout = None)

    dist_place = a[['Place','City_Place','latitude','longitude']]
    lat = a[~(a['latitude'].isnull())]['latitude'].values
    lon = a[~(a['longitude'].isnull())]['longitude'].values
    st  = (location.latitude, location.longitude) #put current location

    for i in zip(lat,lon):
        try:
            pred = model.predict(sc.transform([[passengers,np.log(days_remaining),geodesic(st,i).km]]))
            cost = np.exp(pred)  
            dist_place.loc[dist_place['latitude']==i[0],['Distance']] = geodesic(st,i).km
            dist_place.loc[dist_place['latitude']==i[0],['Cost']] = cost
        except:
            pass
    dist_place=dist_place.sort_values('Distance')
    return dist_place

def day_places(city,places):
    col1,col2,col3 = st.columns(3)
    for i,place in enumerate(places):
        p_id = i
        if(i%3==0):
            with col1:
                if st.button(place, key=f"col1_button_{p_id}_{place}"):
                    st.experimental_set_query_params(city_place_id=p_id)
                    st.session_state['place_clicked'] = city.loc[city['Place']==place,'City_Place'].values[0]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                
        if(i%3==1):
            with col2:
                if st.button(place, key=f"col1_button_{p_id}_{place}"):
                    st.experimental_set_query_params(city_place_id=p_id)
                    st.session_state['place_clicked'] = city.loc[city['Place']==place,'City_Place'].values[0]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
        if(i%3==2):
            with col3:
                if st.button(place, key=f"col1_button_{p_id}_{place}"):
                    st.experimental_set_query_params(city_place_id=p_id)
                    st.session_state['place_clicked'] = city.loc[city['Place']==place,'City_Place'].values[0]
                    # st.markdown(f"**{st.session_state['place_clicked']}** was clicked.")
                    st.experimental_rerun()
                                            
params = st.experimental_get_query_params()
city_place_id = params.get("city_place_id", None)

# Reset key argument and reload the page
if city_place_id is not None:
    st.experimental_set_query_params()
    st.experimental_rerun()
            


def show_city_places(city, passengers=1,days_remaining=10,distance=1000):
    if 'passengers' in st.session_state:
        passengers = st.session_state['passengers']
        days_remaining = st.session_state['days_remains']
        distance = st.session_state['distance']
    ct = city['City'].values[0]
    dist_place = predict_cost(ct, travel,passengers,days_remaining,distance)
    dist_place= dist_place.reset_index(drop=True)
    st.session_state['passengers']  = 1
    st.session_state['days_remains']  = 10
    st.session_state['distance']  = 1000
    
    st.subheader(f"To visit '{ct}' City takes around {int(np.floor(len(dist_place)/6))} - {int(np.ceil(len(dist_place)/5))} days")
    cost = round(dist_place['Cost'].values[0])
    st.subheader(f'It costs Rs. {cost} for {passengers} people')
    day={}
    l=[]
    c =0
    d=0
    for i,j in dist_place.iterrows():
        if c==6:
            day[d] = l
            l=[]
            c=0
            d+=1
        l.append((j[0]))
        c+=1

    day[d] = l
    d_list = ["Day " + str(k+1) for k in day.keys()]
    tab = st.tabs(d_list)
    for i in day: 
        with tab[i]:
            day_places(city,day[i])
            
def show_map(city):
    places = locs.loc[locs['City']==city]
    places_lat_long = places.loc[:,['Place','City_Place', 'Rating','longitude', 'latitude']].dropna()
    best_places_lat_long = places_lat_long[:7]

    city_hotels = hotels.loc[hotels['city']==city]
    hotels_lat_long_area = city_hotels.groupby('locality').first().loc[:, ['property_name','longitude', 'latitude']].dropna().assign(
        n_hotels = hotels.groupby('locality').locality.count(),
        n_reviews = (hotels.assign(site_review_count=hotels.site_review_count.fillna(0))\
                    .groupby('locality').site_review_count.sum())
    )
    hotels_lat_long = city_hotels.loc[:, ['property_name','longitude', 'latitude']].dropna()
    
    location = geolocator.geocode(city,timeout = None)
    m = folium.Map(
        location=[location.latitude, location.longitude],
        zoom_start=12
    )
    try:
        fg_places = folium.FeatureGroup(name = 'All Places',show = False)
        fg_hotel = folium.FeatureGroup(name = 'Hotels',show = False)
        fg_hotel_area = folium.FeatureGroup(name = 'Area-Wise Hotels',show = False)

        best_places_lat_long.apply(
            lambda ll: folium.Marker(
                                    location=[ll.latitude, ll.longitude],
                                    zoom_start = 12,
                                    fill=True,
                                    color='red',
                                    tooltip=ll.Place + '\n(' + str(round(ll.Rating,2))+')',
                                    popup=folium.Popup(ll.City_Place + '\n' + str(round(ll.Rating,2)))).add_to(m), axis='columns')

        places_lat_long.apply(
            lambda ll: folium.Marker(
                                    location=[ll.latitude, ll.longitude],
                                    zoom_start = 12,
                                    fill=True,
                                    color='red',
                                    tooltip=ll.Place + '\n(' + str(round(ll.Rating,2))+')',
                                    popup=ll.Place).add_to(fg_places), axis='columns')

        hotels_lat_long.apply(
            lambda ll: folium.Circle(
                                    location=[ll.latitude, ll.longitude],
                                    zoom_start = 12,
                                    fill=True,
                                    color='black',
                                    popup=ll.property_name).add_to(fg_hotel), axis='columns')

        
        max_n_hotels = hotels_lat_long_area.n_hotels.max()
        hotels_lat_long_area.apply(
            lambda ll: folium.Circle(
                                location=[ll.latitude, ll.longitude],
                                radius=2000 * (ll.n_hotels / max_n_hotels),  #for region where hotels are present
                                zoom_start = 12,
                                fill=True,
                                color='black',
                                popup=ll.property_name).add_to(fg_hotel_area), axis='columns')
        fg_places.add_to(m)
        fg_hotel.add_to(m)
        fg_hotel_area.add_to(m)
        m.add_child(folium.LayerControl())
        st_map = st_folium(m, width=700, height = 400)

    except Exception as e:
        print(e,"\n\nLocation not found: Getting Error !!")

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
    st.subheader(f"Best Hotels and Places to visit when you are in City {city}  ")
    show_map(city)
    show_city_places(ct)