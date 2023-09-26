# put all of APIs here
# fastAPI framework
# pydantic BaseModel is must

from fastapi import FastAPI
import uvicorn
import device, register, user


app = FastAPI()
db_manager = DatabaseManager()
db_manager.connect_to_database()

app.include_router(user.router)
app.include_router(register.router)
app.include_router(device.router)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
