import datetime as dt
from decimal import Decimal
import itertools
from collections import namedtuple


class TimeZone:
    """TimeZone class"""

    def __init__(self, name:str, offset:float):
        """
        TimeZone initializer
        parameters:
            name: timezone name
            offset: the offset of timezone from UTC
        """
        self.name = name
        self.offset = offset

    @property
    def name(self):
        """TimeZone name"""
        return self._name
    
    @name.setter
    def name(self, value:str):
        if type(value) != str or not value:
            raise ValueError('Timezone name must be a non-empty string.')
        else:
            self._name = value.strip()

    @property
    def offset(self):
        """TimeZone offset hours"""
        return self._offset

    @offset.setter
    def offset(self, value:float):
        if type(value) != int and type(value) != float:
            raise ValueError('Hour offset must be a numeric value.')
        
        if value < -12 or value > 14:
            raise ValueError('Offset must be between -12:00 and +14:00.')

        self._offset = dt.timedelta(hours=value)

    def __repr__(self):
        return (f"TimeZone(name='{self.name}', offset={self.offset})")


class BankAcc:
    """This is the main class"""

    encodeTimeFormat = '%Y%m%d%H%M%S'
    trans_counter = itertools.count(100)
    trans_types = {
        'deposit' : 'D',
        'withdraw' : 'W',
        'interest' : 'I',
        'declined' : 'X',
    }
    accNumbers:list = [] # it could be more efficient if we had a database.
    INTREST_RATE = 0.5 # persent

    def __init__(self, accNum:int, name:str, family:str, \
         tz:TimeZone=None, balance:Decimal=Decimal('0.0')):
        """
        BankAcc initializer
        parameters:
            accNum: the account number of the customer
            name: name of customer
            family: family of customer
            tz: timezone of the customer
            balance: the initial value of customer balance
        """
        if self.is_valid_accNum(accNum):
            self.__accNum = accNum
            BankAcc.accNumbers.append(accNum)

        self.name = name
        self.family = family
        self.tz = tz if tz else TimeZone("Tehran", 3.5)

        if self.is_valid_balance(balance):
            self.__balance = balance

    fullname = property(fget = lambda self: self.name + " " + self.family, doc="Customer's fullname")

    @property
    def name(self):
        """name of the customer"""
        return self._name

    @name.setter
    def name(self, value:str):
        if not value or type(value) != str:
            raise ValueError("name must be a non-empty string.")
        else:
            self._name = value.strip()

    @property
    def family(self):
        """family of the customer"""
        return self._family

    @family.setter
    def family(self, value:str):
        if not value or type(value) != str:
            raise ValueError("family must be a non-empty string.")
        else:
            self._family = value.strip()

    @property
    def tz(self):
        """Customer timezone"""
        return self._tz

    @tz.setter
    def tz(self, value:TimeZone):
        if not isinstance(value, TimeZone):
            raise TypeError(f"tz must be an object of " 
            f"class TimeZone you entered {value.__class__.__name__}.")
        else:
            self._tz = value
    
    @property
    def accNum(self):
        """unique account number"""
        return self.__accNum

    @staticmethod
    def is_valid_accNum(accNum:int) -> bool:
        """Validates customer's account number"""
        if type(accNum) != int:
            raise TypeError("accNum must be an integer.")

        if accNum in BankAcc.accNumbers:
            raise ValueError("accNum must be unique.")
        
        return True

    @property
    def balance(self):
        """Customer balance"""
        return self.__balance

    @staticmethod
    def is_valid_balance(balance:int) -> bool:
        """Validates the initial value of balance."""
        if type(balance) not in (int, float, Decimal):
            raise TypeError("balance must be a numeric value.")
        
        if balance < 0:
            raise ValueError("balance must be non-negative.")
        
        return True

    def generate_confirmation_code(self, transCode:str) -> str:
        """
        description: Generates confirmation code
        return: 
            f"{the transaction code}-{the account number}-{the date/time in UTC of the transaction}-{the transaction number}"
        """
        trNum = next(BankAcc.trans_counter)
        dt_str = (dt.datetime.utcnow()+self.tz.offset).strftime(self.encodeTimeFormat)
        
        return f"{transCode}-{self.accNum}-{dt_str}-{trNum}"

    def confirmation_code_parser(self, confCode:str, timeFormat:str="%Y-%m-%d %H:%M:%S", utcTimeFormat:str="%Y-%m-%dT%H:%M:%S"):
        """Parses the confirmation code and return its information"""
        info = namedtuple("info", "transaction_code account_number time transaction_id time_utc")
        transaction_code, account_number, time, transaction_id, time_utc = *confCode.split("-"), dt.datetime.utcnow()
        time_utc = time_utc.strftime(utcTimeFormat)
        time = dt.datetime.strptime(time, self.encodeTimeFormat)
        time = time.strftime(timeFormat) + f" ({self.tz.name})"
        result = info(transaction_code, int(account_number), time, int(transaction_id), time_utc)
        return result
    
    def deposit(self, amount:Decimal) -> str:
        """
        Deposit money to the account.
        parameters:
            amount: amount of money to deposit
        return:
            result confirmation_code
        """
        if type(amount) not in (int, float, Decimal):
            raise TypeError("Deposit amount must be numeric.")
        else:
            amount = Decimal(amount)
        
        if amount <= Decimal('0.0'):
            raise ValueError("Deposit amount must be positive.")
        
        self.__balance += amount
        
        return self.generate_confirmation_code(self.trans_types['deposit'])

    def withdraw(self, amount:Decimal) -> str:
        """
        Withdraw money from the account
        parameters:
            amount: amount of money to withdraw
        return:
            result confirmation_code
        """
        if type(amount) not in (int, float, Decimal):
            raise TypeError("withdraw amount must be numeric.")
        else:
            amount = Decimal(amount)
        
        if amount <= Decimal('0.0'):
            raise ValueError("withdraw amount must be positive.")

        if self.balance < amount:
            return self.generate_confirmation_code(self.trans_types['declined'])
        else:
            self.__balance -= amount
            return self.generate_confirmation_code(self.trans_types['withdraw'])
            
    def pay_interest(self) -> str:
        """Pay monthly interest of customer"""
        amount = Decimal(self.balance * BankAcc.INTREST_RATE / 100)
        self.__balance += amount

        return self.generate_confirmation_code(self.trans_types['interest'])
    
    
if __name__ == "__main__":
    help(BankAcc)
