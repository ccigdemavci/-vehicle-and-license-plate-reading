import serial
import time

class ArduinoController:
    def __init__(self, port='/dev/tty.usbmodem1101', baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Arduino'nun hazır olması için
        except serial.SerialException:
            self.ser = None
            print("Arduino baglantisi kurulamadi.")

    def open_gate(self):
        if self.ser:
            self.ser.write(b'O')  # 'O' -> Open gate
            print("Kapi ac komutu gonderildi.")

    def buzzer_alert(self):
        if self.ser:
            self.ser.write(b'B')  # 'B' -> Buzzer alert
            print("Buzzer uyari komutu gonderildi.")
