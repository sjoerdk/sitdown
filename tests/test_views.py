import datetime
import matplotlib.pyplot as plt
import pytest


from sitdown.filters import FilteredData, FilterSet, StringFilter
from sitdown.views import DataPerMonth, MonthMatrix
from tests.factories import MutationFactory


@pytest.fixture
def mock_filtered_data(long_mutation_sequence):
    return FilteredData(mutations=long_mutation_sequence)


def test_data_per_month(mock_filtered_data):
    mutations = [
        MutationFactory(amount=10, date=datetime.date(2018, 1, 1)) for _ in range(10)
    ] + [MutationFactory(amount=30, date=datetime.date(2018, 4, 15)) for _ in range(10)]
    dpm = DataPerMonth(filtered_data=FilteredData(mutations, None))
    assert len(dpm.bins) == 2
    assert dpm.bins[0].sum() == 100
    assert dpm.bins[1].sum() == 300


def test_data_per_month_plotting(mock_filtered_data):
    dpm = DataPerMonth(mock_filtered_data)
    dpm.plot()
    # plt.show()


def test_data_per_month_set_plotting():

    mutations = {MutationFactory(description="shop A") for _ in range(20)
                 } | {MutationFactory(description="shop B") for _ in range(20)}

    filter_set = FilterSet(filters=[StringFilter(string_to_match="shop A"),
                                    StringFilter(string_to_match="shop B")])

    pms = filter_set.get_filtered_data_set(mutations)
    matrix = MonthMatrix(filtered_data_list=pms.filtered_data_list)

    range = matrix.get_month_range()
    test = 1
