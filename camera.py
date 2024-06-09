import cv2

# Buka kamera
video = cv2.VideoCapture(0) # 0 menunjukkan indeks kamera pertama yang terdeteksi

# Periksa apakah kamera telah terbuka dengan benar
if not video.isOpened():
    print("Tidak dapat membuka kamera")

# Loop untuk membaca dan menampilkan setiap frame dari kamera
while video.isOpened():
    # Baca frame demi frame
    ret, frame = video.read()
    
    # Periksa apakah frame berhasil dibaca
    if not ret:
        print("Tidak dapat membaca frame")
        break
    
    # Tampilkan frame
    cv2.imshow('Video dari Kamera', frame)
    
    # Tambahkan penundaan dan hentikan jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela tampilan
video.release()
cv2.destroyAllWindows()
