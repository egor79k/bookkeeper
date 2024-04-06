""" Expenses' category model """
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Expenses' category

    Attributes:
        name   - name of category
        parent - link to a parent category (foreign key). For top level categories parent=None
        pk     - primary key in repository
    """

    name: str = ''
    parent: int | None = None
    pk: int = 0

    def get_parent(self, repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Get parent category as an Category object.
        If called for top level category, returns None.

        Parameters:
            repo - repository to get objects from

        Returns:
            Object of Category class or None
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> Iterator['Category']:
        """
        Get all categories of top level in the hierarchy.

        Parameters:
            repo - repository to get objects from

        Yields:
            Category objects from parent to the top level category
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self,
                          repo: AbstractRepository['Category']
                          ) -> Iterator['Category']:
        """
        Get all subcategories from the hierarchy.
        That is subcategories of this category, subcategories of them and etc.

        Parameters:
            repo - repository to get objects from

        Yields
            Category objects which are subcategories of different levels lower than this.
        """

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for node in graph[root]:
                yield node
                yield from get_children(graph, node.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
            cls,
            tree: list[tuple[str, str | None]],
            repo: AbstractRepository['Category']) -> list['Category']:
        """
        Create a category tree from the list of child-parent pairs.
        The list should be topologically sorted, i.e. descendants should not meet
        before their parent. The correctness of the source data is not checked.
        When using a DBMS with foreign key verification, an error will be received
        (for sqlite3 - IntegrityError). In the absence of verification by the DBMS,
        the result may be correct if the source data is correct except for sorting.
        If not, then no. "Garbage in, garbage out."

        Parameters:
            tree - list of child-parent pairs
            repo - repository for storing objects

        Returns:
            List of created Category objects
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = cls(child, created[parent].pk if parent is not None else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())
