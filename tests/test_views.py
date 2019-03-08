import datetime
import matplotlib.pyplot as plt
import pytest


from sitdown.filters import FilterSet, StringFilter
from sitdown.core import MutationSet
from sitdown.views import MonthSet, MonthMatrix, Month, MonthBin, MonthSeries
from tests.factories import MutationFactory


@pytest.fixture
def mock_filtered_data(long_mutation_sequence):
    return MutationSet(mutations=long_mutation_sequence)


@pytest.fixture
def a_month_set():

    mutations = [
        MutationFactory(amount=10, date=datetime.date(2018, 1, 1)) for _ in range(10)
    ] + [MutationFactory(amount=30, date=datetime.date(2018, 4, 15)) for _ in range(10)]
    return MonthSet(mutations)


@pytest.fixture
def shop_a_b_filtered_data_set():
    """FilteredDataSet with mutations from both shop A and shop B
    For testing filtering
    """
    mutations = {MutationFactory(description="shop A") for _ in range(20)} | {
        MutationFactory(description="shop B") for _ in range(20)} | {
        MutationFactory(description="shop B", date=datetime.date(year=2017, month=9, day=1))
    }

    filter_set = FilterSet(
        filters=[
            StringFilter(string_to_match="shop A"),
            StringFilter(string_to_match="shop B"),
        ]
    )
    return filter_set.get_filtered_data_set(mutations)


def test_month():
    # A month can be created by string or by date.
    assert Month("1999/11") == Month(datetime.date(year=1999, month=11, day=1))
    # For creating from date, the day part is ignored and set to 1
    assert Month("1999/11") == Month(datetime.date(year=1999, month=11, day=10))
    assert Month("2018/01").date == datetime.date(year=2018, month=1, day=1)
    with pytest.raises(ValueError):
        Month(2018)


def test_data_per_month(a_month_set):
    ms = a_month_set
    assert len(ms.bins()) == 2
    assert ms.bins()[0].sum() == 100
    assert ms.bins()[1].sum() == 300


def test_month_series(a_month_set):
    series = a_month_set.get_series()
    assert len(series) == 4
    assert len(series[Month("2018/03")]) == 0
    assert len(series[Month("2018/04")]) == 10


def test_month_set_accessor(a_month_set):
    dpm = a_month_set
    assert type(dpm[Month(datetime.date(year=2018, month=4, day=1))]) == MonthBin
    with pytest.raises(KeyError):
        dpm[Month(datetime.date(year=2018, month=3, day=1))]


def test_month_set_cast_to_series(a_month_set):
    assert len(a_month_set.bins()) == 2
    assert len(list(a_month_set.bins())[0].mutations) == 10
    series = MonthSeries.from_month_set(a_month_set)
    assert len(series.bins()) == 4
    assert len(list(series.bins())[0].mutations) == 10


def test_month_set_plotting(long_mutation_sequence):
    dpm = MonthSet(long_mutation_sequence)
    dpm.plot()
    # plt.show()


def test_month_matrix(shop_a_b_filtered_data_set):

    matrix = MonthMatrix(filtered_data_list=shop_a_b_filtered_data_set)

    # with this input data, matrix should have two categories:
    assert list(matrix.keys()) == ['shop A', 'shop B']
    # month series should be accessible as keys
    assert type(matrix['shop A']) == MonthSeries
    # Both series should have the same date range
    assert matrix['shop A'].min_month == matrix['shop B'].min_month
    assert matrix['shop A'].max_month == matrix['shop B'].max_month
