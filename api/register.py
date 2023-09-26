from fastapi import FastAPI, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import List
import jwt
import sys
import os
from jwt import PyJWTError
from user import db_manager


router = APIRouter(
    prefix="/v1/register",
    tags=["registers"],
    responses={404: {"description": "Not found"}},
)


# Mô hình Pydantic cho Register
class Register(BaseModel):
    token: str = Field(max_length=15)
    user_name: str = Field(max_length=10)
    problem: str = Field(max_length=50)


# Secret key để mã hóa và giải mã token
SECRET_KEY = "SECRETKEY"


# Hàm tạo token
def create_token(data: dict):
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return token


# Hàm giải mã token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except PyJWTError:
        return None


# API endpoint để tạo Register và tạo token cho người dùng
@router.post("/")
def create_register(post: Register):
    entity = db_manager.get_user(post.Username)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    register_data = {"UserID": entity.UserID, "Problem": post.Problem}
    token = create_token(register_data)
    register_data["Token"] = token
    db_manager.add_register(register_data)
    return JSONResponse(content=register_data, status_code=status.HTTP_200_OK)


# API endpoint để lấy thông tin Register dựa trên UserID
@router.get("/{Username}")
def get_register(Username: str):
    user_data = db_manager.get_user(Username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="Register not found")
    register_data = db_manager.get_register_by_user_id(user_data.UserID)
    return JSONResponse(content=register_data, status_code=status.HTTP_200_OK)


# API endpoint để xóa Register dựa trên UserID
@router.delete("/{Token}")
def delete_register(Token: str, query: str):
    if not db_manager.get_register_by_user_id(query):
        raise HTTPException(status_code=404, detail="Register not found")
    db_manager.delete_register(Token)
    return JSONResponse(
        content={"message": "Register deleted"}, status_code=status.HTTP_200_OK
    )
