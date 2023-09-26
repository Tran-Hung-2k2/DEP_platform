from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from passlib.context import CryptContext
import uvicorn
import sys
import os
import string
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_manager.db_manager import DatabaseManager

router = APIRouter(
    prefix="/v1/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

db_manager = DatabaseManager()
db_manager.connect_to_database()


# Mô hình Pydantic cho đăng nhập (login)
class UserLogin(BaseModel):
    user_name: str = Field(max_length=40)
    password: str = Field(max_length=255)


# Mô hình Pydantic cho tạo người dùng (signup)
class UserSignup(UserLogin):
    gender: Optional[str] = Field(max_length=10, default=None)
    email: Optional[str] = Field(max_length=255, default=None)
    date_of_birth: Optional[str] = None
    phone_number: Optional[str] = Field(max_length=15, default=None)


# Mô hình Pydantic cho User
class User(UserSignup):
    user_id: str = Field(max_length=10)
    balance: float
    role: str = Field(max_length=50)


# Cơ chế mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hàm để hash mật khẩu
def hash_password(password: str):
    return pwd_context.hash(password)


# Hàm để kiểm tra mật khẩu
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Hàm để tạo user_id
def generate_user_id(length=10):
    characters = string.ascii_letters + string.digits
    seed = int(time.time() * 1000)
    random.seed(seed)
    user_id = "".join(random.choice(characters) for _ in range(length))
    return user_id


# API endpoint để lấy thông tin User dựa trên Username
@router.get("/{Username}")
def get_user(Username: str):
    user_data = db_manager.get_user_by_username(Username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_data["date_of_birth"] = user_data["date_of_birth"].isoformat()
    user_data["balance"] = float(user_data["balance"])
    return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)


# API endpoint để cập nhật thông tin User dựa trên Username
@router.put("/{Username}")
def update_user(Username: str, user_data: User):
    user_data = user_data.dict()
    if db_manager.update_user_by_username(Username, user_data):
        return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error Updating"
        )


# API endpoint để xóa User dựa trên Username
@router.delete("/{UserID}")
def delete_user(UserID: str):
    if db_manager.delete_user(UserID):
        return JSONResponse(
            content={"message": "User deleted"}, status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserID do not exist"
        )


# API endpoint để đăng ký người dùng
@router.post("/")
def signup(user_data: UserSignup):
    if db_manager.get_user_by_username(user_data.user_name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password
    new_user_data_id = generate_user_id()
    new_user_data = user_data.dict()
    new_user_data.update(
        {"user_id": f"{new_user_data_id}", "balance": 0.0, "role": "user"}
    )
    if db_manager.add_user(new_user_data):
        return JSONResponse(content=new_user_data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Fail to sign up"
        )


# API endpoint để đăng nhập và kiểm tra thông tin đăng nhập
@router.post("/login")
def login(user_data: UserLogin):
    user = db_manager.get_user_by_username(user_data.user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found",
        )
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    return JSONResponse(
        content={"message": "Login successful"}, status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    uvicorn.run(
        "user:router",
        host="127.0.0.1",
        reload=True,
        port=8000,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
