from ultralytics import YOLO
import cv2
import sqlite3
import easyocr
import numpy as np
from arduino import ArduinoController  # Arduino sınıfını içe aktar

class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture("test.mp4")  # Gerçek video dosyan
        self.model = YOLO('yolov8/best.pt')  # Eğitimli YOLOv8 modelin yolu
        self.reader = easyocr.Reader(['en'])
        self.conn = sqlite3.connect('plates.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.arduino = ArduinoController(port='/dev/tty.usbserial-110')  # Arduino portunu kontrol et

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = self.cap.read()

        results = self.model(frame)[0]
        read_plate = None
        action_message = "Tespit yok"
        detected_vehicle = None

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            if label == 'araba':
                detected_vehicle = 'araba'
                action_message = "🔴 BOZZER UYARISI – Araba tespit edildi"

            elif label == 'kamyon':
                detected_vehicle = 'kamyon'
                action_message = "✅ Kamyon tespit edildi – plaka kontrol ediliyor..."

            elif label == 'plaka':
                plate_roi = frame[y1:y2, x1:x2]
                plate_texts = self.reader.readtext(plate_roi)

                if plate_texts:
                    read_plate = plate_texts[0][1].replace(" ", "").upper()

                    # Plaka veritabanında kayıtlı mı?
                    self.cursor.execute("SELECT * FROM plates WHERE plate = ?", (read_plate,))
                    result = self.cursor.fetchone()

                    if result:
                        action_message = f"✅ Yetkili plaka ({read_plate}) – Kapi acilacak"
                    else:
                        action_message = f"🚫 Yetkisiz plaka ({read_plate}) – Giriş reddedildi"

        # Görseli encode et
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), action_message
