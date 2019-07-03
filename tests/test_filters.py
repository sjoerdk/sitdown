#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from sitdown.core import BankAccount
from sitdown.filters import StringFilter, FilterSet, Filter, AccountFilter, AmountFilter
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


def test_account_filter():
    account1 = BankAccount(number=1233454, description='test1')
    account2 = BankAccount(number=4356345, description='test2')
    mutations = [MutationFactory(account=account1),
                 MutationFactory(account=account1),
                 MutationFactory(account=account1),
                 MutationFactory(account=account2),
                 MutationFactory(account=account2, opposite_account=account1)]

    assert len(AccountFilter(from_account=account1).apply(mutations)) == 3
    assert len(AccountFilter(from_account=account2).apply(mutations)) == 2
    assert len(AccountFilter(from_account=account2, to_account=account1).apply(mutations)) == 1
    assert len(AccountFilter().apply(mutations)) == 5


def test_amount_filter(short_mutation_sequence):
    assert len(short_mutation_sequence) == 10
    assert len(AmountFilter(from_amount=200).apply(short_mutation_sequence)) == 7
    assert len(AmountFilter(to_amount=200).apply(short_mutation_sequence)) == 3
    assert len(AmountFilter(from_amount=100, to_amount=200).apply(short_mutation_sequence)) == 1


def test_string_filter_chain(mutation_sequence_with_set_descriptions):
    """Filters can be chained, so that mutations is passed through all filters in the chain
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


def test_filter():
    """Assert that filter cannot be instatiated directly"""
    with pytest.raises(TypeError):
        Filter(description="some description")


