"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
# from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

db_file = 'bookkeeper.db'

cat_repo = SQLiteRepository[Category](Category, db_file)
exp_repo = SQLiteRepository[Expense](Expense, db_file)

# cat_repo = SQLiteRepository[Category]('category',
#     ('name', 'parent'),
#     ('TEXT NOT NULL', 'INTEGER'),
#     ('FOREIGN KEY(parent) REFERENCES category(pk)'))

# exp_repo = SQLiteRepository[Expense]('expense',
#     ('amount', 'category', 'expense_date', 'added_date', 'comment'),
#     ('INTEGER NOT NULL', 'INTEGER', 'DATETIME', 'DATETIME', 'TEXT'),
#     ('FOREIGN KEY(category) REFERENCES category(pk)'))

cats = '''
products
    meat
        raw meat
        meat products
    sweets
books
clothes
'''.splitlines()
# from inspect import get_annotations
# Category.create_from_tree(read_tree(cats), cat_repo)

# print(Category('test', None, 2) == Category('test', None, 2))
# print(Category('test', None, 2) == Category('tes', None, 2))
# exp = Expense(10, 2)
# pk = exp_repo.add(exp)
# exp1 = exp_repo.get(pk)
# print(exp == exp1)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'categories':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'expenses':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f"category '{name}' not found")
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
    else:
        print(f"Unknown command '{cmd}'")
