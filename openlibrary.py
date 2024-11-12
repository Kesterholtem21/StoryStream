import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep

# Define the path to the SQLite database, consistent with the Flask app
script_dir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(script_dir, "library.sqlite3")
engine = create_engine(f"sqlite:///{dbfile}")

# Set up the base and session
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)


# Ensure the table exists in the database
Base.metadata.create_all(engine)
print('success 1')


# Function to fetch books from the Open Library API
def fetch_books(start=0, limit=10):
    url = f"https://openlibrary.org/search.json?q=fiction&limit={limit}&offset={start}"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json().get('docs', [])


def insert_books(books):
    for book_data in books:
        title = book_data.get('title')
        authors = book_data.get('author_name', ['Unknown'])[0]  # Take the first author if available
        genres = ', '.join(book_data.get('subject', [])) if book_data.get('subject') else 'Unknown'  # Join subjects as genre

        
        book = Book(title=title, author=authors, genre=genres)
        session.add(book)

    session.commit()
    print("Batch of books successfully added to the Books table.")

# Fetch and store books in batches to avoid overloading the API
start = 0
batch_size = 100

while True:
    books = fetch_books(start=start, limit=batch_size)
    if not books:
        break

    insert_books(books)
    start += batch_size

    print(f"Inserted batch starting at {start}")
    sleep(1)

# Close the session after all data is inserted
session.close()
print("Data successfully added to the Books table.")