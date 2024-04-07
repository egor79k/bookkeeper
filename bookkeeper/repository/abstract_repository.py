"""
This module contains definition of the abstract repository

The repository implements object storage by assigning each object a unique identifier
in the pk (primary key) attribute. Objects that can be saved in the repository must
support adding the pk attribute and must not use it for other purposes.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """ Model must contain pk attribute """
    pk: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Abstract repository.

    Abstract methods:
        add
        get
        get_all
        update
        delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Add object to repository, return object id
        and store id into pk attribute.

        Parameters:
            obj - Object to be added

        Returns:
            Added object id in repository
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:
        """
        Get object by id.

        Parameters:
            pk - id of the object in repository

        Returns:
            Object or None
        """

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Get all records by some conditions.

        Parameters:
            where - conditions dictionary {'field_name': value}
                If condition is None returns all records.

        Returns:
            List of objects meeting conditions
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """
        Update object's data. Object must have pk attribute filled.

        Parameters:
            obj - Object to update
        """

    @abstractmethod
    def delete(self, pk: int) -> None:
        """
        Delete record by pk.

        Parameters:
            pk - Object id in repository
        """
