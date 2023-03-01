import unittest
from library import Library
from book import Book
from member import LibraryMember
from unittest.mock import patch


class TestBook(unittest.TestCase):

    def setUp(self):
        self.b1 = Book('1', 'book1')
        self.b5 = Book('5', 'book5')
        Library.books = {self.b1:1, self.b5:5}
        self.m1 = LibraryMember('1', "mohsen")
        self.m2 = LibraryMember('2', "mohammad")
        Library.members = [self.m1, self.m2]

    @patch("library.Book")
    def test_addBook(self, mocked_Book):
        books = Library.books.copy()
        with Library() as lib:
            book = Book('123', 'book1')
            mocked_Book.return_value = book
            try:
                books[book] += 5
            except KeyError:
                books[book] = 5
            lib.addBook('123', 'book1', 5)

            book = Book('456', 'book2')
            mocked_Book.return_value = book
            try:
                books[book] += 5
            except KeyError:
                books[book] = 5

            lib.addBook('456', 'book2', 5)
            self.assertDictEqual(lib.books, books)

    @patch("library.LibraryMember")
    def test_addMember(self, mocked_LibraryMember):
        members = Library.members.copy()
        with Library() as lib:
            mem = LibraryMember('1', 'mohsen')
            mocked_LibraryMember.return_value = mem
            members.append(mem)
            lib.addMember('1', "mohsen")
            
            mem = LibraryMember('2', 'mahdi')
            mocked_LibraryMember.return_value = mem
            members.append(mem)
            lib.addMember('2', "mahdi")

            self.assertListEqual(lib.members, members)

    def test_get(self):
        Library.get('1', '1')
        Library.get('1', '1')

        self.assertListEqual(self.m1.bookList, [self.b1])
        self.assertDictEqual(Library.books, {self.b1:0, self.b5:5})

        Library.get('1', '5')
        Library.get('1', '5')
        Library.get('1', '5')
        Library.get('1', '5')
        
        Library.get('1', '5')

        self.assertListEqual(self.m1.bookList, [self.b1, self.b5, self.b5, self.b5, self.b5])
        self.assertDictEqual(Library.books, {self.b1:0, self.b5:1})
        
    def test_return_book(self):
        Library.get('1', '1')
        Library.get('2', '5')

        self.assertListEqual(self.m1.bookList, [self.b1])
        self.assertListEqual(self.m2.bookList, [self.b5])
        self.assertDictEqual(Library.books, {self.b1:0, self.b5:4})

        Library.return_book('1', '2')
        Library.return_book('2', '5')

        self.assertListEqual(self.m1.bookList, [self.b1])
        self.assertListEqual(self.m2.bookList, [])
        self.assertDictEqual(Library.books, {self.b1:0, self.b5:5})

if __name__ == "__main__":
    unittest.main(verbosity=2)
