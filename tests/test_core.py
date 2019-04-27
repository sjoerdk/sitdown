#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

from sitdown.core import BankAccount, MutationSet
from tests.factories import MutationFactory
from tests import RESOURCE_PATH


def test_objects():
    mutation = MutationFactory(amount=Decimal(10.0), date=datetime.date(year=1990, month=3, day=10))
    assert str(mutation) == "Mutation of 10 on 1990-03-10"

    account = BankAccount(number="ABNA08NL23409324", description="test")
    assert str(account) == "test"


def test_mutation_set(tmp_path, short_mutation_sequence):
    """ Test loading and saving of a mutation set
    """
    org_set = MutationSet(mutations=short_mutation_sequence, description="test_saving")
    file_path = tmp_path / 'mutation_set.pcl'
    with open(file_path, 'wb') as f:
        org_set.save(file=f)

    with open(file_path, 'rb') as f:
        loaded_set = MutationSet.load(f)

    assert loaded_set.mutations == org_set.mutations
