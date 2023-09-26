# put all of APIs here
# fastAPI framework
# pydantic BaseModel is must

from fastapi import FastAPI
import uvicorn
import device, register, user
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_manager.db_manager import DatabaseManager

app = FastAPI()
app.include_router(user.router)
app.include_router(register.router)
app.include_router(device.router)

db_manager = DatabaseManager()
db_manager.connect_to_database()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    import threading
    kafka_thread = threading.Thread(target=db_manager.data_consume("localhost",29092,"alo"))
    kafka_thread.start()

    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
