""" Contains class representing budget for a specific period """

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Budget for a specific period.

    Attributes:
        amount - sum of all expenses in chosen period
        limit  - max allowed sum of expenses for chosen period
        period - name of time period
        pk     - id in database (primary key)
    """
    amount: int = 0
    limit: int = 0
    period: str = 'month' # Allowed values: 'day', 'week', 'month'
    pk: int = 0
