import cv2

# Fungsi untuk memutar gambar
def rotate_image(image, angle):
    # Ambil dimensi gambar
    (h, w) = image.shape[:2]
    # Temukan titik tengah gambar
    center = (w / 2, h / 2)
    # Lakukan rotasi
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h))
    return rotated_image

# Fungsi untuk mengatur nilai warna RGB
def adjust_color(image, r_factor, g_factor, b_factor):
    # Membagi citra menjadi saluran warna
    b, g, r = cv2.split(image)

    # Mengatur nilai saluran warna dengan faktor yang diberikan
    r = cv2.add(r, r_factor)
    g = cv2.add(g, g_factor)
    b = cv2.add(b, b_factor)

    # Gabungkan kembali saluran warna
    adjusted_image = cv2.merge([b, g, r])
    return adjusted_image

# Membuka video capture dengan MMAL backend
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: Couldn't open the camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't capture a frame")
        break

    # Rotasi frame sebelum menampilkannya
    rotated_frame = rotate_image(frame, 270)  # Rotasi 90 derajat, sesuaikan sesuai kebutuhan

    # Resize frame ke resolusi yang lebih kecil untuk mengurangi penggunaan memori
    rotated_frame = cv2.resize(rotated_frame, (400, 400))  # Sesuaikan resolusi yang diinginkan

    # Mengatur warna RGB
    adjusted_frame = adjust_color(rotated_frame, r_factor=-60, g_factor=0, b_factor=-15)  # Sesuaikan faktor warna sesuai kebutuhan

    cv2.imshow('Camera', adjusted_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan VideoCapture dan menutup jendela OpenCV
cap.release()
cv2.destroyAllWindows()
