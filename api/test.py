from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# Khai báo ứng dụng FastAPI
app = FastAPI()

# Khai báo cơ chế xác thực - JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mô hình Pydantic cho người dùng
class User(BaseModel):
    username: str

# Mô hình Pydantic cho thông tin người dùng cần xác thực
class UserInDB(User):
    hashed_password: str

# Mô hình Pydantic cho thông tin đăng ký người dùng
class UserSignup(BaseModel):
    username: str
    password: str

# Cơ chế mã hóa mật khẩu
class HashedPassword:
    def __init__(self, password: str):
        self.password = password

    def hash_password(self):
        return pwd_context.hash(self.password)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Tạo token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Khởi tạo cơ chế xác thực OAuth2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dữ liệu mẫu cho người dùng (thường được lưu trữ trong cơ sở dữ liệu)
fake_users_db = {}
fake_users_db["testuser"] = {
    "username": "testuser",
    "hashed_password": HashedPassword("testpassword").hash_password(),
}

# API endpoint để đăng ký người dùng (signup)
@app.post("/signup")
async def signup(user: UserSignup):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = HashedPassword(user.password).hash_password()
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
    return {"message": "User registered successfully"}

# API endpoint để đăng nhập và tạo token JWT (login)
@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# API endpoint bảo vệ đòi hỏi xác thực
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route", "token": token}
