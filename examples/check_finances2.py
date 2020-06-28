"""
Check out finances May 2019
"""
import datetime

from sitdown.readers import ABNAMROReader
from sitdown.core import BankAccount, Mutation
import matplotlib.pyplot as plt

from sitdown.views import MonthSet, MonthBin, MonthSeries


accounts = {
    "shared": BankAccount(number="254265944", description="Shared Current Acccount"),
    "sjoerd": BankAccount(number="625381173", description="Sjoerd Acccount"),
    "shared_monthly": BankAccount(
        number="816163715", description="Shared Monthly Acccount"
    ),
    "old_sjoerd": BankAccount(number="625335295", description="Old Sjoerd Account"),
}

abn_downloads = ["/home/sjoerd/Documents/finances/2020/TXT200205202318.TAB"]

reader = ABNAMROReader(accounts=list(accounts.values()))
mutations = [reader.read(x) for x in abn_downloads]
all = sorted(list(set([]).union(*mutations)), key=lambda x: x.date)

accounts_found = reader.accounts


def in_out(mutations):
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
    # ax.set_xlim([datetime.date(year=2018, month=7, day=1), datetime.date(year=2019, month=5, day=1)])

    test = 1


shared  = [x for x in all if x.account == accounts["shared"]]

in_out(shared)
# in_out([x for x in all])

plt.show()
