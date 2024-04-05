"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


bgt_repo = SQLiteRepository[Budget](Budget)
exp_repo = SQLiteRepository[Expense](Expense)
cat_repo = SQLiteRepository[Category](Category)

# Subcategories are not supported now
cats = '''
products
meat
raw meat
meat products
sweets
books
clothes
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

exp_repo.add(Expense(123, 2))
exp_repo.add(Expense(199, 3, comment='Meatballs for dinner'))
exp_repo.add(Expense(73, 4, comment='Chocolate'))
exp_repo.add(Expense(1380, 5, comment='Russian-Chinese dictionary'))
exp_repo.add(Expense(599, 6, comment='Bought a new shirt'))

bgt_repo.add(Budget(0, 1000, 'day'))
bgt_repo.add(Budget(0, 7000, 'week'))
bgt_repo.add(Budget(0, 30000, 'month'))
