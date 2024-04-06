""" Contains class representing expense operation """

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Expense operation.

    Attributes:
        amount       - expense cost
        category     - id of expense category (foreign key)
        expense_date - expense date
        added_date   - adding to database date
        comment      - comment
        pk           - id in database (primary key)
    """
    amount: int = 0
    category: int = 0
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0
