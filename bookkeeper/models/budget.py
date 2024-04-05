"""
Описан класс, представляющий бюджет на определенный срок
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    amount - сумма
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int = 0
    limit: int = 0
    period: str = 'month' # Allowed values: 'day', 'week', 'month'
    pk: int = 0
