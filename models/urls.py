from sqlalchemy import Integer, String, Column

from database.connection import Base


class Urls(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    path = Column(String)
    short_path = Column(String, nullable=True)
    user_email = Column(String)
