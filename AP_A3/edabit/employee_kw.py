class Employee:
    """Employee class"""

    def __init__(self, fullname:str, **kwargs) -> None:
        """
        initializer of Employee class
        parameters: 
            fullname: fullname of the employee
            kwargs: other attributes
        """
        self.firstname, self.lastname = fullname.split()
        for key, value in kwargs.items():
            setattr(self, key, value)
