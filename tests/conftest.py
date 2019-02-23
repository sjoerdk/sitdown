"""Pytest fixtures that are available to all tests in /tests

"""
import factory
import pytest

from tests.factories import MutationFactory


@pytest.fixture
def short_mutation_sequence():
    return generate_mutation_sequence(10)


@pytest.fixture
def long_mutation_sequence():
    return generate_mutation_sequence(500)


def generate_mutation_sequence(number):
    """a list of mutations that makes sense in time

    Parameters
    ----------
    number: int
        number of mutations to generate

    Returns
    -------
    Set[Mutation]
    """
    factory.fuzzy.reseed_random(1234)
    mutations = [MutationFactory() for _ in range(number)]
    mutations.sort()
    # make sure the balance on the account makes sens for this sequence
    previous = None
    for mutation in mutations:
        if previous:
            mutation.balance_before = previous.balance_after
            mutation.balance_after = mutation.balance_before + mutation.amount
        previous = mutation
    return set(mutations)
