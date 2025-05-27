from flask import Flask, render_template, Response, request, redirect, jsonify
from camera import VideoCamera
import sqlite3
import serial
import time

app = Flask(__name__)

# Arduino bağlantısını başlatma
arduino = None
try:
    # Terminalde 'ls /dev/tty.*' komutuyla Arduino portunu kontrol edip buraya yazın
    arduino = serial.Serial('/dev/tty.usbserial-110', 9600, timeout=1)


    time.sleep(2)  # Arduino'nun hazır hale gelmesi için bekle
    print("✅ Arduino bağlantısı kuruldu.")
except serial.SerialException as e:
    print(f"❌ Arduino bağlantısı kurulamadı: {e}")

video_camera = VideoCamera()
last_message = ""

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global last_message
    while True:
        frame, message = camera.get_frame()

        # Yetkili kamyon varsa kapı açma sinyali gönder
        if "Kapi acilacak" in message and arduino:
            try:
                arduino.write(b'A')  # 'A' sinyali ile kapı açılacak
                print("🔓 Kapı açma sinyali gönderildi.")
            except Exception as e:
                print(f"Arduino iletişim hatası: {e}")

        # Araba tespit edilince buzzer sinyali gönder
        elif "BOZZER UYARISI" in message and arduino:
            try:
                arduino.write(b'B')  # 'B' sinyali ile buzzer uyarısı
                print("🔴 Buzzer uyarısı sinyali gönderildi.")
            except Exception as e:
                print(f"Arduino iletişim hatası: {e}")

        last_message = message

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tespit')
def tespit():
    return jsonify({"message": last_message})

@app.route('/add_plate', methods=['POST'])
def add_plate():
    plate = request.form['plate'].replace(" ", "").upper()
    try:
        conn = sqlite3.connect("plates.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO plates (plate) VALUES (?)", (plate,))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass  # Aynı plakayı tekrar eklemeyi engelle
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
