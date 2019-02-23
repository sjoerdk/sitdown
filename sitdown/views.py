from typing import List

from sitdown.core import Plotable
from sitdown.filters import FilteredData


class FilteredDataView:
    """Different ways of looking at filtered data"""

    def __init__(self, data: FilteredData):
        self.data = data

    def per_month(self):
        """Aggregate all mutations in this data per month"""
        pass


class FilteredDataCollectionView:
    """Special methods for displaying and plotting a collection of filtered data simultaneously"""

    def __init__(self, filtered_data_list: List[FilteredData]):
        """

        Parameters
        ----------
        filtered_data_list
        """
        self.filtered_data_list = filtered_data_list

    def per_month(self):
        """Aggregate all mutations in this data per month"""
        pass


class DataPerMonth(Plotable):
    def __init__(self, data):
        """
        Parameters
        ----------
        data: DataFrame

        """
        self.data = data

    def plot(self, ax):
        """Plot this data into the given axis"""
        pass
