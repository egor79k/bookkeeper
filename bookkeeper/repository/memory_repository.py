""" This module implements repository working in RAM """

from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class MemoryRepository(AbstractRepository[T]):
    """ Repository working in RAM. Stores data in dictionary. """

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        """
        Add object to repository, return object id
        and store id into pk attribute.

        Parameters:
            obj - Object to be added

        Returns:
            Added object id in repository
        """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
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
        return self._container.get(pk)

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
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        """
        Update object's data. Object must have pk attribute filled.

        Parameters:
            obj - Object to update
        """
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        """
        Delete record by pk.

        Parameters:
            pk - Object id in repository
        """
        self._container.pop(pk)
