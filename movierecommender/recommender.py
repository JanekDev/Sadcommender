from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
import os
import logging

class Recommender:
    def __init__(self, ar_path: str = None, data_path: str = None) -> None:
        if ar_path:
            self.ar = pd.read_csv(ar_path)
        elif data_path:
            self.data_movies = pd.read_csv(os.path.join(data_path, 'movies.csv'))
            self.data_ratings = pd.read_csv(os.path.join(data_path, 'ratings.csv'))
            self.create_association_rules(self.prepare_data())
        else:
            raise ValueError("You must provide either an association rules file or a data path")
        

    def get_recommendations(self, liked_movies: list) -> dict:
        recommendations = {"recommended_movies": []}

        if self.ar is not None:
            for movie in liked_movies:
                recommendations["recommended_movies"].extend(list(self.ar[self.ar['antecedents'] == frozenset([movie])]['consequents'].tolist()))
            recommendations["recommended_movies"] = list(set(recommendations["recommended_movies"]))
            recommendations["recommended_movies"] = [list(movie)[0] for movie in recommendations["recommended_movies"] if list(movie)[0] not in liked_movies]
        else:
            logging.error("No association rules found")
        recommendations["recommended_movies"] = list(set(recommendations["recommended_movies"]))
        recommendations["recommended_movies"] = recommendations["recommended_movies"][:10]
        return recommendations
    
    
    def prepare_data(self, good_rating_thresh: float = 4.5) -> None:
        df_movies = self.data_movies
        df_ratings = self.data_ratings
        df_ratings = df_ratings[df_ratings['rating'] >= good_rating_thresh]
        df_ratings = df_ratings.drop(columns=['timestamp'])
        df_ratings = df_ratings.merge(df_movies, on='movieId')
        df_ratings = df_ratings.drop(columns=['movieId', 'genres'])
        df_ratings = df_ratings.groupby('userId')['title'].apply(list).reset_index(name='watched_movies')
        df_ratings['watched_movies'] = df_ratings['watched_movies'].apply(lambda x: list(set(x)))
        df_ratings['watched_movies'] = df_ratings['watched_movies'].apply(lambda x: sorted(x))
        return df_ratings



    def create_association_rules(self, df: pd.DataFrame = None) -> pd.DataFrame:
        te = TransactionEncoder()
        te_ary = te.fit_transform(df['watched_movies'].tolist())

        frequent_itemsets = apriori(pd.DataFrame(te_ary, columns=te.columns_), min_support=0.04, use_colnames=True)
        self.ar = association_rules(frequent_itemsets, metric="lift")
        self.ar.to_csv('datasets/association_rules.csv', index=False)
        return self.ar
