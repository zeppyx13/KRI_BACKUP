import picamera
import time

# Inisialisasi objek kamera
camera = picamera.PiCamera()

try:
    # Mulai perekaman video
    camera.start_recording('video.h264')

    # Tunggu 10 detik (Anda bisa mengubahnya sesuai kebutuhan)
    camera.wait_recording(10)

    # Stop perekaman video
    camera.stop_recording()

finally:
    # Tutup koneksi kamera saat selesai
    camera.close()
