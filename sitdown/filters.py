from typing import List

from sitdown.core import Mutation
from sitdown.views import Plotable


class Filter:
    """Can filter a set of mutations

    """
    name = "_filter"

    def __init__(self, parent=None):
        """

        Parameters
        ----------
        parent: Filter, optional
            Filter before this one in the filter chain
        """
        self.parent = parent
        pass

    @property
    def name(self):
        if self.parent:
            return self.parent.name + "_" + self._name
        else:
            return self._name

    def apply(self, data: List[Mutation]):
        """Apply this filter to this data. If the filter has parents, apply parent filter first

        Returns
        -------
        List[Mutation]

        """
        if self.parent:
            data = self.parent.apply(data)
        return self._filter(data)

    def _filter(self, data):
        """Actual filtering for this filter. To be overwritten in child classes"""
        return data



class FilteredData(Plotable):
    """Result of applying a filter to some data"""

    def plot(self, ax):
        pass


class FilteredDataCollection:
    """A collection of filtered data"""
    pass
