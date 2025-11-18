import mysql.connector
from datetime import date

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",     
        password="7448582747",     
        database="library_db"
    )

def add_book():
    db = connect_db()
    cursor = db.cursor()

    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")

    query = "INSERT INTO books (book_id, title, author, available) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (book_id, title, author, 1))

    db.commit()
    db.close()
    print(" Book Added Successfully!\n")


def view_books():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    print("\n----- Book List -----")
    for b in books:
        status = "Available" if b[3] == 1 else "Issued"
        print(f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Status: {status}")

    print()
    db.close()


def issue_book():
    db = connect_db()
    cursor = db.cursor()

    book_id = int(input("Enter Book ID to Issue: "))
    borrower = input("Enter Borrower Name: ")

    # Check availability
    cursor.execute("SELECT available FROM books WHERE book_id=%s", (book_id,))
    result = cursor.fetchone()

    if not result:
        print(" Book ID not found.\n")
        return

    if result[0] == 0:
        print(" Book already issued.\n")
        return

    # Issue the book
    query = "INSERT INTO issued_books (book_id, borrower, issue_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, borrower, date.today()))

    cursor.execute("UPDATE books SET available=0 WHERE book_id=%s", (book_id,))

    db.commit()
    db.close()
    print(" Book Issued Successfully!\n")


def return_book():
    db = connect_db()
    cursor = db.cursor()

    book_id = int(input("Enter Book ID to Return: "))

    cursor.execute("SELECT available FROM books WHERE book_id=%s", (book_id,))
    result = cursor.fetchone()

    if not result:
        print(" Book ID not found.\n")
        return

    if result[0] == 1:
        print(" Book was not issued.\n")
        return

    cursor.execute(
        "UPDATE issued_books SET return_date=%s WHERE book_id=%s AND return_date IS NULL",
        (date.today(), book_id)
    )

    cursor.execute("UPDATE books SET available=1 WHERE book_id=%s", (book_id,))

    db.commit()
    db.close()
    print(" Book Returned Successfully!\n")

def main():
    while True:
        print("===== Library Management System =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            print("Exiting system...")
            break
        else:
            print("Invalid choice! Try again.\n")


if __name__ == "__main__":
    main()
