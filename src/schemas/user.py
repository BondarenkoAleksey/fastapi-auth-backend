import enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    role: UserRole
    is_active: bool

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class LoginData(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
