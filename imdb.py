import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the path to the SQLite database, consistent with the Flask app
script_dir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(script_dir, "library.sqlite3")
engine = create_engine(f"sqlite:///{dbfile}")

# Set up the base and session
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the Movie model independently in this script


class Movie(Base):
    __tablename__ = 'Movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    # genre = Column(String, nullable=False)


# Ensure the table exists in the database
Base.metadata.create_all(engine)
print('successfully added data')

# Load data from TSV into a pandas DataFrame
titles_basics = pd.read_csv('title.basics.tsv', sep='\t')
titles_basics = titles_basics.head(1000)

# Insert data into the Movies table
for _, row in titles_basics.iterrows():
    movie = Movie(
        # Replace with the correct DataFrame column name
        title=row['primaryTitle'],
        # Replace with the correct DataFrame column name
        # genre=row['genres']
    )
    session.add(movie)

# Commit all the additions to the database
session.commit()
session.close()

print("Data successfully added to the Movies table.")
