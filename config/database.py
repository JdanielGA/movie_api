# This program creates a database connection and a session.
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# The name of the database file.
sqlite_file_name = 'database.sqlite'

# The path to the directory containing the database file.
base_dir = os.path.dirname(os.path.realpath(__file__))

# The database URI.
database_uri = 'sqlite:///' + os.path.join(base_dir, sqlite_file_name)

# Create an engine to connect to the database.
engine = create_engine(database_uri, echo=True)

# Create a session to interact with the database.
session = sessionmaker(bind=engine)

# Create a base class for all of the tables in the database.
Base = declarative_base()