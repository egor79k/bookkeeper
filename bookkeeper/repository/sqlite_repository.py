""" This module contains repository working with sqlite3 database """

import sqlite3
from typing import Any
from datetime import datetime

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """ Repository working with sqlite3 database """

    def __init__(self, cls_type: type[T], db_file: str) -> None:
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()

        if not hasattr(cls_type, 'pk'):
            raise ValueError(
                "Trying to create SQLiteRepository over class without 'pk' field")

        self._cls_type = cls_type
        self._table_name = cls_type.__name__.lower()
        self._attributes = list(cls_type.__annotations__.keys())
        self._attributes.remove('pk')

        if len(self._attributes) < 1:
            raise ValueError(
                "Trying to create SQLiteRepository over class with only 'pk' field")

        annot_type_to_sql = {
            int: 'INTEGER',
            int | None: 'INTEGER',
            str: 'TEXT',
            str | None: 'TEXT',
            datetime: 'DATETIME',
            datetime | None: 'DATETIME'
        }
        fields = ', '.join([
            '"' + name + '"' + ' ' + annot_type_to_sql[tp]
            for name, tp in cls_type.__annotations__.items()
            if name != 'pk'])

        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' +
            f'{self._table_name} (pk INTEGER PRIMARY KEY, {fields})')
        self._connection.commit()

    def __del__(self) -> None:
        self._connection.commit()
        self._connection.close()

    def tuple_to_object(self, values: list[Any]) -> T:
        """
        Create object from list of attributes.

        Parameters:
            values - list of object's attributes

        Returns:
            Created object
        """
        if values is None:
            return None

        obj = self._cls_type()
        obj.pk = values[0]
        for attr, val in zip(self._attributes, values[1:]):
            attr_type = self._cls_type.__annotations__[attr]
            if attr_type in (datetime, datetime | None) and val is not None:
                val = datetime.fromisoformat(val)
            setattr(obj, attr, val)
        return obj

    def add(self, obj: T) -> Any:
        """
        Add object to repository, return object id
        and store id into pk attribute.

        Parameters:
            obj - Object to be added

        Returns:
            Added object id in repository
        """
        if not isinstance(obj, self._cls_type):
            raise ValueError('Trying to add object of wrong type')
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'Trying to add object {obj} with filled `pk` attribute')

        fields = '"' + '", "'.join(self._attributes) + '"'
        values = [getattr(obj, attr) for attr in self._attributes]
        val_flags = '?, ' * (len(values) - 1) + '?'
        self._cursor.execute(
            f'INSERT INTO {self._table_name} ({fields}) VALUES ({val_flags})', values)
        self._cursor.execute('SELECT last_insert_rowid()')
        self._connection.commit()
        pk = self._cursor.fetchone()[0]
        obj.pk = pk

        return pk

    def get(self, pk: int) -> T | None:
        """
        Get object by id.

        Parameters:
            pk - id of the object in repository

        Returns:
            Object or None
        """
        self._cursor.execute(f'SELECT * FROM {self._table_name} WHERE pk == ?', (pk,))
        return self.tuple_to_object(self._cursor.fetchone())

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Get all records by some conditions.

        Parameters:
            where - conditions dictionary {'field_name': value}
                If condition is None returns all records.

        Returns:
            List of objects meeting conditions
        """
        if where is None:
            self._cursor.execute(f'SELECT * FROM {self._table_name}')
        else:
            conditions = ', '.join(['"' + field + '"' + ' == ?' for field in where])
            values = list(where.values())
            self._cursor.execute(
                f'SELECT * FROM {self._table_name} WHERE {conditions}', values)

        return [self.tuple_to_object(t) for t in self._cursor.fetchall()]

    def update(self, obj: T) -> None:
        """
        Update object's data. Object must have pk attribute filled.

        Parameters:
            obj - Object to update
        """
        if obj.pk == 0:
            raise ValueError('Attempt to update object with unknown primary key')

        fields = ', '.join(['"' + attr + '"' + ' = ?' for attr in self._attributes])
        values = [getattr(obj, attr) for attr in self._attributes]
        values.append(obj.pk)
        self._cursor.execute(
            f'UPDATE {self._table_name} SET {fields} WHERE pk = ?', values)
        self._connection.commit()

    def delete(self, pk: int) -> None:
        """
        Delete record by pk.

        Parameters:
            pk - Object id in repository
        """
        self._cursor.execute(f'DELETE FROM {self._table_name} WHERE pk = ?', [pk])
        if self._cursor.rowcount == 0:
            raise KeyError('Trying to delete unexisting object')
        self._connection.commit()
