# -*- coding: utf-8 -*-

"""Main module."""
import pickle
from abc import ABCMeta, abstractmethod
from typing import Set

from sitdown.classifiers import Category


class Mutation:
    """An increase or decrease of money on an account. Basic object for most things
    in sitdown.

    Is sortable by date by default
    """

    def __init__(
        self,
        amount,
        date,
        account,
        currency="EURO",
        opposite_account=None,
        description="",
        balance_before=None,
        balance_after=None,
        categories: Set[Category] = None,
    ):
        """Create a transaction

        Parameters
        ----------
        amount: Decimal
            amount of money transferred. Negative amount means money is spent
        date: datetime.date
            date of transfer
        account: BankAccount
            Account on which this mutation takes place
        opposite_account: BankAccount, optional
            Account on the other side of the transaction. Might not always be known. Defaults to None
        description: str, optional
            description of this mutation. Defaults to empty string
        currency: str, optional
            currency in which this mutation is done, Defaults to 'EURO'
        balance_before: Decimal, optional
            account balance before mutation. Defaults to None
        balance_after: Decimal, optional
            account balance after mutation. Defaults to None
        categories: Set[Category], optional
            categories to which this mutation belongs. Defaults to empty set
        """

        self.amount = amount
        self.date = date
        self.account = account
        self.currency = currency
        self.opposite_account = opposite_account
        self.description = description
        self.balance_before = balance_before
        self.balance_after = balance_after
        if categories is None:
            categories = set()
        self.categories = categories

    def __str__(self):
        return f"Mutation of {self.amount} on {self.date}"

    def __lt__(self, other):
        return self.date < other.date

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.amount, self.date, str(self.account), self.currency,
                     self.opposite_account, self.description, self.balance_before,
                     self.balance_after))


class BankAccount:
    def __init__(self, number, description=None):
        """A bank account.

        Parameters
        ----------
        number: str
            the account number
        description: str, optional
            short description of the account. For use in graphs etc. Defaults to
            account number

        """
        self.number = number
        if description is None:
            description = str(number)
        self.description = description

    def __eq__(self, other):
        if not other:  # handle comparing to None or other falsy value
            return False
        return self.description == other.description and self.number == other.number

    def __hash__(self):
        return hash((self.description, self.number))

    def __str__(self):
        return self.description


class Plottable(metaclass=ABCMeta):
    """Can be plotted in a matplotlib figure"""

    @abstractmethod
    def plot(self, ax=None):
        """Plot this object in to matplotlib axes ax, or create new ax if none given

        Parameters
        ----------
        ax: matplotlib.Axes, optional
            plot into this axes. Defaults to None, in which case a new axes will be created
            for this plot

        Returns
        -------
        matplotlib.Axes
            The axes into which this plot has been made

        """
        pass


class Persistable(metaclass=ABCMeta):
    """Can be saved to and loaded from disk"""

    @staticmethod
    @abstractmethod
    def load(file):
        """Load this object from the opened file

        Parameters
        ----------
        file: File object
            Read data from this file object

        Returns
        -------
        Object
        """
        pass

    @abstractmethod
    def save(self, file):
        """Save this object to the given file object

        Parameters
        ----------
        file: File object
            write to this file object

        """
        pass


class MutationSet(Plottable, Persistable):
    """Set of mutations with a description

    """

    def __init__(self, mutations, description="Unlabeled"):
        """

        Parameters
        ----------
        mutations: Set[Mutation]
            set of mutations
        description: str, optional.
            name for these mutations
        """

        self.mutations = mutations
        self.description = description

    def __str__(self):
        return f"MutationSet '{self.description}'"

    def save(self, file):
        """Save this mutation set to file

        Parameters
        ----------
        file: open file handle

        """
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        """Load mutation set from open file

        Parameters
        ----------
        file: open file handle

        Returns
        -------
        MutationSet

        Raises
        ------
        TypeError
            When object loaded is not a MutationSet

        PickleError
            When loading fails for some other reason

        """

        obj = pickle.load(file)
        if type(obj) is not MutationSet:
            msg = f"Trying to load a MutationSet, but this file seems to contain a {type(obj)}"
            raise TypeError(msg)
        return obj

    def plot(self, ax):
        pass
