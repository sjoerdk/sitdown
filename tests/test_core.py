#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

import pytest

from sitdown.core import BankAccount
from sitdown.filters import StringFilter, FilterSet, Filter
from tests.factories import MutationFactory


def test_objects():
    mutation = MutationFactory(amount=Decimal(10.0), date=datetime.date(year=1990, month=3, day=10))
    assert str(mutation) == "Mutation of 10 on 1990-03-10"

    account = BankAccount(number="ABNA08NL23409324", description="test")
    assert str(account) == "test"

