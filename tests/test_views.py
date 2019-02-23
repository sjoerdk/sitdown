import pytest

from sitdown.filters import FilteredData
from sitdown.views import DataPerMonth


@pytest.fixture
def mock_filtered_data(long_mutation_sequence):
    return FilteredData(mutations=long_mutation_sequence, filter_used=None)


def test_data_per_month(mock_filtered_data):
    dpm = DataPerMonth(mock_filtered_data)
    per_month = dpm.get_bins()
    assert len(per_month) == 4

