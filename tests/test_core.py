#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sitdown` package."""
import datetime

import pytest

from sitdown.readers import ABNAMROReader
from tests import RESOURCE_PATH


def test_abn_amro_reader():
    reader = ABNAMROReader()
    mutations = reader.read(RESOURCE_PATH / 'example_abn_export.TAB')

    assert len(mutations) == 5
    assert mutations[4].amount == -16.8
    assert mutations[3].date == datetime.date(year=2016, month=8, day=4)


