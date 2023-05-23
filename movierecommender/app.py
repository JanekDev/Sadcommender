import json
from recommender import Recommender
import logging

def get_liked_movies(user_data: dict) -> list:
    liked_movies = [liked_movie["title"] for liked_movie in user_data["liked_movies"]]
    return liked_movies

def recommend_movies(user_data: dict) -> dict:
    liked_movies = get_liked_movies(user_data)
    recommender = Recommender(data_path="datasets/")
    recommendations = recommender.get_recommendations(liked_movies)
    logging.info(f"Found {len(recommendations['recommended_movies'])} movies")
    return recommendations
