"""
Campus Library Manager - Data Structures Project in Python
==========================================================

Project theme:
    A small library system where users can add books, search books, borrow books,
    return books, undo the latest action, and view waiting lists.

Data structures demonstrated:
    1. Linked List       - stores all books in insertion order
    2. Binary Search Tree - searches books quickly by book ID
    3. Hash Table        - stores users by user ID
    4. Queue             - stores waiting list for borrowed books
    5. Stack             - stores undo history

How to run:
    python3 library_project.py

Description:
    This project demonstrates how multiple data structures can work together in
    one real application. Each structure has a clear purpose: the linked list
    preserves order, the BST allows efficient book lookup by ID, the hash table
    provides fast user lookup, the queue models first-come-first-served waiting
    lists, and the stack supports undo functionality.
"""


# ============================================================
# Book Class
# ============================================================

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowed_by = None
        self.waiting_queue = Queue()

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"ID: {self.book_id} | Title: {self.title} | Author: {self.author} | Status: {status}"


# ============================================================
# User Class
# ============================================================

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"User ID: {self.user_id} | Name: {self.name} | Borrowed Books: {self.borrowed_books}"


# ============================================================
# Queue Implementation
# First In, First Out
# Used for book waiting lists
# ============================================================

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        if self.is_empty():
            return "No one is waiting."
        return " -> ".join(str(item) for item in self.items)


# ============================================================
# Stack Implementation
# Last In, First Out
# Used for undo history
# ============================================================

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


# ============================================================
# Linked List Implementation
# Used to store all books in the order they were added
# ============================================================

class LinkedListNode:
    def __init__(self, book):
        self.book = book
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, book):
        new_node = LinkedListNode(book)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def remove(self, book_id):
        if self.head is None:
            return False

        if self.head.book.book_id == book_id:
            self.head = self.head.next
            return True

        current = self.head
        while current.next is not None:
            if current.next.book.book_id == book_id:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def display(self):
        if self.head is None:
            print("No books in the library.")
            return

        current = self.head
        while current is not None:
            print(current.book)
            current = current.next


# ============================================================
# Binary Search Tree Implementation
# Used to search books by book ID
# ============================================================

class BSTNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, book):
        self.root = self._insert_recursive(self.root, book)

    def _insert_recursive(self, node, book):
        if node is None:
            return BSTNode(book)

        if book.book_id < node.book.book_id:
            node.left = self._insert_recursive(node.left, book)
        elif book.book_id > node.book.book_id:
            node.right = self._insert_recursive(node.right, book)

        return node

    def search(self, book_id):
        return self._search_recursive(self.root, book_id)

    def _search_recursive(self, node, book_id):
        if node is None:
            return None

        if book_id == node.book.book_id:
            return node.book
        elif book_id < node.book.book_id:
            return self._search_recursive(node.left, book_id)
        else:
            return self._search_recursive(node.right, book_id)

    def delete(self, book_id):
        self.root = self._delete_recursive(self.root, book_id)

    def _delete_recursive(self, node, book_id):
        if node is None:
            return None

        if book_id < node.book.book_id:
            node.left = self._delete_recursive(node.left, book_id)
        elif book_id > node.book.book_id:
            node.right = self._delete_recursive(node.right, book_id)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            smallest_book = self._find_min(node.right)
            node.book = smallest_book
            node.right = self._delete_recursive(node.right, smallest_book.book_id)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.book


# ============================================================
# Hash Table Implementation
# Used to store and search users by user ID
# ============================================================

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash(key)

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return

        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash(key)

        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]

        return None

    def display(self):
        empty = True

        for bucket in self.table:
            for pair in bucket:
                print(pair[1])
                empty = False

        if empty:
            print("No users registered.")


# ============================================================
# Library System
# Connects all data structures together
# ============================================================

class LibrarySystem:
    def __init__(self):
        self.books_list = LinkedList()
        self.books_tree = BinarySearchTree()
        self.users = HashTable()
        self.undo_stack = Stack()

    def add_book(self, book_id, title, author):
        existing_book = self.books_tree.search(book_id)

        if existing_book is not None:
            print("A book with this ID already exists.")
            return

        book = Book(book_id, title, author)
        self.books_list.append(book)
        self.books_tree.insert(book)
        self.undo_stack.push(("add_book", book))

        print("Book added successfully.")

    def remove_book(self, book_id):
        book = self.books_tree.search(book_id)

        if book is None:
            print("Book not found.")
            return

        if book.is_borrowed:
            print("Cannot remove this book because it is currently borrowed.")
            return

        self.books_list.remove(book_id)
        self.books_tree.delete(book_id)
        self.undo_stack.push(("remove_book", book))

        print("Book removed successfully.")

    def register_user(self, user_id, name):
        existing_user = self.users.get(user_id)

        if existing_user is not None:
            print("A user with this ID already exists.")
            return

        user = User(user_id, name)
        self.users.insert(user_id, user)
        self.undo_stack.push(("register_user", user))

        print("User registered successfully.")

    def search_book(self, book_id):
        book = self.books_tree.search(book_id)

        if book is None:
            print("Book not found.")
        else:
            print(book)

    def borrow_book(self, user_id, book_id):
        user = self.users.get(user_id)
        book = self.books_tree.search(book_id)

        if user is None:
            print("User not found.")
            return

        if book is None:
            print("Book not found.")
            return

        if book.is_borrowed:
            book.waiting_queue.enqueue(user_id)
            print("Book is already borrowed. User added to waiting list.")
            return

        book.is_borrowed = True
        book.borrowed_by = user_id
        user.borrowed_books.append(book_id)
        self.undo_stack.push(("borrow_book", user_id, book_id))

        print("Book borrowed successfully.")

    def return_book(self, user_id, book_id):
        user = self.users.get(user_id)
        book = self.books_tree.search(book_id)

        if user is None:
            print("User not found.")
            return

        if book is None:
            print("Book not found.")
            return

        if book.borrowed_by != user_id:
            print("This user did not borrow this book.")
            return

        book.is_borrowed = False
        book.borrowed_by = None

        if book_id in user.borrowed_books:
            user.borrowed_books.remove(book_id)

        self.undo_stack.push(("return_book", user_id, book_id))

        print("Book returned successfully.")

        if not book.waiting_queue.is_empty():
            next_user_id = book.waiting_queue.dequeue()
            print(f"Next user in waiting list is User ID {next_user_id}.")

    def view_waiting_list(self, book_id):
        book = self.books_tree.search(book_id)

        if book is None:
            print("Book not found.")
            return

        print(f"Waiting list for '{book.title}':")
        print(book.waiting_queue.display())

    def display_books(self):
        self.books_list.display()

    def display_users(self):
        self.users.display()

    def undo(self):
        last_action = self.undo_stack.pop()

        if last_action is None:
            print("Nothing to undo.")
            return

        action_type = last_action[0]

        if action_type == "add_book":
            book = last_action[1]
            self.books_list.remove(book.book_id)
            self.books_tree.delete(book.book_id)
            print("Undo complete: added book removed.")

        elif action_type == "remove_book":
            book = last_action[1]
            self.books_list.append(book)
            self.books_tree.insert(book)
            print("Undo complete: removed book restored.")

        elif action_type == "borrow_book":
            user_id = last_action[1]
            book_id = last_action[2]
            user = self.users.get(user_id)
            book = self.books_tree.search(book_id)

            if user is not None and book is not None:
                book.is_borrowed = False
                book.borrowed_by = None
                if book_id in user.borrowed_books:
                    user.borrowed_books.remove(book_id)
                print("Undo complete: borrowed book returned.")

        elif action_type == "return_book":
            user_id = last_action[1]
            book_id = last_action[2]
            user = self.users.get(user_id)
            book = self.books_tree.search(book_id)

            if user is not None and book is not None:
                book.is_borrowed = True
                book.borrowed_by = user_id
                user.borrowed_books.append(book_id)
                print("Undo complete: returned book borrowed again.")

        elif action_type == "register_user":
            print("Undo for user registration is not supported in this simple version.")


# ============================================================
# Helper Functions for User Input
# ============================================================

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def print_menu():
    print("\n========== Campus Library Manager ==========")
    print("1. Add book")
    print("2. Remove book")
    print("3. Register user")
    print("4. Search book")
    print("5. Borrow book")
    print("6. Return book")
    print("7. View all books")
    print("8. View all users")
    print("9. View waiting list for a book")
    print("10. Undo last action")
    print("0. Exit")
    print("===========================================")


# ============================================================
# Main Program
# ============================================================

def main():
    library = LibrarySystem()

    # Sample starting data so the project does not feel empty
    library.add_book(101, "Introduction to Python", "John Smith")
    library.add_book(205, "Data Structures Made Easy", "Narasimha Karumanchi")
    library.add_book(150, "Clean Code", "Robert C. Martin")
    library.register_user(1, "Kavya")
    library.register_user(2, "Alex")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            book_id = get_integer("Enter book ID: ")
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            library.add_book(book_id, title, author)

        elif choice == "2":
            book_id = get_integer("Enter book ID to remove: ")
            library.remove_book(book_id)

        elif choice == "3":
            user_id = get_integer("Enter user ID: ")
            name = input("Enter user name: ").strip()
            library.register_user(user_id, name)

        elif choice == "4":
            book_id = get_integer("Enter book ID to search: ")
            library.search_book(book_id)

        elif choice == "5":
            user_id = get_integer("Enter user ID: ")
            book_id = get_integer("Enter book ID to borrow: ")
            library.borrow_book(user_id, book_id)

        elif choice == "6":
            user_id = get_integer("Enter user ID: ")
            book_id = get_integer("Enter book ID to return: ")
            library.return_book(user_id, book_id)

        elif choice == "7":
            library.display_books()

        elif choice == "8":
            library.display_users()

        elif choice == "9":
            book_id = get_integer("Enter book ID: ")
            library.view_waiting_list(book_id)

        elif choice == "10":
            library.undo()

        elif choice == "0":
            print("Thank you for using Campus Library Manager. Goodbye!")
            break

        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()
