# put all of APIs here
# fastAPI framework
# pydantic BaseModel is must

from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    Path,
    Query,
    Body,
    File,
    Cookie,
    Header,
    Form,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
from models import *
import shutil
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class User(BaseModel):
    username: str
    password: str


class student(BaseModel):
    id: int
    name: str = Field(None, title="name of student", max_length=10)
    marks: List[int] = []
    percent_marks: float


class percent(BaseModel):
    id: int
    name: str = Field(None, title="name of student", max_length=10)
    percent_marks: float


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name: str):
    return templates.TemplateResponse(
        "hello_name.html", {"request": request, "name": name}
    )


@app.get("/hello/{name}/{age}")
async def hello(
    *,
    name: str = Path(..., min_length=3, max_length=10),
    age: int = Path(..., ge=1, le=100),
):
    return {"name": name, "age": age}


@app.get("/hello/{name}/{age}")
async def hello(
    *,
    name: str = Path(..., min_length=3, max_length=10),
    age: int = Path(..., ge=1, le=100),
    percent: float = Query(..., ge=0, le=100),
):
    return {"name": name, "age": age}


@app.post("/students")
async def student_data(name: str = Body(...), marks: int = Body(...)):
    return {"name": name, "marks": marks}


@app.post("/students/{college}")
async def student_data(college: str, age: int, student: Student):
    retval = {"college": college, "age": age, **student.dict()}
    return retval


@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return User(username=nm, password=pwd)


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("uploadfile.html", {"request": request})


@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
    with open("./static/destination.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


@app.post("/cookie/")
def create_cookie():
    content = {"message": "cookie set"}
    response = JSONResponse(content=content)
    response.set_cookie(key="username", value="admin")
    return response


@app.get("/readcookie/")
async def read_cookie(username: str = Cookie(None)):
    return {"username": username}


@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
    return {"Accept-Language": accept_language}


@app.get("/rspheader/")
def set_rsp_headers():
    content = {"message": "Hello World"}
    headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)


@app.post("/marks", response_model=percent)
async def get_percent(s1: student):
    s1.percent_marks = sum(s1.marks) / 2
    return s1


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
