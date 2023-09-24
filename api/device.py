from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Dữ liệu mẫu cho Entity Description (thường được lưu trữ trong cơ sở dữ liệu)
entity_db = {}


# Mô hình Pydantic cho Entity Description
class EntityDescription(BaseModel):
    DeviceID: str
    UserID: str
    DeviceName: str
    PlateNo: str


# API endpoint để tạo Entity Description
@app.post("/entities/", response_model=EntityDescription)
def create_entity(entity: EntityDescription):
    if entity.DeviceID in entity_db:
        raise HTTPException(
            status_code=400,
            detail="Device with this DeviceID already exists",
        )
    entity_db[entity.DeviceID] = entity
    return entity


# API endpoint để lấy danh sách Entity Descriptions
@app.get("/entities/", response_model=List[EntityDescription])
def get_entities():
    return list(entity_db.values())


# API endpoint để lấy thông tin Entity Description dựa trên DeviceID
@app.get("/entities/{DeviceID}", response_model=EntityDescription)
def get_entity(DeviceID: str):
    entity = entity_db.get(DeviceID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    return entity


# API endpoint để cập nhật thông tin Entity Description dựa trên DeviceID
@app.put("/entities/{DeviceID}", response_model=EntityDescription)
def update_entity(DeviceID: str, updated_entity: EntityDescription):
    if DeviceID not in entity_db:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    entity_db[DeviceID] = updated_entity
    return updated_entity


# API endpoint để xóa Entity Description dựa trên DeviceID
@app.delete("/entities/{DeviceID}")
def delete_entity(DeviceID: str):
    if DeviceID not in entity_db:
        raise HTTPException(status_code=404, detail="Entity Description not found")
    del entity_db[DeviceID]
    return {"message": "Entity Description deleted"}
