"""Entities for Movie Rental"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field

from .exceptions import (
    ForbiddenOperationError,
    OperationError,
    OutOfStockError,
)


@dataclass
class Customer:
    id: int
    name: str
    lastname: str
    rental_history: list = field(default_factory=lambda: [])
    active_rental: Rental = None

    def set_active_rental(self, rental: Rental):
        if self.active_rental:
            raise ForbiddenOperationError(
                "Customer can't have a second active rental"
            )
        self.active_rental = rental

    def finish_active_rental(self):
        if self.active_rental is None:
            raise OperationError('Customer has no active rental')
        self.active_rental = None


@dataclass
class Movie:
    id: int
    name: str
    stock: int
    rented: int
    price_per_day: float

    @property
    def available(self):
        return self.stock - self.rented

    def add_to_inventory(self, number: int):
        self.stock = self.stock + number

    def remove_from_inventory(self, number: int):
        if number > self.stock:
            self.stock = 0
        else:
            self.stock = self.stock - number

    def rent_movie(self):
        if self.rented >= self.stock:
            raise OutOfStockError(f'{self.name} is out of stock')

        self.rented = self.rented + 1

    def return_movie(self):
        if self.rented <= 0:
            raise OperationError(f'all copies of {self.name} already returned')

        self.rented = self.rented - 1

    def get_rent_price(self, *, days: int):
        if days <= 0:
            raise ForbiddenOperationError('days must be greater than zero')
        return self.price_per_day * days


@dataclass
class Rental:
    movies: list[Movie]
    customer: Customer
    rent_date: datetime.datetime
    days: int
    return_date: datetime.datetime = None
    late_fee: float = 0.00

    @property
    def returned(self):
        return self.return_date is not None

    @property
    def amount(self):
        return sum([
            movie.get_rent_price(days=self.days)
            for movie in self.movies
        ])

    @property
    def total_amount(self):
        return self.amount + self.late_fee

    def return_movies(self, return_date: datetime.datetime):
        if return_date < self.rent_date:
            raise OperationError('Return date is eariler than rent date')

        self.return_date = return_date

        rented_time = return_date - self.rent_date
        expected_time = datetime.timedelta(days=self.days)
        if rented_time > expected_time:
            extra_time = rented_time - expected_time
            self.late_fee = sum([
                movie.get_rent_price(days=extra_time.days)
                for movie in self.movies
            ])
