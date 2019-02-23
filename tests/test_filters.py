#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from sitdown.filters import StringFilter
from tests.factories import MutationFactory


@pytest.fixture
def mutation_sequence_with_set_descriptions(short_mutation_sequence):
    extra = [MutationFactory(description='SUPER SHOP'),
             MutationFactory(description='SUPER SHOP alert!'),
             MutationFactory(description='some other alert!')]
    return short_mutation_sequence + extra


def test_mutations(short_mutation_sequence):
    sequence = short_mutation_sequence
    assert sequence[0].balance_after == sequence[1].balance_before


def test_string_filter(mutation_sequence_with_set_descriptions):
    string_filter = StringFilter(string_to_match="SUPER SHOP")
    assert len(string_filter.apply(mutation_sequence_with_set_descriptions)) == 2


def test_string_filter_chain(mutation_sequence_with_set_descriptions):
    """Filters can be chained, so that data is passed through all filters in the chain

    Parameters
    ----------
    short_mutation_sequence

    Returns
    -------

    """
    mutations = mutation_sequence_with_set_descriptions

    string_filter = StringFilter(string_to_match="SUPER SHOP")
    string_filter2 = StringFilter(string_to_match="alert!", parent=string_filter)

    assert len(string_filter.apply(mutations)) == 2
    assert len(string_filter2.apply(mutations)) == 1



