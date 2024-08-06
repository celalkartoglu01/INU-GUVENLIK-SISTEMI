from PyQt5.QtWidgets import *
from akademisyen_cikis import Ui_Form
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import face_recognition
import os
import mysql.connector
from ultralytics import YOLO
import pytesseract
import numpy as np
from PIL import Image
import re

con = mysql.connector.connect(user='root', password='', host='localhost', database='inuguvenlik')
cursor = con.cursor()


model = YOLO("plakatanima.pt")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class AkademisyenCikis(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.akademisyen = Ui_Form()
        self.akademisyen.setupUi(self)
        self.akademisyen.fotografcek.clicked.connect(self.FotografCek)
        self.akademisyen.veritabani.clicked.connect(self.Veritabani)
        self.akademisyen.aracsec.clicked.connect(self.AracSec)
        self.scene = QGraphicsScene(self)
        self.akademisyen.goruntu.setScene(self.scene)
        self.timer = QTimer(self)
        self.known_face_encodings = []
        self.known_face_names = []
        self.folder_path = "akademisyenler"
        self.file_path = None
        self.current_frame = None
        self.update_known_faces()
        self.scene1 = QGraphicsScene(self)
        self.akademisyen.aracgoruntu.setScene(self.scene1)
        self.detected_plate = ""
        self.plate_counter = 1
        self.kayit = ""
        self.akademisyen.cikisiniyap.clicked.connect(self.CikisiniYap)
    

    def clean_plate_text(self, text):
        text = text.upper()
        
        text = re.sub(r'[^A-Z0-9\s]', '', text)
        
        text = ' '.join(text.split())
        
        if text and text[0].isalpha():
            text = text[1:].lstrip()  
        
        return text

    
    
    

    def AracSec(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "*.png *.jpg *.jpeg")

        if self.file_path:
            pixmap = QPixmap(self.file_path)
            view_rect = self.akademisyen.aracgoruntu.rect()
            scaled_pixmap = pixmap.scaled(view_rect.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.scene1.clear()
            self.scene1.addPixmap(scaled_pixmap)
            self.akademisyen.aracgoruntu.setScene(self.scene1)
            self.akademisyen.aracgoruntu.horizontalScrollBar().setVisible(False)
            self.akademisyen.aracgoruntu.verticalScrollBar().setVisible(False)

            im1 = Image.open(self.file_path)

            results = model.predict(source=im1)

            result = results[0]

            boxes = result.boxes

            image_np = np.array(im1)

            for box in boxes.data:
                x1, y1, x2, y2, conf, cls = box
            
                if cls == 0: 
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                
                    plate_image = image_np[y1:y2, x1:x2]
                
                    plate_filename = f'plakalar/plate{self.plate_counter}.jpg'

                    self.plate_counter += 1
                    os.makedirs(os.path.dirname(plate_filename), exist_ok=True)
                    cv2.imwrite(plate_filename, plate_image)

                    plate_image = Image.open(plate_filename)

                    text = pytesseract.image_to_string(plate_image, config='--psm 8')

                    self.detected_plate = text.strip()
                    self.detected_plate = self.clean_plate_text(text)
                    self.akademisyen.plaka.setText(self.detected_plate)
                    break
        
    def Veritabani(self):
        query = "select * from plakalar where plaka = %s"
        cursor.execute(query,(self.detected_plate,))
        result = cursor.fetchone()
        if result:
            self.kayit = "Kayıt Bulundu."
            self.akademisyen.kayit.setText(self.kayit)
        else:
            self.kayit = "Kayıt Bulunamadı."
            self.akademisyen.kayit.setText(self.kayit)
        
    

    def CikisiniYap(self):
        if self.kayit == "Kayıt Bulundu.":
            plaka = self.detected_plate
            isim = self.akademisyen.isim.text()
            soyisim = self.akademisyen.soyisim.text()
            isimsoyisim = isim + " " + soyisim
            query2 = "select * from girenaraclar where plaka = %s"
            cursor.execute(query2,(plaka,))
            result = cursor.fetchone()
            if result:
                giriszamani = result[3]
            query = "INSERT INTO cikanaraclar (aracsahibi,plaka,giriszamani) VALUES (%s, %s,%s)"
            cursor.execute(query,(isimsoyisim,plaka,giriszamani))
            con.commit()
            
            query1 = "DELETE FROM girenaraclar where plaka = %s"
            cursor.execute(query1,(plaka,))
            con.commit()
            QMessageBox.information(self,"Uyarı","Çıkış Başarılı, Güle Güle !")
            self.akademisyen.isim.clear()
            self.akademisyen.soyisim.clear()
            self.akademisyen.bolum.clear()
            self.akademisyen.kayit.clear()
            self.akademisyen.plaka.clear()
            self.scene.clear()
            self.scene1.clear()
        else:
            QMessageBox.information(self,"Uyarı","Araç Kaydı Bulunamadı, Lütfen Kayıt Yaptırın !")

    def update_known_faces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
                image_path = os.path.join(self.folder_path, file_name)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(os.path.splitext(file_name)[0])

    def FotografCek(self):
        if self.timer.isActive():
            self.timer.stop()
            self.camera.release()
            return
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            QMessageBox.critical(self, "Hata", "Kamera açılamadı.")
            return

        self.timer.timeout.connect(self.display_frame)
        self.timer.start(1000 // 30)

    def display_frame(self):
        ret, frame = self.camera.read()
        frame = cv2.flip(frame, 1)

        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.current_frame = rgb_frame.copy()

            self.recognize_faces_in_frame(rgb_frame)

    def recognize_faces_in_frame(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Bilinmeyen yüz"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                query = "select * from akademisyenler where sistemadi = %s"
                cursor.execute(query,(name,))
                result = cursor.fetchone()
                if result:
                    self.akademisyen.isim.setText(result[1])
                    self.akademisyen.soyisim.setText(result[2])
                    self.akademisyen.bolum.setText(result[3])
            else:
                QMessageBox.information(self,"Uyarı","Tanınmayan Yüz !")



