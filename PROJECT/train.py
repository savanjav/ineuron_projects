import pandas as pd
from db import database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

class Train:

        @staticmethod
        def stem(text):
            ps = PorterStemmer()
            y = []
            for i in text.split():
                y.append(ps.stem(i))
            return " ".join(y)

        def train(self):
            db_session = database.CassandraConnect.conn()
            select = "select * from books.books_details"
            df = pd.DataFrame(list(db_session.execute(select)))
            df['tags'] = df['genre'] + ' ' + df['subgenre'] + ' ' + df['publisher'] + ' ' + df['author'] + ' ' + df['title']
            df['tags'] = df['tags'].str.replace(',', '')
            df['tags'] = df['tags'].apply(self.stem)
            cv = CountVectorizer(max_features=622, stop_words='english')
            vector = cv.fit_transform(df['tags']).toarray()
            similarity = cosine_similarity(vector)
            pickle.dump(similarity, open('similarity.pkl', 'wb'))
            pickle.dump(df, open('tag.pkl', 'wb'))
            return "true"

