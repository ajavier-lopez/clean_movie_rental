import datetime
import unittest

from movies import exceptions
from movies.tests.mocks import (
    _create_customer,
    _create_movie,
    _create_rental,
)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = _create_customer()

    def test_rental_customer(self):
        self.assertIsNone(self.customer.active_rental)

        rental = _create_rental(self.customer)
        self.customer.set_active_rental(rental)
        self.assertEqual(rental, self.customer.active_rental)

        self.customer.finish_active_rental()
        self.assertIsNone(self.customer.active_rental)

    def test_unexepected_rental_finish(self):
        with self.assertRaises(exceptions.OperationError):
            self.customer.finish_active_rental()

    def test_forbidden_rental(self):
        rental = _create_rental(self.customer)
        self.customer.set_active_rental(rental)
        with self.assertRaises(exceptions.ForbiddenOperationError):
            self.customer.set_active_rental(_create_rental(self.customer))


class TestMovie(unittest.TestCase):
    def setUp(self):
        self.movie = _create_movie()

    def test_modify_movie_inventory(self):
        current_stock = self.movie.stock
        self.movie.add_to_inventory(3)
        self.assertEqual(self.movie.stock, current_stock + 3)

        current_stock = self.movie.stock
        self.movie.remove_from_inventory(2)
        self.assertEqual(self.movie.stock, current_stock - 2)

    def test_negative_inventory(self):
        current_stock = self.movie.stock
        self.movie.remove_from_inventory(current_stock + 5)
        self.assertEqual(self.movie.stock, 0)

    def test_movie_rental(self):
        rented = self.movie.rented
        self.assertEqual(rented, 0)
        self.movie.rent_movie()
        self.assertEqual(self.movie.rented, rented + 1)
        self.movie.return_movie()
        self.assertEqual(self.movie.rented, rented)

    def test_rent_out_of_stock(self):
        self.assertEqual(self.movie.available, self.movie.stock)
        for _ in range(self.movie.stock):
            self.movie.rent_movie()
        self.assertEqual(self.movie.available, 0)
        with self.assertRaises(exceptions.OutOfStockError):
            self.movie.rent_movie()

    def test_impossible_return(self):
        self.assertEqual(self.movie.rented, 0)
        with self.assertRaises(exceptions.OperationError):
            self.movie.return_movie()

    def test_renting_price(self):
        days = 5
        renting_price = self.movie.get_rent_price(days=days)
        self.assertEqual(self.movie.price_per_day * days, renting_price)

        with self.assertRaises(exceptions.ForbiddenOperationError):
            self.movie.get_rent_price(days=0)

        with self.assertRaises(exceptions.ForbiddenOperationError):
            self.movie.get_rent_price(days=-1)


class TestRental(unittest.TestCase):
    def test_price_amount(self):
        movies = [_create_movie(i) for i in range(5)]
        rent_days = 3
        rental = _create_rental(movies=movies, days=rent_days)

        total_per_day = sum([movie.price_per_day for movie in movies])
        rent_amount = rent_days * total_per_day

        self.assertEqual(rent_amount, rental.amount)

    def test_returning_process(self):
        rental = _create_rental()
        self.assertFalse(rental.returned)
        return_date = datetime.datetime.now() + datetime.timedelta(days=1)
        rental.return_movies(return_date)
        self.assertTrue(rental.returned)
        self.assertEqual(rental.return_date, return_date)

    def test_wrong_return_date(self):
        rental = _create_rental()
        self.assertFalse(rental.returned)
        return_date = datetime.datetime.now() + datetime.timedelta(days=1)
        rental.return_movies(return_date)
        self.assertTrue(rental.returned)
        self.assertEqual(rental.return_date, return_date)

    def test_duplicated_return(self):
        rental = _create_rental()
        return_date = datetime.datetime.now() + datetime.timedelta(days=-1)
        with self.assertRaises(exceptions.OperationError):
            rental.return_movies(return_date)

    def test_late_return(self):
        rental_date = datetime.datetime.now()
        days = 3
        extra_days = 2
        return_date = rental_date + datetime.timedelta(days=days + extra_days)
        movies = [_create_movie(i) for i in range(5)]
        rental = _create_rental(movies=movies, days=days, date=rental_date)
        rental.return_movies(return_date)
        late_fee = sum([
            movie.get_rent_price(days=extra_days)
            for movie in movies
        ])
        self.assertEqual(rental.late_fee, late_fee)
        self.assertEqual(rental.total_amount, rental.amount + late_fee)
