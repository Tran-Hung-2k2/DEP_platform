from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel,Field
from typing import List
import jwt
import sys
import os
from jwt import PyJWTError
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_manager import db_manager as dbm 


router = APIRouter(
    prefix="/register",
    tags=["registers"],
    responses={404: {"description": "Not found"}},
)
# app = FastAPI()
db_manager = dbm.DatabaseManage()
db_manager.connect_to_database()



# Mô hình Pydantic cho Register
class Register(BaseModel):
    Token: str = Field(max_length=255)
    Username: str = Field(max_length=10)
    Problem: str = Field(max_length=255)


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
@router.post("/create", response_model=Register)
def create_entity(post: Register):
    entity = db_manager.get_user(post.Username)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    register_data = {"UserID": entity.UserID, "Problem": post.Problem}
    token = create_token(register_data)
    register_data["Token"] = token
    db_manager.add_register(register_data)
    return register_data



# API endpoint để lấy thông tin Register dựa trên UserID
@router.get("/get/{Username}", response_model=Register)
def get_entity(Username: str):
    user_data = db_manager.get_user(Username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="Register not found")
    register_data = db_manager.get_register_by_user_id(user_data.UserID)
    return register_data



# API endpoint để xóa Register dựa trên UserID
@router.delete("/delete/{Token}")
def delete_entity(Token: str, query:str):
    if not db_manager.get_register_by_user_id(query):
        raise HTTPException(status_code=404, detail="Register not found")
    db_manager.delete_register(Token)
    return {"message": "Register deleted"}
