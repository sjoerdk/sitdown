#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from sitdown.readers import ABNAMROReader
from tests import RESOURCE_PATH


def test_abn_amro_reader():
    reader = ABNAMROReader()
    mutations = reader.read(RESOURCE_PATH / "example_abn_export.TAB")

    assert len(mutations) == 5
    assert mutations[4].amount == -16.8
    assert mutations[3].date == datetime.date(year=2016, month=8, day=4)


def test_mutations(short_mutation_sequence):

    sequence = short_mutation_sequence
    assert sequence[0].balance_after == sequence[1].balance_before
