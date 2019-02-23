from typing import List

from sitdown.core import Plotable


class Filter:
    """Can filter a set of mutations

    """

    name = "_filter"

    def __init__(self, parent=None, description=""):
        """

        Parameters
        ----------
        parent: Filter, optional
            Filter before this one in the filter chain
        description: description, optional
            human readable description of this filter. Defaults to empty string

        """
        self.parent = parent

    @property
    def name(self):
        if self.parent:
            return self.parent.name + "_" + self._name
        else:
            return self._name

    def apply(self, mutations):
        """Apply this filter to these mutations. If the filter has parents, apply parent filter first

        Returns
        -------
        List[Mutations]:
            result of applying this filter and its parents to the given mutations

        """
        if self.parent:
            mutations = self.parent.apply(mutations)
        return self._filter(mutations)

    def get_filtered_data(self, mutations_in):
        """Apply this filter to these mutations and return as FilteredData.

        Same as Filter.apply() but returns result in a more informative format

        Returns
        -------
        FilteredData:
            result of applying this filter and its parents to the given mutations

        """
        return FilteredData(mutations=self.apply(mutations_in), filter_used=self)

    def _filter(self, data):
        """Actual filtering for this filter. To be overwritten in child classes

        Parameters
        ----------
        data: List[Mutations]
            list of mutations to filter

        Returns
        -------
        List[Mutations]:
            The data filtered by this filter and any of its parents
        """
        raise NotImplementedError(
            "This method should be overwritten in implementing classes"
        )


class StringFilter(Filter):
    """A filter that matches a string in the mutation description

    """

    def __init__(self, string_to_match, **kwargs):
        super().__init__(**kwargs)
        self.string_to_match = string_to_match

    def __str__(self):
        return f"StringFilter '{self.string_to_match}'"

    def _filter(self, mutations):
        filtered = [x for x in mutations if self.string_to_match in x.description]
        return filtered


class FilteredData(Plotable):
    """Result of applying a filter to some data

    """

    def __init__(self, mutations, filter_used):
        """

        Parameters
        ----------
        mutations: List[Mutation]
            list of mutations that came out of the filter
        filter_used: Filter
            The filter instance that produced the data
        """

        self.data = mutations
        self.filter_used = filter_used

    def plot(self, ax):
        pass


class FilteredDataCollection:
    """A collection of filtered data"""

    pass
