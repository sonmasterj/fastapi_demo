from fastapi import FastAPI
# from fastapi.param_functions import Body
from pydantic import BaseModel
import time
read_cmmd=True

def rfid_handle():
    time.sleep(1)

class MRZ(BaseModel):
    mrz:str
app = FastAPI()
@app.get("/")
async def root():
    return {"message":"hello world"}
   
@app.post("/mrz")
async def handle(key:MRZ):
    rfid_handle()
    if read_cmmd==True:
        return {
            "code":"0",
            "data":{
                "name":"Son",
                "bod":"14/02/1996",
                "key":key.mrz
            }
        }
    else:
        return {"code":"000","message":"Error connect device"}
