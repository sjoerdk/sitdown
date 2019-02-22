import datetime

import factory
from factory.fuzzy import FuzzyText, FuzzyDate, FuzzyFloat, FuzzyDecimal

from sitdown.core import Mutation, BankAccount


class MutationFactory(factory.Factory):
    """Creates mutations on a bank account"""
    class Meta:
        model = Mutation

    amount = FuzzyDecimal(0.01, 500.00)
    date = FuzzyDate(start_date=datetime.date(2018, 1, 1), end_date=datetime.date(2018, 4, 1))
    account = BankAccount(number="128456789", description='Mock bankaccount')
    currency = "EURO"
    opposite_account = None
    description = FuzzyText(length=30)
    balance_before = FuzzyDecimal(0.01, 500.00)
    balance_after = factory.LazyAttribute(lambda obj: obj.balance_before + obj.amount)


def generate_mutation_sequence():
    """Generate a list of mutations that makes sense in time """
    factory.fuzzy.reseed_random(1234)
    mutations = [MutationFactory() for _ in range(500)]
    mutations.sort()

    # make sure the balance on the account makes sens for this sequence
    previous = None
    for mutation in mutations:
        if previous:
            mutation.balance_before = previous.balance_after
            mutation.balance_after = mutation.balance_before + mutation.amount
        previous = mutation

    return mutations
