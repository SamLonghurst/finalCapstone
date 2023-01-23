from logging import exception
import sqlite3
db = sqlite3.connect('bookstore_db')
cursor = db.cursor()

# Database Creation/Open
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookstore_db(id INTEGER PRIMARY KEY, title TEXT,
                   	author TEXT, qty INTEGER)
''')

# Database record entry
books = [(3001,'A Tale of Two Cities','Charles Dickens',30),
        (3002,"Harry Potter and the Philospher's Stone",'C.S.Lewis',25),
        (3004,'The Lord of the Rings','J.R.R Tolkien',37),
        (3005,'Alice in Wonderland','Lewis Carrol',12)]

cursor.executemany(''' INSERT OR IGNORE INTO bookstore_db(id, title, author, qty) VALUES(?,?,?,?)''',books)
db.commit()

# Book Class
class Book(object):

    def __init__(self,id,title,author,qty):
        self.id = id
        self.title = title
        self.author = author
        self.qty = qty

# == ADD NEW BOOKS ==

def add_book():

    while True:
        try:
            # Book ID
            while True:

                try:           
                    book_id = int(input("Enter the id of this book: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            #print(book_id)

            # Book Title
            book_title = input("Enter the Book's Title: ")

            # Book Author
            book_author = input("Enter the Book's Author: ")

            # Book QTY input with error if not INTEGER
            while True:

                try:           
                    book_qty = int(input("Enter the Quantity of this book: "))
                    break
                except ValueError:
                    print("Please Enter an integer")
        
            cursor.execute(''' INSERT INTO bookstore_db(id, title, author, qty) VALUES(?,?,?,?)''',
                        (book_id,book_title,book_author,book_qty))
            db.commit()

            # User Feedback - successfully added
            cursor.execute('''SELECT title FROM bookstore_db WHERE title = ?''', (book_title,))
            new_book = cursor.fetchone()
            print(f"New book {new_book} successfully added")
            
            break
            
        except sqlite3.IntegrityError:
            print("This ID is already in use please re-enter the books details")
            

# == UPDATE BOOK INFORMATION ==

def update_book():

    # Book ID input with error if not INTEGER
    while True:

        try:           
            book_id = int(input("Enter the ID for the book you would like to update: "))
            break
        except ValueError:
            print("Please Enter an integer")

    # Detail user would like to update
    book_detail_to_change = input('''Enter the information type you would like to change:
    Title
    Author
    QTY
    ''').lower()

    # Check if qty or id, if yes ,then ensure user enter an Integer
    if book_detail_to_change in ['title','author','qty']:

        if book_detail_to_change == 'qty':

            while True:

                try:           
                    change_to = int(input(f"Enter the new {book_detail_to_change} for the book: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            cursor.execute('''UPDATE bookstore_db SET qty = ? WHERE id = ?''',(change_to,book_id))
            db.commit()

        elif book_detail_to_change == 'title':

            change_to = input(f"Enter the new {book_detail_to_change} for the book: ")

            cursor.execute('''UPDATE bookstore_db SET title = ? WHERE id = ?''',(change_to,book_id))
            db.commit()

        elif book_detail_to_change == 'author':

            change_to = input(f"Enter the new {book_detail_to_change} for the book: ")

            cursor.execute('''UPDATE bookstore_db SET author = ? WHERE id = ?''',(change_to,book_id))
            db.commit()


    # User Feedback - successfully updated
    cursor.execute('''SELECT id, title, author, qty FROM bookstore_db WHERE id = ?''', (book_id,))
    updated_book = cursor.fetchone()
    print(f"{updated_book} successfully updated")


# == DELETE BOOKS FROM THE DATABASE ==

def delete_book():

    # Book ID input with error if not INTEGER
    while True:

        try:           
            book_id = int(input("Enter the ID for the book you would like to update: "))
            break
        except ValueError:
            print("Please Enter an integer")

    # Delete book from database
    cursor.execute('''DELETE FROM bookstore_db WHERE id = ?''',(book_id,))
    db.commit()

    # User Feedback - successfully deleted
    print(f"Book successfully deleted")

# == SEARCH THE DATABASE ==

def search_for_book():

    # Choose what to search by
    search_book_by = input('''How would you like to search for the book by:
        ID
        Title
        Author
        QTY
        ''').lower()

    # Enter search for ID
    if search_book_by == 'id':

        # Book ID input with error if not INTEGER
        while True:

            try:           
                book_id = int(input("Enter the ID for the book you would search for: "))
                break
            except ValueError:
                print("Please Enter an integer")

        # Search and print for book via ID
        cursor.execute('''SELECT title, author, qty FROM bookstore_db WHERE id = ?''', (book_id,))
        searched_book = cursor.fetchone()
        print(searched_book)

    # Enter search for title or author:
    elif search_book_by == 'title':

        search_entry = input(f"Enter the {search_book_by} to search for: ")

        # Search and print for book via ID
        cursor.execute('''SELECT title, author, qty FROM bookstore_db WHERE title = ?''', (search_entry,))
        searched_book = cursor.fetchone()
        print(searched_book)

    # Enter search for title or author:
    elif search_book_by == 'author':

        search_entry = input(f"Enter the {search_book_by} to search for: ")

        # Search and print for book via ID
        cursor.execute('''SELECT title, author, qty FROM bookstore_db WHERE author = ?''', (search_entry,))
        searched_book = cursor.fetchone()
        print(searched_book)

    # Enter search for QTY
    elif search_book_by == 'qty':

        filter_qty_results = input('''How would you like to filter the qty:
        > = More than
        < = Less than
        = = equals
        b = between two numbers
        ''')

        #if equals 
        if filter_qty_results == '=':

            # Book QTY input with error if not INTEGER
            while True:

                try:           
                    qty_1 = int(input("Enter the qty: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            cursor.execute('''SELECT id, title, author, qty FROM bookstore_db WHERE qty = ?''', (qty_1,))
            searched_book = cursor.fetchall()
            print(searched_book)

        # if less than 
        elif filter_qty_results == '<':

            # Book QTY input with error if not INTEGER
            while True:

                try:           
                    qty_1 = int(input("Enter the qty: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            cursor.execute('''SELECT id, title, author, qty FROM bookstore_db WHERE qty < ?''', (qty_1,))
            searched_book = cursor.fetchall()
            print(searched_book)

        # if more than
        elif filter_qty_results == '>':

            # Book QTY input with error if not INTEGER
            while True:

                try:           
                    qty_1 = int(input("Enter the qty: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            cursor.execute('''SELECT id, title, author, qty FROM bookstore_db WHERE qty > ?''', (qty_1,))
            searched_book = cursor.fetchall()
            print(searched_book)

        # if between two numbers
        elif filter_qty_results == 'b':

            # Book QTY_1 input with error if not INTEGER
            while True:

                try:           
                    qty_1 = int(input("Enter the qty: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            # Book QTY_2 input with error if not INTEGER
            while True:

                try:           
                    qty_2 = int(input("Enter the qty: "))
                    break
                except ValueError:
                    print("Please Enter an integer")

            cursor.execute('''SELECT id, title, author, qty FROM bookstore_db WHERE qty BETWEEN ? AND ?''', (qty_1,qty_2))
            searched_book = cursor.fetchall()
            print(searched_book)
    

# ===== Main Menu =====
while True:

    main_menu = input('''Choose from the menu
    a = Add a new book
    u = Update a books details
    d = Delete a book
    s = Search for a book
    e = exit
    : ''').lower()

    if main_menu == "a":

        add_book()

    elif main_menu == "u":

        update_book()

    elif main_menu == "d":

        delete_book()
    
    elif main_menu == "s":

        search_for_book()

    elif main_menu == "e":

        db.close
        exit()

    else:

        print("This is not an option")