# -*- coding: utf-8 -*-

"""Main module."""


class Mutation:
    """An increase or decrease of money on an account. Basic object for most things in sitdown.

    Is sortable by date by default
    """

    def __init__(
        self,
        amount,
        date,
        account,
        currency="EURO",
        opposite_account=None,
        description="",
        balance_before=None,
        balance_after=None,
    ):
        """Create a transaction

        Parameters
        ----------
        amount: Decimal
            amount of money transferred. Negative amount means money is spent
        date: datetime.date
            date of transfer
        account: BankAccount
            Account on which this mutation takes place
        opposite_account: BankAccount, optional
            Account on the other side of the transaction. Might not always be known. Defaults to None
        description: str, optional
            description of this mutation. Defaults to empty string
        currency: str, optional
            currency in which this mutation is done, Defaults to 'EURO'
        balance_before: Decimal, optional
            account balance before mutation. Defaults to None
        balance_after: Decimal, optional
            account balance after mutation. Defaults to None
        """

        self.amount = amount
        self.date = date
        self.account = account
        self.currency = currency
        self.opposite_account = opposite_account
        self.description = description
        self.balance_before = balance_before
        self.balance_after = balance_after

    def __str__(self):
        return f'Mutation of {self.amount} on {self.date}'

    def __lt__(self, other):
        return self.date < other.date


class BankAccount:

    def __init__(self, number, description=None):
        """A bank account.

        Parameters
        ----------
        number: str
            the account number
        description: str, optional
            short description of the account. For use in graphs etc. Defaults to account number

        """
        self.number = number
        if description is None:
            description = str(number)
        self.description = description

    def __str__(self):
        return f'Account {self.description}'


