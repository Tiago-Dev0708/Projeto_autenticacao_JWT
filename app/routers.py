from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.depends import get_db
from sqlalchemy.orm import Session
from app.UserAuth import UserService  
from app.schemas import UserCreate

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_case = UserService(db=db)
    user_case.create_user(user=user)
    return JSONResponse(content={'mensagem': 'Usuário criado com sucesso'},
                    status_code=status.HTTP_201_CREATED
                    )


@router.post("/login")
def register_user(requestFormUser: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_case = UserService(db=db)
    user = UserCreate(
        email=requestFormUser.username,
        password=requestFormUser.password
    )
    return JSONResponse(
        content=user_case.user_login(user=user),
        status_code=status.HTTP_200_OK

    )

