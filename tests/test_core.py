#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sitdown` package."""
import datetime

from sitdown.readers import ABNAMROReader
from tests import RESOURCE_PATH
from tests.factories import generate_mutation_sequence


def test_abn_amro_reader():
    reader = ABNAMROReader()
    mutations = reader.read(RESOURCE_PATH / "example_abn_export.TAB")

    assert len(mutations) == 5
    assert mutations[4].amount == -16.8
    assert mutations[3].date == datetime.date(year=2016, month=8, day=4)


def test_mutations():
    mutations = generate_mutation_sequence()
    assert mutations[0].balance_after == mutations[1].balance_before
