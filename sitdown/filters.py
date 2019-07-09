import abc
from abc import abstractmethod
from typing import List

from sitdown.core import MutationSet


class Filter(metaclass=abc.ABCMeta):
    """Can filter a set of mutations

    """

    def __init__(self, parent=None, description="filter"):
        """

        Parameters
        ----------
        parent: Filter, optional
            Filter before this one in the filter chain
        description: description, optional
            human readable description of this filter. Defaults to "filter"

        """
        self.parent = parent
        self.description = description

    def apply(self, mutations):
        """Apply this filter to these mutations. If the filter has parents, apply container filter first

        Returns
        -------
        Set[Mutations]:
            result of applying this filter and its parents to the given mutations

        """
        if self.parent:
            mutations = self.parent.apply(mutations)
        return self._filter(mutations)

    def get_filtered_data(self, mutations_in):
        """Apply this filter to these mutations and return as MutationSet.

        Same as Filter.apply() but returns result in a more informative format

        Returns
        -------
        MutationSet:
            result of applying this filter and its parents to the given mutations

        """
        return MutationSet(mutations=self.apply(mutations_in), description=self.description)

    @abstractmethod
    def _filter(self, data):
        """Actual filtering for this filter. To be overwritten in child classes

        Parameters
        ----------
        data: Set[Mutations]
            set of mutations to filter

        Returns
        -------
        Set[Mutations]:
            The mutations filtered by this filter and any of its parents
        """
        pass


class StringFilter(Filter):
    """A filter that matches a string in the mutation description. Not case-sensitive

    """

    def __init__(self, string_to_match, description=None, **kwargs):
        """

        Parameters
        ----------
        string_to_match: str
            Pass mutations for which description contains this
        description: str, optional
            description for this filter. Defaults to string_to_match
        """
        super().__init__(**kwargs)
        if not description:
            description = string_to_match
        self.description = description
        self.string_to_match = string_to_match

    def __str__(self):
        return f"StringFilter '{self.string_to_match}'"

    def _filter(self, mutations):
        filtered = {x for x in mutations if self.string_to_match.lower() in x.description.lower()}
        return filtered


class CatchAllFilter(Filter):
    """A filter that matches everything. Useful at the end of a FilterSet to model the 'rest' category

    """

    def __init__(self, description, **kwargs):
        """

        Parameters
        ----------
        description: str, optional
            inherited from superclass Filter
        """
        super().__init__(**kwargs)
        if not description:
            description = 'Rest'
        self.description = description

    def __str__(self):
        return f"CatchAllFilter '{self.description}'"

    def _filter(self, mutations):
        return mutations


class AccountFilter(Filter):
    """A filter that matches only the given account to and from

    """

    def __init__(self, from_account=None, to_account=None, description=None, **kwargs):
        """

        Parameters
        ----------
        from_account: BankAccount, optional
            Pass mutations that are coming from the given account, defaults to any (pass all)
        to_account: BankAccount, optional
            Pass mutations that are going to the given account, defaults to any (pass all)
        description: str, optional
            description for this filter.
        """
        super().__init__(**kwargs)
        self.from_account = from_account
        self.to_account = to_account
        if not description:
            description = self.from_to_string()
        self.description = description

    def from_to_string(self):
        if self.from_account:
            frm = str(self.from_account)
        else:
            frm = "*"

        if self.to_account:
            to = str(self.to_account)
        else:
            to = "*"
        return f"From {frm} to {to}"

    def __str__(self):
        return f"AccountFilter '{self.from_to_string()}'"

    def _filter(self, mutations):
        filtered = mutations
        if self.from_account:
            filtered = {x for x in mutations if x.account == self.from_account}
        if self.to_account:
            filtered = {x for x in filtered if x.opposite_account == self.to_account}
        return filtered


class AmountFilter(Filter):
    """A filter that matches a range of amounts

    """

    def __init__(
        self,
        from_amount=None,
        to_amount=None,
        description=None,
        **kwargs,
    ):
        """

        Parameters
        ----------
        from_amount: int, optional
            pass all mutations for which amount is greater than or equal to this, Defaults to having no lower bound
        to_amount: int, optional
            pass all mutations for which amount is lower than this this, Defaults to having no upper bound
        description: str, optional
            description for this filter.
        """
        super().__init__(**kwargs)
        self.from_amount = from_amount
        self.to_amount = to_amount
        if not description:
            description = self.from_to_string()
        self.description = description

    def from_to_string(self):
        if self.from_amount is not None:
            frm = str(self.from_amount)
        else:
            frm = "*"

        if self.to_amount is not None:
            to = str(self.to_amount)
        else:
            to = "*"
        return f"From {frm} to {to}"

    def __str__(self):
        return f"AmountFilter '{self.from_to_string()}'"

    def _filter(self, mutations):
        filtered = mutations
        if self.from_amount is not None:
            filtered = {x for x in mutations if x.amount >= self.from_amount}
        if self.to_amount is not None:
            filtered = {x for x in filtered if x.amount < self.to_amount}
        return filtered


class FilterSet(Filter):
    """A collection of several Filters. Can be used as a regular filter but has extra
    methods for splitting out results for each element in the set"""

    def __init__(self, filters: List[Filter], **kwargs):
        """

        Parameters
        ----------
        filters: List[Filter]
            Tbe filters that make up this filter set.

        Notes
        -----
        The ordering of the list of filters matters. When filtering with a FilterSet, input mutations is fed
        through the first filter first. The remaining mutations is fed through the second filter, and so on.

        """
        super().__init__(**kwargs)
        self.filters = filters

    def _filter(self, mutations):
        """Apply each filter in this set

        Parameters
        ----------
        mutations: Set[Mutation]
            set of mutations to filter

        Returns
        -------
        Set[Mutations]:
            The mutations filtered by this filter and any of its parents
        """
        data_list = self.get_filtered_data_set(mutations)
        mutations_list = [x.mutations for x in data_list]
        return set.union(*mutations_list)

    def get_filtered_data_set(self, mutations):
        """Apply each filter in this set to the mutations consecutively, return result for all filters.

        Parameters
        ----------
        mutations: Set[Mutation]
            input mutations

        Returns
        -------
        List[MutationSet]:
            Filtered mutations for each filter
        """
        dfs = []
        data = mutations
        for fltr in self.filters:
            filtered = fltr.apply(data)
            dfs.append(MutationSet(mutations=filtered, description=fltr.description))
            data = data - filtered
        return dfs
