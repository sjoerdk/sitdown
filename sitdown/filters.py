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
        return MutationSet(mutations=self.apply(mutations_in), filter_used=self)

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
    """A filter that matches a string in the mutation description

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
        filtered = {x for x in mutations if self.string_to_match in x.description}
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
        """Apply each filter in this set to the mutations consecutively, return result for all filters

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


