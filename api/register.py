from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from typing import List
import jwt
import sys
import os
from jwt import PyJWTError
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_manager import db_manager 


# Khởi tạo ứng dụng FastAPI
app = FastAPI()
register_manager = db_manager.DatabaseManage()
register_manager.connect_to_database()



# Mô hình Pydantic cho Register
class Register(BaseModel):
    Token: str = Field(max_length=255)
    UserID: str = Field(max_length=10)
    Service: str = Field(max_length=255)


# Secret key để mã hóa và giải mã token
SECRET_KEY = "tranhungchubedan"


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
@app.post("/register", response_model=Register)
def create_entity(entity: Register):
    if entity.UserID in entity_db:
        raise HTTPException(
            status_code=400,
            detail="Entity with this UserID already exists",
        )
    # Tạo token
    token_data = {"UserID": entity.UserID, "Service": entity.Service}
    token = create_token(token_data)
    entity.Token = token
    entity_db[entity.UserID] = entity
    return entity


# API endpoint để lấy danh sách Registers
@app.get("/entities/", response_model=List[Register])
def get_entities():
    return list(entity_db.values())


# API endpoint để lấy thông tin Register dựa trên UserID
@app.get("/entities/{UserID}", response_model=Register)
def get_entity(UserID: str):
    entity = entity_db.get(UserID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Register not found")
    return entity


# API endpoint để cập nhật thông tin Register dựa trên UserID
@app.put("/entities/{UserID}", response_model=Register)
def update_entity(UserID: str, updated_entity: Register):
    if UserID not in entity_db:
        raise HTTPException(status_code=404, detail="Register not found")
    entity_db[UserID] = updated_entity
    return updated_entity


# API endpoint để xóa Register dựa trên UserID
@app.delete("/entities/{UserID}")
def delete_entity(UserID: str):
    if UserID not in entity_db:
        raise HTTPException(status_code=404, detail="Register not found")
    del entity_db[UserID]
    return {"message": "Register deleted"}
