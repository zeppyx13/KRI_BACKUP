from Ax12 import Ax12
import cv2
import numpy as np
import signal
import threading
from threading import Thread
import time
import numpy as np
import serial
import serial.tools.list_ports
from datetime import datetime
import re
import RPi.GPIO as GPIO
import time
import json

# Mendapatkan daftar port serial yang tersedia
ports = serial.tools.list_ports.comports()
cap = cv2.VideoCapture(0) 

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
       
port = '/dev/ttyACM1' # Sesuaikan dengan port Arduino Anda
baud_rate = 1000000  # Sesuaikan dengan baud rate Arduino Anda
ser = serial.Serial(port, baud_rate)


# Fungsi untuk rotasi gambar
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

# Fungsi untuk mengatur warna
def adjust_color(image, r_factor=0, g_factor=0, b_factor=0):
    B, G, R = cv2.split(image)
    B = cv2.add(B, b_factor)
    G = cv2.add(G, g_factor)
    R = cv2.add(R, r_factor)
    return cv2.merge([B, G, R])

# Fungsi untuk deteksi warna
def detect_color(frame, lower_color, upper_color, min_area):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append((x, y, w, h))
    return boxes

A = False
def vidio_cpture():
     # Ubah indeks kamera jika diperlukan
    global A
    global kamera_detect
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't capture a frame")
            break

        # Rotasi frame sebelum menampilkannya
        rotated_frame = rotate_image(frame, 270)  # Rotasi 270 derajat, sesuaikan sesuai kebutuhan

        # Resize frame ke resolusi yang lebih kecil untuk mengurangi penggunaan memori
        resized_frame = cv2.resize(rotated_frame, (400, 400))  # Sesuaikan resolusi yang diinginkan

        # Mengatur warna RGB
        adjusted_frame = adjust_color(resized_frame, r_factor=-60, g_factor=0, b_factor=-15)  # Sesuaikan faktor warna sesuai kebutuhan

        # Deteksi objek kuning dalam frame
        lower_yellow = np.array([10, 100, 20])  # Rentang bawah untuk kuning dalam HSV
        upper_yellow = np.array([25, 255, 255])  # Rentang atas untuk kuning dalam HSV
        min_area = 100  # Area minimum untuk objek yang terdeteksi

        yellow_boxes = detect_color(adjusted_frame, lower_yellow, upper_yellow, min_area)

        # Inisialisasi penghitung untuk objek di kiri dan kanan
        left_count = 0
        right_count = 0

        # Gambar kotak di sekitar objek kuning dan tentukan posisi mayoritas
        if len(yellow_boxes) > 0:
            for box in yellow_boxes:
                x, y, w, h = box
                cv2.rectangle(adjusted_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Warna kuning untuk kotak
                
                # Print koordinat x dan y
                print(f"Koordinat objek kuning: x={x}, y={y}")
                
                # Tentukan posisi objek kuning (kiri atau kanan)
                frame_center = resized_frame.shape[1] // 2
                object_center = x + w // 2
                if object_center < frame_center:
                    left_count += 1
                else:
                    right_count += 1
        
        # Tentukan mayoritas posisi objek kuning
        
        if left_count > right_count:
            position = "Mayoritas di Kiri"
            
        elif right_count > left_count:
            position = "Mayoritas di Kanan"
            
        else:
            position = "Seimbang"
            

        # Tampilkan teks posisi mayoritas di frame
        cv2.putText(adjusted_frame, position, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
      
       

        # Tambahkan penundaan dan hentikan jika tombol 'q' ditekan
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Tutup video dan jendela tampilan
    cap.release()
    cv2.destroyAllWindows()
if not cap.isOpened():
    print("Error: Couldn't open the camera")
    exit()
       
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
        print(giro_x)
        print(giro_y)
        
        return giro_x, giro_y, compas
    else:
        raise ValueError("Data tidak ditemukan dalam string")

# Contoh penggunaan

giro_x = 0

def ambil_data_sensor_kompas_dan_giro():
    global ser3
    global giro_x
    
    
    while not flag:
        
        data = ser3.readline().decode('latin').strip()
        
        	
        if data:        
            if data.startswith('{') and data.endswith('}'):
                try:
                    
                      data_string = data
                      A,B,C = giro_x, giro_y, compas = extract_data(data_string)
                      giro_x = A
                      print("MK " + str(giro_x))
                  
                       
                except:
                
                    pass
   
    

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
my_dxl13.set_moving_speed(kecepatan)
 

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
            if(idx == 2 or idx == 11):
                A = 1500 - position - 150 
                A = A + 1500
                dxl.set_goal_position(A - 1000)
            elif (idx == 5 or idx == 8 ):    
                A = 1500 - position + 210
                A = A + 1500
                dxl.set_goal_position(A - 1000)
            
            
            else:
                dxl.set_goal_position(position - 1000)
    prev_positions = positions
    time.sleep(0.3)
    
def gerak_lengan_kebawah():
 time.sleep(1)  # Tunggu sebentar agar koneksi stabil
 data = {
    'A': 0,
    'B': 50
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 print(f"Data '{json_data}' telah dikirim ke Arduino.")
    
 time.sleep(1)  # Tunggu sebentar agar koneksi stabil
 data = {
    'A': 0,
    'B': 0
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 print(f"Data '{json_data}' telah dikirim ke Arduino.")
 my_dxl13.set_goal_position(1800 - 1000)

 time.sleep(1)  # Tunggu sebentar agar koneksi stabil
 data = {
    'A': 0,
    'B': 20
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 print(f"Data '{json_data}' telah dikirim ke Arduino.")
 my_dxl13.set_goal_position(1200 - 1000)
 time.sleep(2)
 data = {
    'A': 20,
    'B': 100
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 
 print(f"Data '{json_data}' telah dikirim ke Arduino.")

def gerak_lengan_keatas():
 data = {
    'A': 90,
    'B': 0
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 time.sleep(1)  # Tunggu sebentar agar koneksi stabil
 data = {
    'A': 0,
    'B': 0
 }
 json_data = json.dumps(data)
 ser.write(json_data.encode('latin-1'))
 print(f"Data '{json_data}' telah dikirim ke Arduino.")
 my_dxl13.set_goal_position(1800 - 1000)
 
# Konfigurasi pin
GPIO.setmode(GPIO.BCM)
PING_PIN = 15
gerak_lengan_keatas()
# Setup pin
GPIO.setup(PING_PIN, GPIO.OUT)

def send_trigger_pulse():
    GPIO.output(PING_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 mikrodetik
    GPIO.output(PING_PIN, GPIO.LOW)

def wait_for_echo(value, timeout):
    start_time = time.time()
    while GPIO.input(PING_PIN) != value:
        if time.time() - start_time > timeout:
            return False
    return True

def get_distance():
    # Kirim pulse trigger
    GPIO.setup(PING_PIN, GPIO.OUT)
    send_trigger_pulse()

    # Tunggu echo mulai (HIGH)
    GPIO.setup(PING_PIN, GPIO.IN)
    if not wait_for_echo(GPIO.HIGH, 0.02):
        return None

    start_time = time.time()

    # Tunggu echo selesai (LOW)
    if not wait_for_echo(GPIO.LOW, 0.02):
        return None

    end_time = time.time()

    # Hitung durasi pulsa
    pulse_duration = end_time - start_time

    # Hitung jarak (kecepatan suara = 34300 cm/s)
    distance = pulse_duration * 17150
    return round(distance, 2)




 
  


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
  angkat = - 40
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
  angkat = - 40
  
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1500 - angkat, 1500 - angkat, 1400, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1500, 1350 - angkat, 1500 - angkat, 1300, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
  gerak(1600, 1500 + angkat, 1500 + angkat, 1400 - rotasi, 1300 - angkat, 1500 - angkat, 1300 - rotasi, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500 + angkat)
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
 
 L = 0
 print("Gerak maju di eksekusi...");
 A = nilai_rotasi + -0
 B = nilai_rotasi + -0
 #if(giro_x > -0.20):
  #  L = -20
 #else:99
 #   L = -10
 langkah = -10
 langkah2 = -10
 print("LKLK...........LLL.................... " + str(L))
 
 angkat = -40
 putaran_kaki = -100
 
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
 gerak(1500 - A -B, 1600 + langkah - angkat , 1600 + langkah - angkat,     1400 + putaran_kaki + A,  1500 - langkah , 1500 - langkah,   1500, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1550 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki - A -B, 1600 + langkah  - angkat, 1500 + langkah - angkat,    1400 + putaran_kaki + A , 1500 - langkah , 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1500 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1400 + langkah ,    1400 + putaran_kaki + A , 1500 - langkah, 1500 - langkah ,    1500, 1500 - langkah2,1500 - langkah2,    1600 - putaran_kaki, 1500 + langkah2, 1500 + langkah2)
 gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A,  1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1500 + langkah2 - langkah, 1430 + langkah2 - langkah)
 gerak(1600 - putaran_kaki - A -B, 1500 + langkah , 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2,1500 - langkah2,   1600 - putaran_kaki, 1500 + langkah2 - langkah, 1430 + langkah2 - langkah)
 gerak(1600 - putaran_kaki - A -B, 1500 + langkah, 1500 + langkah ,    1500 + A , 1500 - langkah , 1500 - langkah,    1400 + putaran_kaki, 1500 - langkah2 ,1500 - langkah2,   1500, 1500 + langkah2 - langkah, 1430 + langkah2 - langkah2)
 gerak(1600 - putaran_kaki,        1500 + langkah , 1500 + langkah ,    1500,      1500 - langkah , 1500 - langkah ,    1400 + putaran_kaki, 1500 - langkah2  ,1500 - langkah2,   1500, 1500 + langkah2, 1500)




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

    
 gerak(1600, 1500 + angkat , 1500 + angkat, 1500, 1500 - angkat, 1550 - angkat, 1400, 1500 - angkat,1500 - angkat, 1500, 1500 + angkat, 1500  + angkat)


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
gerak_kiri = False
gerak_kanan = False

def get_timeout():
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    time_int = hour * 10000 + minute * 100 + second
    return time_int

logic_penanda = False
v_mutar_kanan = True
v_mutar_kiri = True
nilai_rotasi = 0
v_maju = True
datai = " "
count = True
count2 = True

def eksekusi_get_giro():
    global datai
    while not flag:
         datai = ambil_data_sensor_kompas_dan_giro()
         
kamera_detect = False
objek_kiri = False
objek_kanan = False
LP = True
count_i = 0;
capit_misi = False;
capitt_kebawah = False
control_capit = 0
def eksekusilidar1():
  global LP
  global capitt_kebawah
  global capit_misi
  global count_i
  global kamera_detect
  global objek_kiri
  global objek_kanan
  global control_capit
  global nilai_0
  global nilai_90
  global nilai_180
  global nilai_270
  global nilai_220
  global nilai_300
  global logic_penanda
  global v_maju
  global count
  global count2
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
  global gerak_kiri
  global gerak_kanan
  
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
                        if(jarak >= 30 and not kamera_detect ):
                         logic_penanda = False
                         nilai_270 = -1
                        else:
                             nilai_220 = -1
                             nilai_300 = -1
                             logic_penanda = True
                             v_mutar_kanan = True
                             v_mutar_kiri = True
                             
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
                      if(kamera_detect):
                          nilai_0 = 100
                     
                          
                       
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
    
    
    if(nilai_0 > nilai_90 and nilai_0 > nilai_180 and nilai_0 > nilai_270):
         print("Putar kiri sebanyak 1 kali")
         v_mutar_kiri  = True
         if(v_maju):
           v_maju = False
         gerak_kiri = True
         gerak_kanan = False
        
      
      
    if(nilai_180 > nilai_0 and nilai_180 > nilai_90 and nilai_180 > nilai_270):
      if(not count_i > 2):
         print("Putar kanan sebanyak 1 kali")
         v_mutar_kanan = True
         if(v_maju):
           v_maju = False
         gerak_kanan = True
         gerak_kiri = False
      else:
         capit_misi = True
          
      
         
         
         
         
      
    if(nilai_90 > nilai_0 and nilai_90 > nilai_180 and nilai_90 > nilai_270 and nilai_90 > 150):
      if(nilai_180 > nilai_0):
         print("Berputar kekanan sebanyak 8 kaali")
         v_mutar_kanan  = True
         if(v_maju):
            v_maju = False
         gerak_kiri = True
         gerak_kanan = False
      else:
         
         print("Berputar kekiri sebanyak 8 kali")
         v_mutar_kiri = True
         if(v_maju):
           v_maju = False
         gerak_kanan = True
         gerak_kiri = False
    
  else:
    print("Eksekusi jalan maju dimulai")
    print("180 derajat = " + str(nilai_180))
    print("220 derajat = " + str(nilai_220))
    print("90 derajat = " + str(nilai_90))
    print("0 derajat = " + str(nilai_0 ))
    print("300 derajat = " + str(nilai_300))
    print("270 derajat = " + str(nilai_270))
   
    v_maju1 = False
    v_maju2 = False
    v_maju3 = False
    v_maju4 = False
    
    if(nilai_90 > nilai_0 and nilai_90 != -1 and nilai_0 != -1 and nilai_90 < nilai_220):
        
        print("kiri dieksekusi bagian 0 kiri")
        #MIRING KANAN CONDONG
        print((nilai_0 - nilai_90) * 10)
        nilai_rotasi = ((nilai_0 - nilai_90) * 5)
        
        v_mutar_kanan = False
    elif(nilai_0 != -1 and nilai_0 != -1 and nilai_90 < nilai_220):
        print("kanan dieksekusi bagian 0 kiri")
        print("MM "  + str((nilai_300 - nilai_0) * 5))
        nilai_rotasi = ((nilai_300 - nilai_0) * 5)
        v_mutar_kiri = False
        
    elif(nilai_220  > nilai_300 and nilai_220 != -1 and nilai_300 != -1 and nilai_220 < nilai_90):
        print("kiri dieksekusi bagian 180 kanan")
        #MIRING KANAN CONDONG
        print((nilai_300 - nilai_220) * 10)
        v_mutar_kanan = False
        nilai_rotasi = ((nilai_300 - nilai_220) * 5)
    
        
    elif (nilai_220 != -1 and nilai_300 != -1 and nilai_220 < nilai_90):
        print("kanan dieksekusi bagian 180 kanan")
        v_mutar_kiri = False
        print("LL " + str((nilai_300 - nilai_220) * 8))
        nilai_rotasi = ((nilai_300 - nilai_220) * 5)
        
   
    print(v_mutar_kanan)
    print(v_mutar_kiri)
        
    if(not v_mutar_kanan and not v_mutar_kiri and not count_i > 3):
        print("............................Jalan Maju................................")
        v_maju = True
        gerak_kanan = False
        gerak_kiri = False
    if(v_mutar_kanan and not v_mutar_kiri):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    elif (not v_mutar_kanan and v_mutar_kiri):
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        
       
        
        
    
    
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
  
  if(capit_misi):
      gerak_kanan = False
      gerak_kiri = False
      
      if(control_capit == 2):
          print("Maju dijalankannnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
          v_maju = True
      else:
          control_capit = 100
      if(LP):
        
        LP = False
        
      

  if(count_i > 2):
      kamera_detect = True
      nilai_rotasi = 0
      
      
   
  
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
    global nilai_rotasi
    global count_i
    global capitt_kebawah
    while not flag:  
       if(gerak_kanan):
           mutar_kanan(80)
           
       if(gerak_kiri):
           
           mutar_kiri(0)
       if(capitt_kebawah):
           gerak_lengan_kebawah()
           capitt_kebawah = False
    
       if(v_maju):
           #gerak_maju(nilai_rotasi)
           gerak_maju(0)
           count_i += 1;
           
       if(not v_mutar_kanan):
           count = True
       if(not v_mutar_kiri):
           count2 = True
       
     # +0 kanan
     # -0 kiri
       #gerak_mundur()
YU = True

def capitu():
 global control_capit
 global kamera_detect
 global count_i
 global v_maju
 global YU
 while True:
  FD = get_distance()
  time.sleep(0.2)
  print(FD)
  print("MMMM =" + str(control_capit))
  if(control_capit > 70):
    
    gerak_lengan_kebawah()
    control_capit = 2
    print("AAAAAAAAAAAAAAAAAAAAAA" + str(control_capit))
  if(FD is not None and FD > 1 and FD < 12 and control_capit == 2):
      v_maju = False
      print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS = " + str(control_capit))
      time.sleep(1)
      data = {
         'A': 20,
         'B': 0
        }
      json_data = json.dumps(data)
      ser.write(json_data.encode('latin-1'))
      time.sleep(2)
      if(YU):
        YU = False
        control_capit == 0
        gerak_lengan_keatas()
        gerak_kiri = True
        gerak_kanan = False
        v_maju = True
        kamera_detect = False
        count_i = 0
      print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
 else:
    print("FD bernilai None atau tidak kurang dari 12")


   
def handle_signal(signal, frame):
    global flag
    print("\nProgram berhenti")
    
    flag = True

signal.signal(signal.SIGINT, handle_signal)

eksekusi_1 = Thread(target=eksekusi_gerakan)
eksekusi_2 = Thread(target=eksekusi_gerakan_5)
eksekusi_3 = Thread(target=ambil_data_sensor_kompas_dan_giro)
eksekusi_4 = Thread(target=vidio_cpture)
eksekusi_5 = Thread(target=capitu)


eksekusi_3.start()
eksekusi_4.start()
eksekusi_1.start()
eksekusi_5.start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

RTP = True

   

while RTP:
 
    UIP = GPIO.input(5)
    time.sleep(1)
    
    if UIP == GPIO.HIGH and RTP:
        print("Tombol start ditekan")
        
        eksekusi_2.start()
        print("Misi robot sar dimulai")
        RTP = False
    
eksekusi_2.join()


    
        
   





