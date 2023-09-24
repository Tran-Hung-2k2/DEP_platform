from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import jwt
from jwt import PyJWTError

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Dữ liệu mẫu cho Entity Description (thường được lưu trữ trong cơ sở dữ liệu)
entity_db = {}


# Mô hình Pydantic cho Entity Description
class EntityDescription(BaseModel):
    Token: str
    UserID: str
    Service: str


# Secret key để mã hóa và giải mã token (bạn cần giữ nó bí mật và an toàn)
SECRET_KEY = "tranhung"


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


# API endpoint để tạo Entity Description và tạo token cho người dùng
@app.post("/entities/", response_model=EntityDescription)
def create_entity(entity: EntityDescription):
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


# API endpoint để lấy danh sách Entity Descriptions
@app.get("/entities/", response_model=List[EntityDescription])
def get_entities():
    return list(entity_db.values())


# API endpoint để lấy thông tin Entity Description dựa trên UserID
@app.get("/entities/{UserID}", response_model=EntityDescription)
def get_entity(UserID: str):
    entity = entity_db.get(UserID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    return entity


# API endpoint để cập nhật thông tin Entity Description dựa trên UserID
@app.put("/entities/{UserID}", response_model=EntityDescription)
def update_entity(UserID: str, updated_entity: EntityDescription):
    if UserID not in entity_db:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    entity_db[UserID] = updated_entity
    return updated_entity


# API endpoint để xóa Entity Description dựa trên UserID
@app.delete("/entities/{UserID}")
def delete_entity(UserID: str):
    if UserID not in entity_db:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    del entity_db[UserID]
    return {"message": "Entity Description deleted"}
