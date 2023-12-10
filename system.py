# Import the necessary library
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
        host='sql12.freemysqlhosting.net',
        user='sql12668515',
        password='a5NWN6g3dl',
        database='sql12668515',
        
)

# Create a cursor to interact with the database
cursor = db.cursor()

# Create a table for books (assuming a simple structure for demonstration)
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(50),
    publication_year INT
)
""")

# Function to add a new book
def add_book(title, author, genre, publication_year):
    cursor.execute("""
    INSERT INTO books (title, author, genre, publication_year)
    VALUES (%s, %s, %s, %s)
    """, (title, author, genre, publication_year))
    db.commit()

# Function to display the list of books
def display_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if not books:
        print("No books found.")
    else:
        print("Book List:")
        for book in books:
            print(book)

# Function to search for books by title
def search_books_by_title(title):
    cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{title}%",))
    books = cursor.fetchall()
    if not books:
        print("No books found with the given title.")
    else:
        print("Search Results:")
        for book in books:
            print(book)

# Example usage
add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925)
add_book("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960)

display_books()

search_books_by_title("Mockingbird")

# Close the cursor and database connection when done
cursor.close()
db.close()
