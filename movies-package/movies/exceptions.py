"""Error definitions"""


class ForbiddenOperationError(Exception):
    """Error triggered when a operation is not allowed"""


class OperationError(Exception):
    """Error triggered when something shouldn't be possible"""


class OutOfStockError(Exception):
    """Error when a movie is out of stock"""
