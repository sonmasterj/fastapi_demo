# Copyright 2009 Jean-Francois Houzard, Olivier Roger
#
# This file is part of pypassport.
#
# pypassport is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pypassport is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with pyPassport.
# If not, see <http://www.gnu.org/licenses/>.

from pypassport import epassport, reader
import os, string


MRZ_bob       = "EH123456<0BEL8510035M1508075<<<<<<<<<<<<<<02"
MRZ_oli       = "EH276509<0BEL8406158M1302217<<<<<<<<<<<<<<04"
MRZ_helen     = "EF486766<8BEL8803023F1103056<<<<<<<<<<<<<<00"
MRZ_fred      = "EG491433<0BEL8305099M1208157<<<<<<<<<<<<<<04"
MRZ_camille   = "08CH022724FRA8706021F1807066<<<<<<<<<<<<<<06"
MRZ_nico      = "EH288866<9BEL8605113M1303269<<<<<<<<<<<<<<00"
MRZ_caro      = "EH266828<7BEL8405243F1302206<<<<<<<<<<<<<<02"
MRZ_n =         "7065198411GBR9703072M1206256<<<<<<<<<<<<<<02"
# MRZ_tohue =     "IDVNM1830015170026183001517<<28310073F2310071VNM<<<<<<<<<<<2"      # Huong
# MRZ_tohue =     "IDVNM0990303372001099030337<<39905050M2405056VNM<<<<<<<<<<<2"      # quang anh 
MRZ_tohue =     "IDVNM0960146541001096014654<<29604021M3604029VNM<<<<<<<<<<<6"      # hai
#Remplire la 2e ligne ici
#MRZ_ = "4479426958USA4307121M1806173228204573<883790"
##Dir ou enregistrer les dumps
#DIR_DUMP = "c:\\tmp"

def trace(name, msg):
    if name == "EPassport":
        print(name + "> " + msg)

sep = os.path.sep
Sim = False
# Sim = True
r=None
if not Sim:
    print("haitn13 simulation = true")
    r = reader.ReaderManager().waitForCard()
    
else:
    print("haitn13 simulation true" )
    r = reader.ReaderManager().create("DumpReader")
    r.connect("C:\\tmp")

print("haitn13 MRX_tohue =" + MRZ_tohue )
ep = epassport.EPassport(r, MRZ_tohue)
# print("haitn13 MRZ_oli =" + MRZ_oli )
# ep = epassport.EPassport(r, MRZ_oli)


ep.register(trace)
# print("Access CA " + os.getcwd() + sep + "data" + sep + "cert")
# ep.setCSCADirectory(os.getcwd() + sep + "data" + sep + "cert", False)

print("haitn13 certificate " + os.getcwd() + sep + "testData" + sep + "3d36cc9e.0")
ep.setCSCADirectory(os.getcwd() + sep + "testData" + sep + "3d36cc9e.0", False)

import time

start = time.time()
print("haitn13 done Epassport")
try:
    ep.readPassport()
    print("haitn13 done readPassportd")
except Exception as msg:
    print(msg)
# ep.readPassport()
print(time.time() - start)


if False:
    try:
        ep.doVerifySODCertificate()
    except Exception as msg:
       print(msg)
    try:
        p = ep.readDataGroups()
        print(ep.doVerifyDGIntegrity(p))
    except Exception as msg:
        print(msg)

if False:
    ep.doActiveAuthentication()

import io
from PIL import Image

passportimage = ep['DG2']['A1']['5F2E']
imgfp = io.BytesIO(passportimage)
img = Image.open(imgfp)
img.save("passport.png")
import subprocess
subprocess.call(['xdg-open', 'passport.png'])
