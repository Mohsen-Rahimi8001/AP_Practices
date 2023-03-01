class Employee:
    """Employee class"""

    def __init__(self, firstname:str, lastname:str) -> None:
        """
        initializer of the Employee class
        parameters: 
            firstname: firstname of the employee
            lastname: lastname of the employee
        """
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = self.firstname + " " + self.lastname
        self.email = "%s.%s@company.com" % (self.firstname.lower(), self.lastname.lower())