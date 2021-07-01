from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
read_cmmd=False

# read rfid func
def rfid_handle():
    time.sleep(3)

class MRZ(BaseModel):
    mrz:str
app = FastAPI()
# add cors rule
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# api test
@app.get("/")
async def root():
    return {"message":"hello world"}

# api post mrz key   
@app.post("/mrz")
async def handle(key:MRZ,req:Request):
    if "signature" in req.headers:
        token = req.headers["signature"]
        # print(token)
        if token!="AIoT2020@&":
            return {"code":"002","message":"Sai token xác thực!"}
        rfid_handle()
        if read_cmmd==True:
            return {
                "code":"000",
                "data":{
                    "name":"Son",
                    "bod":"14/02/1996",
                    "key":key.mrz
                }
            }
        else:
            return {"code":"001","message":"Lỗi kết nối thiết bị đọc thẻ!"}
    else :
        return {"code":"002","message":"Lỗi xác thực!"}
