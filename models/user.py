from passlib.hash import bcrypt
from sqlalchemy import Integer, String, Column

from database.connection import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)
