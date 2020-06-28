""" Different ways of plotting mutations. Just some examples"""
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt

from sitdown.core import Mutation
from sitdown.views import MonthSeries, MonthSet


def plot_balance(mutations: List[Mutation]):
    """Plot balance over time. List of mutations should come from a single account"""
    mutations.sort()

    _, ax = plt.subplots(figsize=(12, 12))
    ax.set_ylim([0, 1000])
    ax.grid(b=True, which='both', color='0.65', linestyle='-')
    ax.set_xlim([datetime.date(year=2019, month=7, day=1),
                 datetime.date(year=2020, month=2, day=1)])
    ax.plot([x.date for x in mutations], [x.balance_after for x in mutations])
    return ax


def in_out(mutations: List[Mutation]):
    """Plot incoming / outgoing total per month for given mutations

    Call plt.show() to actually render this plot
    """
    ax = None
    if not ax:
        _, ax = plt.subplots(figsize=(12, 12))

    incoming = MonthSeries([x for x in mutations if x.amount > 0])
    outgoing = MonthSeries([x for x in mutations if x.amount <= 0])

    all = MonthSet(mutations)

    plt.xticks(rotation=70)
    incoming.plot(ax)
    outgoing.plot(ax)
    all.plot(ax)

    diff_text = [f"{x.date} - {x.sum():.1f}" for x in all.bins()]
    print("\n".join(diff_text))

    diff_text = [f"{x.date} - {x.sum():.1f}" for x in all.bins()]

    ax.grid(b=True, which="both", color="0.65", linestyle="-")
    ax.set_ylim([-6000, 6000])

    return ax
