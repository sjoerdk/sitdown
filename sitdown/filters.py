from sitdown.core import Plottable


class Filter:
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
        """Apply this filter to these mutations. If the filter has parents, apply parent filter first

        Returns
        -------
        Set[Mutations]:
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
        data: Set[Mutations]
            set of mutations to filter

        Returns
        -------
        Set[Mutations]:
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
        filtered = {x for x in mutations if self.string_to_match in x.description}
        return filtered


class FilterSet(Filter):
    """A collection of several Filters. Can be used as a regular filter but has extra
    methods for splitting out results for each element in the set"""

    def __init__(self, filters, **kwargs):
        """

        Parameters
        ----------
        filters: List[Filter]
            Tbe filters that make up this filter set.

        Notes
        -----
        The ordering of the list of filters matters. When filtering with a FilterSet, input data is fed
        through the first filter first. The remaining data is fed through the second filter, and so on.

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
            The data filtered by this filter and any of its parents
        """
        data_list = self.get_filtered_data_set(mutations).filtered_data_list
        mutations_list = [x.data for x in data_list]
        return set.union(*mutations_list)

    def get_filtered_data_set(self, mutations):
        """Apply each filter in this set to the data consecutively, return result for all filters

        Parameters
        ----------
        mutations: Set[Mutation]
            input data

        Returns
        -------
        FilteredDataSet:
            Filtered data for each filter
        """
        dfs = []
        data = mutations
        for fltr in self.filters:
            filtered = fltr.apply(data)
            dfs.append(FilteredData(mutations=filtered, filter_used=fltr))
            data = data - filtered
        return FilteredDataSet(filtered_data_list=dfs)


class FilteredData(Plottable):
    """Result of applying a filter to some data

    """

    def __init__(self, mutations, filter_used):
        """

        Parameters
        ----------
        mutations: Set[Mutation]
            set of mutations that came out of the filter
        filter_used: Filter
            The filter instance that produced the data
        """

        self.data = mutations
        self.filter_used = filter_used

    def plot(self, ax):
        pass


class FilteredDataSet(Plottable):
    """A collection of filtered data"""

    def __init__(self, filtered_data_list):
        """

        Parameters
        ----------
        filtered_data_list: List[FilteredData]
        """
        self.filtered_data_list = filtered_data_list

    def plot(self, ax):
        pass
