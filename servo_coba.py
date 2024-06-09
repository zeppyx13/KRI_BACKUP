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

my_dxl.set_goal_position(500)
time.sleep(1000)

def gerak(*positions):
    dxl_list = [my_dxl, my_dxl2, my_dxl3, my_dxl4, my_dxl5, my_dxl6, my_dxl7, my_dxl8, my_dxl9, my_dxl10, my_dxl11, my_dxl12]
    prev_positions = None
    
    for idx, (dxl, position) in enumerate(zip(dxl_list, positions)):
        if prev_positions is None or position != prev_positions[idx]:
            dxl.set_goal_position(position - 1000)
    prev_positions = positions
    time.sleep(0.5)
    
    
                                                                                                                                                                                                                                   
   
    
    
    

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
  
while True:
    mutar_kanan(0)