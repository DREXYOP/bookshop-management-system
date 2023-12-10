import mysql.connector

# Establishing a MySQL connection
conn = mysql.connector.connect(
        host='sql12.freemysqlhosting.net',
        user='sql12668515',
        password='a5NWN6g3dl',
        database='sql12668515',
)
# Creating a cursor
cursor = conn.cursor()

# Create the Book table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Book (
        BOOK_ID INT ,
        BOOK_NAME VARCHAR(255),
        AUTHOR VARCHAR(255),
        GENRE VARCHAR(255),
        QUANTITY INT,
        PRICE DECIMAL(10, 2)
    )
''')

# Create the Customer table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customer (
        CUSTOMER_ID INT ,
        CUSTOMER_NAME VARCHAR(255),
        PHONE_NUMBER VARCHAR(15),  -- Assuming phone number is stored as a string
        EMAIL VARCHAR(255),
        BOOKS_BOUGHT INT
    )
''')

# Insert data into the Book table with a new BOOK_ID
cursor.execute('''
    INSERT INTO Book VALUES (1, 'FLAMINGO', 'NCERT', 'STORY & POEMS', 5, 10.99)
''')

# Insert data into the Customer table
cursor.execute('''
    INSERT INTO Customer VALUES (8, 'John Doe', '1234567890', 'john@example.com', 10)
''')

# Join the tables to create a bill
cursor.execute('''
    SELECT
        Customer.CUSTOMER_ID,
        Customer.CUSTOMER_NAME,
        Book.BOOK_NAME,
        Book.QUANTITY,
        Book.PRICE * Book.QUANTITY AS TOTAL_PRICE
    FROM
        Customer
    JOIN
        Book ON Customer.BOOKS_BOUGHT = Book.BOOK_ID
''')

# Fetch the result
result = cursor.fetchall()
for row in result:
    print(row)

# Update existing tables (for demonstration, you can modify this based on your actual requirements)
cursor.execute('''
    UPDATE Book SET QUANTITY = QUANTITY - 1 WHERE BOOK_ID = 2
''')

cursor.execute('''
    UPDATE Customer SET BOOKS_BOUGHT = NULL WHERE CUSTOMER_ID = 1
''')

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()