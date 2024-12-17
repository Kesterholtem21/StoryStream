import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep

script_dir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(script_dir, "library.sqlite3")
engine = create_engine(f"sqlite:///{dbfile}")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    poster_path = Column(String, nullable=True)
    description = Column(String, nullable=True)



Base.metadata.create_all(engine)
print('success 1')


def fetch_books(start=0, limit=10):
    url = f"https://openlibrary.org/search.json?q=fiction&limit={limit}&offset={start}"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json().get('docs', [])


def construct_image_url(cover_id):
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return None


def insert_books(books):
    for book_data in books:
        title = book_data.get('title')
        authors = book_data.get('author_name', ['Unknown'])[0]
        genres = ', '.join(book_data.get('subject', [])) if book_data.get('subject') else 'Unknown'
        cover_id = book_data.get('cover_i')
        poster_path = construct_image_url(cover_id)

        num_pages = book_data.get('number_of_pages_median', 'Unknown')

        book = Book(title=title, author=authors, genre=genres, poster_path=poster_path, description=str(num_pages))
        session.add(book)

    session.commit()
    print("Batch of books successfully added to the Books table.")

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

session.close()
print("Data successfully added to the Books table.")
