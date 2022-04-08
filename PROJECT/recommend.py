import pandas as pd
from db import database
import pickle

class Recommend:


    @staticmethod
    def recommend(movie):
        rec_movies = []
        tag_file = open('tag.pkl', 'rb')
        similarity_file = open('similarity.pkl', 'rb')
        new = pickle.load(tag_file)
        similarity = pickle.load(similarity_file)
        index = new[new['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            rec_movies.append(int(new.iloc[i[0]].id))
        return rec_movies