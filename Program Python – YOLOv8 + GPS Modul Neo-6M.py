import serial
import pynmea2
import cv2
import csv
from ultralytics import YOLO
from datetime import datetime

# Fungsi ambil GPS
def get_gps(port='COM3', baud=9600):
    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                    try:
                        msg = pynmea2.parse(line)
                        return [msg.latitude, msg.longitude]
                    except:
                        continue
    except:
        return [None, None]

# Inisialisasi kamera & model
cam = cv2.VideoCapture(0)  # Ganti jika pakai IP cam
model = YOLO("yolov8n.pt")

# Log file
with open('log_gps_modul.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Latitude", "Longitude", "Objects Detected"])
    
    while True:
        ret, frame = cam.read()
        if not ret:
            break

       results = model(frame)
labels = []
for cls in results[0].boxes.cls:
    class_id = int(cls)
    label = results[0].names[class_id]
    labels.append(label)
gps = get_gps()


        # Tampilkan
cv2.imshow("YOLO + GPS Modul", results[0].plot())
writer.writerow([datetime.now(), gps[0], gps[1], labels])

if cv2.waitKey(1) == 27:  # ESC to quit
            break

cam.release()
cv2.destroyAllWindows()
