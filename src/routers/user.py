import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Optional

from src.db.session import AsyncSessionLocal
from src.models.user import User
from src.schemas.user import LoginData, Token, UserCreate, UserRead, UpdateUser

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    '''
    Хэширование пароля
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Верификация пароля
    '''
    return pwd_context.verify(plain_password, hashed_password)

async def get_db():
    '''
    Создание сессии
    '''
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    '''
    Возврат пользователя по email'у
    '''
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    '''
    Создание токена
    '''
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserRead)
async def register_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    '''
    Регистрация нового пользователя
    '''
    existing_user = await get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user_create.password)
    new_user = User(
        name=user_create.name,
        lastname=user_create.lastname,
        email=user_create.email,
        hashed_password=hashed_password,
        role=user_create.role,
        is_active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.put("/user/{user_id}", response_model=UserRead)
async def update_user(user_id: int, update_user: UpdateUser, db: AsyncSession = Depends(get_db)):
    '''
    Обновление данных пользователя
    '''
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(update_user).items():
        if value is not None:
            setattr(user, var, value)
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    '''
    Деактивация пользователя (удаление)
    '''
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    await db.commit()
    return None

@router.post("/login", response_model=Token)
async def login(login_data: LoginData, db: AsyncSession = Depends(get_db)):
    '''
    Вход с получением JWT токена
    '''
    user = await get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    '''
    Выход
    '''
    return {"message": "Logout successful"}



