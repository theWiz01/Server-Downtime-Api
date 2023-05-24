from typing import Optional
from sqlmodel import Field, SQLModel

from utils.models import IDTimeBasedModel

class User(IDTimeBasedModel, table=True):
    __tablename__ = "users"

    first_name : str
    last_name : str
    email : str
    password : str

    def __repr__(self):
        return self.email or f'{self.first_name} {self.last_name}'