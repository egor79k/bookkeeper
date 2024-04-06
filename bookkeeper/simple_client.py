""" Simple test script for terminal """

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

DB_FILE = 'bookkeeper.db'

cat_repo = SQLiteRepository[Category](Category, DB_FILE)
exp_repo = SQLiteRepository[Expense](Expense, DB_FILE)

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
