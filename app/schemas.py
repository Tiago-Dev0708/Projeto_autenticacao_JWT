from pydantic import BaseModel, field_validator
import re

class UserCreate(BaseModel):
    email: str 
    password: str 

    @field_validator("email")
    def validate_email(cls, value):
        if not re.match('([A-Z]|[a-z]|[0-9]|@)+$', value):
            raise ValueError("O formato do email está inválido.")
        return value
    

   