import mysql.connector
import os
from termcolor import cprint

os.system("cls")

# connection
db = mysql.connector.connect(
    host='sql12.freemysqlhosting.net',
    user='sql12668515',
    password='a5NWN6g3dl',
    database='sql12668515',
)

cursor=db.cursor()

def Book():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS BOOK (
        BOOK_ID     INT,
        BOOK_NAME   VARCHAR(255),
        Author      VARCHAR(255),
        Quantity    INT,
        PRICE       DECIMAL(10,2)
        );
        
        """, 
        multi=True
    )

def entry():
    print("Enter Book details--")
    book_name=input("Name: ") 
    book_author=input("Author Name:")
    book_quantity=input("Quantity:")
    book_price=float(input("M.R.P: ₹"))

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS BOOK (
        BOOK_ID     INT,
        BOOK_NAME   VARCHAR(255),
        Author      VARCHAR(255),
        Quantity    INT,
        PRICE       DECIMAL(10,2)
        );
        INSERT INTO BOOK (BOOK_ID,BOOK_NAME, AUTHOR, QUANTITY, PRICE) 
        VALUES(NOW(),%s, %s, %s, %s)

        """,
        
        (book_name, book_author, book_quantity, book_price),multi=True
    )
    # Commit the changes to the database
    db.commit()

    print("Book details inserted successfully!")

def enquiry():
    cursor.execute(
        """
        SELECT * FROM BOOK;
        """
    )


def Customer_Table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CUSTOMER (
        CUSTOMER_ID     VARCHAR(10)     PRIMARY KEY,
        CUSTOMER_NAME   VARCHAR(255),
        PHONE           INT(10),
        EMAIL           VARCHAR(255),
        BOOKS_BOUGHT    INT(50)
        );

        DELIMITER //
        CREATE TRIGGER before_insert_CUSTOMER
        BEFORE INSERT ON CUSTOMER
        FOR EACH ROW
        BEGIN
            SET NEW.CUSTOMER_ID = CONCAT('CUSTOMER', LPAD(CAST((SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = 'CUSTOMER') AS CHAR), 3, '0'));
        END;
        //
        DELIMITER ;
        """, 
        multi=True
    )

def customer_search():
    customer_phone=int(input("Enter 10 digit phone number:"))
    cursor.execute(
        """
        SELECT * FROM CUSTOMER
        WHERE PHONE=(%s);

    """,(customer_phone)
    )

def Book_enquiry():
    cursor.execute(
        """
        SELECT * FROM BOOK;
        SHOW
    """
    )

def welcome():
    cprint("\nWelcome to our BOOK SHOP MANAGEMENT SYSTEM!\n","light_cyan",attrs=["bold"])
    
def Admin():
      admin_name=input("Enter name:")
      pin=0000
      while pin!=1111:
        pin=int(input("Enter 4 digit Pin:"))
        if pin==1111:
            print ("Logged in as Admin")
            print("select a option--\n1.Book enquiry\n2.Book entry\n3.Customer Verification")
            c=int(input("Choose option--"))
            if c==1:
                Book_enquiry()
            elif c==2:
                entry()
            elif c==3:
                customer_search()
            else:
                print("Invalid choice...")
        else:
            print("Incorrect Pin.Try again")

def Customer():
    print("Choose as per your requirement:")
    print("1.Old Customer\n2.New Customer\n3.Check Profile")
    c=int(input("Enter choice(1-3):"))
    customer_name=input("Enter name:")
    customer_phone=int(input("Enter 10 digit Phone number:"))
    if c==1:
        pass

def login():
    print("Login as--")
    cprint("> ADMIN(1)\n> CUSTOMER(2)","green")
    cprint("Enter E to exit","red")

Book()
welcome()
login()
n=int
while n!=1 or n!=2:
    n=(input("Enter your choice:\n"))
    if n=='1':   
        # Admin
        print("Logging as Admin...")
        Admin()
        break;
    elif n=='2':  
        # Customer
        print("Logging as Customer...")
        Customer()
        break;
    elif n=='E' or n=='e' :
        exit()

    else:
        print("Invalid Entry....Try again.")
    login()