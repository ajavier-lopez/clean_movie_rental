"""Use cases for movie rental"""
from __future__ import annotations

from . import settings
from .entities import Movie


# As a customer, I want to be able to see the available movies to rent
def list_available_movies():
    movies = settings.movies_repository
    return movies.all(condition=lambda movie: movie.available)


# As an administrator, I want to add a new movie to the catalog
def add_movie(movie: Movie):
    movies = settings.movies_repository
    movies.add(movie)
