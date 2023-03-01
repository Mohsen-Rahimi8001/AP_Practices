class Person:
    """Person class"""

    def __init__(self, name:str, age:int) -> None:
        """
        initializer of Person class
        parameters: 
            name: name of the person.
            age: age of the person.
        """
        self.name = name
        self.age = age

    def compare_age(self, other:"Person") -> None:
        """compares my age with other age"""
        assert isinstance(other, Person)
	
        if self.age > other.age:
            return "%s is younger than me." % other.name
        elif self.age < other.age:
            return "%s is older than me." % other.name
        else:
            return "%s is the same age as me." % other.name
