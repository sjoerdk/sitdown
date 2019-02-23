#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from sitdown.filters import StringFilter, FilterSet
from tests.factories import MutationFactory


@pytest.fixture
def mutation_sequence_with_set_descriptions(short_mutation_sequence):
    extra = {
        MutationFactory(description="SUPER SHOP"),
        MutationFactory(description="SUPER SHOP alert!"),
        MutationFactory(description="some other alert!"),
    }
    return short_mutation_sequence | extra


def test_string_filter(mutation_sequence_with_set_descriptions):
    """Test whether this filter actually filters out strings """
    string_filter = StringFilter(string_to_match="SUPER SHOP")
    assert len(string_filter.apply(mutation_sequence_with_set_descriptions)) == 2


def test_string_filter_chain(mutation_sequence_with_set_descriptions):
    """Filters can be chained, so that data is passed through all filters in the chain
    """
    mutations = mutation_sequence_with_set_descriptions

    string_filter = StringFilter(string_to_match="SUPER SHOP")
    string_filter2 = StringFilter(string_to_match="alert!", parent=string_filter)
    string_filter3 = StringFilter(
        string_to_match="some other string", parent=string_filter2
    )

    assert len(string_filter.apply(mutations)) == 2
    assert len(string_filter2.apply(mutations)) == 1
    assert len(string_filter3.apply(mutations)) == 0


def test_string_filter_set(mutation_sequence_with_set_descriptions):
    """Filter set combines several filters
    """
    mutations = mutation_sequence_with_set_descriptions

    filters = {
        StringFilter(string_to_match="SUPER SHOP"),
        StringFilter(string_to_match="alert!"),
    }
    # both filters should yield 2 mutations
    for fltr in filters:
        assert len(fltr.apply(mutations)) == 2

    # but on mutation is in both sets, so the set should only have 3 unique
    filter_set = FilterSet(filters=filters)
    assert len(filter_set.apply(mutations)) == 3
