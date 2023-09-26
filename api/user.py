from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from passlib.context import CryptContext
import uvicorn
from datetime import date
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
    Username: str = Field(max_length=40)
    Password: str = Field(max_length=255)


# Mô hình Pydantic cho tạo người dùng (signup)
class UserSignup(UserLogin):
    Email: str = Field(max_length=255)
    Gender: str = Field(max_length=10)
    Email: str = Field(max_length=255)
    DateOfBirth: str
    PhoneNumber: str = Field(max_length=15)


# Mô hình Pydantic cho User
class User(UserSignup):
    UserID: str = Field(max_length=10)
    Balance: float
    UserRole: str = Field(max_length=50)


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
@router.get("/{Username}", response_model=User)
def get_user(Username: str):
    entity = db_manager.get_user_by_username(Username)
    print(entity)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    entity["date_of_birth"] = entity["date_of_birth"].isoformat()
    entity["balance"] = float(entity["balance"])
    return JSONResponse(content=entity, status_code=status.HTTP_200_OK)


# API endpoint để cập nhật thông tin User dựa trên Username
@router.put("/{Username}", response_model=User)
def update_user(Username: str, post: User):
    if db_manager.update_user_by_username(Username, post):
        return JSONResponse(content=post, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Error Updating")


# API endpoint để xóa User dựa trên Username
@router.delete("/{Username}")
def delete_user(Username: str):
    if db_manager.delete_user(Username):
        return JSONResponse(
            content={"message": "User deleted"}, status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(status_code=404, detail="Error Deleting")


# API endpoint để đăng ký người dùng
@router.post("/", response_model=User)
def signup(post: UserSignup):
    if db_manager.get_user_by_username(post.Username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    hashed_password = hash_password(post.Password)
    post.Password = hashed_password
    new_user_data_id = generate_user_id()
    new_user_data = post.dict()
    new_user_data.update(
        {"UserID": f"{new_user_data_id}", "Balance": 0.0, "UserRole": "user"}
    )
    db_manager.add_user(new_user_data)
    new_user_data["DateOfBirth"] = new_user_data["DateOfBirth"].isoformat()
    return JSONResponse(content=new_user_data, status_code=status.HTTP_200_OK)


# API endpoint để đăng nhập và kiểm tra thông tin đăng nhập
@router.post("/login")
def login(post: UserLogin):
    user_data = db_manager.get_user(post.Username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found",
        )
    if not verify_password(post.Password, user_data.Password):
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
