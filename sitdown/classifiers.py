"""Modules for classifying mutations into categories

Classifiers and filters serve similar purposes as both can be used to distinguish
between mutations. The difference is that classifying is more complex and ambiguous,
like 'Is this mutation about shopping or about sports?'. While filters should be
more straightforward, like 'All incoming'

In terms of responsibility, classifiers should reduce any ambiguity about mutations
as much as possible, so that filters later on do not have to deal with it.
"""
import abc
import re
from abc import abstractmethod
from typing import Dict, List, Set, Union
from yaml import load
from yaml.loader import Loader


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
    def classify(self, mutation) -> Set['Category']:
        """Determine the categories of the given mutation

        Parameters
        ----------
        mutation: Mutation

        Returns
        -------
        Set[Category]

        """
        pass


class Category:
    """Description of a mutation, like 'shopping' or 'study'

    Can be nested. For example 'bars' and 'dinner' can both be part of 'going out' """

    def __init__(self, name: str, parent: 'Category' = None):
        """

        Parameters
        ----------
        name: str
            name and unique description of this category
        parent: Category, optional
            Parent category that contains this category, for example a category
            'Gym card' could have a
            container 'Sports'. Defaults to None
        """
        self.name = name
        self.parent = parent

    def is_in(self, other):
        """Is this category contained by category 'other'?

        Notes
        -----
        Categories contain themselves. So
        >>> sports = Category('sports')
        >>> gym = Category('gym', parent=sports)
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
            if self.parent:
                return self.parent.is_in(other)
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
            category.
        """
        self.mapping = mapping

    def categories(self):
        return list(self.mapping.values())

    def classify(self, mutation) -> Set[Category]:
        """Match all strings in mapping to mutation description case (insensitive).
         Removes excess spaces from description"""
        def normalise(string):
            """Remove double spaces, make lower case. Just remove some weirdness"""
            return re.sub(' +', ' ', string).lower()
        return {cat for string, cat in self.mapping.items()
                if normalise(string) in normalise(mutation.description)}


def string_match_classifier_from_yaml(f) -> StringMatchClassifier:
    """Build StringMatchClassifier from a yaml file. Yaml is much easier to edit
    in real-world classifiers that often include 50+ lines

    Example
    -------
    The YAML content
        shopping:
            - albert_heijn:
                - AH betaling
            - bakery:
                - Johns bakery
                - Bakery&Co
        fun:
            - netflix

    Is equivalent to

    """
    content = load(f, Loader=Loader)
    mapping = {}

    def parse_category(name: str, items: List[Union[str, Dict]],
                       parent: Category = None):
        mapping_ = {}
        current_cat = Category(name, parent=parent)
        for item in items:
            if type(item) == str:
                # this a string that if matched, should assign current category
                mapping_[item] = current_cat
            elif type(item) == dict:
                # this is a sub-category. recurse
                for key, value in item.items():
                    mapping_.update(
                        parse_category(name=key, items=value, parent=current_cat))
        return mapping_

    for x, y in content.items():
        mapping.update(parse_category(name=x, items=y))

    return StringMatchClassifier(mapping=mapping)
