from sqlalchemy import Column, Integer, String 
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
