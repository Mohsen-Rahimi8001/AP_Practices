class LibraryMember:
    """LibraryMember class"""

    def __init__(self, id:str, name:str) -> None:
        """
        initilizer of the LibraryMember class
        parameters: 
            id: id of the member
            name: name of the member
        """
        self.name = name
        self.id = id
        self.bookList = []

    def find_book(self, id:str, default=None):
        """finds the book by its id in self.bookList"""
        for book in self.bookList:
            if book.id == id:
                return book
        else:
            return default

    def del_book(self, id:str) -> None:
        """deletes the book by its id in self.bookList"""
        for i, book in enumerate(self.bookList):
            if book.id == id:
                self.bookList.pop(i)
