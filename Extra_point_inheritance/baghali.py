"""
Define      Name        Buying Cost     Selling Cost
Delete      Name
Sell        Name        Count
Buy         Name        Count
Status
Financial
Exit
"""
import re

class Item:
    def __init__(self, name, b_cost, s_cost):
        self.name = name
        self.b_cost = b_cost
        self.s_cost = s_cost
    
    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        else:
            return NotImplemented

class Baghali: 
    items:list[Item] = []
    mojood:dict[str, int] = {} # name : count
    financial_log:dict[str, list[int, int]] = {} # name:[buy, sell]

    @staticmethod
    def check_if_foat_or_int(*values) -> bool:
        """Checks if all the values are numeric."""
        for value in values:
            if not re.fullmatch("[1-9]+[0-9]*(?:\.[0-9]+)?", value):
                return False
        else:
            return True

    @classmethod
    def get_stuff_by_name(cls, name:str, default=None) -> Item:
        """Search in cls.items"""
        try:
            return cls.items[cls.items.index(name)]
        except ValueError as exp:
            if str(exp) == f'{name} is not in list':
                return default
            else:
                raise exp

    @classmethod
    def define(cls, name:str, b_cost:str, s_cost:str):
        """Defines an item and adds it to cls.items"""
        if cls.check_if_foat_or_int(b_cost, s_cost):
            cls.items.append(Item(name, float(b_cost), float(s_cost)))
            cls.mojood[name] = 0
            cls.financial_log[name] = [0, 0]
        else:
            raise TypeError(f"b_cost and s_cost must be numeric.")

    @classmethod
    def delete(cls, name):
        """Deletes an item if it exists in cls.items"""
        if name in cls.mojood and cls.mojood[name] > 0:
            print("!")
        else:
            item = cls.get_stuff_by_name(name)
            cls.items.remove(item)
            del cls.mojood[name]
            del cls.financial_log[name]

    @classmethod
    def sell(cls, name:str, count:str) -> None:
        """Sells count number of items."""
        if not count.isdigit() or (count:=int(count)) < 0:
            raise ValueError("count must be an integer.")

        if name in cls.mojood:
            if count > cls.mojood[name]:
                raise ValueError("Not enough items to sell.")
            cls.mojood[name] -= count
            cls.financial_log[name][1] += count # financial --> dict(name : [buy, sell])
        
        elif name not in cls.items:
            raise ValueError(f"{name} is not a defined item.")

    @classmethod
    def buy(cls, name:str, count:str) -> None:
        """Buys count number of items."""
        if not count.isdigit() or (count:=int(count)) < 0:
            raise ValueError("count must be an integer.")

        if name not in cls.items:
            raise ValueError(f"{name} is not a defined item. you can define it using {Baghali.define}.")
        else:
            cls.mojood[name] += count
            cls.financial_log[name][0] += count

    @classmethod
    def status(cls):
        """Shows all defined items with their information."""
        print(f"{'Name':<10}{'b_cost':<10}{'s_cost':<10}{'count':<10}")
        for name, count in cls.mojood.items():
            item = cls.get_stuff_by_name(name)
            if isinstance(item, Item):
                print(f"{item.name:<10}{item.b_cost:<10}{item.s_cost:<10}{count:<10}")
            else:
                raise ValueError(f"{name} is not a defined item. you can should define first.")

    @classmethod
    def financial(cls):
        """Shows a summary of income and outlay."""
        print(f"{'Name':<10}{'Buys':<10}{'Sells':<10}{'Total':<10}")
        for name, buy_sell in cls.financial_log.items():
            item = cls.get_stuff_by_name(name)
            if isinstance(item, Item):
                total = buy_sell[1] * item.s_cost - buy_sell[0] * item.b_cost
                print(f"{name:<10}{buy_sell[0]:<10}{buy_sell[1]:<10}{total:<10.2f}")
            else:
                raise ValueError(f"{name} is not a defined item. you can should define first.")


if __name__ == "__main__":
    while True:
        command = input().split()
        
        if not command: # when user hit enter without any character
            continue

        if command[0].lower() == 'exit':
            break

        else:      
            try:
                exec('Baghali.'+command[0].lower()+f"(*{command[1:]})")
            except AttributeError as exp:
                print("Invalid command.")
            except TypeError as exp:
                print("Invalid Arguments.")
            except ValueError as exp:
                print("Invalid Arguments.")
