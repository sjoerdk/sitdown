import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from collections import defaultdict, OrderedDict
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

    @property
    def bins(self):
        """ Mutations binned per month

        Returns
        -------
        List[MonthBin]

        """
        bins = defaultdict(list)
        for mutation in self.filtered_data.data:
            bins[Month(mutation.date)].append(mutation)

        return [MonthBin(mutations=y, month=x) for x, y in bins.items()]

    @property
    def min_month(self):
        return min(self.bins).month

    @property
    def max_month(self):
        return max(self.bins).month

    def sums(self):
        """Sum of mutations per month

        Returns
        -------
        OrderedDict[Month, int]
            total for each month, ordered by month
        """
        bins = list(self.bins)
        bins.sort()
        return OrderedDict([(mbin.month, mbin.sum()) for mbin in bins])

    def plot(self, ax=None):
        """Plot this data per month as a bar graph

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
        if not ax:
            _, ax = plt.subplots()

        sums = self.sums()
        months = list(sums.keys())
        sum_values = list(sums.values())

        ind = np.arange(len(months))
        ax.bar(x=ind, height=sum_values)

        ax.set_ylabel(f"{self.filtered_data.description} (Euro)")
        ax.set_xlabel("Month")
        ax.grid(which="both", axis="y")
        ax.set_xticks(ind)
        ax.set_xticklabels([str(x) for x in months])

        return ax


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

    @property
    def date(self):
        """

        Returns
        -------
        datetime.date
            This month as a date, set on the 1st of that month

        """
        return self.month.date

    def __str__(self):
        return f"Bin {self.month}"

    def __lt__(self, other):
        return self.month < other.month

    def sum(self):
        return sum([x.amount for x in self.mutations])


def month_iterator(start_month, end_month):
    """Generate all months between start and end, inclusive"""
    current = start_month
    while current <= end_month:
        year = current.date.year
        month = current.date.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        new = Month(datetime.date(year=year, month=month, day=1))
        yield current
        current = new


class MonthMatrix(Plottable):
    """Per month data for a set of Filtered Datas

    """

    def __init__(self, filtered_data_list):
        """
        Parameters
        ----------
        filtered_data_list: List[FilteredData]

        """
        self.filtered_data_list = filtered_data_list
        self.per_month_list = [
            DataPerMonth(filtered_data=x) for x in self.filtered_data_list
        ]

    @property
    def min_month(self):
        return min([x.min_month for x in self.per_month_list])

    @property
    def max_month(self):
        return max([x.max_month for x in self.per_month_list])

    def get_month_range(self):
        """Get all months in between min and max months. For consistent plotting

        """
        return [x for x in month_iterator(self.min_month, self.max_month)]

    def matrix(self):
        """Return """

        return [DataPerMonth(filtered_data=x) for x in self.filtered_data_list]

    def plot(self, ax):
        """Plot this data into the given axis"""
        pass
