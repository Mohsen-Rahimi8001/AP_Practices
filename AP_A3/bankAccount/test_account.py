import unittest
from account import BankAcc, TimeZone
import datetime as dt
import itertools
from decimal import Decimal

class TestBankAcc(unittest.TestCase):

    def setUp(self):
        self.accNum = 1000
        self.name = "Mohsen"
        self.family = "Rahimi"
        self.tz = TimeZone("MSN", -2.5)
        self.firstBalance = 100
        self.account = BankAcc(self.accNum, self.name, self.family, tz=self.tz, balance=self.firstBalance)

    def tearDown(self):
        BankAcc.accNumbers = []
        BankAcc.trans_counter = itertools.count(100)

    def test_init(self):
        self.assertRaises(TypeError, BankAcc, '123', 'a', 'a')
        with self.assertRaises(ValueError):
            BankAcc(123, 'mohsen', 'reza')
            BankAcc(123, 'ali', 'akbar')
        with self.assertRaises(AttributeError):
            acc = BankAcc(345, 'mohsen', 'reza')
            acc.accNum = 5
        with self.assertRaises(AttributeError):
            self.account.fullname = 'foo bar'

        with self.assertRaises(ValueError):
            self.account.family = ""
        
        with self.assertRaises(ValueError):
            self.account.family = None

        with self.assertRaises(ValueError):
            self.account.name = ""
        
        with self.assertRaises(ValueError):
            self.account.name = None

        self.assertEqual(self.account.accNum, self.accNum)
        self.assertEqual(self.account.name, self.name)
        self.assertEqual(self.account.family, self.family)
        self.assertEqual(self.account.tz, self.tz)
        self.assertEqual(self.account.balance, self.firstBalance)
        self.assertEqual(self.account.fullname, self.name + " " + self.family)

    def test_deposit(self):
        self.assertRaises(TypeError, self.account.deposit, 'bluh bluh')
        self.assertRaises(ValueError, self.account.deposit, 0)
        self.account.deposit(1)
        self.assertEqual(self.account.balance, 101)
        
    def test_generate_confirmation_code(self):
        dt_now = dt.datetime.utcnow()
        code = self.account.generate_confirmation_code('X')
        expectation = f"X-{self.account.accNum}-{(dt_now + self.account.tz.offset).strftime('%Y%m%d%H%M%S')}-100"
        self.assertEqual(code, expectation)

    def test_confirmation_code_parser(self):
        dt_now = dt.datetime.utcnow()
        code = self.account.generate_confirmation_code('X')
        information = self.account.confirmation_code_parser(code)
        self.assertEqual(information.transaction_code, 'X')
        self.assertEqual(information.account_number, self.account.accNum)
        
        expected_time = f'{(dt_now + self.account.tz.offset).strftime("%Y-%m-%d %H:%M:%S")} ({self.account.tz.name})'
        self.assertEqual(expected_time, information.time)
        
        self.assertEqual(information.transaction_id, 100)
        self.assertEqual(information.time_utc, dt_now.strftime("%Y-%m-%dT%H:%M:%S"))

    def test_pay_intereset(self):
        acc = BankAcc(1235, self.name, self.family, tz=self.tz, balance=333)
        expected = acc.balance + Decimal(acc.INTREST_RATE * acc.balance / 100)
        acc.pay_interest()
        self.assertEqual(acc.balance, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
