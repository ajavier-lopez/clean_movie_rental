import unittest

from movies import actions, settings
from movies.adapters.repository import MoviesRepo
from movies.tests.mocks import _create_movie, _get_mock_movies


class TestCRUDMovies(unittest.TestCase):
    def setUp(self):
        self.movies = _get_mock_movies(number=5)
        settings.movies_repository = MoviesRepo(self.movies)

    def test_list_available_movies(self):
        movies = actions.list_available_movies()
        self.assertEqual(self.movies, movies)

        for movie in self.movies.values():
            movie.rented = movie.stock
        movies = actions.list_available_movies()
        self.assertEqual({}, movies)

    def test_add_movie(self):
        id_ = len(self.movies) + 1
        self.assertNotIn(id_, settings.movies_repository.all())

        movie = _create_movie(i=id_)
        actions.add_movie(movie)
        self.assertIn(id_, settings.movies_repository.all())
