
# from json import load
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from pypassport import epassport, reader
import os
# import io
# from PIL import Image
# from mrz.checker.td1 import TD1CodeChecker, get_country
import base64
import cv2

#define dg13 zone
idCodeZone="02010113";
personNameZone="0201020c";
dateOfBirthZone="02010313";
genderZone="0201040c";
nationalityZone="0201050c";
raceZone="0201060c";
religionZone="0201070c";
originPlaceZone="0201080c";
residencePlaceZone="0201090c";
personalIdentificationZone="02010a0c";
beginDateZone="02010b13";
expiryDateZone="02010c0c";
fatherNameZone="02010d30";
wifeNameZone="02010e30";
oldIdCodeZone="02010f13";

#func handle dg13
def readZone(data,zone):
    zoneIndex = data.find(zone)+8
    if(zoneIndex<8):
        return ""
    zonLen = bytes.fromhex(data[zoneIndex:zoneIndex+2])[0]
    # print("zone len :",zonLen)
    if(len(data)<zoneIndex+zonLen*2):
        return ""
    result = bytes.fromhex(data[zoneIndex+2:zoneIndex+2+zonLen*2]).decode('utf8')
    # print("zone result:"+result)
    return result


def readFatherZone(data,zone):
    list =[]
    zoneIndex = data.find(zone)+8
    if(zoneIndex<8):
        return list
    zonLen1 = bytes.fromhex(data[zoneIndex:zoneIndex+2])[0]
    if(len(data)<zoneIndex+zonLen1*2):
        return list
    zoneLen2 =bytes.fromhex(data[zoneIndex+4:zoneIndex+6])[0]
    if(zonLen1!=zoneLen2+2):
        return list
    resultFather = bytes.fromhex(data[zoneIndex+6:zoneIndex+6+zoneLen2*2]).decode('utf8')
    list.append(resultFather)
    zoneMotherIndex = zoneIndex+6+zoneLen2*2+2
    zonLen3 =bytes.fromhex(data[zoneMotherIndex:zoneMotherIndex+2])[0]
    zonLen4 =bytes.fromhex(data[zoneMotherIndex+4:zoneMotherIndex+6])[0]
    if(zonLen3==zonLen4+2):
        resultMother = bytes.fromhex(data[zoneMotherIndex+6:zoneMotherIndex+6+zonLen4*2]).decode('utf8')
        list.append(resultMother)

    # print( list)
    return list

def readWifeZone(data,zone):
    zoneIndex = data.find(zone)+8
    if(zoneIndex<8):
        return ""
    zonLen1 = bytes.fromhex(data[zoneIndex:zoneIndex+2])[0]
    if(len(data)<zoneIndex+zonLen1*2):
        return ""
    zoneLen2 =bytes.fromhex(data[zoneIndex+4:zoneIndex+6])[0]
    if(zonLen1!=zoneLen2+2):
        return ""
    result = bytes.fromhex(data[zoneIndex+6:zoneIndex+6+zoneLen2*2]).decode('utf8')
    return result
# import subprocess
# MRZ_tohue =     "IDVNM1830015170026183001517<<28310073F2310071VNM<<<<<<<<<<<2"      # Huong
# MRZ_tohue =     "IDVNM0990303372001099030337<<39905050M2405056VNM<<<<<<<<<<<2"      # quang anh 
# MRZ_tohue =     "IDVNM0960146541001096014654<<29604021M3604029VNM<<<<<<<<<<<6"      # hai
# MRZ_tohue =     "IDVNM0790110761034079011076<<47912104M3912106VNM<<<<<<<<<<<4"      # luc
# global mrz
def trace(name, msg):
    if name == "EPassport":
        print(name + "> " + msg)

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

# api update mrz
# @app.post("/update-mrz")
# async def handle(key:MRZ):
#     print(key.mrz)
#     global mrz
#     mrz=key.mrz
#     return(key.mrz)
# api capture image
@app.get('/capture')
async def capture():
    try:
        cam = cv2.VideoCapture(0)
        ret,frame = cam.read()
        if ret == False:
            cam.release()
            return {
                "code":"001",
                "message":"Chụp ảnh thất bại!"
            }
        else:
            cv2.imwrite('capture.jpg',frame)

            os.system('sh /home/pi/ultimateMRZ-SDK/samples/python/recognizer/run_rpi_armv7l.sh')
            # print(res)
            file = open('key.txt','r')
            mrz = file.read()
            with open("capture.jpg", "rb") as image_file:
                encodeImg = base64.b64encode(image_file.read())
                # print("send")
                return{
                    "code":"000",
                    "message":"Chụp ảnh thành công!",
                    "img":"data:image/jpeg;base64,"+encodeImg.decode('ascii'),
                    "mrz":mrz
                }

    except Exception as msg:
        print(msg)
        cam.release()
        return {
            "code":"001",
             "message":"Chụp ảnh thất bại!"
        }
# api post mrz key   
@app.post("/mrz")
async def handle(key:MRZ,req:Request):
    print("haitn13 certificate " + os.getcwd())
    print("haitn13 rfid_handler, mrz = " ,key.mrz)
    ############################Run###########################

    sep = os.path.sep
    Sim = False
    # Sim = True
    r=None
    if not Sim:
        print("haitn13 simulation = False")
        try:
            r = reader.ReaderManager().waitForCard()
        except Exception as msg:
            return{
                "code":"002",
                "message":str(msg)
            }
    
    else:
        print("haitn13 simulation true" )
        r = reader.ReaderManager().create("DumpReader")
        r.connect("C:\\tmp")

    # print("haitn13 MRX_tohue =" + key.mrz )
    # global ep
    ep=None
    try:
        ep = epassport.EPassport(r,key.mrz)
        ep.register(trace)
        ep.setCSCADirectory(os.getcwd() + sep + "testData" + sep + "3d36cc9e.0", False)
    except Exception as msg:
        return{
            "code":"001",
            "message":str(msg)
        }

    start = time.time()
    
    print("haitn13 done Epassport")
    try:
        ep.readPassport()
        print("haitn13 done readPassportd")
    except Exception as msg:
        
        print("loi")
        print(msg)
        # continue
        # print(str(type(msg)))
        # err=str(msg)
        # if "No information given" in err:
        #     print("stopping reading wrong key")
        #     ep.stopReading()
        #     ep.reset()
        #     continue
            
            
        # return{
        #     "code":"003",
        #     "message":str("Mã MRZ sai!")
        # }
    # ep.readPassport()
    # print(err)
    print(time.time() - start)
    passportimage = ep['DG2']['A1']['5F2E']
    # temp = ep['DG1']['5F1F']
    dg13= ep["DG13"]['30']
    dg13Raw= dg13.hex()
    print("dg13 data:",dg13.hex())
    if(len(dg13)>100):
        imgData = base64.b64encode(passportimage)
        #convert dg13 data
        idCode = readZone(dg13Raw,idCodeZone)
        personName = readZone(dg13Raw,personNameZone)
        dateOfBirth = readZone(dg13Raw,dateOfBirthZone)
        gender = readZone(dg13Raw,genderZone)
        nationality = readZone(dg13Raw,nationalityZone)
        race = readZone(dg13Raw,raceZone)
        religion = readZone(dg13Raw,religionZone)
        originPlace = readZone(dg13Raw,originPlaceZone)
        residencePlace = readZone(dg13Raw,residencePlaceZone)
        personalIdentification = readZone(dg13Raw,personalIdentificationZone)
        beginDate = readZone(dg13Raw,beginDateZone)
        expiryDate = readZone(dg13Raw,expiryDateZone)
        list = readFatherZone(dg13Raw,fatherNameZone)
        fatherName = list[0] if len(list)>0 else ""
        motherName = list[1] if len(list)>1 else ""
        wifeName = readWifeZone(dg13Raw,wifeNameZone)
        oldIdCode = readZone(dg13Raw,oldIdCodeZone)
        return{
            "code":"000",
            "message":"Lấy dữ liệu thành công!",
            "data":{
                "idCode":idCode,
                "personName":personName,
                "dateOfBirth":dateOfBirth,
                "gender":gender,
                "nationality":nationality,
                "race":race,
                "religion":religion,
                "originPlace":originPlace,
                "residencePlace":residencePlace,
                "personalIdentification":personalIdentification,
                "issueDate":beginDate,
                "expiryDate":expiryDate,
                "fatherName":fatherName,
                "motherName":motherName,
                "wifeName":wifeName,
                "oldIdCode":oldIdCode,
                "img_data":"data:image/jpeg;base64,"+imgData.decode('ascii')
            } 
        }
    else:
        return{
            "code":"002",
            "message":"Dg13 data error!"
        }




    # mrz_output = temp.decode('ascii')
    # if len(mrz_output) == 90:
    #     mrz_temp = mrz_output[0:30] + "\n" + mrz_output[30:60] + "\n" + mrz_output[60:90]
    #     td1_check = TD1CodeChecker(mrz_temp)
    #     field = td1_check.fields()
    #     # print("haitn13 name = " + field.name)
    #     ma_CCCD = field.optional_data[0:12]

    #     # imgfp = io.BytesIO(passportimage)
    #     # img = Image.open(imgfp)
    #     # img.save("passport.png")
    #     # display image
    #     # import subprocess
    #     # subprocess.call(['xdg-open', 'passport.png'])
    #     imgData = base64.b64encode(passportimage)

    #     return{
    #         "code":"000",
    #         "message":"Lấy dữ liệu thành công!",
    #         "data":{
    #             "surname":field.surname,
    #             "name":field.name,
    #             "state":get_country(field.country),
    #             "nationality":get_country(field.nationality),
    #             "birth_date":field.birth_date,
    #             "expiry_date":field.expiry_date,
    #             "sex":field.sex,
    #             "document_type":field.document_type,
    #             "document_number":field.document_number,
    #             "id_number":ma_CCCD,
    #             "img_data":"data:image/jpeg;base64,"+imgData.decode('ascii')
    #         }
            
    #     }
            
    
