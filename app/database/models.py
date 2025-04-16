from sqlalchemy import Column, Integer, String 
from app.database.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
