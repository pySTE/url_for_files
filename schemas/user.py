from pydantic import BaseModel, EmailStr


class UserSchem(BaseModel):
    email: EmailStr
    password: str