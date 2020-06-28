"""Modules for classifying mutations into categories

Classifiers and filters serve similar purposes as both can be used to distinguish
between mutations. The difference is that classifying is more complex and ambiguous,
like 'Is this mutation about shopping or about sports?'. While filters should be
more straightforward, like 'All incoming'

In terms of responsibility, classifiers should reduce any ambiguity about mutations
as much as possible, so that filters later on do not have to deal with it.
"""
import abc
from abc import abstractmethod

from sitdown.core import Mutation


class Classifier(metaclass=abc.ABCMeta):
    """Can classify a mutation by adding one or more tags to it"""

    @abstractmethod
    def categories(self):
        """

        Returns
        -------
        List[Category]
            List of all categories that could potentially returned by classify()
        """
        pass

    @abstractmethod
    def classify(self, mutation):
        """Determine the category of the given mutation

        Parameters
        ----------
        mutation: Mutation

        Returns
        -------
        Category

        """
        pass


class Category:
    """Description of a mutation, like 'shopping' or 'study'

    Can be nested. For example 'bars' and 'dinner' can both be part of 'going out' """

    def __init__(self, name, container=None):
        """

        Parameters
        ----------
        name: str
            name and unique description of this category
        container: Category, optional
            Parent category that contains this category, for example a category
            'Gym card' could have a
            container 'Sports'. Defaults to None
        """
        self.name = name
        self.container = container

    def is_in(self, other):
        """Is this category contained by category 'other'?

        Notes
        -----
        Categories contain themselves. So
        >>> sports = Category('sports')
        >>> gym = Category('gym', container=sports)
        >>> gym.is_in(sports)
        >>> True
        >>> gym.is_in(gym)
        >>> True

        Parameters
        ----------
        other: Category
            Category to compare with

        Returns
        -------
        Bool
            True if this category is the same as or is contained by other
        """
        if self.name == other.name:
            return True
        else:
            if self.container:
                return self.container.is_in(other)
            else:
                return False

    def __str__(self):
        return self.name


class StringMatchClassifier(Classifier):
    """classifies by matching strings in the mutation description"""

    def __init__(self, mapping):
        """
        Parameters
        ----------
        mapping: OrderedDict(str, Category)
            For each string in this dict, if the string matches, assign the
            category. Strings are matched in order from left to right. If a
            match is found, matching is halted.
        """
        self.mapping = mapping

    def categories(self):
        return list(self.mapping.values())

    def classify(self, mutation):
        for string_to_match, category in self.mapping.items():
            if string_to_match in mutation.description:
                return category

