#Carlos Mejia
#SciFiLi //
#May 1, 2023

#################################### IMPORTS #########################################

#Import TKINTER to make the GUI buttons and create a grid to organize them

import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.filedialog as filedialog


#################################### CLASSES #########################################

#Create book class (title, author, check in status and priority number)
class Book:
    def __init__(self, title, author, checked_in, priority):
        self.title = title
        self.author = author
        self.checked_in = checked_in
        self.priority = priority
        self.left = None
        self.right = None

#defines a class called BookNode which represents a node in a binary search tree for storing books.
class BookNode:
    def __init__(self, book):
        self.book = book
        self.left_child = None
        self.right_child = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert_book(self, sbook):
        new_node = BookNode(book)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_book(new_node, self.root)

    def _insert_book(self, new_node, current_node):
        if new_node.book.title < current_node.book.title:
            if current_node.left_child is None:
                current_node.left_child = new_node
            else:
                self._insert_book(new_node, current_node.left_child)
        elif new_node.book.title > current_node.book.title:
            if current_node.right_child is None:
                current_node.right_child = new_node
            else:
                self._insert_book(new_node, current_node.right_child)
        else:
            current_node.book = new_node.book

    def search_by_author(self, author):
        books = []
        if self.root:
            self._search_by_author(self.root, author, books)
        if books:
            books = sorted(books, key=lambda node: node.book.title)
            books = [f"{book.book.title} by {book.book.author}, {'checked in' if book.book.checked_in else 'checked out'}, priority {book.book.priority}"
                     for book in books]
            result = "\n".join(books)
        else:
            result = f"No books by {author} found"
        return result

    def _search_by_author(self, node, author, books):
        if node is not None:
            self._search_by_author(node.left_child, author, books)
            if node.book.author == author:
                books.append(node.book)
            self._search_by_author(node.right_child, author, books)

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None
        
    def is_empty(self):
        return self.head is None
        
    def push(self, value):
        new_node = Node(value)
        # If queue is empty or new node's value is less than the head node's value
        # then insert new node at the beginning of the queue
        if self.is_empty() or new_node.value < self.head.value:
            new_node.next = self.head
            self.head = new_node
        else:
            # Find the position where the new node should be inserted based on its value
            curr_node = self.head
            while curr_node.next is not None and curr_node.next.value < new_node.value:
                curr_node = curr_node.next
            # Insert the new node at the found position
            new_node.next = curr_node.next
            curr_node.next = new_node
    
    def pop(self):
        if self.is_empty():
            return None
        value = self.head.value
        self.head = self.head.next
        return value
    
    def peek(self):
        if self.is_empty():
            return None
        return self.head.value

#Create library class (book, author, queue and title)
class Library:
    def __init__(self):
        self.books = []
        self.author_dict = {}
        self.priority_queue = []
        self.title_dict = {}
        self.root= None
        
    #read_books reads list of books and add them to library
    def read_books(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                title, author, checked_in, priority = line.strip().split(', ')
                #Transform check-in status to boolean as needed in instructions
                checked_in = bool(int(checked_in))
                #priority isconverted to integer
                priority = int(priority)
                #create book object with check in status and priority
                book = Book(title, author, checked_in, priority)
                self.books.append(book)
                if author not in self.author_dict:
                    self.author_dict[author] = []
                self.author_dict[author].append(book)
                #if book is checked in, it is added to priority queue
                if checked_in:
                    self.priority_queue.append(book)

                # Add the book to the title dictionary
                hash_value = hash(title)
                if hash_value not in self.title_dict:
                    self.title_dict[hash_value] = []
                self.title_dict[hash_value].append(book)
    
    def search_by_author(self, author):
        if author in self.author_dict:
            result = []
            for book in self.author_dict[author]:
                status = 'checked in' if book.checked_in else 'checked out'
                result.append(f"{book.title}, {status}, priority {book.priority}")
            return result
        else:
            return f"No books found for author {author}."
        
    #searches for a book by its title in a dictionary mapping titles to book objects and returns information about the book's status and priority.
    def search_by_title(self, title):
        hash_value = hash(title)
        if hash_value in self.title_dict:
            for book in self.title_dict[hash_value]:
                if book.title == title:
                    status = 'checked in' if book.checked_in else 'checked out'
                    return f'{title} by {book.author}, {status}, priority {book.priority}'
        return f'{title} not found'
    #checks out a book by its title, removing it from a priority queue if it's available, or returns an error message if it's already checked out or not found in the library's dictionary of books.
    def check_out_book(self, title):
        hash_value = hash(title)
        if hash_value in self.title_dict:
            for book in self.title_dict[hash_value]:
                if book.title == title and book.checked_in:
                    book.checked_in = False
                    self.priority_queue.remove(book)
                    return f'{title} checked out successfully'
            return f'{title} is already checked out'
        return f'{title} not found'
    # checks if a book is available in a library, and if it is checked out, it marks it as checked in and adds it to the priority queue.
    def check_in_book(self, title):
        hash_value = hash(title)
        if hash_value in self.title_dict:
            for book in self.title_dict[hash_value]:
                if book.title == title:
                    if not book.checked_in:
                        book.checked_in = True
                        self.priority_queue.append(book)
                        return f'{title} checked in successfully'
                    else:
                        return f'{title} is already checked in'
        return f'{title} not found'
    
     #saves list of books to a file
    def save_books_to_file(self, filename):
        books = sorted(self.books, key=lambda b: b.title)
        with open(filename, 'w') as f:
            for book in books:
                status = 'in' if book.checked_in else 'out'
                f.write(f'{book.title}, {book.author}, {status}, {book.priority}\n')
    #retreived checked in books and sort by priority number
    def rescue_books(self):
        rescued = sorted((book for book in self.priority_queue if book.checked_in), key=lambda b: b.priority)
        result = [f"{book.title} by {book.author}, priority {book.priority}" for book in rescued]
        return result



 
######################################### LIBRARY GUI ##########################################################


#Create GUI with buttons for user input
class LibraryGUI:
    def __init__(self, library):
        self.library = library
        self.window = tk.Tk()
        self.window.title('')
        #set title and font family and size
        title_label = tk.Label(self.window, text='SciFiLi-brary :)', font=('sans-serif', 80))
        #create grid to perfectly organize buttons
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        
        
        #button grid positions and commands assignment
        search_title_button = tk.Button(self.window, text='Search book by title', command=self.search_by_title)
        search_title_button.grid(row=1, column=0, padx=10, pady=0)

        search_author_button = tk.Button(self.window, text='Search book by author', command=self.search_by_author)
        search_author_button.grid(row=2, column=0, padx=10, pady=5)

        check_out_button = tk.Button(self.window, text='Check out book', command=self.check_out_book)
        check_out_button.grid(row=3, column=0, padx=10, pady=5)

        check_in_button = tk.Button(self.window, text='Check in book', command=self.check_in_book)
        check_in_button.grid(row=4, column=0, padx=10, pady=5)

        save_quit_button = tk.Button(self.window, text='Save and Quit', command=self.save_and_quit)
        save_quit_button.grid(row=2, column=1, padx=10, pady=5)

        rescue_books_button = tk.Button(self.window, text='Rescue books', command=self.rescue_books)
        rescue_books_button.grid(row=1, column=1, padx=10, pady=5)

        quit_button = tk.Button(self.window, text='Quit', command=self.Quit)
        quit_button.grid(row=3, column=1, padx=10, pady=5)
        
        secret_button = tk.Button(self.window, text='Secret', command=self.openFile)
        secret_button.grid(row=4, column=1, padx=10, pady=5)


######################################### GUI BUTTONS #####################################################
   
  #functions // commands for buttons. Ask for user input // prompt the string to the user 
    def search_by_title(self):
        title = tk.simpledialog.askstring('Search book by title', 'Please enter book title:')
        if title:
            result = self.library.search_by_title(title)
            tk.messagebox.showinfo('Search book by title', result)
    #button for author search
    def search_by_author(self):
        author = tk.simpledialog.askstring('Search book by author', 'Please enter name of author:')
        if author:
            result = self.library.search_by_author(author)
            tk.messagebox.showinfo('Search by author', result)
    #button that prompts book check out
    def check_out_book(self):
        title = tk.simpledialog.askstring('Check out book', 'Please enter book title:')
        if title:
            result = self.library.check_out_book(title)
            tk.messagebox.showinfo('Check out book', result)
    #button that prompts book check in
    def check_in_book(self):
        title = tk.simpledialog.askstring('Check in book', 'Please enter book title:')
        if title:
            self.library.check_in_book(title)
            tk.messagebox.showinfo('Check in book', f'{title} has been checked in successfully')

    #button that prompts the books to be saved (priority number)
    def rescue_books(self):
        result = self.library.rescue_books()
        if result:
            tk.messagebox.showinfo('Rescue books', '\n'.join(result))
        else:
            tk.messagebox.showinfo('Rescue books', 'No rescued books were found')
    #button that prompts a save file and quit option
    def save_and_quit(self):
        self.library.save_books_to_file('library.txt')
        self.window.destroy()
    #button that kills/exits program 
    def Quit(self):
        self.window.destroy()
    
    #button that opens the files (used for secret file)
    def openFile(self):
            filepath = filedialog.askopenfilename()
            file = open(filepath, 'r', encoding='utf-16')
            print(file.read())
            file.close()

#code only executes if script is being run
if __name__ == '__main__':
    #Create instance of library
    library = Library()
    library.read_books('books.txt')
    #create gui intansce with library argument
    gui = LibraryGUI(library)
    gui.window.mainloop()



################################### ANALYSIS #############################

#In my program I used three data structures: a hash table, a binary search tree, and a priority queue.
#I used a hash table to implement a dictionary that quickly maps book titles to their corresponding book objects, enabling me to find the books I need in constant time.
#I also used a binary search tree to keep track of all the books in the library, allowing me to easily add, remove, and iterate through them.
#Finally, I used a priority queue using a linked-list to organize the checked-in books by priority level, allowing me to quickly locate and check out the book with the highest priority
#These data structures solve the specific needs of the program and produce quick results
    
#Extra: You might need to extend the shell to read the "Secret file" completely
    
    

################################### SOURCES ##################################
    
#https://www.c-sharpcorner.com/blogs/create-menu-bar-in-python-gui-application --> Creating GUI Menu
#https://blog.boot.dev/computer-science/binary-search-tree-in-python/ ---> Binary Tree with Nodes
#https://www.geeksforgeeks.org/priority-queue-set-1-introduction/ -----> Priority Queue
#https://www.edureka.co/blog/hash-tables-and-hashmaps-in-python/#:~:text=Hash%20tables%20or%20has%20maps,and%20they%20can%20be%20changed.
    
    
    