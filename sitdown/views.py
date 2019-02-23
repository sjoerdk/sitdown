import datetime
from collections import defaultdict
from functools import total_ordering
from typing import List

from sitdown.core import Plottable
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


class DataPerMonth(Plottable):
    """Sorts input data per month. Easy to get sum, mutations for a certain month

    """
    def __init__(self, filtered_data):
        """
        Parameters
        ----------
        filtered_data: FilteredData

        """
        self.filtered_data = filtered_data
        
    def get_bins(self):
        bins = defaultdict(list)
        for mutation in self.filtered_data.data:
            bins[Month(mutation.date)].append(mutation)
        return bins

    def plot(self, ax):
        """Plot this data into the given axis"""
        pass


@total_ordering
class Month:
    """Like date, but day is always 1"""

    def __init__(self, date):
        self.date = datetime.date(year=date.year, month=date.month, day=1)

    def __str__(self):
        return f"{self.date.year}/{self.date.month}"

    def __lt__(self, other):
        return self.date < other.date

    def __eq__(self, other):
        return self.date == other.date

    def __hash__(self):
        return hash(self.date)


class MonthBin:
    """A collection of mutations for a single month"""

    def __init__(self, mutations, month: Month):
        """

        Parameters
        ----------
        mutations: List[mutations]
            all mutations for this month
        month: datetime.date
            Should be the first of the month indicated


        """
        self.mutations = mutations
        self.month = month

    def __str__(self):
        return f"Bin {self.month}"

    def __lt__(self, other):
        return self.month < other.month
    
    def sum(self):
        return sum([x.amount for x in self.mutations])



class DataSetPerMonth(Plottable):
    def __init__(self, data_set):
        """
        Parameters
        ----------
        data_set: FilteredDataSet

        """
        self.data_set = data_set

    def plot(self, ax):
        """Plot this data into the given axis"""
        pass
