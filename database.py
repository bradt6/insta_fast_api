import databases
from databases.core import DatabaseURL
import sqlalchemy
from databases import Database

DATABASE_URL = "sqlite:///users.db"
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

def get_database():
    return database