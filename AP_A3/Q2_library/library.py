from book import Book
from member import LibraryMember

class Library:
    books:dict[Book, int] = {}
    members:list[LibraryMember] = []

    @classmethod
    def addMember(cls, id:str, name:str) -> None:
        """add a new member to Library.members"""
        cls.members.append(LibraryMember(id, name))
    
    @classmethod
    def addBook(cls, id:str, name:str, count:int) -> None:
        """add books to Library.books in the number of count"""
        book = cls.find_book(id) # book key of dictionary
        if book:
            cls.books[book] += count
        else:
            cls.books[Book(id, name)] = count

    @classmethod
    def find_book(cls, id:str, default=None):
        """finds a book by its id in Library.books"""
        for book in cls.books:
            if book.id == id:
                return book
        else:
            return default

    @classmethod
    def find_member(cls, id:str, default=None):
        """finds a member by its id in Library.members"""
        for mem in cls.members:
            if mem.id == id:
                return mem
        else:
            return default
    
    @classmethod
    def get(cls, member_id:str, book_id:str) -> None:
        """get member_id the book book_id if it exists and 
        member_id books are not reached to maximum limit"""
        member = cls.find_member(member_id)
        book = cls.find_book(book_id)
        
        if member and book:
            if len(member.bookList) >= 5:
                print(f"MaxReached : {member.name} {member_id}")
            elif cls.books[book] == 0:
                print(f"NotAvailable : {book.name} {book_id}")
            else:
                member.bookList.append(book)
                cls.books[book] -= 1
        else:
            print(f"member {member_id} or book {book_id} not found.")

    @classmethod
    def return_book(cls, member_id:str, book_id:str) -> None:
        """Return the book from member_id to Library.books"""
        member = cls.find_member(member_id)
        book = member.find_book(book_id)
        
        if member and book:
            member.del_book(book_id)
            cls.books[book] += 1
    
    @classmethod
    def memberState(cls) -> None:
        """prints the members and thier books in a special format."""
        print("----------------------------------------------------------")
        
        for member in cls.members:
            print(f"{member.name} {member.id}")
            for book in member.bookList:
                print(f"\t- {book.name} {book.id}")
        
        print("----------------------------------------------------------")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self
