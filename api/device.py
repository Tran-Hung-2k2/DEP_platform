from fastapi import FastAPI, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os
import string
import random
import time
from user import db_manager

router = APIRouter(
    prefix="/v1/device",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)


# Mô hình Pydantic cho Device
class Device(BaseModel):
    user_name: str = Field(max_length=40)
    device_name: Optional[str] = Field(max_length=255, default=None)
    plate_no: Optional[str] = Field(max_length=20, default=None)


def generate_device_id(length=10):
    characters = string.ascii_letters + string.digits
    seed = int(time.time() * 1000)
    random.seed(seed)
    user_id = "".join(random.choice(characters) for _ in range(length))
    return user_id


# API endpoint để tạo Device
@router.post("/")
def create_device(post: Device):
    entity = db_manager.get_user_by_username(post.user_name)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    device_id = generate_device_id()
    device_data = {
        "device_id": device_id,
        "user_id": entity["user_id"],
        "device_name": post.device_name,
        "plate_no": post.plate_no,
    }
    if db_manager.add_device(device_data):
        return JSONResponse(content=device_data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Create failed")


# API endpoint để lấy thông tin Device dựa trên DeviceID
@router.get("/deviceid/{DeviceID}")
def get_device_by_device_id(DeviceID: str):
    entity = db_manager.get_device(DeviceID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return JSONResponse(content=entity, status_code=status.HTTP_200_OK)


# API endpoint để cập nhật thông tin Device dựa trên Username
@router.get("/username/{Username}")
def get_device_by_user_id(Username: str):
    user_data = db_manager.get_user_by_username(Username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    entity = db_manager.get_device_by_user(user_data["user_id"])
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return JSONResponse(content=entity, status_code=status.HTTP_200_OK)


# API endpoint để xóa Device dựa trên DeviceID
@router.delete("/{DeviceID}")
def delete_device(DeviceID: str):
    entity = db_manager.get_device(DeviceID)
    if entity is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db_manager.delete_device(DeviceID)
    return JSONResponse(
        content={"message": "Device deleted"}, status_code=status.HTTP_200_OK
    )
