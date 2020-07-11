"""Use cases for movie rental"""
from __future__ import annotations

from movies.adapters import repos
from movies.entities import Movie


# As a customer, I want to be able to see the available movies to rent
def list_available_movies():
    movies = repos.movies
    return movies.all(condition=lambda movie: movie.available)


# As an administrator, I want to add a new movie to the catalog
def add_movie(movie: Movie):
    movies = repos.movies
    movies.add(movie)
