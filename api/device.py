from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os
import string
import random
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_manager.db_manager import DatabaseManager

router = APIRouter(
    prefix="/v1/device",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)
db_manager = DatabaseManager()
db_manager.connect_to_database()


# Mô hình Pydantic cho Device
class Device(BaseModel):
    DeviceID: str = Field(max_length=10)
    Username: str = Field(max_length=40)
    DeviceName: str = Field(max_length=255)
    PlateNo: str = Field(max_length=20)


def generate_device_id(length=15):
    characters = string.ascii_letters + string.digits
    seed = int(time.time() * 1000)
    random.seed(seed)
    user_id = "".join(random.choice(characters) for _ in range(length))
    return user_id


# API endpoint để tạo Device
@router.post("/", response_model=Device)
def create_entity(post: Device):
    entity = db_manager.get_user(post.Username)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    device_id = generate_device_id()
    device_data = {
        "DeviceID": device_id,
        "UserID": entity.UserID,
        "DeviceName": post.DeviceName,
        "PlateNo": post.PlateNo,
    }
    db_manager.add_device(device_data)
    return device_data


# API endpoint để lấy thông tin Device dựa trên DeviceID
@router.get("/deviceid/{DeviceID}", response_model=Device)
def get_entity(DeviceID: str):
    entity = db_manager.get_device(DeviceID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return entity


# API endpoint để cập nhật thông tin Device dựa trên UserID
@router.get("/userid/{UserID}", response_model=Device)
def get_entity_many(UserID: str):
    entity = db_manager.get_device_by_user(UserID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return entity


# API endpoint để xóa Device dựa trên DeviceID
@router.delete("/{DeviceID}")
def delete_entity(DeviceID: str):
    entity = db_manager.get_device(DeviceID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db_manager.delete_device(DeviceID)
    return {"message": "Device deleted"}
