"""Reading in financial mutations
"""
import re
from csv import DictReader
from datetime import datetime
from locale import setlocale, LC_NUMERIC, atof

from sitdown.core import Mutation, BankAccount


class ABNAMROReader:
    """Reads in mutations downloaded from ABN AMRO website as 'text'

    Example content lines:

    665481173	EUR	20160715	12,79   249,79	20160715	116,00	socks.com socks
    665481173	EUR	20160725	753,40	749,25	20160725	-3,15	something expensive
    etc..

    """

    LOCALE = 'NL-nl'  # Any locale that uses comma as decimal place indicator
    HEADER_NAMES = [
        "account",
        "currency",
        "date",
        "balance_before",
        "balance_after",
        "interest_date",
        "amount",
        "description",
    ]

    def read(self, input_file):
        """Try to read ABN AMRO input file and parse contents as mutations

        Parameters
        ----------
        input_file: Path
            path to abn amro mutations file

        Returns
        -------
        Set[Mutation]

        """
        setlocale(LC_NUMERIC, self.LOCALE)

        mutations = set()
        with open(input_file, "r") as tabfile:
            reader = DictReader(tabfile, delimiter="\t", fieldnames=self.HEADER_NAMES)
            for line in reader:
                try:
                    mutations.add(self.parse_to_mutation(line))
                except ValueError as e:
                    raise ReaderException(f"Error reading line '{line}': {e}")
        return mutations

    def parse_to_mutation(self, line):
        """Try to parse given line to mutation object

        """
        return Mutation(amount=atof(line['amount']),
                        date=datetime.strptime(line['date'], '%Y%m%d').date(),
                        account=BankAccount(number=line['account']),
                        currency=line['currency'],
                        opposite_account=self.find_iban(line['description']),
                        description=line['description'],
                        balance_after=atof(line['balance_after']),
                        balance_before=atof(line['balance_before'])
                        )

    @staticmethod
    def find_iban(text):
        """Try to find an IBAN account number in the given text

        """
        accounts = re.findall('[a-z,A-Z]{2}[0-9]{2}[a-z,A-Z]{0,4}[0-9]{10,}', text)
        if accounts:
            return accounts[0]
        else:
            return None


class ReaderException(Exception):
    pass
