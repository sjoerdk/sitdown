import datetime

import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict, OrderedDict, UserDict
from functools import total_ordering
from typing import List

from sitdown.core import Plottable, MutationSet


class MonthSet(UserDict, Plottable):
    """An ordered Dictionary-like object of Month: MonthBin. Ordered by month

    """

    def __init__(self, mutations, description="Unnamed"):
        """
        Parameters
        ----------
        mutations: List[Mutations]
            The mutations in this dataset


        """
        super().__init__(self)

        self.mutations = mutations
        self.description = description

        months = defaultdict(list)
        for mutation in mutations:
            months[Month(mutation.date)].append(mutation)

        self.data = OrderedDict()
        for x in sorted(list(months.keys())):
            self.data[x] = MonthBin(mutations=months[x], month=x)

    def __str__(self):
        return f"Dataset {self.description}"

    def months(self):
        """List of all months in this series, sorted by date

        Returns
        -------
        List[Month]
        """
        return list(self.data.keys())

    def bins(self):
        """List of all MonthBins in this series, sorted by date

         Returns
         -------
         List[MonthBin]
         """
        return list(self.data.values())

    def sums(self):
        """Summed amount of all mutations per month, sorted by date

        Returns
        -------
        List[Decimal]
        """

        return [x.sum() for x in self.bins()]

    @property
    def min_month(self):
        if self.months():
            return self.months()[0]

    @property
    def max_month(self):
        if self.months():
            return self.months()[-1]

    @staticmethod
    def get_month_range(from_month, to_month):
        """Get all months in between min and max months. For consistent plotting

        Parameters
        ----------
        from_month: Month
            Start with this month.
        to_month: Month
            End with this month

        """
        if from_month and to_month:
            return [x for x in month_iterator(from_month, to_month)]
        else:
            return []

    def get_series(self, from_month=None, to_month=None):
        """Get MonthBins for each month between the months given, creating empty bin_dict if there is no mutations

        Parameters
        ----------
        from_month: Month, optional
            Start with this month. Defaults to first month in the mutations
        to_month: Month, optional
            End with this month. Defaults to last month in the mutations

        Returns
        -------
        MonthSeries
            series of bins for each month

        """
        return MonthSeries.from_month_set(
            self, from_month=from_month, to_month=to_month
        )

    def plot(self, ax=None):
        """Plot this mutations per month as a bar graph

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

        months = self.months()
        sum_values = [x.sum() for x in self.bins()]

        ind = np.arange(len(months))
        ax.bar(x=ind, height=sum_values)

        ax.set_ylabel(f"{self.description} (Euro)")
        ax.set_xlabel("Month")
        ax.grid(which="both", axis="y")
        ax.set_xticks(ind)
        ax.set_xticklabels([str(x) for x in months])

        return ax


class MonthSeries(MonthSet):
    """A MonthSet that is guaranteed to have all consecutive months between min and max

    Months without mutations will just have empty month bins"""

    def __init__(
        self, mutations, description="Unnamed", from_month=None, to_month=None
    ):
        """Create a consecutive series of month bins with the given mutations.

        When from_month and/or to_month arg given, cut or pad with empty month bins if needed

        Parameters
        ----------
        mutations: List[Mutations]
            The mutations in this dataset
        from_month: Month, optional
            Start with this month. Defaults to first month in the mutations
        to_month: Month, optional
            End with this month. Defaults to last month in the mutations


        """
        super().__init__(mutations, description)

        # MonthSet might have missing months. Make into range
        self.data = self.make_into_series(self.data, from_month, to_month)

    @classmethod
    def from_month_set(cls, month_set, from_month=None, to_month=None):
        """Create a MonthSeries from A MonthSet.

        For efficient casting from MonthSet. Without needing to sort all mutations again

        Parameters
        ----------
        month_set: MonthSet
            The MonthSet instance to create MonthSeries from
        from_month: Month, optional
            Start with this month. Defaults to first month in the mutations
        to_month: Month, optional
            End with this month. Defaults to last month in the mutations

        """
        if not from_month:
            from_month = month_set.min_month
        if not to_month:
            to_month = month_set.max_month
        series = cls(mutations=month_set.mutations, description=month_set.description)
        series.data = series.make_into_series(
            month_set.data, from_month=from_month, to_month=to_month
        )
        return series

    def make_into_series(self, bin_dict, from_month, to_month):
        """Make the given dictionary of bins into a series of consecutive months

        Parameters
        ----------
        bin_dict: OrderedDict[Month, MonthBin]:
            A collection of month bins. Does not need to be oredered or consecutive
        from_month: Month, optional
            Start with this month. Defaults to first month in the mutations
        to_month: Month, optional
            End with this month. Defaults to last month in the mutations

        Returns
        -------
        OrderedDict[Month, MonthBin]

        """
        if not bin_dict:
            return bin_dict  # handy empty input dict

        if not from_month:
            from_month = self.min_month
        if not to_month:
            to_month = self.max_month

        bin_dict_series = OrderedDict()
        for month in self.get_month_range(from_month, to_month):
            if month in bin_dict:
                bin_dict_series[month] = bin_dict[month]
            else:
                bin_dict_series[month] = MonthBin(mutations=[], month=month)
        return bin_dict_series


@total_ordering
class Month:
    """Like date, but day is always 1"""

    def __init__(self, date):
        """

        Parameters
        ----------
        date: datetime.date or str
            When datetime.date, only the year and week are used.
            When string, needs to have yyyy/mm format
        """
        if type(date) == str:
            self.date = datetime.datetime.strptime(date, "%Y/%m").date()
        elif type(date) == datetime.date:
            self.date = datetime.date(year=date.year, month=date.month, day=1)
        else:
            raise ValueError(
                f"parameter date needs to be str or datetime.date, found {type(date)}"
            )

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

    def __len__(self):
        return len(self.mutations)

    def __iter__(self):
        return self.mutations.__iter__()

    @property
    def date(self):
        """The date for this bin

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

    def sum(self) -> float:
        """Sum of all amounts in this bin"""
        return sum([x.amount for x in self.mutations])

    def sum_in(self) -> float:
        """Sum of all incoming amounts in this bin"""
        return sum([x.amount for x in self.mutations if x.amount > 0])

    def sum_out(self) -> float:
        """Sum of all outgoing amounts in this bin"""
        return sum([x.amount for x in self.mutations if x.amount < 0])


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


class MonthMatrix(Plottable, UserDict):
    """Holds MonthSeries for a number of categories. Dictionary of str: MonthSeries

    """

    def __init__(self, filtered_data_list):
        """
        Parameters
        ----------
        filtered_data_list: List[MutationSet]

        """
        super().__init__()
        # Separate each mutations list into months
        sets = [MonthSet(mutations=x.mutations, description=x.description) for x in filtered_data_list]

        # determine the full month range of all sets
        self.min_month = min([x.min_month for x in sets])
        self.max_month = max([x.max_month for x in sets])

        # make all sets into series of the same length
        series = {x.description: MonthSeries.from_month_set(x, self.min_month, self.max_month) for x in sets}
        self.data = series

    def descriptions(self):
        return list(self.data.keys())

    def get_month_range(self):
        """Get all months in between min and max months. For consistent plotting

        """
        return [x for x in month_iterator(self.min_month, self.max_month)]

    def matrix(self):
        """Data per month, per category as a 2D array

        Returns
        -------
        Dict[Month, List[MonthBin]]
        """

        matrix = {}
        for per_month in self.per_month_list:
            matrix[per_month.description] = per_month.get_series(
                self.min_month, self.max_month
            )

        return matrix

    def plot(self, ax=None):
        """Plot this matrix as a stacked graph

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

        # get sums for each series rounded
        sums = {x: [int(z) for z in y.sums()] for x, y in self.data.items()}

        months = self.get_month_range()
        ind = np.arange(len(months))  # the x locations for the bars

        # work out bottom, height for each series by stacking for each month
        test = 1
        # start with a height of 0
        current_height = [0] * len(months)
        handles = []
        for series_sums in sums.values():
            handles.append(plt.bar(ind, series_sums, width=0.8, bottom=current_height))
            current_height = piece_wise_add(current_height, series_sums)

        # arange for len(months)

        # plt.bar(ind, series, width, bottom)


        plt.ylabel('amount')
        #plt.title('Scores by group and gender')
        plt.xticks(ind, [str(x.date.strftime("%b `%y")) for x in months])
        #plt.yticks(np.arange(0, 81, 10))
        plt.legend(reversed([x[0] for x in handles]), reversed(self.descriptions()))


def piece_wise_add(list_a, list_b):
    """Add each element of list a to list b.

    After trying to get numpy to work with decimals for about 10 minuts
    it was raising cryptic errors. Enough of that nonsense.
    """
    return [x+y for x, y in zip(list_a, list_b)]

