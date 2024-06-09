from Ax12 import Ax12

import signal
import threading
from threading import Thread
import time
import numpy as np
import serial
import serial.tools.list_ports
from datetime import datetime
import re

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
    if(port.description == "ttyACM0"):
       print("Port: ", port.device)
       print("Nama: ", port.name)
       print("Deskripsi: ", port.description)
       ser3 = serial.Serial(port.device, 1000000)
#209
       
def extract_data(data_string):
    # Definisikan pola regex untuk mengekstrak nilai yang diperlukan
    pattern = r'giro_x(-?\d+\.\d+)giro_y(-?\d+\.\d+)compas(\d+)'
    
    # Mencari pola dalam string
    match = re.search(pattern, data_string)
    
    if match:
        # Mengambil nilai dari grup regex yang cocok
        giro_x = float(match.group(1))
        giro_y = float(match.group(2))
        compas = int(match.group(3))
        
        return giro_x, giro_y, compas
    else:
        raise ValueError("Data tidak ditemukan dalam string")

# Contoh penggunaan

       

def ambil_data_sensor_kompas_dan_giro():
    logic = True
    
    data = " "
    while logic:
        data = ser3.readline().decode('latin').strip()
        
        	
        if data:        
            if data.startswith('{') and data.endswith('}'):
                try:
                    
                      data_string = data
                      data = giro_x, giro_y, compas = extract_data(data_string)
                      logic = False
                       
                except:
                
                    pass
   
    return data

#sensor = mpu6050(0x68)


 


#283
#358

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
my_dxl13 = Ax12(13)

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
    time.sleep(0.2)
    
    
                                                                                                                                                                                                                                   
   
    
    
    

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
  angkat = - 80
  gerak(1600 + rotasi , 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat ,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1600 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400, 1500 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1400 - angkat ,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1600 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1600 + angkat , 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1700, 1600 + angkat, 1500 + angkat) 
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat ,1500 - angkat, 1500, 1600 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1400 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1400 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)


  
def mutar_kiri(rotasi):
  angkat = - 80
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1400 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1400 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat ,1500 - angkat, 1500, 1600 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1700, 1600 + angkat, 1500 + angkat) 
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1600 + rotasi, 1600 + angkat , 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1600 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1500, 1400 - angkat ,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1400 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400, 1500 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1700, 1500 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1700, 1600 + angkat, 1500 + angkat)
  gerak(1500, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1500 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1600 + angkat, 1500 + angkat)
  gerak(1600 + rotasi , 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  
  
  
def gerak_maju(nilai_rotasi):
 
 print("Gerak maju di eksekusi...");
 A = nilai_rotasi + -25
 B = nilai_rotasi + -25
 langkah = -80
 langkah2 = -80
 angkat = -50
 putaran_kaki = -70
 
#         +++++++++++++++++++++      +++++++++++++++++++        ++++++++++++       ++++++++++++++
#        p1             p2             p3                 p4          p5    p6       p7    p8   p9      p10    p11  p12 
 gerak(1600 - putaran_kaki,          1500 + langkah, 1500 + langkah ,   1500  ,      1400 - langkah + langkah, 1400 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki- A - B , 1500 + langkah, 1500 + langkah,   1400 + putaran_kaki,      1400 - langkah + langkah, 1500 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki - A - B , 1500 + langkah , 1500 + langkah,   1400 + putaran_kaki,      1500 - langkah , (1600 - langkah + langkah) ,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
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
  A = nilai_rotasi + -25
  B = nilai_rotasi + -25
  langkah = -80
  langkah2 = -80
  angkat = 0
  putaran_kaki = 0
  gerak(1600 - putaran_kaki,        1500 + langkah , 1500 + langkah ,    1500,      1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2  ,1500 - langkah2,   1500, 1550 + langkah2, 1500)
  gerak(1600 - putaran_kaki - A -B, 1500 + langkah, 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,   1500, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah2)
  gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah)
  gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A,  1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1460 + langkah2 - langkah, 1430 + langkah2 - langkah)
  gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1400 + langkah ,    1400 + putaran_kaki + A , 1500 - langkah, 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1600 - putaran_kaki - A -B, 1600 + langkah  - angkat, 1500 + langkah - angkat,    1400 + putaran_kaki + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1500 - A -B, 1600 + langkah - angkat , 1600 + langkah - angkat,     1400 + putaran_kaki + A,  1500 - langkah , 1500 - langkah,   1500, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2 ,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1500 - A - B , 1500 + langkah, 1500 + langkah,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
  gerak(1500 - A - B , 1500 + langkah , 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2) 
  gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1570 + langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1540 - langkah2 ,1570 - langkah2 ,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
  gerak(1600 - putaran_kaki - A - B , 1500 + langkah , 1500 + langkah,   1400 + putaran_kaki,      1500 - langkah , (1600 - langkah + langkah) ,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
  gerak(1600 - putaran_kaki- A - B , 1500 + langkah, 1500 + langkah,   1400 + putaran_kaki,      1400 - langkah + langkah, 1500 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
  gerak(1600 - putaran_kaki,          1500 + langkah, 1500 + langkah ,   1500  ,      1400 - langkah + langkah, 1400 - langkah + langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
  
  
  
  
  
  
  
  

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
    
    
    data = ser2.readline().decode('latin').strip()
    
    mutar_kiri(0)
    print("hako")




    

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
 
 print("Gerak maju di eksekusi...");
 angkat = -50
 gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500  + angkat)
berdiri()
time.sleep(2)

waktu_timeout = 0
waktu_end = 0
penanda_aktif = False
v_mutar_kiri = False
nilai_0 = 0
nilai_90 = 0
nilai_180 = 0
nilai_270 = 0
nilai_220 = 0
nilai_300 = 0
status = 0
LKJ = True

def get_timeout():
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    time_int = hour * 10000 + minute * 100 + second
    return time_int

logic_penanda = False
v_mutar_kanan = False
nilai_rotasi = 0
v_maju = False
datai = " "
count = True 

def eksekusi_get_giro():
    global datai
    while not flag:
         datai = ambil_data_sensor_kompas_dan_giro()

def eksekusilidar1():
  global nilai_0
  global nilai_90
  global nilai_180
  global nilai_270
  global nilai_220
  global nilai_300
  global logic_penanda
  global v_maju
  global count
  nilai_0 = 0
  nilai_90 = 0
  nilai_180 = 0
  nilai_270 = 0
  global waktu_timeout
  global waktu_end
  global penanda_aktif
  global v_mutar_kanan
  global v_mutar_kiri
  global nilai_rotasi
  
  waktu_timeout = get_timeout()
  set_waktu = 20
  waktu_end = waktu_timeout + set_waktu
  

  
  
  
  while(nilai_0 == 0 or nilai_90 == 0 or nilai_180 == 0 or nilai_270 == 0 or nilai_220 == 0 or nilai_300 == 0):
      
       
        if(waktu_end - get_timeout() < 1 and penanda_aktif):
           
            print("Misi Waktu timeout dijalankan")
            waktu_end = get_timeout() + set_waktu
            if(nilai_0 == 0):
                nilai_0 = -1
            if(nilai_90 == 0):
                nilai_90 = -1
            if(nilai_180 == 0):
                nilai_180 = -1
            if(nilai_270 == 0):
                nilai_270 = -1
            if(nilai_220 == 0):
                nilai_220 = -1
            if(nilai_300 == 0):
                nilai_300 = -1
            
        
        data = ser2.readline().decode('latin').strip()
        	
        if data:        
            if data.startswith('{a') and data.endswith('}'):
                try:                  
                      sudut = int(data[data.index('a')+1:data.index('b')])
                      jarak = int(data[data.index('b')+1:data.index('}')])
                      penanda_aktif = True
                      if(sudut > 260 and sudut < 280  and not logic_penanda):
                        if(jarak >= 30):
                         logic_penanda = False
                         nilai_270 = -1
                        else:
                             nilai_220 = -1
                             nilai_300 = -1
                             logic_penanda = True
                      if (logic_penanda):
                        if(sudut > 355 and sudut < 360 or sudut < 5 and nilai_0 == 0):
                          nilai_0 = jarak
                        
                        if(sudut > 85 and sudut < 95 and nilai_90 == 0):
                          
                          nilai_90 = jarak
                        
                        if(sudut > 175 and sudut < 185 and nilai_180 == 0):
                          print(jarak)
                          nilai_180 = jarak
                          #kana
                        if(sudut > 265 and sudut < 275 and nilai_270 == 0):
                          
                          nilai_270 = jarak
                        
                      
                      elif(sudut == 180 and not logic_penanda and nilai_220 == 0):
                         print("LL" + str(jarak))
                         print("wss " + str(nilai_220))
                         nilai_220 = jarak
                         
                      elif(sudut == 190 and not logic_penanda and nilai_300 == 0):
                         print("L1" + str(jarak))
                         nilai_300 = jarak
                         
                         
                      elif(sudut > 175 and sudut < 185 and nilai_180 == 0):
                          print(jarak)
                          nilai_180 = jarak
                          
                      elif(sudut == 350  and nilai_90 == 0):
                          nilai_90 = jarak
                          
                      elif(sudut > 0 and sudut < 5):
                          nilai_0 = jarak
                      if(nilai_90 != 0 and nilai_0 != 0):
                          set_waktu -= 5
                      if(nilai_220 != 0 and nilai_300 != 0):
                          set_waktu -= 5
                       
                except:
                
                    pass
  print("Berhenti mengeksekusi")
  if(nilai_220 == -1 and nilai_300 == -1):
    print(" ")
    print("Eksekusi putar dimulai")
    print("0 derajat = " + str(nilai_0))
    print("90 derajat = " + str(nilai_90))
    print("180 derajat = " + str(nilai_180))
    print("270 derajat = " + str(nilai_270))
    
    
    
    
    stop = False
    
    
    if(nilai_0 > nilai_90 and nilai_0 > nilai_180 and nilai_0 > nilai_270 or stop):
         print("Putar kiri sebanyak 1 kali")
         v_mutar_kiri  = True
        
      
      
    if(nilai_180 > nilai_0 and nilai_180 > nilai_90 and nilai_180 > nilai_270):
         print("Putar kanan sebanyak 1 kali")
         v_mutar_kanan = True
         
         
      
    if(nilai_90 > nilai_0 and nilai_90 > nilai_180 and nilai_90 > nilai_270):
      if(nilai_180 > nilai_0):
        print("Berputar kekanan sebanyak 8 kaali")
      else:
        print("Berputar kekiri sebanyak 8 kali")
    
    
  else:
    print("Eksekusi jalan maju dimulai")
    print("180 derajat = " + str(nilai_180))
    print("220 derajat = " + str(nilai_220))
    print("90 derajat = " + str(nilai_90))
    print("0 derajat = " + str(nilai_0 ))
    print("300 derajat = " + str(nilai_300))
    print("270 derajat = " + str(nilai_270))
   
    
    
    if(nilai_90 > nilai_0 and nilai_90 != -1 and nilai_0 != -1 and nilai_90 < nilai_220):
        
        print("kiri dieksekusi bagian 0 kiri")
        #MIRING KANAN CONDONG
        print((nilai_0 - nilai_90) * 10)
        nilai_rotasi = ((nilai_0 - nilai_90) * 10)
        
        v_mutar_kanan = False
    elif(nilai_0 != -1 and nilai_0 != -1 and nilai_90 < nilai_220):
        print("kanan dieksekusi bagian 0 kiri")
        print("MM "  + str((nilai_300 - nilai_0) * 5))
        nilai_rotasi = ((nilai_300 - nilai_0) * 5)
        v_mutar_kiri = False
        v_maju = True
    elif(nilai_220  > nilai_300 and nilai_220 != -1 and nilai_300 != -1 and nilai_220 < nilai_90):
        print("kiri dieksekusi bagian 180 kanan")
        #MIRING KANAN CONDONG
        print((nilai_300 - nilai_220) * 10)
        v_mutar_kanan = False
        nilai_rotasi = ((nilai_300 - nilai_220) * 10)
        
    elif (nilai_220 != -1 and nilai_300 != -1 and nilai_220 < nilai_90):
        print("kanan dieksekusi bagian 180 kanan")
        v_mutar_kiri = False
        print("LL " + str((nilai_300 - nilai_220) * 10))
        nilai_rotasi = ((nilai_300 - nilai_220) * 10)
        v_maju = True
    
  logic_penanda = False
  nilai_0 = 0
  nilai_90 = 0
  nilai_180 = 0
  nilai_270 = 0
  nilai_220 = 0
  nilai_300 = 0
  waktu_timeout = 0
  waktu_end = 0
  penanda_aktif = False
  LKJ = False
  
  
  
#
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


        


#def cek_apakah_posisi_depan_robot_sudah_berada_lurus_dengan_arena():
  #  while True:

def eksekusi_gerakan(): 
    global enstain;
    while not flag:         
      eksekusilidar1()
     

def eksekusi_gerakan_5():
    while not flag:  
       if(v_mutar_kanan):
           if(count):
              gerak_mundur(0)
              count = False
           mutar_kanan(90)
       if(v_mutar_kiri):
           
           mutar_kiri(0)
          
           
       if(not v_mutar_kanan and  v_maju):
           gerak_maju(nilai_rotasi)
           
       if(not v_mutar_kanan):
           count = True
       
     # +0 kanan
     # -0 kiri
       #gerak_mundur()
        

        

        
def handle_signal(signal, frame):
    global flag
    print("\nProgram berhenti")
    
    flag = True

signal.signal(signal.SIGINT, handle_signal)
eksekusi_1 = Thread(target=eksekusi_gerakan)
eksekusi_2 = Thread(target=eksekusi_gerakan_5)



eksekusi_1.start()
eksekusi_2.start()
