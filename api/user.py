from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
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
from db_manager import db_manager as dbm

# Khởi tạo ứng dụng FastAPI
# app = FastAPI()
app = APIRouter(prefix='/user')
db_manager = dbm.DatabaseManage()
db_manager.connect_to_database()


# Mô hình Pydantic cho đăng nhập (login)
class UserLogin(BaseModel):
    Username: str= Field(max_length=255)
    Password: str= Field(max_length=255)


# Mô hình Pydantic cho tạo người dùng (signup)
class UserSignup(UserLogin):
    Username: str= Field(max_length=255)
    Password: str= Field(max_length=255)
    Email: str= Field(max_length=255)
    Gender: str
    Email: str= Field(max_length=255)
    DateOfBirth: date
    PhoneNumber: str= Field(max_length=20)
    

# Mô hình Pydantic cho User
class User(UserSignup):
    UserID: str= Field(max_length=10)
    Balance: float
    UserRole: str= Field(max_length=255)


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
    user_id = ''.join(random.choice(characters) for _ in range(length))
    return user_id


@app.get("/")
def admin_page():
    return {"message": "Hello World"}

# API endpoint để tạo User
@app.post("/create", response_model=User)
def create_entity(entity: User):
    db_manager.add_user(entity.dict())
    return entity


# API endpoint để lấy thông tin User dựa trên Username
@app.get("/get/{Username}", response_model=User)
def get_entity(Username: str):
    entity = db_manager.get_user(Username)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    return entity


# API endpoint để cập nhật thông tin User dựa trên Username
@app.put("/put/{Username}", response_model=User)
def update_entity(Username: str, updated_entity: User):
    if db_manager.update_user(Username, updated_entity):
        return updated_entity
    else:
        raise HTTPException(status_code=404, detail="Error Updating")


# API endpoint để xóa User dựa trên Username
@app.delete("/entities/{Username}")
def delete_entity(Username: str):
    if db_manager.delete_user(Username):
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="Error Deleting")


# API endpoint để đăng ký người dùng
@app.post("/signup", response_model=User)
def signup(user: UserSignup):
    if db_manager.get_user(user.Username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    hashed_password = hash_password(user.Password)
    user.Password = hashed_password
    new_user_data_id=generate_user_id()
    new_user_data = user.dict() 
    new_user_data.update({"UserID": f"{new_user_data_id}", "Balance": 0.0, "UserRole": "user"})
    db_manager.add_user(new_user_data)
    return JSONResponse(content=new_user_data, status_code=status.HTTP_200_OK)


# API endpoint để đăng nhập và kiểm tra thông tin đăng nhập
@app.post("/login")
def login(user: UserLogin):
    user_data=db_manager.get_user(user.Username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found",
        )

    if not verify_password(user.Password, user_data.Password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    return {"message": "Login successful"}



if __name__ == "__main__":
    uvicorn.run(
        "user:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
