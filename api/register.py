from fastapi import HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import string, time, random
from user import db_manager


router = APIRouter(
    prefix="/v1/register",
    tags=["registers"],
    responses={404: {"description": "Not found"}},
)


# Mô hình Pydantic cho Register
class Register(BaseModel):
    user_name: str = Field(max_length=10)
    problem: str = Field(max_length=50)


# Hàm để tạo token
def create_token(length=15):
    characters = string.ascii_letters + string.digits
    seed = int(time.time() * 1000)
    random.seed(seed)
    token = "".join(random.choice(characters) for _ in range(length))
    return token


# API endpoint để tạo Register và tạo token cho người dùng
@router.post("/")
def create_register(post: Register):
    entity = db_manager.get_user_by_username(post.user_name)
    if entity is None:
        raise HTTPException(status_code=404, detail="User not found")
    register_data = {"user_id": entity["user_id"], "problem": post.problem}
    token = create_token()
    register_data["token"] = token
    db_manager.add_register(register_data)
    return JSONResponse(content=register_data, status_code=status.HTTP_200_OK)


# API endpoint để lấy thông tin Register dựa trên UserID
@router.get("/{Username}")
def get_register(Username: str):
    user_data = db_manager.get_user_by_username(Username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    register_data = db_manager.get_register_by_user_id(user_data["user_id"])
    if register_data is None:
        raise HTTPException(
            status_code=404, detail="This user does not have any register"
        )
    return JSONResponse(content=register_data, status_code=status.HTTP_200_OK)


# API endpoint để xóa Register dựa trên UserID
@router.delete("/{Token}")
def delete_register(token: str):
    if db_manager.delete_register(token):
        return JSONResponse(
            content={"message": "Register deleted"}, status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(status_code=404, detail="Register not found")
