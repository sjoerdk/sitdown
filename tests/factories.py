import datetime

import factory
from factory.fuzzy import FuzzyText, FuzzyDate, FuzzyDecimal

from sitdown.classifiers import StringMatchClassifier
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

class StringMatchClassifierFactory(factory.Factory):

    class Meta:
        model = StringMatchClassifier

