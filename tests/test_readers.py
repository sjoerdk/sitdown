#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from sitdown.readers import ABNAMROReader
from tests import RESOURCE_PATH


def test_abn_amro_reader():
    reader = ABNAMROReader()
    mutations = reader.read(RESOURCE_PATH / "example_abn_export.TAB")

    assert len(mutations) == 5
    assert type(mutations.pop().amount) == float
    assert type(mutations.pop().date) == datetime.date
