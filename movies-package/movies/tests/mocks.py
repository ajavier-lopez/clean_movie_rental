import datetime

from movies.entities import (
    Customer,
    Movie,
    Rental,
)


def _create_customer(i=1):
    return Customer(id=i, name=f'test{i}', lastname=f'customer{i}')


def _create_movie(i=1, stock=5, price=2.99):
    return Movie(
        id=i,
        name=f'test movie {i}',
        stock=stock,
        price_per_day=price,
    )


def _create_rental(movies=None, customer=None, days=3, date=None):
    customer = customer or _create_customer()
    movies = movies or [_create_movie()]
    date = date or datetime.datetime.now()
    return Rental(movies=movies, customer=customer, rent_date=date, days=days)


def _get_mock_movies(number=5):
    return {
        i: _create_movie(i) for i in range(number)
    }
