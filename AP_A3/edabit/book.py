class Book:
    """Book class"""

    def __init__(self, title:str, author:str) -> None:
        """
        initializer of Book class
        parameters:
            title: title of the book
            author: author of the book
        """
        self.title = title
        self.author = author
		
    def get_author(self) -> str:
        """author attribute getter"""
        return "Author: %s" % self.author
		
    def get_title(self) -> str:
        """title attribute getter"""
        return "Title: %s" % self.title

PP = Book("Pride and Prejudice", "Jane Austen")
H = Book("Hamlet", "William Shakespeare")
WP = Book("War and Peace", "Leo Tolstoy")
