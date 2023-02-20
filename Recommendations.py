import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


places_dict = pickle.load(open('./pickle_files/places_dict.pkl','rb'))
place_similarity = pickle.load(open('./pickle_files/place_similarity.pkl','rb'))
popular_city_similarity = pickle.load(open('./pickle_files/pop_city_similarity.pkl','rb'))
p_ct = pd.DataFrame(pickle.load(open('./pickle_files/similar_city_dict.pkl','rb')))

locs = pd.DataFrame(places_dict)

def pop_similar_cities(city):

    # find the index of the city then find the other cities which are closely similar to that city 
    city_index = p_ct[p_ct['City']==city].index[0]
    distances = popular_city_similarity[city_index]
    similar_cities = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])
    sim_city=[]
    for i in similar_cities:
      if p_ct.iloc[i[0]].City not in sim_city:
        sim_city.append(p_ct.iloc[i[0]].City)
    return sim_city[:30]

def recommend_cities(city):
    pt1 = pd.DataFrame()
    #First find the similar cities of the given city then select the all places of the top 30 city
    for i in pop_similar_cities(city):
        p2 = p_ct[p_ct['City']==i]
        pt1=pd.concat([pt1,p2])

    #pivot table is used to the ratings and then send this table for the similarity betwwen data
    pt = pt1.pivot_table(index ='City',columns='Place',values='Rating')
    pt.fillna(0,inplace=True)
    similarity_score = cosine_similarity(pt)

    # find the index of the city then find the other cities which are closely similar to that city 
    ind = np.where(pt.index==city)[0][0]
    popular_cities = sorted(list(enumerate(similarity_score[ind])),key=lambda x:x[1],reverse=True)[1:13]
    
    recommend_cities=[]
    for i in popular_cities:
        recommend_cities.append(pt.index[i[0]])
    return recommend_cities

def recommend_place(place):
    
    # find the index of the place then find the other cities which are closely similar to that city 
    place_index = locs[locs['Place']==place].index[0]
    distances = place_similarity[place_index]
    similar_places = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:13]

    recommend_places=[]
    for i in similar_places:
        recommend_places.append(locs.iloc[i[0]].Place + "-" + locs.iloc[i[0]].City)
    return recommend_places