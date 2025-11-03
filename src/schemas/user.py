from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    lasname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    password: str


class UserRead(BaseModel):
    id: int

    class Config:
        orm_mode = True
