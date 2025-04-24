from datetime import datetime, timedelta
from fastapi import status  
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.schemas import UserCreate
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado.",
            )
        
    def user_login(self, user: UserCreate, expires_in: int = 30):
        user_existing = self.db.query(UserModel).filter_by(email=user.email).first()

        if user_existing is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
            )
        
        if not crypt_context.verify(user.password, user_existing.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user.email,
            'exp': exp
        }
        
        acess_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'acess_token': acess_token,
            'exp': exp.isoformat()
        }  

  #  def get_user(self, username: str):
  #      return self.db.query(UserModel).filter(UserModel.username == username).first()

   # def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        #return crypt_context.verify(plain_password, hashed_password)