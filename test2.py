from Ax12 import Ax12

import signal
import threading
from threading import Thread
import time
import numpy as np
import serial
import serial.tools.list_ports


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
    for dxl, position in zip(dxl_list, positions):
        dxl.set_goal_position(position - 1000)
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
  time.sleep(2000)

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
  gerak(1600, 1500, 1500, 1500, 1500, 1500, 1400, 1500,1500, 1500, 1500, 1500)
  
berdiri()


while(0):
    nilai_0 = 0
    nilai_90 = 0
    nilai_180 = 0
    nilai_270 = 0
        
    while(1):   
        
        data = ser2.readline().decode('latin').strip()
    
        if data:        
            if data.startswith('{a') and data.endswith('}'):
                try:                  
                    sudut = int(data[data.index('a')+1:data.index('b')])
                    jarak = int(data[data.index('b')+1:data.index('}')])
                   
                      
                    if(sudut == 90):
                      A1 = False
                      data_160 = jarak
                      print("jarak 90 " + str(jarak))
                      nilai_90 = jarak
                      #belang
                      
                    if(sudut == 180):
                      A1 = False
                      data_180 = jarak
                      print("jarak 0 " + str(jarak))
                      nilai_180 = jarak
                      #kanan
                      
                    if(sudut == 270):
                      A1 = False
                      data_160 = jarak
                      print("jarak 270 " + str(jarak))
                      nilai_270 = jarak
                      #depan
                    if(sudut == 0):
                      A1 = False
                      data_160 = jarak
                      print("jarak 0 " + str(jarak))
                      nilai_0 = jarak
                      #kiri
                    
                       
                except:
                
                    pass

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

while TrueL:
    mutar_kiri(0)
 
def gerak_maju(nilai_rotasi):
 
 print("Gerak maju di eksekusi...");
 A = nilai_rotasi 
 B = nilai_rotasi
 langkah = - 50
 langkah2 = 0
 angkat = 0
 
#         +++++++++++++++++++++      +++++++++++++++++++        ++++++++++++       ++++++++++++++
#        p1             p2             p3                 p4          p5    p6       p7    p8   p9      p10    p11  p12 
 gerak(1600,          1500 + langkah, 1500 + langkah ,   1500,      1400 - langkah + langkah, 1400 - langkah + langkah,    1400, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - A - B , 1500 + langkah, 1500 + langkah,   1400,      1400 - langkah + langkah, 1500 - langkah + langkah,    1400, 1500 - langkah2,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - A - B , 1500 + langkah , 1500 + langkah,   1400,      1500 - langkah , 1600 - langkah ,    1400, 1500 - langkah2 ,1500 - langkah2,    1500, 1500 + langkah2, 1500 + langkah2)
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1400, 1540 - langkah2 ,1570 - langkah2 ,    1600, 1500 + langkah2, 1500 + langkah2)
 gerak(1500 - A - B , 1500 + langkah , 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600, 1500 + langkah2, 1500 + langkah2) 
 
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1450 - langkah2 + angkat,1570 - langkah2 + angkat,    1600, 1500 + langkah2, 1500 + langkah2) 
 
 gerak(1500 - A - B , 1500 + langkah, 1500 + langkah ,   1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2 ,1500 - langkah2,    1600, 1500 + langkah2, 1500 + langkah2)
 misi_eksekusi()
 
 if(not A1 and not A2 and not A3 or True):
   
     #    +++++++++++++++++++++      +++++++++++++++++++        ++++++++++++       ++++++++++++++
     #   p1             p2    p3     p4          p5    p6       p7    p8   p9      p10    p11  p12
  
   gerak(1500 - A -B, 1600 + langkah - angkat , 1600 + langkah - angkat,     1400 + A,  1500 - langkah , 1500 - langkah,   1500, 1500 - langkah2,1500 - langkah2,   1600, 1500 + langkah2, 1500 + langkah2)
   gerak(1600 - A -B, 1600 + langkah  - angkat, 1500 + langkah - angkat,    1400 + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600, 1500 + langkah2, 1500 + langkah2)
   gerak(1600 - A -B, 1500 + langkah , 1400 + langkah ,    1400 + A , 1500 - langkah, 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600, 1500 + langkah2, 1500 + langkah2)
   gerak(1600 - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A,  1500 - langkah , 1500 - langkah ,    1400, 1500 - langkah2,1500 - langkah2,   1600, 1460 + langkah2 - langkah, 1430 + langkah2 - langkah)
   gerak(1600 - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400, 1500 - langkah2,1500 - langkah2,   1600, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah)
   gerak(1600 - A -B, 1500 + langkah, 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400, 1500 - langkah2 ,1500 - langkah2,   1500, 1550 + langkah2 - langkah, 1430 + langkah2 - langkah2)
   gerak(1600,        1500 + langkah , 1500 + langkah ,    1500,      1500 - langkah , 1500 - langkah ,    1400, 1500 - langkah2  ,1500 - langkah2,   1500, 1500 + langkah2, 1500 + langkah2)
   

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

  

LK = 0
LB = 0


flag = False
enstain = 0;
while True:
    gerak_maju(0)

def eksekusi_gerakan():
    global enstain;
    while not flag:
      #gerak_mundur(10) 
      gerak_maju(-10)
     # +0 kanan
     # -0 kiri
       #gerak_mundur()
        
        
def eksekusi_get_giro():
    while not flag:
        
        accelerometer_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        print("Akselerometer: ")
        print("  X =", accelerometer_data['x'])
        print("  Y =", accelerometer_data['y'])
        print(enstain)
        

        
def handle_signal(signal, frame):
    global flag
    print("\nProgram berhenti")
    
    flag = True

signal.signal(signal.SIGINT, handle_signal)
eksekusi_1 = Thread(target=eksekusi_gerakan)
eksekusi_2 = Thread(target=eksekusi_get_giro)



eksekusi_1.start()
