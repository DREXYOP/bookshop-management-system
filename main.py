from database.manager import connection
from user.admin import Admin
from user.customer import Customer
from termcolor import cprint



def data():
    db = connection()
    if db.is_connected():
        print("DB connected")
    else:
        print("DB not connected")
        exit()
    return db



def welcome():
    cprint("\nWelcome to our BOOK SHOP MANAGEMENT SYSTEM!\n","light_cyan",attrs=["bold"])
    print("This System is Developed by:\n1.DEBAJYOTI RAY BARMAN\n\n")
   
    

def login():
    print("Login as--")
    cprint("> ADMIN(1)\n> CUSTOMER(2)","green")
    cprint("Enter E to exit","red")
    n=(input("Enter your choice:\n"))

    if n=='1':   
        """--Admin"""
        Admin()
    elif n=='2':  
        """--Customer"""
        Customer()
    elif n=='E' or n=='e' :
        exit()

    else:
        print("Invalid Entry....Try again.")


db = data()
db.cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        Book_id     INT     PRIMARY KEY,
        Title       VARCHAR(255),
        Author      VARCHAR(255),
        Genre       VARCHAR(255),
        Quantity    INT
    );
    """)

# cursor=db.cursor()
# logiqn()
