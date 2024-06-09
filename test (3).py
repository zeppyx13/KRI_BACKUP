from Ax12 import Ax12

import signal
import threading
from threading import Thread
import time
import numpy as np
import serial
import serial.tools.list_ports
from datetime import datetime


# Mendapatkan daftar port serial yang tersedia
ports = serial.tools.list_ports.comports()


for port in ports:
    if(port.description == "OpenRB-150"):
       print("Port: ", port.device)
       Ax12.DEVICENAME = port.device
       Ax12.BAUDRATE = 1_000_000
       Ax12.connect()
       print("Nama: ", port.name)
       print("Deskripsi: ", port.description)
    if(port.description == "USB2.0-Serial"):
       print("Port: ", port.device)
       print("Nama: ", port.name)
       print("Deskripsi: ", port.description)
       ser2 = serial.Serial(port.device, 2000000)


#sensor = mpu6050(0x68)



my_dxl = Ax12(1)
my_dxl2 = Ax12(2)
my_dxl3 = Ax12(3)
my_dxl4 = Ax12(4)
my_dxl5 = Ax12(5)
my_dxl6 = Ax12(6)
my_dxl7 = Ax12(7)
my_dxl8 = Ax12(8)
my_dxl9 = Ax12(9)
my_dxl10 = Ax12(10)
my_dxl11 = Ax12(11)
my_dxl12 = Ax12(12)

kecepatan = 1000
my_dxl.set_moving_speed(kecepatan)
my_dxl2.set_moving_speed(kecepatan)
my_dxl3.set_moving_speed(kecepatan)
my_dxl4.set_moving_speed(kecepatan)
my_dxl5.set_moving_speed(kecepatan)
my_dxl6.set_moving_speed(kecepatan)
my_dxl7.set_moving_speed(kecepatan)
my_dxl8.set_moving_speed(kecepatan)
my_dxl9.set_moving_speed(kecepatan)
my_dxl10.set_moving_speed(kecepatan)
my_dxl11.set_moving_speed(kecepatan)
my_dxl12.set_moving_speed(kecepatan)

 

A1 = True
A2 = True
A3 = True

data_160 = 0
data_180 = 0
data_200 = 0
data_rotasi = 0



def gerak(*positions):
    dxl_list = [my_dxl, my_dxl2, my_dxl3, my_dxl4, my_dxl5, my_dxl6, my_dxl7, my_dxl8, my_dxl9, my_dxl10, my_dxl11, my_dxl12]
    prev_positions = None
    
    for idx, (dxl, position) in enumerate(zip(dxl_list, positions)):
        if prev_positions is None or position != prev_positions[idx]:
            dxl.set_goal_position(position - 1000)
    prev_positions = positions
    time.sleep(0.1)
    
    
                                                                                                                                                                                                                                   
   
    
    
    

#              +++++++++++++
#       +      +           +     -
# p12, p11,p10 +           + p7, p8, p9
#       -      +           +     +
#              +           +
#      +       +           +     -
#  p6 ,p5, p4  +           + p1, p2, p3
#      -       +           +     +
#              +++++++++++++
#                   +_+
#      p1    p2    p3     p4   p5    p6    p7    p8   p9  p10    p11  p12






def mutar_kanan(rotasi):
  gerak(1600 + rotasi , 1500, 1500, 1500, 1500, 1500, 1400 - rotasi, 1500,1500, 1500, 1500, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1600, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1700, 1600, 1500)
  gerak(1500, 1500, 1500, 1400, 1500, 1500, 1300, 1500,1500, 1700, 1500, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1400,1500, 1700, 1500, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1400,1500, 1700, 1500, 1500)
  gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
  gerak(1500, 1600, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
  gerak(1600 + rotasi, 1600, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
  gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
  gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1400,1500, 1700, 1500, 1500)
  gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300, 1400,1500, 1700, 1500, 1500)
  gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300, 1500,1500, 1700, 1500, 1500)
  gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1700, 1600, 1500)
  gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1600, 1500)
  gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
  gerak(1600, 1500, 1500, 1400 - rotasi, 1400, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
  gerak(1600, 1500, 1500, 1500, 1400, 1500, 1300, 1500,1500, 1500, 1500, 1500)
  gerak(1600, 1500, 1500, 1500, 1500, 1500, 1400, 1500,1500, 1500, 1500, 1500)
  
def mutar_kiri(rotasi):
 gerak(1600, 1500, 1500, 1500, 1500, 1500, 1400, 1500,1500, 1500, 1500, 1500)
 gerak(1600, 1500, 1500, 1500, 1400, 1500, 1300, 1500,1500, 1500, 1500, 1500)
 gerak(1600, 1500, 1500, 1400 - rotasi, 1400, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
 gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
 gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1600, 1500)
 gerak(1600, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1700, 1600, 1500)
 gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300, 1500,1500, 1700, 1500, 1500)
 gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300, 1400,1500, 1700, 1500, 1500)
 gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1400,1500, 1700, 1500, 1500)
 gerak(1600 + rotasi, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
 gerak(1600 + rotasi, 1600, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
 gerak(1500, 1600, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1500,1500, 1700, 1500, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1500, 1400,1500, 1700, 1500, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1400,1500, 1700, 1500, 1500)
 gerak(1500, 1500, 1500, 1400, 1500, 1500, 1300, 1500,1500, 1700, 1500, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1700, 1600, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1600, 1500)
 gerak(1500, 1500, 1500, 1400 - rotasi, 1500, 1500, 1300 - rotasi, 1500,1500, 1500, 1500, 1500)
 gerak(1600 + rotasi , 1500, 1500, 1500, 1500, 1500, 1400 - rotasi, 1500,1500, 1500, 1500, 1500)
 
 
def gerak_maju(nilai_rotasi):
 
 print("Gerak maju di eksekusi...");
 A = nilai_rotasi 
 B = nilai_rotasi
 langkah = -50
 langkah2 = -50
 angkat = -50
 putaran_kaki = -50
 
#         +++++++++++++++++++++      +++++++++++++++++++        ++++++++++++       ++++++++++++++
#        p1             p2             p3                 p4          p5    p6       p7    p8   p9      p10    p11  p12 
 gerak(1600 - putaran_kaki,          1500 + langkah, 1500 + langkah ,   1500  ,      1400 - langkah + langkah, 1400 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki- A - B , 1500 + langkah, 1500 + langkah,   1400 + putaran_kaki,      1400 - langkah + langkah, 1500 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki - A - B , 1500 + langkah , 1500 + langkah,   1400 + putaran_kaki,      1500 - langkah , 1600 - langkah ,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 
 
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1540 - langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1570 + langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
 
 gerak(1500 - A - B , 1500 + langkah , 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
 
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
 
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2 ,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
 
 
 if(not A1 and not A2 and not A3 or True):
   
     #    +++++++++++++++++++++      +++++++++++++++++++        ++++++++++++       ++++++++++++++
     #   p1             p2    p3     p4          p5    p6       p7    p8   p9      p10    p11  p12
  
  #gerak(1500 - A -B, 1600 + langkah - angkat , 1600 + langkah - angkat,     1400 + putaran_kaki + A,  1500 - langkah , 1500 - langkah,   1500, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
   #gerak(1600 - putaran_kaki - A -B, 1600 + langkah  - angkat, 1500 + langkah - angkat,    1400 + putaran_kaki + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
   #gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1400 + langkah ,    1400 + putaran_kaki + A , 1500 - langkah, 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
   #gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A,  1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1460 + langkah2 - langkah, 1430 + langkah2 - langkah)
   #gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah)
   #gerak(1600 - putaran_kaki - A -B, 1500 + langkah, 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,   1500, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah2)
   #gerak(1600 - putaran_kaki,        1500 + langkah , 1500 + langkah ,    1500,      1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2  ,1500 - langkah2,   1500, 1500 + langkah2, 1500)
     gerak(1600 - putaran_kaki,          1500 + langkah, 1500 + langkah ,   1500  ,      1400 - langkah + langkah, 1400 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
     gerak(1600 - putaran_kaki- A - B , 1500 + langkah, 1500 + langkah,   1400 + putaran_kaki,      1400 - langkah + langkah, 1500 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
     gerak(1600 - putaran_kaki - A - B , 1500 + langkah , 1500 + langkah,   1400 + putaran_kaki,      1500 - langkah , 1600 - langkah ,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
     gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1540 - langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1570 + langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1500 - A - B , 1500 + langkah , 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
     gerak(1500 - A - B , 1500 + langkah, 1500 + langkah,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
     gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2 ,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1500 - A -B, 1600 + langkah - angkat , 1600 + langkah - angkat,     1400 + putaran_kaki + A,  1500 - langkah , 1500 - langkah,   1500, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1600 - putaran_kaki - A -B, 1600 + langkah  - angkat, 1500 + langkah - angkat,    1400 + putaran_kaki + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1400 + langkah ,    1400 + putaran_kaki + A , 1500 - langkah, 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
     gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A,  1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1460 + langkah2 - langkah, 1430 + langkah2 - langkah)
     gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah)
     gerak(1600 - putaran_kaki - A -B, 1500 + langkah, 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,   1500, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah2)
     gerak(1600 - putaran_kaki,        1500 + langkah , 1500 + langkah ,    1500,      1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2  ,1500 - langkah2,   1500, 1550 + langkah2, 1500)


def gerak_mundur(nilai_rotasi):
  A = nilai_rotasi 
  B = nilai_rotasi
  print("Gerak mundur di eksekusi...")
  gerak(1600,        1500, 1500,    1500,      1500, 1500,    1400, 1500,1500,   1500, 1500, 1500)
  gerak(1600 - A -B, 1500, 1500,    1500 + A , 1500, 1500,    1400, 1500,1500,   1500, 1550, 1430)
  gerak(1600 - A -B, 1500, 1500,    1500 + A , 1500, 1500,    1400, 1500,1500,   1600, 1550, 1430)
  gerak(1600 - A -B, 1500, 1500,    1500 + A,  1500, 1500,    1400, 1500,1500,   1600, 1460, 1430)
  gerak(1600 - A -B, 1500, 1400,    1400 + A , 1500, 1500,    1500, 1500,1500,   1600, 1500, 1500)
  gerak(1600 - A -B, 1600, 1500,    1400 + A , 1500, 1500,    1500, 1500,1500,    1600, 1500, 1500)
  gerak(1500 - A -B, 1600, 1600,     1400 + A,  1500, 1500,   1500, 1500,1500,   1600, 1500, 1500)
  gerak(1500 - A - B , 1500, 1500,   1400 + A , 1500, 1500,    1500, 1500,1500,    1600, 1500, 1500)
  gerak(1500 - A - B , 1500, 1500,   1400 + A , 1500, 1500,    1500, 1450,1570,    1600, 1500, 1500)
  gerak(1500 - A - B , 1500, 1500,   1400 + A , 1500, 1500,    1500, 1450,1570,    1600, 1500, 1500)
  gerak(1500 - A - B , 1500, 1500,   1400 + A , 1500, 1500,    1400, 1540,1570,    1600, 1500, 1500)
  gerak(1600 - A - B , 1500, 1500,   1400,      1500, 1600,    1400, 1500,1500,    1500, 1500, 1500)
  gerak(1600 - A - B , 1500, 1500,   1400,      1400, 1500,    1400, 1500,1500,    1500, 1500, 1500)
  gerak(1600,          1500, 1500,   1500,      1400, 1400,    1400, 1500,1500,    1500, 1500, 1500)

def gerak_samping():
    #                -                -                  +                                                     
  gerak(1600, 1500, 1500, 1500, 1500, 1600, 1400, 1500,1500, 1500, 1500, 1500)
  time.sleep(3)
  gerak(1600, 1500, 1400, 1500, 1500, 1400, 1400, 1500,1600, 1500, 1500, 1600)
  time.sleep(3)
  gerak(1600, 1500, 1500, 1500, 1500, 1500, 1400, 1500,1500, 1500, 1500, 1500)
  time.sleep(3)
  

def eksekusi_lidar():
    global A1
    global A2
    global A3
    global data_160
    global data_180
    global data_200
    
    while A1 or A2 or A3:
        data = ser2.readline().decode('latin').strip()
    
        if data:        
            if data.startswith('{a') and data.endswith('}'):
                try:                  
                    sudut = int(data[data.index('a')+1:data.index('b')])
                    jarak = int(data[data.index('b')+1:data.index('}')])
                    
                    if(sudut == 160):
                      A1 = False
                      data_160 = jarak
                      
                    if(sudut == 180):
                      LK = jarak
                      A2 = False
                      data_180 = jarak
                    if(sudut == 200):
                      LK = jarak
                      A3 = False
                      data_200 = jarak
      
                       
                except:
                
                    pass
                
                

                




def misi_eksekusi():
  global A1
  global A2
  global A3
  global data_rotasi;
  A1 = True
  A2 = True
  A3 = True
  eksekusi_lidar()
  print(data_160)
  print(data_180)
  print(data_200)
  print(data_160 - data_200)
  data_rotasi = data_160 - data_200
  print("Berhasil tereksekusi")
  

def berdiri():
#              +++++++++++++
#       +      +           +     -
# p12, p11,p10 +           + p7, p8, p9
#       -      +           +     +
#              +           +
#      +       +           +     -
#  p6 ,p5, p4  +           + p1, p2, p3
#      -       +           +     +
#              +++++++++++++
#                   +_+


# (+) depan, atas, atas
# (-) belakang, bawah, bawah,
#         ++++++++++++     ++++++++++++++    ++++++++++++++   ++++++++++++++
#       +p1-  +p2-  -p3+  -p4+  -p5+  +p6-  +p7-  +p8- +p9-  +p10-  +p11- -p12+
  gerak(1600, 1500, 1400, 1500, 1500, 1500, 1400, 1500,1500, 1500, 1500, 1500)


berdiri()
waktu_timeout = 0
waktu_end = 0
penanda_aktif = False
nilai_0 = 0
nilai_90 = 0
nilai_180 = 0
nilai_270 = 0

def get_timeout():
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    time_int = hour * 10000 + minute * 100 + second
    return time_int

while True:
    gerak_maju(0)


def eks():
  global nilai_0
  global nilai_90
  global nilai_180
  global nilai_270
  global waktu_timeout
  global waktu_end
  waktu_timeout = get_timeout()
  waktu_end = waktu_timeout + 20
  

  
  
  
  while(nilai_0 == 0 or nilai_90 == 0 or nilai_180 == 0 or nilai_270 == 0):
      
        if(waktu_end - get_timeout() < 1 and penanda_aktif):
           
            print("Misi Waktu timeout dijalankan")
            
            waktu_end = get_timeout() + 20
        
        data = ser2.readline().decode('latin').strip()
        	
        if data:        
            if data.startswith('{a') and data.endswith('}'):
                try:                  
                    sudut = int(data[data.index('a')+1:data.index('b')])
                    jarak = int(data[data.index('b')+1:data.index('}')])
                   
                       
                    if(sudut == 90 and nilai_90 == 0):
                      A1 = False
                      print("jarak 90 " + str(jarak))
                      if(jarak < 20):
                        print("Mode mundur dijalankan dan kemudian berputar")
                        print("Taha putar aktif")
                        nilai_90 = jarak
                      else:
                        print("Mode mundur dijalankan dan kemudian berputar")
                        print("Taha putar aktif")
                        nilai_90 = jarak
                    if(sudut == 180 and nilai_180 == 0):
                      A1 = False
                      data_180 = jarak
                      print("jarak 180 " + str(jarak))
                      nilai_180 = jarak
                      #kanan
                      
                    if(sudut == 270 and nilai_270 == 0):
                      A1 = False
                      data_160 = jarak
                      print("jarak 270 " + str(jarak))
                      nilai_270 = jarak
                      #depan
                    if(sudut == 0 and nilai_0 == 0):
                      A1 = False
                      data_160 = jarak
                      print("jarak 0 " + str(jarak))
                      nilai_0 = jarak
                      
                    penanda_aktif = True
                    
                       
                except:
                
                    pass
#pENANDA
  penanda_aktif = False
  print("hasil " + str(nilai_270))
  
  if(nilai_270 < nilai_0 or nilai_270 < nilai_90 < nilai_270 < nilai_180):
         print("Misi putar rotasi aktif")
         if(nilai_90 > nilai_270 and nilai_90 > nilai_0  and nilai_90 > nilai_180):
             print("Robot berputar 180 derjata")
             if(nilai_0 > nilai_180):
                 print("Robot berputar kiri dari belakang")
             else:
                 print("Robot berputar ike kanan dari belakang")
         elif(nilai_0 > nilai_180):
             print("Robot belok ke kiri")
             putar_kiri(0)
         else:
             print("Robot belok ke kanan")
             putar_kanan(0)
  else:
      print("Robot langsung jalan")
    

      
      
#eks()
#time.sleep(1000)


 #L1
 #jika sudut 0 lebih besar dari 180 robot berputar ke kiri sebanyak 3 putaran
 #jika tidak robot berputar ke kanan sebanyak 3 putaran

#Flow cart
#Robot start
#Robot mencari sudut yang terbesar
#Jika sudut depan 270 derajat tidak menjadi jarak tebesar
#jila jarak pada sudt 90 lebih besar (belakang) daripada jarak pada sudut lainya L1
#jika sudut 0 lebih besar dari 270 robot berputar kekiri sebanyak 1 putaran
#jika tidak robot berputar ke kekanan sebanyak 1 putaran
#jika jarak pada sudut 0 derajat sudah lebih besar daripada jarak sudut lainya robot bergerak maju

#robot melangkah
#



  

LK = 0
LB = 0


flag = False
enstain = 0;


        
def eksekusi_get_giro():
    while not flag:
        
        accelerometer_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        print("Akselerometer: ")
        print("  X =", accelerometer_data['x'])
        print("  Y =", accelerometer_data['y'])
        print(enstain)


def eksekusi_gerakan():
    global enstain;
    while not flag:
      #gerak_mundur(10) 
       gerak_maju(-15)
       
       print("halo apa kabar")
       
     # +0 kanan
     # -0 kiri
       #gerak_mundur()
        

        
while True:
    
    gerak_maju(0)
        
def handle_signal(signal, frame):
    global flag
    print("\nProgram berhenti")
    
    flag = True

signal.signal(signal.SIGINT, handle_signal)
eksekusi_1 = Thread(target=eksekusi_gerakan)
eksekusi_2 = Thread(target=eksekusi_get_giro)



eksekusi_1.start()
