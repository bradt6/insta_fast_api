import sqlalchemy
from pydantic import BaseModel

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(length=254), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(length=254), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(length=254), nullable=False),
)