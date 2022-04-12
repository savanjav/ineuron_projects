import pickle
from AppLogger import AppLogger

class Recommend:
    @staticmethod
    def recommend(movie):
        logger = AppLogger(__class__.__name__)
        logger.log("recommend start")
        try:
            rec_movies = []
            tag_file = open('tag.pkl', 'rb')
            similarity_file = open('similarity.pkl', 'rb')
            new = pickle.load(tag_file)
            similarity = pickle.load(similarity_file)
            index = new[new['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            for i in distances[1:6]:
                rec_movies.append(int(new.iloc[i[0]].id))
            logger.log("recommend end")
            return rec_movies
        except Exception as e:
            logger.error(e)
