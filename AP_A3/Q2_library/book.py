class Book:
    """Book class"""
    def __init__(self, id:str, name:str) -> None:
        """
        initializer of the Book class
        parameters:
            id: the book id
            name: the name of the book
        """
        self.id = id
        self.name = name
