""" Script for example filling of empty database """
from datetime import datetime, timedelta

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


DB_FILE = 'bookkeeper.db'

bgt_repo = SQLiteRepository[Budget](Budget, DB_FILE)
exp_repo = SQLiteRepository[Expense](Expense, DB_FILE)
cat_repo = SQLiteRepository[Category](Category, DB_FILE)

# Subcategories are not supported now
cats = '''
Alcohol
Books
Clothes
Electronics
Medicines
Products
    Bakery
    Dairy products
    Fish
    Fruits
    Meat
    Preserves
    Seafood
    Sweets
    Tea
    Vegetables
Stationery
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)


def get_cat_pk(name: str) -> int:
    ''' Returns category pk by name '''
    return cat_repo.get_all({'name': name})[0].pk


exps_data = (
    (2600, 'Clothes',     timedelta(days=45),  ''),
    (1450, 'Seafood',     timedelta(days=43),  'Sushi'),
    (8999, 'Electronics', timedelta(days=40),  'New wireless headphones'),
    (33,   'Tea',         timedelta(days=8),   ''),
    (2440, 'Stationery',  timedelta(days=7),   ''),
    (239,  'Fruits',      timedelta(days=4),   'Apples'),
    (37,   'Sweets',      timedelta(days=4),   'Chewing gum'),
    (110,  'Bakery',      timedelta(days=4),   'Donuts'),
    (95,   'Preserves',   timedelta(days=4),   'Green pea'),
    (239,  'Fish',        timedelta(days=4),   'Cod fillet'),
    (80,   'Medicines',   timedelta(days=2),   'Ascorbic acid'),
    (350,  'Medicines',   timedelta(days=2),   'Headache pills'),
    (978,  'Alcohol',     timedelta(hours=36), 'Payment at the bar'),
    (199,  'Clothes',     timedelta(days=1),   'Bought a new shirt'),
    (1380, 'Books',       timedelta(days=1),   'Russian-Chinese dictionary'),
    (450,  'Meat',        timedelta(0),        'Beef'),
    (199,  'Meat',        timedelta(0),        'Meatballs for dinner'),
    (73,   'Sweets',      timedelta(0),        'Chocolate'),
)

# Add expenses to database
for exp_data in exps_data:
    exp_repo.add(Expense(
        amount=exp_data[0],
        category=get_cat_pk(exp_data[1]),
        expense_date=datetime.now() - exp_data[2],
        comment=exp_data[3]))
