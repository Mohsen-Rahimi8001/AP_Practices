import datetime as dt
from numbers import Real
import math
import os

class MedadRangi:
    discount_rate:float = 10 # persent
    geo_loc:tuple[float] = (35.74317403843504, 51.50185488303431)
    items:list["MedadRangi"] = []

    def __init__(self, name:str, price:float, number:int, country:str, company:str):
        self.name = name
        self.price = price
        self.number = number
        self.country = country
        self.company = company

    @property
    def name(self):
        """The name of the item."""
        return self._name

    @name.setter
    def name(self, new_name:str):
        if not isinstance(new_name, str):
            raise TypeError("name must be of type str.")
        if not new_name:
            raise ValueError(f"Invalid name {new_name}")
        else:
            self._name = new_name

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, new_number:int):
        if not isinstance(new_number, int):
            raise TypeError("number must be of type int.")
        if new_number < 0:
            raise ValueError("number must be positive.")
        self._number = new_number

    @property
    def country(self):
        """The country of the item."""
        return self._country

    @country.setter
    def country(self, new_country:str):
        if not isinstance(new_country, str):
            raise TypeError("country must be of type str.")
        if not new_country:
            raise ValueError(f"Invalid name {new_country}")
        else:
            self._country = new_country

    @property
    def company(self):
        """The company of the item."""
        return self._company

    @company.setter
    def company(self, new_company:str):
        if not isinstance(new_company, str):
            raise TypeError("company must be of type str.")
        if not new_company:
            raise ValueError(f"Invalid name {new_company}")
        else:
            self._company = new_company

    @property
    def price(self):
        """The price of the item."""
        return self._price

    @price.setter
    def price(self, new_price:float):
        if not isinstance(new_price, Real):
            raise TypeError(f"price must be an object of float or int class you entered {type(new_price).__name__}")
        if new_price < 0:
            raise ValueError("price must be a positive number.")
        self._price = new_price

    @staticmethod
    def welcome() -> None:
        """print a message according to the current time"""
        time = dt.datetime.now().time()
        if dt.time(6) <= time <= dt.time(12):
            return "Good morning!!!"
        elif dt.time(12) < time <= dt.time(18):
            return "Good evening!!!"
        else:
            return "The shop is closed!!!"

    @classmethod
    def loat_csv(cls, directory:str) -> None:
        """Load csv file and store the data in items attribute"""
        if os.path.exists(directory):
            with open(directory, 'r') as f:
                args = f.readline().strip().split(',')
                for line in f.readlines():
                    item_args = line.strip().split(',')
                    data = {key:value for key, value in zip(args, item_args)}
                    cls.add_item(**data)

        else:
            print("No such file or directory: " + directory)

    @classmethod
    def add_item(cls, name:str, price:float, number:int, country:str, company:str):
        """Create and add a new item to the shop"""
        try:
            price = float(price)
            number = int(number)
        except ValueError:
            print(f"{price} must be convertable to float and {number} must be convertable to int.")

        new_item = cls(name.strip(), price, number, country.strip(), company.strip())
        cls.items.append(new_item)

    @classmethod
    def calculate_distance(cls, dest_loc:tuple[float]):
        """
        Calculate the distance between the shop location an dest_loc using 'Haversine formula'
        dest_loc: (Longitude, Latitude)
        result: the distance in kilometers.
        """

        lon1, lat1 = math.radians(dest_loc[0]), math.radians(dest_loc[1])
        lon0, lat0 = math.radians(cls.geo_loc[0]), math.radians(cls.geo_loc[1])
        
        delta_longitude = (lon1 - lon0)
        delta_latitude = (lat1 - lat0)
        
        # Haversine formula
        a = math.sin(delta_latitude / 2) ** 2 + math.cos(lat0) * math.cos(lat1) * math.sin(delta_longitude / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in KM.
        r = 6371
    
        return c * r

    def final_price(self):
        """Calculate the final price considering discount rate"""
        return self.price * (100 - self.discount_rate) / 100

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return self.name == other.name and self.price == other.price and self.number\
                 == other.number and self.company == other.company and self.country == other.country

    def __repr__(self):
        return f"item({self.name}, {self.price}, {self.number}, {self.country}, {self.company})"
