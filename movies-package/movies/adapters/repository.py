from __future__ import annotations
from typing import Callable

from ..entities import Movie


class MoviesRepo:
    def __init__(self, movies: dict[Movie] = None):
        self.movies = movies or {}

    def _generate_id(self):
        id_ = len(self.movies) + 1
        while id_ in self.movies:
            id_ = id_ + 1
        return id_

    def all(self, condition: Callable = None) -> dict[Movie]:
        if condition:
            return {
                id_: movie
                for id_, movie in self.movies.items()
                if condition(movie)
            }

        return self.movies

    def get(self, id_: int) -> Movie:
        return self.movies.get(id_)

    def add(self, movie: Movie):
        if movie.id is None:
            movie.id = self._generate_id()
        self.movies[movie.id] = movie

    def delete(self, movie: Movie):
        del self.movies[movie.id]
