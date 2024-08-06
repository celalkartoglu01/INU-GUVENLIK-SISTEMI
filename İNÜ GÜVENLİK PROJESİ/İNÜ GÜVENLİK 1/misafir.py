from PyQt5.QtWidgets import *
from misafir_giris import Ui_Form
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
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

class Misafir(QWidget):
    def __init__(self)->None:
        super().__init__()
        self.misafir = Ui_Form()
        self.misafir.setupUi(self)
        self.misafir.fotografcek.clicked.connect(self.FotografCek)
        self.misafir.aracsec.clicked.connect(self.AracSec)
        self.misafir.kaydet.clicked.connect(self.Kaydet)
        self.scene = QGraphicsScene(self)
        self.misafir.goruntu.setScene(self.scene)
        self.timer = QTimer(self)
        self.known_face_encodings = []
        self.known_face_names = []
        self.folder_path = "misafirler"
        self.file_path = None
        self.current_frame = None
        self.scene1 = QGraphicsScene(self)
        self.misafir.aracgoruntu.setScene(self.scene1)
        self.detected_plate = ""
        self.plate_counter = 1
        self.kayit = ""
        self.misafir.icerial.clicked.connect(self.IceriAl)
        self.photo_name = ""
        self.photo_path = ""
        self.is_capturing = False
    
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
            view_rect = self.misafir.aracgoruntu.rect()
            scaled_pixmap = pixmap.scaled(view_rect.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.scene1.clear()
            self.scene1.addPixmap(scaled_pixmap)
            self.misafir.aracgoruntu.setScene(self.scene1)
            self.misafir.aracgoruntu.horizontalScrollBar().setVisible(False)
            self.misafir.aracgoruntu.verticalScrollBar().setVisible(False)

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
                    self.misafir.plaka.setText(self.detected_plate)
                    break
    
    def IceriAl(self):
        plaka = self.detected_plate
        isim = self.misafir.isim.text()
        soyisim = self.misafir.soyisim.text()
        isimsoyisim = isim + " " + soyisim
        query = "INSERT INTO girenaraclar (aracsahibi,plaka) VALUES (%s, %s)"
        cursor.execute(query,(isimsoyisim,plaka))
        con.commit()
        QMessageBox.information(self,"Uyarı","Giriş Başarılı, Hoşgeldiniz !")
        self.misafir.isim.clear()
        self.misafir.soyisim.clear()
        self.misafir.ziyaretsebebi.clear()
        self.misafir.plaka.clear()
        self.scene.clear()
        self.scene1.clear()
    

   
    def FotografCek(self):
        if self.is_capturing:
            self.is_capturing = False
            self.timer.stop()
            self.camera.release()
            self.camera = None

            if hasattr(self, 'current_frame'):
                text, ok = QInputDialog.getText(self, 'Fotoğraf Kaydet', 'Fotoğraf için bir isim girin:')
                if ok and text:
                    self.photo_name = text

                    folder = 'misafirler'
                    os.makedirs(folder, exist_ok=True)
                    self.photo_path = os.path.join(folder, f'{self.photo_name}.jpg')

                    web_folder = r'C:\xampp\htdocs\İNÜ GÜVENLİK\misafirler'
                    os.makedirs(web_folder, exist_ok=True)
                    self.web_photo_path = os.path.join(web_folder, f'{self.photo_name}.jpg')

                    cv2.imwrite(self.photo_path, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(self.web_photo_path, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))

                    relative_web_path = os.path.relpath(self.web_photo_path, start=r'C:\xampp\htdocs')
                    web_photo_url = "http://localhost/İNÜ%20GÜVENLİK/" +folder +"/"+ self.photo_name+ ".jpg"

                    self.web_photo_url = web_photo_url

                    QMessageBox.information(self, "Başarılı", f"Fotoğraf {self.photo_path} ve {self.web_photo_path} olarak kaydedildi.")
                else:
                    QMessageBox.warning(self, "Uyarı", "Geçerli bir isim girmediniz.")
        else:
            self.camera = cv2.VideoCapture(0)

            if not self.camera.isOpened():
                QMessageBox.critical(self, "Hata", "Kamera açılamadı.")
                return

            self.is_capturing = True
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
    
 



    def Kaydet(self):
        isim = self.misafir.isim.text()
        soyisim = self.misafir.soyisim.text()
        ziyaretsebebi = self.misafir.ziyaretsebebi.text()
        web_photo_url = self.web_photo_url
        sistemadi = self.photo_name
        plaka = self.detected_plate

        query = "INSERT INTO misafirler (ad, soyad, ziyaretsebebi, fotograf, sistemadi,plaka) VALUES (%s, %s, %s, %s, %s,%s)"
        cursor.execute(query,(isim,soyisim,ziyaretsebebi,web_photo_url,sistemadi,plaka))
        con.commit()
        QMessageBox.information(self,"Uyarı","Misafir Kaydı Yapıldı !")

        

    

    