from fastapi import status  
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.schemas import UserCreate
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["sha256_crypt"])


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        hashed_password = crypt_context.hash(user.password)
        user_model = UserModel(email=user.email, password=hashed_password)
        try:
            self.db.add(user_model)
            self.db.commit()
            self.db.refresh(user_model)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado.",
            )
        


        

    def get_user(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return crypt_context.verify(plain_password, hashed_password)