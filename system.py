import mysql.connector
import os
from termcolor import cprint
from datetime import datetime

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

# Connection details
db_host = "sql12.freemysqlhosting.net"
db_user = "sql12668515"
db_password = "a5NWN6g3dl"
db_name = "sql12668515"

# Connect to the database
try:
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
    )
    cursor = db.cursor()

    # Function definitions

    def create_tables():
        """Creates the BOOK and CUSTOMER tables if they don't exist."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BOOK (
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                book_name VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                price DECIMAL(10,2) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CUSTOMER (
                customer_id VARCHAR(10) PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                phone INT(10) NOT NULL,
                email VARCHAR(255),
                password VARCHAR(255),
                books_bought INT(50) NOT NULL DEFAULT 0
            );
        """)
        db.commit()

    def validate_input(text, min_length=1, max_length=255):
        """Validates user input for text fields."""
        while True:
            if not text:
                print("Please enter a valid value.")
                continue
            if len(text) < min_length or len(text) > max_length:
                print(f"Input must be between {min_length} and {max_length} characters.")
                continue
            break
        return text

    def validate_int(text):
        """Validates user input for integer fields."""
        while True:
            try:
                number = int(text)
                if number < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please enter a valid positive integer.")
                text = input("> ")
        return number

    def validate_phone(text):
        """Validates user input for phone numbers."""
        while True:
            if len(text) != 10 or not text.isdigit():
                print("Please enter a valid 10-digit phone number.")
                text = input("> ")
            else:
                break
        return text

    def book_entry():
        """Adds a new book to the database."""
        print("Enter the book name: ")
        book_name = validate_input(input("> "))
        print("Enter the author of the book: ")
        author = validate_input(input("> "))

        quantity = validate_int(input("Quantity: "))
        price = float(input("Price: "))

        cursor.execute("""
            INSERT INTO BOOK (book_name, author, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (book_name, author, quantity, price))
        db.commit()
        print("Book added successfully!")

    def book_search():
        """Searches for books based on user input."""
        search_term = input("Enter book title or author name: ")
        cursor.execute("""
            SELECT * FROM BOOK
            WHERE book_name LIKE %s OR author LIKE %s
        """, ("%" + search_term + "%", "%" + search_term + "%"))
        results = cursor.fetchall()

        if results:
            print("Found books:")
            for row in results:
                print(f"- {row[1]} by {row[2]} ({row[4]})")
        else:
            print("No books found matching your search.")

    
    def customer_register():
        """Registers a new customer."""
        customer_name = validate_input(input("Please enter your name:"))
        phone = validate_phone(input("Phone: "))
        email = validate_input(input("Email (optional): "))
        password = validate_input(input("enter your password: "))
        re_password = validate_input(input("re-enter your password: "))
        if password == re_password:
            now = datetime.now()
            
            timestamp_str = str(now.timestamp())
            
            # Generate unique customer ID based on phone number
            customer_id = f"CUST{timestamp_str[-4:]}"

            cursor.execute("""
                INSERT INTO CUSTOMER (customer_id, customer_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """, (customer_id, customer_name, phone, email))
            db.commit()
            print(f"Customer '{customer_name}' registered successfully with ID: {customer_id}")
        else:
            print("Password doesn't match")
            customer_register()

    def customer_login(phone):
        """Checks if a customer exists based on phone number and returns their details."""
        cursor.execute("""
            SELECT * FROM CUSTOMER
            WHERE phone = %s
        """, (phone,))
        result = cursor.fetchone()
        return result if result else None

    def customer_profile(customer_details):
        """Displays customer information and purchase history."""
        customer_id, name, phone, email, books_bought = customer_details
        print(f"Customer ID: {customer_id}")
        print(f"Name: {name}")
        print(f"Phone: {phone}")
        print(f"Email: {email if email else 'N/A'}")
        print(f"Books Bought: {books_bought}")

        # Show purchase history if available
        if books_bought > 0:
            cursor.execute("""
                SELECT book_name, author, price
                FROM BOOK
                INNER JOIN CUSTOMER_BOOK
                ON BOOK.book_id = CUSTOMER_BOOK.book_id
                WHERE CUSTOMER_BOOK.customer_id = %s
            """, (customer_id,))
            history = cursor.fetchall()
            print("\nPurchase History:")
            for book in history:
                print(f"- {book[0]} by {book[1]} ({book[2]})")

    def buy_book(customer_id):
        """Allows a customer to purchase a book and update their purchase history."""
        book_search()  # Display available books

        book_id = validate_int(input("Enter book ID to purchase: "))
        cursor.execute("""
            SELECT * FROM BOOK
            WHERE book_id = %s
        """, (book_id,))
        book_details = cursor.fetchone()

        if book_details:
            book_name, author, quantity, price = book_details
            if quantity > 0:
                cursor.execute("""
                    UPDATE BOOK
                    SET quantity = quantity - 1
                    WHERE book_id = %s
                """, (book_id,))
                cursor.execute("""
                    INSERT INTO CUSTOMER_BOOK (customer_id, book_id)
                    VALUES (%s, %s)
                """, (customer_id, book_id))
                db.commit()
                print(f"Successfully purchased '{book_name}' by {author}!")
                cursor.execute("""
                    UPDATE CUSTOMER
                    SET books_bought = books_bought + 1
                    WHERE customer_id = %s
                """, (customer_id,))
                db.commit()
            else:
                print(f"Sorry, '{book_name}' is currently out of stock.")
        else:
            print("Invalid book ID entered.")

    # Main program loop

    create_tables()  # Create tables if needed

    while True:
        cprint("\nWelcome to our Book Shop Management System!", "light_cyan", attrs=["bold"])
        print("1. Login as Admin")
        print("2. Login as Customer")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Admin login
            print("Enter Admin PIN: ")
            pin = input("> ")
            if pin == "1234":
                print("Logged in as Admin.")
                # Admin menu
                while True:
                    print("\nAdmin Options:")
                    print("1. Add Book")
                    print("2. Search Books")
                    print("3. View Customer List")
                    print("4. Exit Admin")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        book_entry()
                    elif admin_choice == "2":
                        book_search()
                    elif admin_choice == "3":
                        cursor.execute("""
                            SELECT * FROM CUSTOMER
                        """)
                        customers = cursor.fetchall()
                        print("\nCustomers:")
                        for customer in customers:
                            print(f"- {customer[1]} ({customer[2]})")
                    
                    elif admin_choice == "4":
                        break  # Exit admin menu

                    else:
                        print("Invalid choice. Please try again.")

        elif choice == "2":
            # Customer login
            
            print("\nCustomer Options:")
            print("1. Register")
            print("2. Login")
            print("3. Exit Customer")

            customer_choice = input("Enter your choice: ")
            customer_details = None

            if customer_choice == "1":
                customer_register()
            elif customer_choice == "2":
                print("Enter phone number to login: ")
                phone = validate_phone(input("> "))
                customer_details = customer_login(phone)
            elif customer_choice == "3":
                        break  # Exit admin menu

            else:
                print("Invalid choice. Please try again.")
                        
            

            if customer_details:
                print(f"Welcome back, {customer_details[1]}!")
                # Customer menu
                while True:
                    print("\nCustomer Options:")
                    print("1. View Profile")
                    print("2. Search Books")
                    print("3. Buy Book")
                    print("4. Logout")

                    customer_choice = input("Enter your choice: ")

                    if customer_choice == "1":
                        customer_profile(customer_details)
                    elif customer_choice == "2":
                        book_search()
                    elif customer_choice == "3":
                        buy_book(customer_details[0])
                    elif customer_choice == "4":
                        break  # Logout

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Customer not found. Please register if you're new.")

        else:
            # Exit program
            print("Thank you for using our Book Shop Management System!")
            break

finally:
    # Close database connection
    db.close()


