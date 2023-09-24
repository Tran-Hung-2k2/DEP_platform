from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Dữ liệu mẫu cho Entity Description (thường được lưu trữ trong cơ sở dữ liệu)
entity_db = {}
user_db = {}


# Mô hình Pydantic cho Entity Description
class EntityDescription(BaseModel):
    UserID: str
    Username: str
    Password: str
    Gender: str
    Email: str
    DateOfBirth: str
    PhoneNumber: str
    Balance: float
    UserRole: str


# Mô hình Pydantic cho tạo người dùng (signup)
class UserSignup(BaseModel):
    UserID: str
    Username: str
    Password: str
    Email: str
    UserRole: str


# Mô hình Pydantic cho đăng nhập (login)
class UserLogin(BaseModel):
    UserID: str
    Password: str


# Cơ chế mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hàm để hash mật khẩu
def hash_password(password: str):
    return pwd_context.hash(password)


# Hàm để kiểm tra mật khẩu
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# API endpoint để tạo Entity Description
@app.post("/entities/", response_model=EntityDescription)
def create_entity(entity: EntityDescription):
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


# API endpoint để đăng ký người dùng
@app.post("/signup/", response_model=UserSignup)
def signup(user: UserSignup):
    if user.UserID in user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    hashed_password = hash_password(user.Password)
    user.Password = hashed_password
    user_db[user.UserID] = user
    return JSONResponse(content=user.dict(), status_code=status.HTTP_200_OK)


# API endpoint để đăng nhập và kiểm tra thông tin đăng nhập
@app.post("/login/")
def login(user: UserLogin):
    if user.UserID not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stored_user = user_db[user.UserID]
    if not verify_password(user.Password, stored_user.Password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    return {"message": "Login successful"}


# API endpoint để lấy thông tin người dùng dựa trên UserID
@app.get("/users/{UserID}", response_model=UserSignup)
def get_user(UserID: str):
    if UserID not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user_db[UserID]
