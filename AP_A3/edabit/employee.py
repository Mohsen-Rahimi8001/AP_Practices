class Employee:
    """Employee class"""

    def __init__(self, firstname:str, lastname:str, salary:int) -> None:
        """
        initializer of the Employee class
        parameters: 
            firstname: firstname of the employee
            lastname: lastname of the employee
            salary: salary of the employee
        """
        self.firstname = firstname
        self.lastname = lastname
        self.salary = salary
	
    @staticmethod
    def from_string(string:str) -> "Employee":
        """
        creates a new Employee
        string: seperated by '-' as follows: firstname-lastname-salary
        """
        firstname, lastname, salary = string.split('-')
        return Employee(firstname, lastname, int(salary))
